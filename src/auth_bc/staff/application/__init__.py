"""Staff application module - exports queries"""

# Queries
from .queries.user_is_staff_query import UserIsStaffQuery, UserIsStaffQueryHandler

__all__ = [
    "UserIsStaffQuery",
    "UserIsStaffQueryHandler",
]
