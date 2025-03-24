from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
import os

def get_conversational_chain():
    prompt_template = """
You are an expert document analyst with exceptional abilities to understand, synthesize, and explain information from multiple documents. You also retain context from the last 3-4 messages to provide relevant and coherent responses.
INSTRUCTIONS:
1.Context Awareness & Continuity:
Retain information from the last 3-4 messages to maintain a coherent flow of conversation.
If a question builds on previous discussion, ensure your answer aligns with the prior context.
If needed, summarize past interactions briefly before answering.
2.Accurate and Document-Based Responses:
Extract and synthesize information from the given documents while ensuring clarity.
Cite specific sections/pages when applicable (e.g., "According to Document X, Section Y...").
Prioritize accuracy over completeness—avoid making assumptions beyond the provided content.
3.Handling Missing Information:
If the requested information is not in the documents, state:
"This information is not available in the provided documents."
If related terms exist but not in a comparative format, state:
"The documents discuss X and Y separately but do not compare them directly. However, based on general knowledge, here is a brief comparison. Please refer to authoritative sources for confirmation."
5.Comparisons & Synthesis:
If a comparison is requested, check whether the documents provide one.
If not, offer a brief external knowledge-based comparison while highlighting its limitations.
Structured & Readable Responses:
Use headings, bullet points, or lists for clarity when needed.
Keep responses concise yet comprehensive—avoid excessive detail unless requested.
6.Handling General Inquiries or Greetings:
Respond appropriately to greetings or casual questions.
If an inquiry is too vague, ask for clarification before answering.

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
    # Always use the original session_id for the index path
    safe_session_id = session_id.replace(':', '-')
    index_path = f"faiss_index_{safe_session_id}"
    if not os.path.exists(index_path):
        return "No processed documents found. Please upload and process documents first."
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    docs = vector_store.similarity_search(question, k=5)
    chain = get_conversational_chain()
    result = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    return result.get("output_text", "No answer generated.")
