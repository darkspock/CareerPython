import bcrypt


class PasswordService:
    """Domain service for password operations"""

    @classmethod
    def hash_password(cls, plain_password: str) -> str:
        """Hash a plain password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a bcrypt hashed password"""
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False

    @classmethod
    def generate_random_password(cls, length: int = 12) -> str:
        """Generate a random password"""
        # Import here to avoid circular imports
        from src.user.domain.entities.user import User
        return User.generate_random_password(length)
