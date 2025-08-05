from utils.faiss_handler import search_index
from utils.embedding_utils import get_pdf_embedding
import numpy as np
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def answer_user_query(user_query: str, report_text: str, index, model, chunks: list, k: int = 5) -> str:

    query_embedding = get_pdf_embedding(user_query)

    distances, indices = search_index(index, query_embedding, k)
    retrieved_chunks = [chunks[i] for i in indices[0]]

    context = "\n\n".join(retrieved_chunks)

    if report_text:

        prompt = f"""You are a medically intelligent, empathetic AI assistant called MediSight.

    Use the following medical report and external references to answer the user's question accurately, clearly, and kindly.

    Medical Report:
    {report_text}

    External References (trusted sources):
    {context}

    User's Question:
    {user_query}

    Instructions:
    -------------
    1. Explain abnormalities in the report (if any).
    2. Use external references to support your explanation.
    3. Structure your response clearly, using sections or bullet points.
    4. Use emojis like ⚠️, ✅, 📌 to highlight key points.
    5. Be kind, concise, and helpful.
    6. Remind the user to consult a real doctor.

    Now, write your answer:
    """

    else:

        prompt = f"""You are a medically intelligent, empathetic AI assistant called MediSight.

    Use the external references to answer the user's medical question clearly and kindly.

    External References (trusted sources):
    {context}

    User's Question:
    {user_query}

    Instructions:
    -------------
    1. Use trusted information to give a concise answer.
    2. Structure your response clearly.
    3. Use emojis like ⚠️, ✅, 📌 to highlight key points.
    4. Be kind, concise, and helpful.
    5. Remind the user to consult a real doctor.

    Now, write your answer:
    """


    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    return response.text