import fitz
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb')

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def get_pdf_embedding(text : str) -> list:
    embedding = model.encode(text)
    return embedding.tolist()