# Contributing to Agentic Data Pipeline

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Run tests and ensure they pass
6. Submit a pull request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/agentic-data-pipeline.git
cd agentic-data-pipeline

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests to verify setup
pytest
```

## Code Style

This project follows PEP 8 style guidelines with some modifications:

- Maximum line length: 127 characters
- Use Black for code formatting
- Use isort for import sorting
- Use flake8 for linting

Before committing, run:

```bash
# Format code
black agents/ orchestrator/ ui/ main.py

# Sort imports
isort agents/ orchestrator/ ui/ main.py

# Lint
flake8 agents/ orchestrator/ ui/
```

## Testing

All new features should include tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=orchestrator

# Run specific test file
pytest tests/agents/test_inspector.py -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names
- Use fixtures from `conftest.py`

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Add tests for any new functionality
3. Ensure all tests pass
4. Update documentation as needed
5. Follow the pull request template
6. Request review from maintainers

## Pull Request Guidelines

- **Title**: Use a clear, descriptive title
- **Description**: Explain what changes you made and why
- **Testing**: Describe how you tested your changes
- **Screenshots**: Include screenshots for UI changes

## Commit Messages

Use clear, descriptive commit messages:

```
feat: Add new feature X
fix: Resolve bug in Y
docs: Update README with Z
test: Add tests for W
refactor: Improve code structure in V
```

## Bug Reports

When reporting bugs, please include:

1. Description of the bug
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details (Python version, OS, etc.)
6. Error messages or logs

## Feature Requests

When requesting features:

1. Describe the feature clearly
2. Explain the use case
3. Provide examples if possible
4. Discuss potential implementation approaches

## Code Review

All submissions require review. We use GitHub pull requests for this purpose:

- Be respectful and constructive
- Focus on the code, not the person
- Ask questions if something is unclear
- Suggest improvements where appropriate

## Questions?

If you have questions, feel free to:

- Open an issue with the "question" label
- Start a discussion in GitHub Discussions
- Contact the maintainers

Thank you for contributing! 🎉
