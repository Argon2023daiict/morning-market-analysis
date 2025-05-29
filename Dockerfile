# Use the official Python 3.11 slim image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and git-lfs
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    ffmpeg \
    espeak \
    && git lfs install \
    && rm -rf /var/lib/apt/lists/*

# Create cache directory for Whisper
RUN mkdir -p /app/.cache

# Clone the sentence-transformers model from Hugging Face
RUN git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 /models/all-MiniLM-L6-v2

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Expose the Streamlit or Uvicorn port
EXPOSE 7860

# Start the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
