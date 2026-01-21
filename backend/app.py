from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time
import hashlib

# Aapka purana RAG logic
from rag_pipeline import RAGPipeline, QuestionRequest, AnswerResponse

# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title="NLPAssist+ for Iqra University",
    version="1.0"
)

# =========================
# CORS (Frontend Access)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sab origins allow hain taake local HTML file connect ho sakay
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# CACHE & LOGGING
# =========================
cache = {}
query_log = []

# =========================
# INITIALIZE RAG
# =========================
# System check ke liye hum startup par message dikhayenge
print("Starting RAG Pipeline for Iqra University...")
rag_pipeline = RAGPipeline()

# =========================
# REQUEST / RESPONSE MODELS
# =========================
class ChatRequest(BaseModel):
    question: str
    user_id: Optional[str] = "student"

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float
    response_time: float
    cached: bool = False
    retrieved_chunks: List[str]

# =========================
# UTILS
# =========================
def get_cache_key(question: str) -> str:
    return hashlib.md5(question.lower().strip().encode()).hexdigest()

# =========================
# MAIN QA ENDPOINT
# =========================
@app.post("/api/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    start_time = time.time()
    cache_key = get_cache_key(request.question)

    print(f"Sawal aaya: {request.question}") # Terminal mein check karne ke liye

    # -------- CACHE CHECK --------
    if cache_key in cache:
        print("Jawab cache se mil gaya!")
        cached_data = cache[cache_key]
        return ChatResponse(
            **cached_data,
            cached=True,
            response_time=round(time.time() - start_time, 3)
        )

    try:
        # -------- RAG PIPELINE --------
        # Pipeline se answer mangwayein
        result: AnswerResponse = rag_pipeline.ask(request.question)

        response_time = round(time.time() - start_time, 3)

        chat_response = ChatResponse(
            answer=result.answer,
            sources=result.sources,
            confidence=result.confidence,
            retrieved_chunks=result.retrieved_chunks,
            response_time=response_time,
            cached=False
        )

        # -------- CACHE STORE --------
        cache[cache_key] = {
            "answer": result.answer,
            "sources": result.sources,
            "confidence": result.confidence,
            "retrieved_chunks": result.retrieved_chunks
        }

        # -------- LOGGING --------
        query_log.append({
            "question": request.question,
            "user_id": request.user_id,
            "response_time": response_time,
            "timestamp": time.time()
        })

        return chat_response

    except Exception as e:
        print(f"ERROR: {str(e)}") # Agar koi masla aaye toh terminal mein dikhayein
        raise HTTPException(status_code=500, detail=f"Backend Error: {str(e)}")

# =========================
# LOCAL RUN
# =========================
if __name__ == "__main__":
    import uvicorn
    # Make sure port 8000 is free
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
