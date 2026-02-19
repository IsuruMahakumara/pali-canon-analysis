# Use official Apache AGE image
FROM apache/age:latest

# 1. Identify the PG version and install the correct dev headers
# We use a trick to pull the version from pg_config automatically
RUN apt-get update && \
    PG_VERSION=$(pg_config --version | grep -oP 'PostgreSQL \K[0-9]+') && \
    apt-get install -y \
    build-essential \
    git \
    "postgresql-server-dev-$PG_VERSION" \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Install PGVector
# -----------------------------
RUN git clone --branch v0.8.1 https://github.com/pgvector/pgvector.git /tmp/pgvector \
    && cd /tmp/pgvector \
    && make \
    && make install \
    && rm -rf /tmp/pgvector

# -----------------------------
# Initialize extensions
# -----------------------------
# Note: Ensure your init-extensions.sql contains:
# CREATE EXTENSION IF NOT EXISTS age;
# CREATE EXTENSION IF NOT EXISTS vector;
COPY init-extensions.sql /docker-entrypoint-initdb.d/