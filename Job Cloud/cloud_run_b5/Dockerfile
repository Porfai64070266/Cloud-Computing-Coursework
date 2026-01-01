# Cloud Run Dockerfile for BigQuery query UI
FROM python:3.11-slim

WORKDIR /app

# Install system deps (optional) then copy requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

ENV PORT=8080
CMD ["python", "app/app.py"]
