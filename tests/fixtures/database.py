"""
Database fixtures for integration tests
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.database import SQLAlchemyDatabase
from core.base import Base


@pytest.fixture(scope="function")
def test_database():
    """Create a test database instance with transaction rollback"""
    # Use in-memory SQLite for fast tests
    test_db_url = "sqlite:///:memory:"
    engine = create_engine(test_db_url, echo=False)

    # Create all tables
    Base.metadata.create_all(engine)

    # Create database instance
    database = SQLAlchemyDatabase()
    database.engine = engine
    database.session_factory = sessionmaker(bind=engine)

    yield database

    # Cleanup
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(test_database):
    """Provide a database session for tests"""
    with test_database.get_session() as session:
        yield session