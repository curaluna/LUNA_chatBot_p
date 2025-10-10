FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app
    
WORKDIR /app 

COPY requirements/ requirements/

RUN pip install --upgrade pip && \
    pip install -r requirements/core.txt -r requirements/ui.txt


COPY . .
RUN mkdir -p data/pdfs data/vectorstore 

EXPOSE 8000

CMD ["sh","-c","chainlit run apps/chainlit/app.py --host 0.0.0.0 --port ${PORT:-8000}"]