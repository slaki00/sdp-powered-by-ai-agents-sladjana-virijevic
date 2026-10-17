FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY tests/ tests/

# Make the bankocr package importable from src/
ENV PYTHONPATH=/app/src

# Run tests by default
CMD ["pytest", "tests/", "-v", "--tb=short"]
