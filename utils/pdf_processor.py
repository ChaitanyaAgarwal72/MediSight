import fitz
import os

def extract_text_from_pdf_bytes(pdf_bytes):
    text = ""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception:
        return None
    return text.strip()

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def load_and_chunk_pdf(folder_path: str) -> list:
    total_chunks = []
    for pdf_file in os.listdir(folder_path):
        if pdf_file.endswith('.pdf'):
            text = extract_text_from_pdf(os.path.join(folder_path, pdf_file))
            words = text.split()

            chunk_size = 200
            chunks = []

            for i in range(0, len(words), chunk_size):
                chunk = words[i : i+chunk_size]
                chunks.append(' '.join(chunk))
            total_chunks.extend(chunks)
        print(f"Processed {pdf_file}, created {len(chunks)} chunks.")
    return total_chunks
