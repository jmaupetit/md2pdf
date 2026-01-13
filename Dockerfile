# Install uv
FROM python:3.12-slim AS base

LABEL org.opencontainers.image.authors="Julien Maupetit <julien@maupetit.net>"

# Upgrade system packages to install security updates and weasyprint dependencies
RUN apt update && \
    apt -y upgrade && \
    apt install -y \
      libpango-1.0-0 \
      libpangoft2-1.0-0 \
      libharfbuzz-subset0 \
      && \
    rm -rf /var/lib/apt/lists/*

# Change the working directory to the `app` directory
WORKDIR /app

# 
# -- BUILDER --
# 
FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --extra cli --extra latex --locked --no-install-project --no-editable

# Copy the project into the intermediate image
COPY . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

#
# -- PRODUCTION --
#
FROM base AS production

# Copy the environment, but not the source code
COPY --from=builder --chown=app:app /app/.venv /app/.venv

ENTRYPOINT ["/app/.venv/bin/md2pdf"]
