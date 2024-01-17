# -- Base image --
FROM python:3.12-slim as base

MAINTAINER Julien Maupetit <julien@maupetit.net>

# Upgrade pip to its latest release to speed up dependencies installation
RUN pip install --upgrade pip

# Upgrade system packages to install security updates
RUN apt update && \
    apt -y upgrade && \
    apt install -y libpango-1.0-0 libpangoft2-1.0-0 && \
    rm -rf /var/lib/apt/lists/*

# -- Builder --
FROM base as builder

WORKDIR /build

COPY . /build/

ENV PATH  $PATH:/root/.local/bin

# Install poetry
RUN pip install pipx && \
    pipx install poetry
# Build and install md2pdf
RUN poetry build && \
    pip install dist/*.whl

# -- Core --
FROM base as core

COPY --from=builder /usr/local /usr/local

# -- App --
FROM core as production

VOLUME ["/app"]

WORKDIR /app

USER "1000:1000"

ENV HOME="/tmp"

ENTRYPOINT ["md2pdf"]
