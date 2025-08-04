from utils.faiss_handler import search_index
from utils.embedding_utils import get_pdf_embedding
import numpy as np

def answer_user_query(user_query: str, report_text: str, index, model, chunks: list, k: int = 5) -> str:

    query_embedding = get_pdf_embedding(user_query)

    distances, indices = search_index(index, query_embedding, k)
    retrieved_chunks = [chunks[i] for i in indices[0]]

    context = "\n\n".join(retrieved_chunks)

    if report_text:

        prompt = f"""You are a helpful and kind AI medical assistant. 
        Use the following medical report of the user and the external references to answer the user's question:

        1.Medical Report: 
        {report_text}

        2.External References: 
        {context}

        3.User's Question: 
        {user_query}

        Answer:
        """

    else:

        prompt = f"""You are a helpful and kind AI medical assistant. 
        Use the following external references to answer the user's question:

        1.External References: 
        {context}

        2.User's Question: 
        {user_query}

        Answer:
        """

    response = "[Temp]"
    
    return response