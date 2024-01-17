# -- General
SHELL := /bin/bash

POETRY     = poetry
POETRY_RUN = $(POETRY) run

# ==============================================================================
# RULES

default: help

bootstrap: ## boostrap the project to start hacking
bootstrap: install
.PHONY: bootstrap

build: ## build python package
	$(POETRY) build
.PHONY: build

install: ## install project with its dependencies
	$(POETRY_RUN) install
.PHONY: install

lint: ## lint python sources
	$(POETRY_RUN) ruff md2pdf
.PHONY: lint

lint-fix: ## fix lint errors
	$(POETRY_RUN) ruff --fix md2pdf
.PHONY: lint-fix

publish: ## publish a new package release
publish: build
	$(POETRY) publish
.PHONY: publish

test: ## run the test suite
	$(POETRY_RUN) pytest
.PHONY: test

# -- Misc
help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
