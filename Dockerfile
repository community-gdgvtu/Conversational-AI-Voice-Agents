FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# Using shell form to dynamically read the PORT environment variable
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}