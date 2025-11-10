"""Enums for async job management."""

from enum import Enum


class AsyncJobStatus(Enum):
    """Status of an async job."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class AsyncJobType(Enum):
    """Type of async job."""
    PDF_ANALYSIS = "pdf_analysis"
    EMAIL_PROCESSING = "email_processing"
    DATA_MIGRATION = "data_migration"
    REPORT_GENERATION = "report_generation"
