
.poetry/bin/poetry:
	@curl -sSL https://install.python-poetry.org | POETRY_HOME=$(PWD)/.poetry python3 -

install: .poetry/bin/poetry .git/hooks/pre-commit ## Install the poetry environment and git hooks
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@.poetry/bin/poetry install
	@.poetry/bin/poetry shell

.git/hooks/pre-commit: git_hooks/pre-commit
	@echo "Copying pre-commit hooks from git_hooks/pre-commit"
	@cp git_hooks/pre-commit .git/pre-commit

format: .poetry/bin/poetry ## Format code using isort and black.
	@echo "🚀 Formatting code: Running isort and black"
	@.poetry/bin/poetry run isort .
	@.poetry/bin/poetry run black .

check: .poetry/bin/poetry ## Check code formatting using isort, black and flake8.
	@echo "🚀 Checking code formatting: Running isort"
	@.poetry/bin/poetry run isort --check-only --diff .
	@echo "🚀 Checking code formatting: Running black"
	@.poetry/bin/poetry run black --check .
	@echo "🚀 Checking code formatting: Running flake8"
	@.poetry/bin/poetry run flake8 .

test: .poetry/bin/poetry ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@.poetry/bin/poetry run pytest --doctest-modules

build: clean-build .poetry/bin/poetry ## Build wheel file using poetry
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

docs-test:  .poetry/bin/poetry## Test if documentation can be built without warnings or errors
	@.poetry/bin/poetry run @mkdocs build -s

docs:  .poetry/bin/poetry ## Build and serve the documentation
	@.poetry/bin/poetry run mkdocs serve

.PHONY: docs

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help