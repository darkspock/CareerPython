# Testing Documentation

## 🧪 Test Structure

```
tests/
├── integration/                    # Integration tests
│   ├── conftest.py                # Pytest configuration for integration tests
│   ├── test_interview_templates.py # Interview templates API tests
│   └── mothers/                   # Object Mothers (test data builders)
│       ├── base_mother.py
│       ├── interview_template_mother.py
│       └── user_mother.py
├── fixtures/                      # Shared test fixtures
│   ├── database.py               # Database fixtures
│   └── auth.py                   # Authentication fixtures
└── README.md                     # This file
```

## 🚀 Running Tests

### With Docker (Recommended)
```bash
# Run all tests
make test

# Run only integration tests
make test-integration

# Run interview template tests specifically
make test-interview-templates

# Run quick integration tests (skip database-dependent ones)
make test-integration-quick

# Run with coverage
make test-coverage
```

### Local Development
```bash
# Install dependencies first
uv sync

# Run tests with pytest
pytest tests/integration/test_interview_templates.py -v

# Run tests with specific markers
pytest tests/integration/ -m "not skip" -v
```

## 🏗️ Writing Tests

### Object Mothers Pattern

Object Mothers create test data in a readable and maintainable way:

```python
# Create test data in database
template = InterviewTemplateMother.create_enabled(
    database,
    name="Python Developer Template",
    job_category=JobCategoryEnum.PYTHON_DEVELOPER
)

# Create different variations
draft_template = InterviewTemplateMother.create_draft(database)
disabled_template = InterviewTemplateMother.create_disabled(database)
```

### Authentication Testing

Use the `TestAuthMixin` for authenticated API calls:

```python
class TestMyEndpoints(TestAuthMixin):
    def test_admin_endpoint(self):
        # Create authenticated admin client
        admin_client = self.as_admin("admin@test.com")

        # Make authenticated request
        response = admin_client.get("/admin/endpoint")

        # Assert response
        assert response.status_code == 200

        # Clean up
        admin_client.close()
```

### Integration Test Pattern

Follow the AAA (Arrange-Act-Assert) pattern:

```python
def test_list_templates_with_filters(self, test_database):
    # Arrange
    template1 = InterviewTemplateMother.create_enabled(test_database)
    template2 = InterviewTemplateMother.create_draft(test_database)
    admin_client = self.as_admin()

    # Act
    response = admin_client.get("/admin/interview-templates?status=ENABLED")

    # Assert
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) == 1
    assert templates[0]["status"] == "ENABLED"

    admin_client.close()
```

## 🎯 Test Categories

### Integration Tests
- Test complete HTTP request/response cycles
- Test authentication and authorization
- Test database interactions
- Test API contract compliance

### Test Markers
- `@pytest.mark.skip("reason")` - Skip test (for database-dependent tests during development)
- `@pytest.mark.asyncio` - Async test
- `@pytest.mark.slow` - Slow tests (can be excluded with `-m "not slow"`)

## 🔧 Configuration

### Database Testing
- Uses in-memory SQLite for fast tests
- Each test gets fresh database instance
- Database schema is created/dropped per test function

### Authentication Testing
- Mock authentication for unit tests
- Real authentication flow for integration tests
- Test different user roles (admin, regular user)

## 📝 Best Practices

1. **Use Object Mothers** for test data creation
2. **Clean up resources** - close HTTP clients, database connections
3. **Test the happy path first**, then edge cases
4. **Use descriptive test names** that explain the scenario
5. **Arrange-Act-Assert** pattern for clarity
6. **Mark slow/database tests** appropriately
7. **Test authentication and authorization** separately from business logic

## 🐛 Debugging Tests

```bash
# Run specific test with verbose output
pytest tests/integration/test_interview_templates.py::TestInterviewTemplatesIntegration::test_specific_method -v -s

# Run with pdb debugger
pytest tests/integration/test_interview_templates.py --pdb

# Show test coverage
pytest --cov=src --cov-report=term-missing
```