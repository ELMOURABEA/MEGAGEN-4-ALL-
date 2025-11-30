# Contributing to MEGA-Bot

Thank you for your interest in contributing to MEGA-Bot! This document provides guidelines and instructions for contributing.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/MEGAGENT.git
   cd MEGAGENT
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/ELMOURABEA/MEGAGENT.git
   ```

## Development Setup

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Write or update tests as needed
4. Ensure all tests pass:
   ```bash
   pytest
   ```

## Testing

All contributions should include tests. We use pytest for testing.

Run tests:
```bash
pytest tests/ -v
```

Check test coverage:
```bash
pytest --cov=megabot tests/
```

## Submitting Changes

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```
2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
3. Open a Pull Request on GitHub

### Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed
- Follow the existing code style

## Style Guidelines

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

Example:
```python
def validate_query(query: str, max_length: int = 10000) -> tuple[bool, Optional[str]]:
    """
    Validate user query for safety and correctness
    
    Args:
        query: The query string to validate
        max_length: Maximum allowed length for queries
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Implementation here
```

### Documentation

- Update README.md for user-facing changes
- Update DOCUMENTATION.md for API changes
- Add entries to CHANGELOG.md
- Include code examples where helpful

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense (Add, Fix, Update, etc.)
- Keep the first line under 50 characters
- Provide details in the body if needed

Examples:
- `Add input validation for user queries`
- `Fix caching bug in research engine`
- `Update documentation for new features`

## Types of Contributions

### Bug Reports

- Use the issue tracker
- Provide detailed steps to reproduce
- Include error messages and stack traces
- Specify your environment (OS, Python version, etc.)

### Feature Requests

- Use the issue tracker
- Describe the feature and its benefits
- Provide use cases
- Consider implementation suggestions

### Code Contributions

- New features
- Bug fixes
- Performance improvements
- Documentation improvements
- Test coverage improvements

### AI Platform Integrations

To add a new AI platform integration:

1. Create a new file in `megabot/integrations/`
2. Extend the `BaseIntegration` class
3. Implement required methods: `query()`, `research()`, `get_latest_updates()`
4. Add tests in `tests/test_megabot.py`
5. Update documentation

## Questions?

If you have questions:
- Check existing documentation
- Search closed issues
- Open a new issue with your question

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to MEGA-Bot! 🚀
