# Contributing to CareerPython

Thank you for your interest in contributing to CareerPython! This document provides guidelines and instructions for contributing to this project.

## 🚀 Getting Started

Before you begin:
- Read our [Code of Conduct](CODE_OF_CONDUCT.md)
- Check the [Development Guide](DEVELOPMENT.md) for setup instructions
- Look at existing [Issues](https://github.com/darkspock/CareerPython/issues) and [Pull Requests](https://github.com/darkspock/CareerPython/pulls)

## 🛠️ Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/darkspock/CareerPython.git
   cd CareerPython
   ```
3. **Follow the setup instructions** in the [Development Guide](DEVELOPMENT.md)

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include steps to reproduce, expected behavior, and actual behavior
- Add screenshots or error logs when helpful
- Check if the issue already exists before creating a new one

### ✨ Feature Requests
- Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Explain the problem you're solving and why it's valuable
- Describe your proposed solution
- Consider discussing in an issue before implementing large features

### 📝 Documentation
- Fix typos or improve clarity
- Add missing documentation for features
- Update outdated information
- Translate documentation to other languages

### 🧪 Testing
- Add tests for uncovered code
- Improve existing test coverage
- Add integration or E2E tests
- Fix flaky or failing tests

## 📋 Pull Request Process

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Your Changes
- Follow the [code standards](#code-standards)
- Write tests for new functionality
- Update documentation if needed
- Ensure all tests pass

### 3. Commit Your Changes
Use [Conventional Commits](https://conventionalcommits.org/):

```bash
git commit -m "feat: add candidate search functionality"
git commit -m "fix: resolve authentication token expiration"
git commit -m "docs: update API documentation"
git commit -m "test: add unit tests for user service"
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding tests
- `refactor`: Code refactoring
- `style`: Code style changes
- `ci`: CI/CD changes
- `chore`: Maintenance tasks

### 4. Push and Create PR
```bash
git push origin your-branch-name
```

Then create a Pull Request on GitHub with:
- Clear title describing the change
- Detailed description of what was changed and why
- Link to related issues
- Screenshots or GIFs for UI changes

## 🏗️ Code Standards

### Python Code Style
- Follow [PEP 8](https://pep8.org/)
- Use type hints for all functions and methods
- Write docstrings for public classes and methods
- Use descriptive variable and function names
- Maximum line length: 120 characters

### Architecture Guidelines
- Follow Clean Architecture principles
- Maintain separation between layers
- Use CQRS pattern (Commands for writes, Queries for reads)
- Implement proper error handling
- Use dependency injection

### Testing Requirements
- Write unit tests for business logic
- Add integration tests for external dependencies
- Maintain minimum 80% code coverage
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

Example test structure:
```python
def test_create_candidate_success():
    """Test successful candidate creation with valid data"""
    # Arrange
    command = CreateCandidateCommand(...)

    # Act
    result = handler.execute(command)

    # Assert
    assert result.success is True
    assert result.candidate_id is not None
```

### Database Changes
- Always create migrations for schema changes
- Test migrations both forward and backward
- Use descriptive migration names
- Don't modify existing migrations
- Consider performance impact of changes

## 🔍 Code Review Process

### What Reviewers Look For
- Code follows architectural patterns
- Tests are comprehensive and meaningful
- Changes are well-documented
- No security vulnerabilities
- Performance considerations
- Backward compatibility

### Responding to Feedback
- Address all reviewer comments
- Ask questions if feedback is unclear
- Update your branch with requested changes
- Re-request review after making changes

## 🚦 Continuous Integration

All PRs must pass:
- ✅ **Unit Tests** - All tests must pass
- ✅ **Code Coverage** - Minimum 80% coverage
- ✅ **Linting** - Code must pass flake8, mypy
- ✅ **Security Scan** - No security vulnerabilities
- ✅ **Docker Build** - Application must build successfully

## 📦 Release Process

1. **Version Bumping**: Update version in `pyproject.toml`
2. **Changelog**: Update `CHANGELOG.md` with new features and fixes
3. **Testing**: Ensure all tests pass on main branch
4. **Tagging**: Create git tag with version number
5. **Release Notes**: Create GitHub release with notes

## 🎖️ Recognition

Contributors are recognized in:
- Project README.md
- Release notes
- GitHub contributors list
- Special recognition for significant contributions

## 📞 Getting Help

If you need help:
- 💬 **Discussions**: Use GitHub Discussions for questions
- 🐛 **Issues**: Create an issue for bugs or feature requests
- 📧 **Email**: Contact [extjmv@gmail.com](mailto:extjmv@gmail.com)
- 💼 **LinkedIn**: [Juan Macías](https://linkedin.com/in/juanmaciasvela)

## 📄 Additional Resources

- [Development Guide](DEVELOPMENT.md) - Complete setup and development guide
- [Architecture Documentation](CLAUDE.md) - Project architecture details
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## 🙏 Thank You

Thank you for contributing to CareerPython! Your contributions help make this project better for everyone.

---

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](LICENSE).