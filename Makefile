
.poetry/bin/poetry:
	@curl -sSL https://install.python-poetry.org | POETRY_HOME=$(PWD)/.poetry python3 -

install: .poetry/bin/poetry ## Install the poetry environment
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@.poetry/bin/poetry install	
	@.poetry/bin/poetry shell

format: ## Format code using isort and black.
	@echo "🚀 Formatting code: Running isort and black"
	@isort .
	@black .

check: ## Check code formatting using isort, black and flake8.
	@echo "🚀 Checking code formatting: Running isort"
	@isort --check-only --diff .
	@echo "🚀 Checking code formatting: Running black"
	@black --check .
	@echo "🚀 Checking code formatting: Running flake8"
	@flake8 .

test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@.poetry/bin/poetry run pytest --doctest-modules

build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@.poetry/bin/poetry build

clean-build: ## clean build artifacts
	@rm -rf dist

publish: ## publish a release to pypi.
	@echo "🚀 Publishing: Dry run."
	@.poetry/bin/poetry config pypi-token.pypi $(PYPI_TOKEN)
	@.poetry/bin/poetry publish --dry-run
	@echo "🚀 Publishing."
	@.poetry/bin/poetry publish

build-and-publish: build publish ## Build and publish.

docs-test: ## Test if documentation can be built without warnings or errors
	@mkdocs build -s

docs: ## Build and serve the documentation
	@mkdocs serve

.PHONY: docs

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help