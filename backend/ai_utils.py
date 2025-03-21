from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
import os

def get_conversational_chain():
    prompt_template = """
You are an expert document analyst with exceptional abilities to understand, synthesize, and explain information from multiple documents.
INSTRUCTIONS:
1. Provide detailed, comprehensive answers based on the context provided.
2. If information appears in multiple documents, synthesize it into a coherent response.
3. Cite specific sections or pages when relevant (e.g., "According to document X...").
4. If the answer isn't in the context, clearly state "This information is not available in the provided documents".
5. If the question is a greeting or general inquiry, respond appropriately.
6. Structure complex answers with headings and bullet points for clarity when appropriate.
7. Prioritize accuracy over completeness.
Context:
{context}
Question:
{question}
Answer:
"""
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", temperature=0.2)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

def ask_question(session_id, question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    index_path = f"faiss_index_{session_id}"
    if not os.path.exists(index_path):
        return "No processed documents found. Please upload and process documents first."
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    docs = vector_store.similarity_search(question, k=5)
    chain = get_conversational_chain()
    result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    return result.get("output_text", "No answer generated.")