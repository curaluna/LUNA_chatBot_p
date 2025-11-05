FROM python:3.12-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app \
    VECTOR_DIR=/app/data/vectorstore
                                                                                                        
WORKDIR /app


COPY pyproject.toml README.md ./
COPY src/ ./src/


RUN pip install --upgrade pip && \
    pip install .

COPY . .


RUN mkdir -p /app/data/pdfs /app/data/vectorstore

EXPOSE 8000



CMD ["sh","-c","chainlit run app.py --host 0.0.0.0 --port ${PORT:-8000}"]
