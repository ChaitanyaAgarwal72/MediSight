import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from utils import extract_text_from_pdf

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == 'POST':
        uploaded_report = request.files['report']
        uploaded_img = request.files['img_file']
        
        print(f"Report file: {uploaded_report.filename if uploaded_report else 'None'}")
        print(f"Image file: {uploaded_img.filename if uploaded_img else 'None'}")
        
        report_path = None
        img_path = None

        if uploaded_report and uploaded_report.filename != '':
            filename = secure_filename(uploaded_report.filename)
            upload_dir = os.path.join(os.path.dirname(__file__), "static", "uploads", "reports")
            os.makedirs(upload_dir, exist_ok=True)
            report_path = os.path.join(upload_dir, filename)
            uploaded_report.save(report_path)
            extracted_text = extract_text_from_pdf(report_path)
            print(f"Extracted text from report: {extracted_text[:500]}...")

        if uploaded_img and uploaded_img.filename != '':
            filename = secure_filename(uploaded_img.filename)
            upload_dir = os.path.join(os.path.dirname(__file__), "static", "uploads", "xrays")
            os.makedirs(upload_dir, exist_ok=True)
            img_path = os.path.join(upload_dir, filename)
            uploaded_img.save(img_path)

        return render_template("index.html", 
                               report_path=report_path, img_path=img_path)
    return render_template("index.html")

@app.route("/about")
def about():
    return "<h1>MediSight : Your AI Medical Assistant</h1>"

if __name__ == "__main__":
    app.run(debug=True)