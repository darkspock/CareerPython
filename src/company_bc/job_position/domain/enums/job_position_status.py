import enum


class JobPositionStatusEnum(str, enum.Enum):
    """
    Status enum for job positions - Publishing Flow State Machine.

    Flow:
    DRAFT → PENDING_APPROVAL → APPROVED → PUBLISHED → CLOSED → ARCHIVED
                ↓                                         ↓
            REJECTED                                   ON_HOLD

    Transitions:
    - DRAFT: Initial state, can edit freely
    - PENDING_APPROVAL: Waiting for budget/finance approval
    - APPROVED: Budget approved, ready to publish
    - REJECTED: Approval denied, returns to draft for revisions
    - PUBLISHED: Live and visible to candidates
    - ON_HOLD: Temporarily paused (hiring freeze)
    - CLOSED: No longer hiring (with reason: filled, cancelled, on_hold)
    - ARCHIVED: Historical record (terminal state)
    """
    DRAFT = "draft"                         # Being created/edited
    PENDING_APPROVAL = "pending_approval"   # Waiting for budget/finance approval
    APPROVED = "approved"                   # Budget approved, ready to publish
    REJECTED = "rejected"                   # Approval denied, needs revision
    PUBLISHED = "published"                 # Live and visible to candidates
    ON_HOLD = "on_hold"                     # Temporarily paused (hiring freeze)
    CLOSED = "closed"                       # No longer hiring
    ARCHIVED = "archived"                   # Historical record

    # Legacy values for backwards compatibility
    ACTIVE = "active"                       # @deprecated: Use PUBLISHED
    PAUSED = "paused"                       # @deprecated: Use ON_HOLD
    CONTENT_REVIEW = "content_review"       # @deprecated: Use APPROVED
