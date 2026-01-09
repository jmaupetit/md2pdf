# -- General
SHELL := /bin/bash

UV     = uv
UV_RUN = $(UV) run

# ==============================================================================
# RULES

default: help

bootstrap: ## boostrap the project to start hacking
bootstrap: \
  build
.PHONY: bootstrap

build: ## install project with its dependencies
	$(UV) sync --locked --all-extras --dev
.PHONY: build


build-docker: ## build Docker images
build-docker: \
  build-docker-debian \
  build-docker-alpine
.PHONY: build-docker

build-docker-debian: ## build Docker (debian) image
	docker build . --target production --tag jmaupetit/md2pdf:latest
.PHONY: build-docker-debian

build-docker-alpine: ## build Docker (alpine) image
	docker build . -f Dockerfile.alpine --target production --tag jmaupetit/md2pdf:alpine
.PHONY: build-docker-alpine

lint: ## lint all sources
lint: \
	lint-black \
	lint-ruff
.PHONY: lint

lint-black: ## lint python sources with black
	@echo 'lint:black started…'
	uv run black src/md2pdf tests
.PHONY: lint-black

lint-black-check: ## check python sources with black
	@echo 'lint:black check started…'
	uv run black --check src/md2pdf tests
.PHONY: lint-black-check

lint-ruff: ## lint python sources with ruff
	@echo 'lint:ruff started…'
	uv run ruff check src/md2pdf tests
.PHONY: lint-ruff

lint-ruff-fix: ## lint and fix python sources with ruff
	@echo 'lint:ruff-fix started…'
	uv run ruff check --fix src/md2pdf tests
.PHONY: lint-ruff-fix

test: ## run the test suite
	$(UV_RUN) pytest
.PHONY: test

# -- Misc
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
