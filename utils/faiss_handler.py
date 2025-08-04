import faiss
import numpy as np

def init_faiss_index(dim : int):
    return faiss.IndexFlatL2(dim)

def add_to_index(index, embedding: list):
    array = np.array(embedding).reshape(1, -1)
    index.add(array)

def search_index(index, query_embedding: list, k: int = 5) -> list:
    query_array = np.array(query_embedding).reshape(1, -1)
    distances, indices = index.search(query_array, k)
    return distances.tolist(), indices.tolist()

def build_faiss_index_from_chunks(chunks: list, model) -> faiss.IndexFlatL2:
    temp = model.encode(chunks[0])
    index = faiss.IndexFlatL2(temp.shape[0])
    for chunk in chunks:
        embedding = model.encode(chunk)
        embedding = np.array(embedding).reshape(1, -1)
        index.add(embedding)
    
    save_path = "vector_db/medical_knowledge.index"
    faiss.write_index(index, save_path)
    print(f"Saved FAISS index to {save_path}")

    return index

def load_faiss_index(index_path: str) -> faiss.IndexFlatL2:
    index = faiss.read_index(index_path)
    return index