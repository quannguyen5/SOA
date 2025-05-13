FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn

# Copy service files
COPY . .

# Expose the service port
EXPOSE 8004

# Start the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]