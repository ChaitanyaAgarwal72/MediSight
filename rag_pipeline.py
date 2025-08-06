from utils.faiss_handler import search_index
from utils.embedding_utils import get_pdf_embedding
import numpy as np
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def answer_user_query(user_query: str, report_text: str, index, model, chunks: list, conversation_history: list = None, k: int = 5) -> str:

    query_embedding = get_pdf_embedding(user_query)

    distances, indices = search_index(index, query_embedding, k)
    retrieved_chunks = [chunks[i] for i in indices[0]]

    context = "\n\n".join(retrieved_chunks)

    conversation_context = ""
    if conversation_history and len(conversation_history) > 0:
        recent_history = conversation_history[-6:] if len(conversation_history) > 6 else conversation_history
        conversation_context = "\n".join(recent_history)

    if report_text:

        prompt = f"""You are a medically intelligent, empathetic AI assistant called MediSight.

            Use the following medical report, previous conversation context, and external references to answer the user's question accurately, clearly, and kindly.

            Medical Report:
            {report_text}

            Previous Conversation Context:
            {conversation_context}

            External References (trusted sources):
            {context}

            User's Current Question:
            {user_query}

            Instructions:
            -------------
            1. Remember the previous conversation context when answering.
            2. Explain abnormalities in the report (if any).
            3. Use external references to support your explanation.
            4. Structure your response clearly, using sections or bullet points.
            5. Use emojis like ⚠️, ✅, 📌 to highlight key points.
            6. Be kind, concise, and helpful.
            7. Remind the user to consult a real doctor.
            8. If the user is asking follow-up questions, refer back to previous parts of our conversation.
            9. If the report is not related to medical conditions, inform the user that the report does not contain relevant medical information.

            Now, write your answer:
            """

    else:

        prompt = f"""You are a medically intelligent, empathetic AI assistant called MediSight.

            Use the previous conversation context and external references to answer the user's medical question clearly and kindly.

            Previous Conversation Context:
            {conversation_context}

            External References (trusted sources):
            {context}

            User's Current Question:
            {user_query}

            Instructions:
            -------------
            1. Remember the previous conversation context when answering.
            2. Use trusted information to give a concise answer.
            3. Structure your response clearly.
            4. Use emojis like ⚠️, ✅, 📌 to highlight key points.
            5. Be kind, concise, and helpful.
            6. Remind the user to consult a real doctor.
            7. If the user is asking follow-up questions, refer back to previous parts of our conversation.

            Now, write your answer:
            """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    return response.text