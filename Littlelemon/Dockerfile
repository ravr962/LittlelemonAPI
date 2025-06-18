# Use Python slim image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd gcc postgresql-client && apt-get clean

# Copy requirements.txt from parent (repo root)
COPY ../requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files into container
COPY ../ .

# Run app (used for production, override in docker-compose for local dev)
CMD ["gunicorn", "Littlelemon.wsgi:application", "--bind", "0.0.0.0:8000"]
