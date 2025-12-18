# AsyncIO Background Worker Dockerfile
# Multi-stage build for optimized production image

# ============================================
# Stage 1: Base image with dependencies
# ============================================
FROM python:3.12-slim as base

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# Stage 2: Development image
# ============================================
FROM base as development

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run worker
CMD ["python", "-m", "src.main"]

# ============================================
# Stage 3: Production image
# ============================================
FROM base as production

# Create non-root user for security
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Run worker
CMD ["python", "-m", "src.main"]
