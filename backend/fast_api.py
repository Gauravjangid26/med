from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from RAG_chain import get_rag_with_memory
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict

load_dotenv()

app = FastAPI(
    title="Medical AI Assistant",
    description="Doctor-like AI agent with memory",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class PatientInfo(BaseModel):
    Name: str
    Age: int
    Sex: str
    Region: Optional[str] = ""
    Existing_conditions: Optional[str] = ""
    Current_symptoms: Optional[str] = ""

class QueryRequest(BaseModel):
    user_id: str
    question: str
    patient_info: Optional[PatientInfo] = None  # Accept details from frontend

class QueryResponse(BaseModel):
    answer: str

# Hold QA chains per user
user_chains = {}

def get_chain_for_user(user_id: str):
    if user_id not in user_chains:
        user_chains[user_id] = get_rag_with_memory(user_id)
    return user_chains[user_id]

@app.get("/")
def home():
    return {"message": "Medical AI Assistant API is running"}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    qa_chain = get_chain_for_user(request.user_id)

    # Convert patient info to string
    patient_context = ""
    if request.patient_info:
        info = request.patient_info.dict()
        patient_context = "\n".join([f"{k}: {v}" for k, v in info.items() if v])

    # Combine patient info and question into one string
    full_input = f"{patient_context}\nQuestion: {request.question}"

    # Pass a single input key for LangChain memory
    response = qa_chain.run(full_input)

    return QueryResponse(answer=response)
