# NLPAssist+ : LLM-Powered Question Answering System with RAG

**Version:** BS(AI)V1.0  
**Course:** BS (AI) – Natural Language Processing  
**Department:** Faculty of Engineering Sciences and Technology (FEST)  

---

## Project Overview

**NLPAssist+** is an end-to-end Question Answering system powered by **Local/Open-Source LLMs** and **Retrieval-Augmented Generation (RAG)**. The system allows users (students, faculty, or general users) to:

- Ask natural language questions about university, course content, uploaded documents, or FAQs.  
- Receive chat-style responses with **chat bubbles, timestamps, and typing indicators**.  
- Retrieve and view source snippets or citations for transparency.  
- Benefit from a **secure and efficient backend** with caching and logging.

The solution integrates a **backend NLP/RAG service** with a **frontend client application** for a modern chat experience.

---

## Features

### Backend (Python + FastAPI/Flask)
- **Document Ingestion & Indexing**
  - Upload or configure documents (e.g., FAQs, course outlines, policies).
  - Preprocess documents: clean text, chunk into paragraphs, and generate embeddings.
  - Store embeddings in a vector store (FAISS, ChromaDB, or in-memory).

- **Question Answering Pipeline**
  - Accept queries via REST API (`/api/ask`).
  - Retrieve top-k relevant chunks using embeddings similarity.
  - Generate answers using LLM based on retrieved context.
  - Return structured responses: answer text + source snippets + optional confidence scores.

- **Security, Logging, and Caching**
  - Environment-variable-based secrets for API keys.
  - Input validation and basic authentication/rate-limiting.
  - Caching of embeddings or full responses to reduce latency.
  - Logging of queries, answers, errors, and latency metrics.

### Frontend (React / React Native)
- **Chat-style interface**
  - Input box for user queries.
  - Chat bubbles for user and assistant messages.
  - Typing indicator while LLM generates response.
  - Scrollable conversation history.

- **Source Display**
  - Shows retrieved sources/citations below each answer.
  
- **Optional Features**
  - Multi-turn conversation context.
  - Confidence-based messages if retrieval is low.
  - Analytics page for query statistics.

---


**Components**
1. Document Preprocessing & Chunking
2. Embedding Generation & Vector Store Indexing
3. RAG-based Retrieval & Prompt Construction
4. LLM Answer Generation
5. API Layer (FastAPI/Flask)
6. Frontend Chat UI (React / React Native)

---

## Tools & Technologies

| Area                  | Tools / Libraries |
|-----------------------|-----------------|
| Backend               | Python, FastAPI / Flask, VS Code / PyCharm |
| LLM & Embeddings      | HuggingFace Transformers, Sentence-Transformers |
| Vector Store / RAG    | FAISS, ChromaDB, LangChain (optional) |
| Frontend              | React / React Native, Axios / Fetch |
| Data Storage / Cache  | JSON, SQLite, Redis (optional) |
| Security              | Environment variables, basic auth, input validation |
| Testing & Debugging   | Postman / Thunder Client, Browser DevTools |

---

## Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/<muhammadsufyan-khan>/NLPAssistPlus.git
cd NLPAssistPlus


## System Architecture

```
## Setup Backend
```
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn app:app --reload
```
## Access Application
```
Backend API runs at http://localhost:8000/api/ask
```
## Usage

Upload documents via backend or configure default dataset.

Type questions in the chat input box.

Receive responses with cited sources and confidence scores.

Monitor logs for backend queries and performance metrics.

### Deliverables

## Report

Introduction, Objective & Goals

System Architecture Diagrams

Data Flow & RAG Pipeline Diagrams

Methodology, Tools, Libraries

Results & Discussion (Screenshots and Analysis)

## Code

Backend: Python, RAG pipeline

Frontend: React / React Native

Instructions in README.md

## Future Enhancements

Enhanced multi-turn conversations with memory.

Advanced analytics dashboard for usage insights.

Integration with larger LLM models or cloud vector databases.

## License

This project is licensed under the MIT License. See LICENSE for details.

## Acknowledgements

HuggingFace Transformers & Sentence-Transformers

FAISS / ChromaDB for vector search

FastAPI / Flask for backend APIs

React / React Native for frontend development
# NLP-CHATBOT-
