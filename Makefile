.PHONY: install format lint test clean

install:
	poetry install
	pre-commit install

format:
	poetry run isort zmapsdk
	poetry run black zmapsdk

lint:
	poetry run isort --check-only --diff .
	poetry run black --check .
	poetry run pyupgrade --py311-plus $$(find . -name '*.py' -not -path './.venv/*')

test:
	poetry run pytest tests/ -v

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
