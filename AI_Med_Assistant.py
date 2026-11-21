import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from vectorstore import vectorstore

load_dotenv()

llm = ChatGoogleGenerativeAI(model= "gemini-3.8-flash")


def ask(question):
    
    results = vectorstore.similarity_search(question, k=4)

    
    context = "\n\n".join([doc.page_content for doc in results])

    
    prompt = f"""You are a medical document assistant.
Answer ONLY from the context below.
If the answer is not in the context, say: "I could not find this in the uploaded documents."
Do not diagnose or prescribe. Keep the answer simple.

Context:
{context}

Question: {question}
"""

    
    answer = llm.invoke(prompt).text

    
    sources = set()
    for doc in results:
        name = os.path.basename(doc.metadata.get("source", "unknown"))
        if "page" in doc.metadata:
            name += f" (page {doc.metadata['page'] + 1})"
        sources.add(name)

    return answer, sorted(sources)