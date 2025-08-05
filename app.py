import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from utils.embedding_utils import get_pdf_embedding
from utils.pdf_processor import extract_text_from_pdf
from utils.faiss_handler import load_faiss_index
from rag_pipeline import answer_user_query
from sentence_transformers import SentenceTransformer
import pickle
import markdown
from flask import jsonify

model = SentenceTransformer('pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb')
index = load_faiss_index("vector_db/medical_knowledge.index")

with open("vector_db/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

app = Flask(__name__)

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

        extracted_text = None
        if uploaded_report and uploaded_report.filename != '':
            filename = secure_filename(uploaded_report.filename)
            upload_dir = os.path.join(os.path.dirname(__file__), "static", "uploads", "reports")
            os.makedirs(upload_dir, exist_ok=True)
            report_path = os.path.join(upload_dir, filename)
            uploaded_report.save(report_path)
            extracted_text = extract_text_from_pdf(report_path)

        response = answer_user_query(user_query, extracted_text, index, model, chunks)
        
        if response is None:
            response = "I apologize, but I couldn't generate a response. Please try again."
        
        response = str(response).strip()
        
        return jsonify({"answer": response})
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/articles")
def show_articles():
    return "<h1>Articles Page</h1>"

@app.route("/about")
def about():
    return "<h1>MediSight : Your AI Medical Assistant</h1>"

if __name__ == "__main__":
    app.run(debug=True)