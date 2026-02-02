# -- General
SHELL := /bin/bash

# Docs 
DOCS_SNIPPETS_PATH = ./docs/snippets
DOCS_SNIPPETS_MD   = $(wildcard $(DOCS_SNIPPETS_PATH)/*.md)
DOCS_SNIPPETS_PDF  = $(patsubst %.md,%.pdf,$(DOCS_SNIPPETS_MD))

# Assets
MD2PDF_CSS = ./examples/md2pdf.css

# Tools
UV     = uv
UV_RUN = $(UV) run

# ==============================================================================
# RULES

default: help

$(DOCS_SNIPPETS_PATH)/%.pdf: $(DOCS_SNIPPETS_PATH)/%.md
	@echo -e "---\n📼 $< → $@"
	uv run md2pdf -i $< -o $@ -c $(MD2PDF_CSS)

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

docs: ## build documentation
docs: docs-snippets
	uv run zensical build -c
.PHONY: docs

docs-snippets: ## build documentation snippets
docs-snippets: \
  $(DOCS_SNIPPETS_PDF) \
  $(MD2PDF_CSS)
	@echo "✅ Documentation snippets rendered"
.PHONY: docs-snippets

docs-snippets-watch: ## work on docs snippets and styles (watch mode)
	echo $(DOCS_SNIPPETS_MD) | \
		xargs printf -- '-i %s ' | \
		xargs uv run md2pdf -c $(MD2PDF_CSS) -w
.PHONY: docs-snippets-watch

docs-serve: ## run documentation server
	uv run zensical serve
.PHONY: docs-serve

lint: ## lint all sources
lint: \
	lint-black \
	lint-ruff \
  lint-mypy
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

lint-mypy: ## lint python sources with mypy
	@echo 'lint:mypy started…'
	uv run mypy src/md2pdf tests
.PHONY: lint-mypy

test: ## run the test suite
	$(UV_RUN) pytest
.PHONY: test

# -- Misc
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
