FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \ 
    LUNA_DATA_DIR=/app/data/chroma_vectorstorage

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --upgrade pip && pip install .

COPY app.py ./       
COPY chainlit.md ./ 
COPY data/ ./data/
COPY data/chroma_vectorstorage ./data/chroma_vectorstorage
COPY public/ ./public/

RUN mkdir -p /app/data/pdfs /app/data/chroma_vectorstorage

EXPOSE 8000

CMD ["sh","-c","chainlit run app.py --host 0.0.0.0 --port ${PORT:-8000}"]
