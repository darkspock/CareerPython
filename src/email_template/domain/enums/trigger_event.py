"""
Trigger Event Enum
Phase 7: Email template trigger events
"""

from enum import Enum


class TriggerEvent(str, Enum):
    """Events that can trigger email sending"""

    # Application lifecycle events
    APPLICATION_CREATED = "application_created"  # When candidate applies
    APPLICATION_UPDATED = "application_updated"  # When application is updated

    # Stage transition events
    STAGE_ENTERED = "stage_entered"  # When application enters a stage
    STAGE_COMPLETED = "stage_completed"  # When stage is marked complete
    STAGE_CHANGED = "stage_changed"  # When moving between stages

    # Status change events
    STATUS_ACCEPTED = "status_accepted"  # When application accepted
    STATUS_REJECTED = "status_rejected"  # When application rejected
    STATUS_WITHDRAWN = "status_withdrawn"  # When application withdrawn

    # Deadline events
    DEADLINE_APPROACHING = "deadline_approaching"  # X days before deadline
    DEADLINE_PASSED = "deadline_passed"  # When deadline passes

    # Manual trigger
    MANUAL = "manual"  # Manually triggered by user
