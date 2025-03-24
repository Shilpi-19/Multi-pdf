from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this import
from database import init_db, save_message, save_pdf_upload, get_messages, get_pdf_uploads, get_all_chat_history_ids, delete_session
from pdf_processor import process_pdfs
from ai_utils import ask_question
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

app = Flask(__name__)
# Enable CORS for all routes, allowing requests from http://localhost:3000
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
init_db()

@app.route('/sessions', methods=['GET'])
def list_sessions():
    sessions = get_all_chat_history_ids()
    return jsonify(sessions)

@app.route('/sessions', methods=['POST'])
def create_session():
    session_id = datetime.now().strftime("%d-%m-%Y,%H:%M:%S")
    return jsonify({'session_id': session_id})

@app.route('/sessions/<session_id>', methods=['DELETE'])
def delete_session_route(session_id):
    delete_session(session_id)
    index_path = f"faiss_index_{session_id}"
    if os.path.exists(index_path):
        import shutil
        shutil.rmtree(index_path)
    return jsonify({'message': 'Session deleted'})

@app.route('/sessions/<session_id>/upload', methods=['POST'])
def upload_pdfs(session_id):
    if 'pdfs' not in request.files:
        return jsonify({'error': 'No PDFs uploaded'}), 400
    pdf_files = request.files.getlist('pdfs')
    success = process_pdfs(session_id, pdf_files)
    if success:
        for pdf in pdf_files:
            save_pdf_upload(session_id, pdf.filename)
        return jsonify({'message': f'{len(pdf_files)} document(s) processed'})
    return jsonify({'error': 'No text extracted from PDFs'}), 400

@app.route('/sessions/<session_id>/ask', methods=['POST'])
def ask_question_route(session_id):
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    answer = ask_question(session_id, question)
    save_message(session_id, 'user', 'text', question)
    save_message(session_id, 'assistant', 'text', answer)
    return jsonify({'answer': answer})

@app.route('/sessions/<session_id>/messages', methods=['GET'])
def get_messages_route(session_id):
    messages = get_messages(session_id)
    return jsonify(messages)

@app.route('/sessions/<session_id>/pdfs', methods=['GET'])
def get_pdfs_route(session_id):
    pdfs = get_pdf_uploads(session_id)
    return jsonify(pdfs)

@app.route('/sessions/<session_id>/rename', methods=['PUT'])
def rename_session(session_id):
    new_name = request.json.get('new_name')
    if not new_name:
        return jsonify({'error': 'New name is required'}), 400
    
    # Add validation to prevent duplicate names
    sessions = get_all_chat_history_ids()
    if new_name in sessions:
        return jsonify({'error': 'Session name already exists'}), 409
    
    # Rename the session (you'll need to implement this function)
    try:
        # Rename associated files/directories
        old_index_path = f"faiss_index_{session_id.replace(':', '-')}"
        new_index_path = f"faiss_index_{new_name}"
        if os.path.exists(old_index_path):
            os.rename(old_index_path, new_index_path)
        
        # Update any other session-related data
        # ... (implement according to your storage mechanism)
        
        return jsonify({'success': True, 'new_name': new_name})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
