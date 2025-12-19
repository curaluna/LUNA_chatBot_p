FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 

WORKDIR /app

COPY pyproject.toml ./
COPY src/ /app/src/

RUN pip install --upgrade pip && pip install .

EXPOSE 8080

CMD ["sh","-c","uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
