import os
import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from brain import ask_assistant
from upstash_redis import Redis

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# specific CORS configuration for production
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:5173",             # Local development
        "https://axiom-tutor.vercel.app",    # Your new custom domain
        "https://axiom-frontend.vercel.app"  # Your original Vercel URL (as a backup)
    ],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# Upstash Redis configuration
# Updated Redis initialization in server.py
UPSTASH_URL = os.environ.get('UPSTASH_REDIS_REST_URL', '').strip()
UPSTASH_TOKEN = os.environ.get('UPSTASH_REDIS_REST_TOKEN', '').strip()

redis = None
if UPSTASH_URL and UPSTASH_TOKEN:
    # Ensure the URL starts with https://
    if not UPSTASH_URL.startswith('http'):
        UPSTASH_URL = f"https://{UPSTASH_URL}"
    
    try:
        redis = Redis(url=UPSTASH_URL, token=UPSTASH_TOKEN)
        print(f"✅ Redis initialized with URL: {UPSTASH_URL[:15]}...")
    except Exception as e:
        print(f"❌ Failed to create Redis client: {e}")

# Rate limit settings (e.g. 30 requests per 60 seconds)
RATE_LIMIT_MAX_REQUESTS = 30
RATE_LIMIT_WINDOW_SECONDS = 60

def get_client_ip():
    """Extract client IP from request, handling proxies."""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    if request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    return request.remote_addr or 'unknown'

def hash_ip(ip):
    """Hash IP for privacy-conscious rate limiting."""
    return hashlib.sha256(ip.encode()).hexdigest()[:16]

def check_rate_limit(ip_hash):
    """Check rate limit using Upstash Redis REST API."""
    if not redis:
        # Skip rate limiting if Redis not configured
        print("⚠️ Upstash Redis not configured. Rate limiting disabled.")
        return True, RATE_LIMIT_MAX_REQUESTS
    
    key = f"uniguardian:ratelimit:{ip_hash}"
    
    try:
        # 1. Atomically increment the counter first to prevent race conditions
        current_count = redis.incr(key)
        
        # 2. Only set the expiration on the very first request of the window
        # This prevents "rolling windows" that lock users out permanently
        if current_count == 1:
            redis.expire(key, RATE_LIMIT_WINDOW_SECONDS)
        
        # 3. Check if the incremented count exceeds the limit
        if current_count > RATE_LIMIT_MAX_REQUESTS:
            return False, 0
            
        return True, RATE_LIMIT_MAX_REQUESTS - current_count
        
    except Exception as e:
        print(f"Rate limit check error: {e}")
        # 4. Fail Closed: Block the request if Redis is unreachable 
        # to protect your LLM API budget.
        return False, 0

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint for chatting with the assistant."""
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400
        
    query = data['query']
    
    client_ip = get_client_ip()
    ip_hash = hash_ip(client_ip)
    
    allowed, remaining = check_rate_limit(ip_hash)
    if not allowed:
        return jsonify({
            "error": "Rate limit exceeded. Please try again later.",
            "remaining": 0
        }), 429
        
    try:
        # Process query through brain.py
        response_text, retrieved_docs = ask_assistant(query)
        
        # Format the context snippets securely for the response
        sources = []
        if retrieved_docs:
             for doc in retrieved_docs:
                sources.append({
                    "source": doc.metadata.get("university_source", "Unknown Source"),
                    "page": doc.metadata.get("page_num", "?"),
                    "preview": f"{doc.page_content.strip()[:100]}..."
                })
        
        return jsonify({
            "response": response_text,
            "sources": sources,
            "remaining_requests": remaining
        })
    except Exception as e:
        print(f"Error processing question: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/status', methods=['GET'])
def status():
    """Get rate limit status without consuming a request."""
    client_ip = get_client_ip()
    ip_hash = hash_ip(client_ip)
    
    if not redis:
        # No rate limiting configured
        return jsonify({
            'remaining': RATE_LIMIT_MAX_REQUESTS,
            'limit': RATE_LIMIT_MAX_REQUESTS,
            'limited': False
        })
    
    key = f"uniguardian:ratelimit:{ip_hash}"
    
    try:
        current_count = redis.get(key)
        current_count = int(current_count) if current_count else 0
        
        remaining = max(0, RATE_LIMIT_MAX_REQUESTS - current_count)
        return jsonify({
            'remaining': remaining,
            'limit': RATE_LIMIT_MAX_REQUESTS,
            'limited': remaining == 0
        })
    except Exception as e:
        print(f"Status check error: {e}")
        return jsonify({
            'remaining': RATE_LIMIT_MAX_REQUESTS,
            'limit': RATE_LIMIT_MAX_REQUESTS,
            'limited': False
        })
        
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'redis_configured': redis is not None
    })

if __name__ == '__main__':
    print(f"Starting UniGuardian API with Rate Limit: {RATE_LIMIT_MAX_REQUESTS} req / {RATE_LIMIT_WINDOW_SECONDS} sec")
    # debug MUST be False in production. HF Spaces requires port 7860.
    app.run(host='0.0.0.0', port=7860, debug=False)
