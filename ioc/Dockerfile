FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

# PyTorch CPU-only.
# Avoid installing the CUDA/NVIDIA stack: IoC only needs CPU embeddings.
RUN pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    "torch==2.14.0+cpu"

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "p2.api:app", "--host", "0.0.0.0", "--port", "8000"]