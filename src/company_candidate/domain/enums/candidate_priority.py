from enum import Enum


class CandidatePriority(str, Enum):
    """Priority level assigned to a candidate by the company"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
