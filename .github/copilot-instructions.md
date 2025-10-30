# Copilot Instructions for Agentic Data Pipeline

## Project Overview
This is an automated data analytics pipeline using agentic AI. The project focuses on building intelligent, autonomous data processing workflows that can adapt and make decisions based on data characteristics and business requirements.

## Coding Standards

### General Principles
- Write clean, maintainable, and well-documented code
- Follow the DRY (Don't Repeat Yourself) principle
- Prioritize readability and clarity over cleverness
- Use meaningful variable and function names that convey intent

### Documentation
- Add docstrings to all functions, classes, and modules
- Include type hints for function parameters and return values
- Document complex logic with inline comments
- Keep README files up-to-date with setup and usage instructions

## Architecture and Design Patterns

### Data Pipeline Design
- Use modular components for each stage of the pipeline (ingestion, processing, analysis, output)
- Implement clear interfaces between pipeline components
- Design for scalability and fault tolerance
- Include proper error handling and logging at each stage

### Agentic AI Integration
- Design agents with clear responsibilities and capabilities
- Implement decision-making logic that is explainable and auditable
- Use structured prompts and responses for AI interactions
- Include fallback mechanisms for AI failures

### Testing Strategy
- Write unit tests for individual components
- Include integration tests for pipeline workflows
- Test edge cases and error conditions
- Mock external dependencies and AI services in tests

## Dependencies and Tools

### Preferred Stack
- Python for data processing and AI integration
- Use virtual environments (venv or conda) for dependency management
- Prefer well-maintained, popular libraries for data processing (pandas, numpy, polars)
- Use standard logging libraries for observability

### AI and ML Tools
- Use established AI frameworks and APIs
- Implement proper API key management and security
- Include rate limiting and retry logic for API calls
- Cache AI responses when appropriate

## Security and Best Practices

### Data Security
- Never commit sensitive data, API keys, or credentials
- Use environment variables for configuration
- Implement proper data validation and sanitization
- Follow data privacy and compliance requirements

### Code Quality
- Run linters and formatters before committing (black, flake8, pylint)
- Keep dependencies up-to-date
- Review and address security vulnerabilities
- Use .gitignore to exclude build artifacts and sensitive files

## Error Handling and Logging

- Use structured logging with appropriate log levels
- Include context in error messages for debugging
- Implement graceful degradation for non-critical failures
- Log pipeline execution metrics for monitoring

## Performance Considerations

- Profile code to identify bottlenecks
- Use efficient data structures and algorithms
- Implement batch processing where appropriate
- Consider memory usage for large datasets
- Use async/await for I/O-bound operations

## Contributing Guidelines

- Create feature branches from main
- Write clear commit messages
- Include tests with new features
- Update documentation for significant changes
- Request code reviews before merging
