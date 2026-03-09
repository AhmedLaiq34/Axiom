# Axiom

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=flat&logo=react&logoColor=%2361DAFB)

Axiom is a full-stack, AI-powered conversational tutor. Built to provide intelligent, context-aware responses, it leverages advanced Retrieval-Augmented Generation (RAG) to serve accurate information from a custom knowledge base, tailored to FAST NUCES University curriculum.

This project demonstrates proficiency in building scalable full-stack applications, integrating state-of-the-art Large Language Models (LLMs), managing vector databases, and creating responsive, modern user interfaces.

---

## 🚀 Features

*   **Intelligent Conversational AI:** Utlilizes LangChain and HuggingFace to provide accurate, context-aware answers.
*   **Retrieval-Augmented Generation (RAG):** Integrates ChromaDB as a vector store to retrieve semantic source documents, ensuring the AI's responses are grounded in provided data.
*   **Robust Backend API:** Built with Python and Flask, featuring secure endpoints, CORS configuration, and scalable architecture.
*   **Advanced Rate Limiting:** Implements Upstash Redis for privacy-conscious, IP-hashed rate limiting to protect API endpoints and manage quota.
*   **Modern, Responsive Frontend:** A sleek React application built with Vite, styled with Tailwind CSS, and enriched with Framer Motion animations.
*   **Source Citation:** The UI transparently presents the sources and page numbers used to generate the AI's answers.

---

## 🛠️ Technology Stack

### Backend (`axiom-backend`)
*   **Framework:** Flask
*   **AI / LLM:** LangChain, HuggingFace, Sentence Transformers
*   **Vector Database:** ChromaDB
*   **Caching & Rate Limiting:** Upstash Redis
*   **Other Tools:** Pydantic, Gunicorn, PyTorch

### Frontend (`axiom-frontend`)
*   **Framework:** React 19 (managed via Vite)
*   **Styling:** Tailwind CSS, PostCSS, Autoprefixer
*   **Icons & Animations:** Lucide React, Framer Motion
*   **Markdown Rendering:** React Markdown, Remark GFM

---

## 📂 Project Structure

```text
axiom/
├── axiom-backend/       # Python/Flask Backend API
│   ├── brain.py         # Core LLM and RAG logic (LangChain orchestration)
│   ├── server.py        # Flask application, routing, and Redis rate limiting
│   ├── ingestion.py     # Document processing and ChromaDB embedding pipeline
│   └── requirements.txt # Python dependencies
└── axiom-frontend/      # React/Vite Frontend Application
    ├── src/             # React components and hooks
    ├── package.json     # Node.js dependencies
    ├── tailwind.config.js # Tailwind CSS configuration
    └── vite.config.js   # Vite bundler configuration
```

---

## 💻 Getting Started

### Prerequisites
*   Node.js (v18+)
*   Python (3.10+)
*   Upstash Redis account (for rate limiting)
*   HuggingFace/Groq API Keys (depending on your LLM setup in `.env`)

### Local Development Setup

#### 1. Backend Setup
```bash
cd axiom-backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in `axiom-backend/` based on your configuration:
```env
UPSTASH_REDIS_REST_URL=your_redis_url
UPSTASH_REDIS_REST_TOKEN=your_redis_token
# Add your specific LLM API keys here
```

Run the backend server:
```bash
python server.py
```
*The API will start on `http://localhost:7860`.*

#### 2. Frontend Setup
Open a new terminal window:
```bash
cd axiom-frontend
npm install
npm run dev
```
*The frontend will start on usually `http://localhost:5173`.*

---

## 🤝 Contact & links

*   **Repository:** [https://github.com/AhmedLaiq34/Axiom](https://github.com/AhmedLaiq34/Axiom)
*   **Frontend Deployment (Example):** [https://axiom-tutor.vercel.app](https://axiom-tutor.vercel.app)

---
*This repository is designed to showcase full-stack development and AI integration skills. Feel free to explore the codebase!*
