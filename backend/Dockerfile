FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including curl for healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY ./backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (needed for imports to work)
COPY . .

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Expose the application port
EXPOSE 8000

# Run the startup script
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
