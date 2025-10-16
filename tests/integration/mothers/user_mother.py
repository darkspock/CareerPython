"""
User Object Mother for authentication tests
"""
from faker import Faker
from tests.integration.mothers.base_mother import BaseMother

fake = Faker()


class UserMother(BaseMother):
    """Object Mother for User test data"""

    def build(self, **kwargs):
        """Build User model with fake data"""
        # This is a placeholder - adjust based on your User model
        defaults = {
            'email': kwargs.get('email', fake.email()),
            'password': kwargs.get('password', 'test_password'),
            'is_admin': kwargs.get('is_admin', True),
            'is_active': kwargs.get('is_active', True)
        }

        # TODO: Replace with actual User model when available
        # return UserModel(**defaults)
        return defaults

    @classmethod
    def create_admin(cls, database, email: str = None, **kwargs):
        """Create an admin user"""
        mother = cls(database)
        return mother.create_in_db(
            email=email or fake.email(),
            is_admin=True,
            **kwargs
        )

    @classmethod
    def create_regular_user(cls, database, email: str = None, **kwargs):
        """Create a regular user"""
        mother = cls(database)
        return mother.create_in_db(
            email=email or fake.email(),
            is_admin=False,
            **kwargs
        )