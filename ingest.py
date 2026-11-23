"""Saving Documents into chunks"""
import time
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from vectorstore import vectorstore

BATCH_SIZE = 20
WAIT_SECONDS = 15


def save_batch(batch):
    """Ek batch save karo. Limit lag jaye to 60 second ruk kar dobara try karo."""
    for attempt in range(4):
        try:
            vectorstore.add_documents(batch)
            return
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print("Limit lag gayi, 60 second ruk raha hoon...")
                time.sleep(60)
            else:
                raise
    raise RuntimeError("Baar-baar limit lag rahi hai. Thodi der baad try karo.")


def ingest_files(file_paths):
    # Step 1: Reading Files
    documents = []
    for path in file_paths:
        if path.lower().endswith(".pdf"):
            documents.extend(PyPDFLoader(path).load())
        else:
            documents.extend(TextLoader(path, encoding="utf-8").load())

    # Step 2: Make chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(documents)

    # Step 3: Saving into database
    for i in range(0, len(chunks), BATCH_SIZE):
        save_batch(chunks[i : i + BATCH_SIZE])
        print(f"{min(i + BATCH_SIZE, len(chunks))}/{len(chunks)} chunks save hue")
        time.sleep(WAIT_SECONDS)

    return len(chunks)

if __name__ == "__main__":
    import sys

    total = ingest_files(sys.argv[1:])
    print(f"{total} chunks save ho gaye.")