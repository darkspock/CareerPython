import uuid


def generate_id() -> str:
    """Genera un ID único como string"""
    return str(uuid.uuid4())
