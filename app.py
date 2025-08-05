import os
from flask import Flask, render_template, request
from matplotlib.pylab import indices
from werkzeug.utils import secure_filename
from utils.embedding_utils import get_pdf_embedding
from utils.pdf_processor import extract_text_from_pdf
from utils.faiss_handler import load_faiss_index, search_index

index = load_faiss_index("vector_db/medical_knowledge.index")
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == 'POST':
        uploaded_report = request.files['report']
        
        report_path = None

        if uploaded_report and uploaded_report.filename != '':
            filename = secure_filename(uploaded_report.filename)
            upload_dir = os.path.join(os.path.dirname(__file__), "static", "uploads", "reports")
            os.makedirs(upload_dir, exist_ok=True)
            report_path = os.path.join(upload_dir, filename)
            uploaded_report.save(report_path)
            extracted_text = extract_text_from_pdf(report_path)

        return render_template("index.html", report_path=report_path)
    return render_template("index.html")

@app.route("/articles")
def show_articles():
    return "<h1>Articles Page</h1>"

@app.route("/about")
def about():
    return "<h1>MediSight : Your AI Medical Assistant</h1>"

if __name__ == "__main__":
    app.run(debug=True)