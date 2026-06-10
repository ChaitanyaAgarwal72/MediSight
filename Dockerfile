FROM python:3.11-slim

# Set up a non-root user (required by Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY --chown=user:user requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the SentenceTransformer model during build
# This prevents downloading a 400MB+ model on every container startup
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb')"

# Copy the rest of the application
COPY --chown=user:user . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port Hugging Face Spaces uses
EXPOSE 7860

# Run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7860", "--timeout", "120", "--workers", "2", "app:app"]
