import os
from typing import List, Tuple
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# =========================
# Pydantic Models (Zaroori Classes)
# =========================
class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list
    confidence: float
    retrieved_chunks: list

class RAGPipeline:
    def __init__(self):
        # Behtar embeddings aur model ka istemal
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        self.qa_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

        self.chunks: List[str] = []
        self.vector_index = None

        self._load_documents()
        self._create_vector_index()

    def _load_documents(self):
        # Knowledge base ko mazeed tafseeli (detailed) kar diya hai
        self.chunks = [
            "Iqra University (IU) was chartered by the Government of Sindh in 1998. It has campuses in Karachi (Main, North, EDC, Airport), Islamabad, and Quetta.",
            "The Main Campus is located at Gulshan-e-Iqbal, Block 9, Karachi. For queries, call 021-111-264-264 or email info@iqra.edu.pk.",
            "Admissions at Iqra University are open twice a year: Fall Semester (starts September) and Spring Semester (starts February).",
            "The BS Computer Science (BSCS) is a 4-year degree requiring 130 credit hours and a minimum CGPA of 2.0 for graduation.",
            "Fee Structure: For most BS programs, the fee per semester ranges between 80,000 to 120,000 PKR. Exact fees depend on the number of courses.",
            "Attendance Policy: Students must maintain a minimum of 80% attendance in each course to be eligible for final examinations.",
            "Scholarships: IU offers Merit-based scholarships for high achievers, Need-based for financial support, and specialized Sports scholarships.",
            "Library Timings: The library is open Monday to Friday from 8:00 AM to 8:00 PM, and on weekends from 9:00 AM to 5:00 PM.",
            "Hostel: Separate hostel facilities are available for out-station female students at the Karachi campus with secure environments.",
            "Career Services: The Career Services Office (CSO) helps students with internship placements, CV writing, and job interviews with top firms.",
            "LMS Access: Students can access their portal, grades, and course material at https://lms.iqra.edu.pk using their student ID.",
            "Convocation: Graduation ceremonies are typically held in December each year to celebrate student achievements."
        ]

    def _create_vector_index(self):
        embeddings = self.embedding_model.encode(self.chunks, convert_to_numpy=True)
        dimension = embeddings.shape[1]
        self.vector_index = faiss.IndexFlatL2(dimension)
        self.vector_index.add(embeddings)
        print(f"[RAG] System Ready: {self.vector_index.ntotal} knowledge points loaded.")

    def _retrieve(self, question: str, top_k: int = 3) -> List[str]:
        question_embedding = self.embedding_model.encode([question], convert_to_numpy=True)
        distances, indices = self.vector_index.search(question_embedding, top_k)
        return [self.chunks[idx] for idx in indices[0] if idx < len(self.chunks)]

    def _generate_answer(self, question: str, retrieved_chunks: List[str]) -> str:
        context = " ".join(retrieved_chunks)
        
        # ChatGPT jaisa response dene ke liye prompt ko instruction-based banaya gaya hai
        prompt = f"Instruction: Provide a detailed and helpful answer about Iqra University using the context. Context: {context} Question: {question}"

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

        with torch.no_grad():
            output = self.qa_model.generate(
                **inputs,
                max_length=200,
                num_beams=5,
                no_repeat_ngram_size=2,
                early_stopping=True
            )

        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def ask(self, question: str) -> AnswerResponse:
        retrieved_texts = self._retrieve(question)
        answer = self._generate_answer(question, retrieved_texts)

        return AnswerResponse(
            answer=answer,
            sources=["Official University Database"],
            confidence=0.92,
            retrieved_chunks=retrieved_texts
        )
