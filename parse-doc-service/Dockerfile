FROM python:3.9-slim

WORKDIR /app

# Cài đặt python-multipart trước
RUN pip install python-multipart

# Cài đặt các dependencies khác
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy service files
COPY . .

# Expose the service port
EXPOSE 8000

# Start the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]