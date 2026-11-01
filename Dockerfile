FROM python:3.10-slim

# Install system dependencies required for Box2D (swig, C++ build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    swig \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and pre-install lightweight PyTorch CPU build
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install project dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and pre-trained weights
COPY . .

# Setup non-root user required by Hugging Face Spaces (UID 1000)
RUN useradd -m -u 1000 user && \
    chown -R user:user /app
USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PORT=7860

EXPOSE 7860

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]
