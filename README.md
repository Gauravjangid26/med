<<<<<<< HEAD
# 🩺 Medical Chatbot using LangChain + Gemini + Streamlit + FastAPI + Docker

A specialized medical chatbot that answers only **medical-related questions**, using **Google Gemini via LangChain**, with a frontend using **Streamlit** (or Telegram bot), backend via **FastAPI**, and containerized with **Docker**.

---

## 🚀 Features

- ✅ Uses Gemini instead of OpenAI
- ✅ Medical domain-specific (ignores general chit-chat)
- ✅ LangChain-powered Retriever + Conversational Memory
- ✅ Streamlit or Telegram interface
- ✅ FastAPI backend
- ✅ Dockerized for deployment

---

## 🗂️ Project Structure

```
medical-chatbot/
│
├── main.py                     # FastAPI app
├── chatbot.py                  # Chat logic using LangChain + Gemini
├── vectorstore.py              # Vector DB setup (FAISS, etc.)
├── ingest.py                   # Loads & embeds medical docs
├── memory.py                   # LangChain memory integration
├── prompt.py                   # Prompt template for Gemini
├── interface/
│   ├── streamlit_app.py        # Streamlit interface
│   └── telegram_bot.py         # (Optional) Telegram bot interface
├── data/                       # Store medical documents
│   └── medical_docs.pdf
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## ⚙️ Setup (Windows)

### 1. 🐍 Create environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. 📦 Install requirements

```bash
pip install -r requirements.txt
```

Or use `uv`:

```bash
uv pip install -r requirements.txt
```

### 3. 📁 Embed documents

```bash
python ingest.py
```

### 4. ▶️ Run Streamlit interface

```bash
streamlit run interface/streamlit_app.py
```

### 5. ▶️ Run FastAPI server

```bash
uvicorn main:app --reload
```

---

## 🐳 Docker (Optional)

```bash
docker build -t medical-chatbot .
docker run -p 8000:8000 medical-chatbot
```

---

## 🔐 API Keys

Create a `.env` file:

```env
GEMINI_API_KEY=your_google_gemini_key_here
```

Or set it in your system environment variables.

---

## 👨‍⚕️ Example Prompts

- “What are the symptoms of dengue?”
- “How is hypertension treated?”
- “Can I take ibuprofen with paracetamol?”

---

## 🧠 LangChain Memory

This chatbot supports **Conversational Memory** for context-aware replies using LangChain.

---

=======
# AI-medical-assistant
>>>>>>> f9a4a99 (first commit)
# med
# med
