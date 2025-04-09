install:
	pip install --upgrade pip
	pip install .
dev-setup:
	pip install --upgrade pip
	pip install -r requirements-dev.txt
	pip install -e .
format:
	black src tests
lint:
	pylint --disable=R,C,W src tests
test:
	python -m pytest -vv --cov=src
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf build
	rm -rf dist
	rm -rf src/*.egg-info
all: dev-setup format lint test clean
