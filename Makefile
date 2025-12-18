.PHONY: help install install-dev format lint test test-coverage clean run

# Default target
help:
	@echo "JAUs Startup Page - Development Commands"
	@echo "========================================"
	@echo "install     - Install production dependencies"
	@echo "install-dev - Install development dependencies"
	@echo "format      - Format code with black and isort"
	@echo "lint        - Run linting and type checking"
	@echo "test        - Run tests"
	@echo "test-coverage - Run tests with coverage"
	@echo "clean       - Clean up cache files"
	@echo "run         - Run the application"
	@echo "build       - Build executable with PyInstaller"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

# Code formatting and linting
format:
	@echo "Formatting code with black..."
	black src/ tools/
	@echo "Sorting imports with isort..."
	isort src/ tools/

lint:
	@echo "Running black check..."
	black --check src/ tools/
	@echo "Running isort check..."
	isort --check-only src/ tools/
	@echo "Running mypy type checking..."
	mypy src/

# Testing
test:
	@echo "Running tests..."
	python -m pytest tools/ -v

test-coverage:
	@echo "Running tests with coverage..."
	python -m pytest tools/ --cov=src --cov-report=html --cov-report=term

# Cleanup
clean:
	@echo "Cleaning up cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/

# Running the application
run:
	@echo "Starting JAUs Startup Dashboard Editor..."
	python src/main.py

# Building executable
build:
	@echo "Building executable with PyInstaller..."
	pyinstaller --onefile --windowed \
		--name "StartupDashboardEditor" \
		--icon="assets/icons/startup-dashboard-editor.png" \
		src/main.py

# Quick development setup
setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make run' to start the application."