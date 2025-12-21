FROM python:3.11-slim

WORKDIR /app
# Install CPU-only PyTorch first to avoid CUDA/cuBLAS dependencies (faster, smaller image)
# Increased timeout (900s=15min) and retries (5) for slow/unstable network connections
# Remove this line and pip will install CUDA version (needed only if you have NVIDIA GPU)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY .env.example ./.env
ENV PYTHONUNBUFFERED=1

CMD ["python", "app/workers/worker.py"]
