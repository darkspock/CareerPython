"""Interview Score Calculator Service"""
from typing import List, Optional

from src.interview_bc.interview_template.domain.enums import ScoringModeEnum


class InterviewScoreCalculator:
    """Service for calculating interview scores based on scoring mode"""

    @staticmethod
    def calculate_score(
        answer_scores: List[float],
        scoring_mode: Optional[ScoringModeEnum] = None
    ) -> Optional[float]:
        """
        Calculate interview score based on scoring mode and answer scores.

        Args:
            answer_scores: List of individual answer scores
            scoring_mode: Scoring mode (DISTANCE or ABSOLUTE)

        Returns:
            Calculated interview score (0-100) or None if no scores
        """
        if not answer_scores:
            return None

        if scoring_mode == ScoringModeEnum.DISTANCE:
            return InterviewScoreCalculator._calculate_distance_score(answer_scores)
        elif scoring_mode == ScoringModeEnum.ABSOLUTE:
            return InterviewScoreCalculator._calculate_absolute_score(answer_scores)
        else:
            # Legacy mode: simple average, scale to 0-100
            return InterviewScoreCalculator._calculate_legacy_score(answer_scores)

    @staticmethod
    def _calculate_absolute_score(answer_scores: List[float]) -> float:
        """
        Calculate score using ABSOLUTE mode.
        In ABSOLUTE mode, higher scores are better.
        Average the scores and scale to 0-100 (assuming scores are 1-10).
        """
        if not answer_scores:
            return 0.0

        # Average of scores (1-10 range)
        average = sum(answer_scores) / len(answer_scores)

        # Scale from 1-10 to 0-100
        # Formula: ((score - 1) / 9) * 100
        # This maps 1 -> 0, 10 -> 100
        scaled_score = ((average - 1) / 9) * 100

        # Ensure result is within 0-100 range
        return max(0.0, min(100.0, scaled_score))

    @staticmethod
    def _calculate_distance_score(answer_scores: List[float]) -> float:
        """
        Calculate score using DISTANCE mode.
        In DISTANCE mode, scores closer to requirements (ideal = 10) are better.
        Calculate average distance from ideal (10) and convert to score.
        """
        if not answer_scores:
            return 0.0

        # Calculate average distance from ideal (10)
        # Distance = |10 - score|, so smaller distance is better
        distances = [abs(10 - score) for score in answer_scores]
        average_distance = sum(distances) / len(distances)

        # Convert distance to score: score = 10 - distance
        # This gives maximum score (10) when distance is 0, and lower scores as distance increases
        # Then scale to 0-100
        ideal_score = 10 - average_distance
        scaled_score = ((ideal_score - 1) / 9) * 100

        # Ensure result is within 0-100 range
        return max(0.0, min(100.0, scaled_score))

    @staticmethod
    def _calculate_legacy_score(answer_scores: List[float]) -> float:
        """
        Calculate score using legacy mode (no scoring_mode).
        Scores are already in 0-100 range, so just average them.
        """
        if not answer_scores:
            return 0.0

        return sum(answer_scores) / len(answer_scores)

