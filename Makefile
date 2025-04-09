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
	#flake8 or pylint
test:
	#test code
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf .pytest_cache
	rm -f .coverage
	rm -rf build
	rm -rf dist
	rm -rf src/*.egg-info
all: install lint test clean
