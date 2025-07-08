FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for python3-saml with specific versions
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies with specific versions to avoid conflicts
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    lxml==4.9.3 \
    xmlsec==1.3.13 \
    python3-saml==1.15.0 \
    Flask==2.3.3 \
    gunicorn==21.2.0

# Copy application code
COPY app.py .

# Expose port
EXPOSE 8000

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "app:app"]