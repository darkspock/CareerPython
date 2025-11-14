from enum import Enum


class ReviewScoreEnum(int, Enum):
    """Review score for a candidate review"""
    ZERO = 0  # Ban - Prohibited
    THREE = 3  # Thumbs down - Not recommended
    SIX = 6  # Thumbs up - Recommended
    TEN = 10  # Favorite - Highly recommended
