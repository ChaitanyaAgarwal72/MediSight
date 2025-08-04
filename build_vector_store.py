from utils.pdf_processor import load_and_chunk_pdf
from utils.faiss_handler import build_faiss_index_from_chunks
from sentence_transformers import SentenceTransformer
import faiss

folder_path = "data/"
pdf_chunks = load_and_chunk_pdf(folder_path)

model = SentenceTransformer("pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb")

build_faiss_index_from_chunks(pdf_chunks, model)