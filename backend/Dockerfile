FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Set the working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project configuration
COPY pyproject.toml ./

# Install dependencies using UV with increased timeout and retries
ENV UV_HTTP_TIMEOUT=300
ENV UV_INSTALL_RETRIES=5
RUN uv pip install --system -r pyproject.toml

# Copy the rest of the project source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]