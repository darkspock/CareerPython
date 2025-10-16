"""
Base Mother class for all test data builders
"""
import factory
from faker import Faker
from sqlalchemy.orm import Session
from core.database import SQLAlchemyDatabase

fake = Faker()


class BaseMother:
    """Base class for all Object Mothers"""

    def __init__(self, database: SQLAlchemyDatabase):
        self.database = database

    def create_in_db(self, **kwargs):
        """Create object in database and return it"""
        obj = self.build(**kwargs)
        with self.database.get_session() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def build(self, **kwargs):
        """Build object without saving to database"""
        raise NotImplementedError("Subclasses must implement build method")