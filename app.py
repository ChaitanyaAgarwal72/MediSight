import os
from flask import Flask, render_template, request, session
from utils.pdf_processor import extract_text_from_pdf_bytes
from utils.faiss_handler import load_faiss_index
from utils.fetcher import fetch_medical_data
from utils.risk_predictor import predict_risk
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

@app.route("/predict", methods=["POST"])
def predict_heart_risk():
    try:
        data = request.get_json()
        prediction, proba = predict_risk(data)
        
        result_text = "High risk of heart disease" if prediction == 1 else "Low risk of heart disease"
        
        return jsonify({
            "result": result_text
        })
    
    except Exception as e:
        print(f"Error in risk prediction: {str(e)}")
        return jsonify({"error": "Failed to predict risk. Please check the input data."}), 500

@app.route("/lifestyle_suggestions", methods=["POST"])
def get_lifestyle_suggestions():
    try:
        data = request.get_json()
        user_data = data.get('user_data', {})
        risk_level = data.get('risk_level', '')
        
        session_id = get_session_id()
        if session_id not in conversation_storage:
            conversation_storage[session_id] = []

        lifestyle_prompt = f"""
            As a medical AI assistant, provide comprehensive lifestyle recommendations for cardiovascular health.

            PATIENT RISK ASSESSMENT: {risk_level}

            PATIENT PROFILE:
            Age: {user_data.get('age', 'N/A')} years
            Sex: {user_data.get('sex', 'N/A')}
            Chest Pain Type: {user_data.get('chestPainType', 'N/A')}
            Blood Pressure: {user_data.get('bloodPressure', 'N/A')} mmHg
            Cholesterol Level: {user_data.get('cholesterol', 'N/A')} mg/dl
            Fasting Blood Sugar: {user_data.get('fastingBloodSugar', 'N/A')}
            Maximum Heart Rate: {user_data.get('maxHeartRate', 'N/A')} bpm
            Exercise Induced Angina: {user_data.get('exerciseAngina', 'N/A')}

            Please provide lifestyle recommendations in these areas:
            1. DIET AND NUTRITION
            2. PHYSICAL ACTIVITY AND EXERCISE
            3. RISK FACTOR MANAGEMENT
            4. LIFESTYLE MODIFICATIONS  
            5. MONITORING AND FOLLOW-UP

            IMPORTANT FORMATTING INSTRUCTIONS:
            - Write in plain text format only
            - Do NOT use markdown symbols like **, ###, -, or checkboxes
            - Do NOT use emojis or special symbols
            - Use simple line breaks and indentation
            - Write as if speaking directly to the patient
            - Keep recommendations clear and actionable

            Provide specific advice tailored to this patient's risk level and health parameters. Base recommendations on current medical guidelines and emphasize consulting healthcare providers.
            """

        conversation_storage[session_id].append(f"User: Lifestyle suggestions request")
        conversation_history = conversation_storage.get(session_id, [])

        response = answer_user_query(lifestyle_prompt, None, index, model, chunks, conversation_history)
        
        if response is None:
            response = "I apologize, but I couldn't generate lifestyle recommendations at this time. Please consult with your healthcare provider for personalized advice."
        
        response = str(response).strip()
        import re        
        response = re.sub(r'^#{1,6}\s*', '', response, flags=re.MULTILINE)
        response = re.sub(r'\*\*(.*?)\*\*', r'\1', response)
        response = re.sub(r'\*(.*?)\*', r'\1', response)
        response = re.sub(r'[✅❌📋💡🏃‍♂️🍎⚕️🧘📊]', '', response)
        response = re.sub(r'^[-*+]\s*', '• ', response, flags=re.MULTILINE)
        response = re.sub(r'\n\s*\n\s*\n', '\n\n', response)
        response = response.strip()
        
        conversation_storage[session_id].append(f"AI: {response}")
        
        return jsonify({"suggestions": response})
    
    except Exception as e:
        print(f"Error generating lifestyle suggestions: {str(e)}")
        return jsonify({"error": "Failed to generate lifestyle suggestions. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True)