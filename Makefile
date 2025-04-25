.PHONY: install format lint test clean

install:
	poetry install
	pre-commit install

format:
	poetry run isort zmapsdk
	poetry run black zmapsdk

lint:
	poetry run isort zmapsdk --check-only --diff .
	poetry run black zmapsdk --check .
	poetry run pyupgrade zmapsdk --py311-plus $$(find . -name '*.py')

test:
	poetry run pytest tests/ -v

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
