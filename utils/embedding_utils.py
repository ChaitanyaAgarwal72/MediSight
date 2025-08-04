from sentence_transformers import SentenceTransformer

model = SentenceTransformer('pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb')

def get_pdf_embedding(text : str) -> list:
    embedding = model.encode(text)
    return embedding.tolist()

