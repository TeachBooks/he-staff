FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install flask gunicorn

# Copy application code
COPY app.py .

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]


