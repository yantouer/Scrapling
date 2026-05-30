FROM python:3.12-slim-bookworm

LABEL io.modelcontextprotocol.server.name="io.github.D4Vinci/Scrapling"

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy source code
COPY . .

# Install project and dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        build-essential && \
    pip install --no-cache-dir -e .[all] && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Expose port for MCP server HTTP transport
EXPOSE 8000

# Keep container running
CMD ["sh", "-c", "while true; do sleep 1; done"]
