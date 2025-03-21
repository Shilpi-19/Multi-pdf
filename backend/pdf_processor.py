from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

def get_pdf_text(pdf_files):
    text = ""
    for pdf in pdf_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter.split_text(text)

def create_vector_store(text_chunks, session_id):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    index_path = f"faiss_index_{session_id}"
    if os.path.exists(index_path):
        vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_texts(text_chunks)
    else:
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(index_path)
    return vector_store

def process_pdfs(session_id, pdf_files):
    raw_text = get_pdf_text(pdf_files)
    if not raw_text.strip():
        return False
    text_chunks = get_text_chunks(raw_text)
    create_vector_store(text_chunks, session_id)
    return True