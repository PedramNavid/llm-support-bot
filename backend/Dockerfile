FROM python:3.11-bookworm

ARG OPENAI_API_KEY
ARG PINECONE_API_KEY

WORKDIR /app
COPY setup.py .
RUN pip install -e .
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--app-dir=./llm_support_bot"]
