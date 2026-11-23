"""Streamlit UI for the AI Medical Document Assistant."""
import os
import tempfile

import streamlit as st

from ingest import ingest_files
from AI_Med_Assistant import ask
from vectorstore import clear_database

st.set_page_config(page_title="AI Medical Document Assistant", page_icon="🩺")
st.title("🩺 AI Medical Document Assistant")
st.caption("Upload medical documents (PDF/TXT) and ask questions about them.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Sidebar: upload ----------
with st.sidebar:
    st.header("Documents")
    files = st.file_uploader(
        "Upload PDF / TXT", type=["pdf", "txt"], accept_multiple_files=True
    )
    if st.button("Process documents") and files:
        with st.spinner("Reading and indexing..."):
            tmp_dir = tempfile.mkdtemp()
            paths = []
            for f in files:
                p = os.path.join(tmp_dir, f.name)
                with open(p, "wb") as out:
                    out.write(f.getbuffer())
                paths.append(p)
            n = ingest_files(paths)
        st.success(f"Done! {n} chunks stored.")

    if st.button("Clear database"):
        clear_database()
        st.session_state.messages = []
        st.success("Database cleared.")

    st.info("⚠️ Educational project. Not a substitute for professional medical advice.")

# ---------- Chat ----------
for role, text in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(text)

question = st.chat_input("Ask something about your documents...")
if question:
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer, sources = ask(question)
                reply = answer
                if sources:
                    reply += "\n\n**Sources:** " + ", ".join(sources)
            except Exception as e:
                reply = f"Error: {e}"
        st.markdown(reply)
    st.session_state.messages.append(("user", question))
    st.session_state.messages.append(("assistant", reply))