# Axiom (UniGuardian)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=flat&logo=react&logoColor=%2361DAFB)

Axiom (formerly UniGuardian) is a sophisticated, full-stack AI conversational tutor. Born from the need for highly accurate, context-aware academic assistance, Axiom leverages an advanced **Retrieval-Augmented Generation (RAG)** pipeline. Unlike generic chatbots, Axiom's responses are strictly grounded in custom-ingested course materials (PDFs, slides, scanned documents), providing students with reliable, verifiable answers complete with exact source and page citations.

This repository serves as a showcase of modern full-stack engineering, combining scalable frontend frameworks, robust Python API design, and cutting-edge machine learning integration.

*   **Live Website:** [https://axiom-tutor.vercel.app](https://axiom-tutor.vercel.app)
  
---

## 🏗️ System Architecture

Axiom operates on a decoupled architecture, ensuring scalability and separation of concerns.

### 1. The Frontend (Client Layer)
*   **Vite + React 19:** Ensures lightning-fast HMR during development and heavily optimized static assets for production.
*   **Tailwind CSS:** Utility-first styling for a highly responsive, modern, and cohesive UI.
*   **Framer Motion:** Delivers fluid micro-animations, enhancing user experience without blocking the main event loop.
*   **Markdown Rendering:** Utilizes `react-markdown` and `remark-gfm` to properly render complex mathematical notation, code blocks, and structured text returned by the LLM.

### 2. The Backend (API & Orchestration Layer)
*   **Flask / Gunicorn:** Provides a lightweight, high-performance WSGI web application to serve API endpoints.
*   **Upstash Redis Rate Limiting:** Implements a privacy-first (IP-hashed) rate limiter using Upstash Redis. It employs atomic counters to prevent race conditions and rolling-window lockouts, safeguarding backend LLM API budgets.
*   **CORS Management:** Strictly configures allowed origins (e.g., Vercel distinct domains) and methods for cross-domain security.

### 3. The AI & Data Layer (Core Engine)
This layer manages the complex interplay between vector databases and Large Language Models.

---

## 🧠 The AI Engine: Deep Dive

### High-Resolution Ingestion Pipeline (`ingestion.py`)
A custom document loader designed to handle difficult, real-world academic materials.
*   **Hi-Res OCR:** Uses `UnstructuredLoader` and `poppler` to aggressively parse scanned documents and images within PDFs, effectively extracting text that standard parsers miss.
*   **Semantic Chunking:** Employs LangChain's `RecursiveCharacterTextSplitter` (1000 chunk size / 100 overlap) to preserve context boundaries.
*   **Metadata Tagging & Sanitization:** Tags every chunk with its source file, course code, page number, and flags scanned origins. Metadata is sanitized (`filter_complex_metadata`) to ensure native compatibility with ChromaDB's strict schema standards.
*   **GPU-Accelerated Local Upload:** Leverages local GPU hardware (PyTorch) to batch process and compute embeddings at immense speeds, writing directly to the persistent `ChromaDB` store.

### The Retrieval System
*   **Maximal Marginal Relevance (MMR):** Instead of naive cosine similarity, Axiom uses MMR (`search_type="mmr"`, pulling 20 chunks and narrowing down to the 6 best). This optimizes for *both* relevance to the query and *diversity* among the chunks, preventing repetitive data ingestion and enriching the LLM's context window.

### Multi-Model LangChain Pipeline (`brain.py`)
Axiom uses a highly sophisticated multi-stage processing pipeline built with LCEL (LangChain Expression Language).
1.  **The Rewriter:** A dedicated prompt transforms the user's conversational query (based on chat history) into a highly optimized, standalone search query for the vector database.
2.  **The Retriever & Formatter:** Executes the MMR search. Crucially, it formats the retrieved text, stripping duplicates and prefixing every chunk with a warning if the text originated from OCR, allowing the LLM to account for artifact errors.
3.  **The RAG Generator:** The primary LLM operates under strict systemic guardrails: it *must* act as a Teaching Assistant, it *must* only use the provided concepts, and it *must* refuse if the context is insufficient.
4.  **The Refiner (Llama 4 Scout Polish):** A specialized secondary prompt chain acts as a pedagogical editor. It automatically repairs common OCR artifacts (e.g., `vo1d` → `void`), cleans up formatting, and ensures an encouraging, academic tone before the response is finally returned to the user.

---

## 📂 Project Structure

```text
axiom/
├── axiom-backend/       
│   ├── brain.py            # LCEL Multi-model pipeline and MMR logic
│   ├── server.py           # Flask endpoints and Upstash Redis rate limiting
│   ├── ingestion.py        # Hi-res OCR, semantic chunking, and ChromaDB DB population
│   ├── config.py           # Environment and model LLM bootstrapping
│   └── requirements.txt    
└── axiom-frontend/      
    ├── src/             
    ├── tailwind.config.js  # Custom theme extensions
    ├── vite.config.js      # Bundler config
    └── package.json     
```

---

## 💻 Getting Started Locally

### Prerequisites
*   Node.js (v18+)
*   Python (3.10+) -> Note: Requires `poppler` installed on your system PATH for OCR.
*   Upstash Redis REST URL & Token.
*   HuggingFace / Groq API Keys.

### 1. Backend Setup
```bash
cd axiom-backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in `axiom-backend/`:
```env
UPSTASH_REDIS_REST_URL=your_redis_url
UPSTASH_REDIS_REST_TOKEN=your_redis_token
GROQ_API_KEY=your_api_key
```

Start the API:
```bash
python server.py
```
*(Runs on `http://localhost:7860`)*

### 2. Frontend Setup
```bash
cd axiom-frontend
npm install
npm run dev
```
*(Runs on `http://localhost:5173`)*

---

