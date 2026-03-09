import os
import shutil
from dotenv import load_dotenv
from langchain_groq import ChatGroq
# 1. Swapped Google Generative AI for HuggingFace Local Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

def find_tool_path(tool_name):
    path = shutil.which(tool_name)
    if path:
        return os.path.dirname(path)
    return None

# Poppler and Tesseract dynamic paths
POPPLER_BIN = find_tool_path("pdftoppm")
TESSERACT_EXE = shutil.which("tesseract")

if not TESSERACT_EXE:
    print("⚠️ Tesseract not found in PATH. OCR might fail.")
if not POPPLER_BIN:
    print("⚠️ Poppler not found in PATH. PDF rendering might fail.")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found! Did you forget to set it in your .env file?")

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.5,
    # This helps stop the model from repeating the same phrases
    model_kwargs={
        "frequency_penalty": 0.5, 
        "presence_penalty": 0.5
    }
)

refiner_llm = ChatGroq(
    model_name="meta-llama/llama-4-scout-17b-16e-instruct", 
    temperature=0.2,
    model_kwargs={
        "frequency_penalty": 0.5, 
        "presence_penalty": 0.5
    }
)

print("✅ Groq LLM initialized successfully.")

# 2. Replaced Gemini with the Local Qwen3 Model
embeddings = HuggingFaceEmbeddings(
    model_name="Qwen/Qwen3-Embedding-0.6B", 
    model_kwargs={
        'device': 'cpu', # <--- Changed from 'cuda' to 'cpu' for cloud deployment
        'trust_remote_code': True 
    },
    encode_kwargs={
        'normalize_embeddings': True
    }
)

CHROMA_PATH = "./chroma_db"
DATA_PATH = "./data"