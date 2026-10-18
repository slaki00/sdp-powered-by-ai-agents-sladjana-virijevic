FROM python:3.12-slim

# Create a non-root user (rarely changes, so it stays cached)
RUN useradd --create-home appuser

WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY tests/ tests/

# Make the bankocr package importable from src/
ENV PYTHONPATH=/app/src

# Run as the non-root user
USER appuser

# Run tests by default
CMD ["pytest", "-p", "no:cacheprovider", "tests/", "-v", "--tb=short"]
