# backend/RAG_chain.py
from langchain.chains import ConversationalRetrievalChain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Store memory per user
user_memories = {}

def get_rag_with_memory(user_id: str):
    # Path to FAISS vectorstore
    dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_FAISS_PATH = os.path.join(dir_path, "vectorstore", "db_faiss")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    
    prompt_template = """
    You are a professional, friendly, and careful medical assistant acting like a doctor.

    Instructions:

    1. Greet the patient warmly and acknowledge their question.
    2. Review the PATIENT INFO (Name, Age, Sex, Region, Existing conditions, Symptoms) and refer to it naturally.
    3. Go step by step:
    - Ask politely for any missing details.
    - Analyze each symptom, condition, or concern mentioned.
    - Consider context from any additional information available.
    - Explain your reasoning clearly in plain language, as if talking to a real patient.
    4. After completing the step-by-step analysis, provide a **final assessment** including:
    - Severity: 🟢 Mild, 🟡 Moderate, 🔴 Severe
    - Suggested Action: specific next steps or precautions
    - Answer: concise explanation summarizing your analysis
    5. Always include: "⚠️ This is not a medical diagnosis. Please consult a qualified doctor."

    CONTEXT: {context}
    CHAT_HISTORY: {chat_history}
    QUESTION: {question}

    Respond conversationally first, walk through the analysis step by step, and then provide the final assessment at the end.
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "chat_history", "patient_info", "question"]
    )

    llm = ChatOpenAI(
        openai_api_base="https://router.huggingface.co/v1",
        openai_api_key=HF_TOKEN,
        model="openai/gpt-oss-20b:fireworks-ai",
        temperature=0
    )

    if user_id not in user_memories:
        user_memories[user_id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    memory = user_memories[user_id]

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )

    return chain
