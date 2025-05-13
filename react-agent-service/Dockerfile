FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn python-dotenv llama_index requests

# Copy service files
COPY . .

# Expose the service port
EXPOSE 8003

# Start the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]