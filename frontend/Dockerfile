FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Disable file validation for the debugger
ENV PYDEVD_DISABLE_FILE_VALIDATION=1

# Set the working directory
WORKDIR /app

# Install curl for healthcheck
RUN apt-get update \
    && apt-get install -y curl \
	&& rm -rf /var/lib/apt/lists/*
    
# Copy the project files
COPY uv.lock frontend/pyproject.toml ./

# Install the project dependencies
RUN uv sync

# Copy the rest of the project source code
COPY frontend/ ./

CMD ["uv", "run", "streamlit", "run", "main.py", "--server.address", "0.0.0.0", "--server.port", "80"]