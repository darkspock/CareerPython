"""
Pytest configuration and fixtures for integration tests
"""
import pytest
import asyncio
from typing import Generator

# Import fixtures to make them available
from tests.fixtures.database import test_database, db_session
from tests.fixtures.auth import authenticated_client


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test"""
    # Add any global test setup here
    yield
    # Add any global test cleanup here