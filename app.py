import os
from flask import Flask, render_template, request, session
from utils.pdf_processor import extract_text_from_pdf_bytes
from utils.faiss_handler import load_faiss_index
from utils.fetcher import fetch_medical_data
from rag_pipeline import answer_user_query
from sentence_transformers import SentenceTransformer
import pickle
from flask import jsonify
import hashlib
import time
from dotenv import load_dotenv
load_dotenv()

model = SentenceTransformer('pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb')
index = load_faiss_index("vector_db/medical_knowledge.index")

with open("vector_db/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'medisight:'

report_storage = {}
conversation_storage = {}

def get_session_id():
    if 'session_id' not in session:
        session['session_id'] = hashlib.md5(f"{time.time()}".encode()).hexdigest()
        session.permanent = True
    return session['session_id']

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        uploaded_report = request.files.get('report')
        user_query = request.form.get('user_query', '').strip()
        if not user_query:
            return jsonify({"error": "No query provided"}), 400
        
        session_id = get_session_id()
        if session_id not in conversation_storage:
            conversation_storage[session_id] = []
            
        extracted_text = report_storage.get(session_id, None)
        if uploaded_report and uploaded_report.filename != '':
            pdf_bytes = uploaded_report.read()
            new_extracted_text = extract_text_from_pdf_bytes(pdf_bytes)
            if new_extracted_text:
                report_storage[session_id] = new_extracted_text
                session['report_filename'] = uploaded_report.filename
                conversation_storage[session_id] = []
                extracted_text = new_extracted_text
            else:
                return jsonify({"error": "Failed to extract text from PDF. Please ensure it's a valid PDF file."}), 400
        
        conversation_storage[session_id].append(f"User: {user_query}")
        conversation_history = conversation_storage.get(session_id, [])
        response = answer_user_query(user_query, extracted_text, index, model, chunks, conversation_history)
        if response is None:
            response = "I apologize, but I couldn't generate a response. Please try again."
        
        response = str(response).strip()
        conversation_storage[session_id].append(f"AI: {response}")
        
        return jsonify({"answer": response})
    
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/clear_session", methods=["POST"])
def clear_session():
    session_id = get_session_id()
    if session_id in report_storage:
        del report_storage[session_id]
    
    if session_id in conversation_storage:
        del conversation_storage[session_id]
    
    session.pop('report_filename', None)
    return jsonify({"message": "Session cleared successfully"})

# Endpoint to check session status for Debugging
@app.route("/session_status", methods=["GET"])
def session_status():
    session_id = get_session_id()
    return jsonify({
        "session_id": session_id,
        "has_report": session_id in report_storage,
        "report_filename": session.get('report_filename', None),
        "conversation_length": len(conversation_storage.get(session_id, [])),
        "active_sessions": len(report_storage)
    })

@app.route("/search_articles", methods=["POST"])
def search_articles():
    try:
        data = request.get_json()
        user_query = data.get("query", "").strip()
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400
        
        articles = fetch_medical_data(user_query)
        return jsonify(articles)
    
    except Exception as e:
        return jsonify({"error": f"Failed to fetch articles: {str(e)}"}), 500

@app.route("/about")
def about():
    return "<h1>MediSight : Your AI Medical Assistant</h1>"

if __name__ == "__main__":
    app.run(debug=True)