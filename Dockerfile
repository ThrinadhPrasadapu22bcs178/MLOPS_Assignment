FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy source code and mlruns (for the model)
COPY src/ src/
COPY mlruns/ mlruns/
COPY metrics.json .
COPY mlflow.db .

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
