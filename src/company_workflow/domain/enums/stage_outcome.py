from enum import Enum


class StageOutcome(str, Enum):
    """Outcome when moving from a stage"""
    PASSED = "passed"  # Candidate passed this stage
    FAILED = "failed"  # Candidate failed this stage
    PENDING = "pending"  # Outcome not yet determined
    SKIPPED = "skipped"  # Stage was skipped
