# Use Python 3.11 slim with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Don't write .pyc files, unbuffer stdout/stderr, no pip cache
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install system deps for build tools, libpq (psycopg) and libmagic
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      libmagic1 \
 && rm -rf /var/lib/apt/lists/*

# Copy only the project metadata (no wildcard)
COPY pyproject.toml uv.lock ./

# Install dependencies only (not the project itself)
RUN uv venv .venv \
 && uv sync --no-install-project

# Copy application code
COPY . .

# Now install the project
RUN uv sync

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Run via UV
CMD ["uv", "run", "uvicorn", "opendms.main:app", "--host", "0.0.0.0", "--port", "8000"] 