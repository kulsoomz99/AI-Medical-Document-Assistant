# 🩺 AI Medical Document Assistant

A chatbot that answers questions using **your uploaded medical documents** (PDF or TXT). It uses **Retrieval-Augmented Generation (RAG)**

> ⚠️ **Disclaimer:** This is an educational project. It does not diagnose, prescribe, or replace professional medical advice. Always consult a qualified doctor. Do not upload real patient records; use public or synthetic documents only.

---

## Features

- Upload one or more PDF / TXT medical documents
- Ask questions in a chat interface
- Answers are based **only** on the uploaded documents
- Shows sources (file name and page number) when an answer is found
- Says "I could not find this in the uploaded documents" instead of guessing
- Persistent vector database (documents only need to be processed once)
- Fully free stack (Gemini free API key, local ChromaDB)

---

## Tools & Technologies

| Part | Technology |
|---|---|
| Language | Python 3.10+ |
| LLM | Google Gemini (via `langchain-google-genai`) |
| Embeddings | Gemini embeddings (`models/gemini-embedding-001`) |
| Vector database | ChromaDB |
| Framework | LangChain |
| PDF reading | PyPDF |
| UI | Streamlit |


---

## How It Works

The app has two phases.

### 1. Ingestion

1. **Upload** a PDF / TXT file.
2. **Extract text** using PyPDF (page numbers are kept as metadata).
3. **Chunking** with `RecursiveCharacterTextSplitter` (1000 characters, 150 overlap).
4. **Embeddings**: each chunk is converted into a vector (list of numbers that represents its meaning).
5. **Vector database**: chunks and vectors are saved in ChromaDB (`chroma_db/` folder).

### 2. Question answering

1. Your question is converted into a vector.
2. ChromaDB returns the **4 most similar chunks**.
3. The chunks and the question are placed in a prompt that tells Gemini to answer **only from the context**.
4. Gemini writes the answer.
5. The app shows the answer and the source pages (hidden if the answer was not found).

```
Upload → Extract text → Chunk → Embed → ChromaDB
                                           │
Question → Embed → Search top 4 chunks ────┘
                         │
                  Prompt + context → Gemini → Answer + Sources
```

---

## 📁 Project Structure

```
AI-Medical-Document-Assistant/
├── Med_application.py   # Streamlit chat UI (main file to run)
├── AI_Med_Assistant.py               # Answering: search + prompt + Gemini
├── ingest.py            # Read documents, chunk, save to database
├── vectorstore.py       # ChromaDB and embeddings setup
├── requirements.txt     # Python dependencies
├── .gitignore           # Keeps .env and chroma_db/ out of Git
└── chroma_db/           # Created automatically (vector database)
```

| File | Responsibility |
|---|---|
| `Med_application.py` | Upload button, "Process documents", chat box |
| `ingest.py` | `ingest_files()` reads files, splits into chunks, saves in batches |
| `AI_Med_Assistant.py` | `ask()` retrieves chunks, builds the prompt, calls Gemini, returns answer and sources |
| `vectorstore.py` | Creates the embedding model and the ChromaDB `vectorstore`, plus `clear_database()` |


---


### Prerequisites

- Python 3.10 or newer
- A free Gemini API key
- VS Code (or any editor)

### 1. Get a free Gemini API key

1. Go to https://aistudio.google.com/apikey
2. Sign in with a Google account
3. Click **Create API key** and copy it

### 2. Clone or download the project

```bash
git clone <your-repo-url>
cd AI-Medical-Document-Assistant
```

### 3. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Mac / Linux:
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the app

```bash
streamlit run Med_application.py
```

