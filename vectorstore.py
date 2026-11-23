from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# Text to numbers
embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# ChromaDB: chunks saved
vectorstore = Chroma(
    collection_name="medical_docs",
    persist_directory="chroma_db",
    embedding_function=embedding_model,
)


def clear_database():
    vectorstore.delete_collection()