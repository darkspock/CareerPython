# Simple development Dockerfile
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    curl \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf-xlib-2.0-dev \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY ./pyproject.toml /code/

# Create virtual environment and install dependencies
RUN uv venv
RUN uv pip install -r pyproject.toml

# Copy application code
COPY . /code/

# Activate the virtualenv by updating PATH
ENV PATH="/code/.venv/bin:$PATH"

# Set PYTHONPATH if needed for module imports
ENV PYTHONPATH="${PYTHONPATH}:/code"

# Run the application with hot reload for development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]