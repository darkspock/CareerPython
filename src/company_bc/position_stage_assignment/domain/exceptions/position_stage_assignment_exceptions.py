"""Position stage assignment domain exceptions"""


class PositionStageAssignmentException(Exception):
    """Base exception for position stage assignment domain"""
    pass


class PositionStageAssignmentNotFoundException(PositionStageAssignmentException):
    """Raised when a position stage assignment is not found"""
    pass


class PositionStageAssignmentValidationError(PositionStageAssignmentException):
    """Raised when position stage assignment validation fails"""
    pass


class DuplicatePositionStageAssignmentException(PositionStageAssignmentException):
    """Raised when trying to create a duplicate position-stage assignment"""
    pass
