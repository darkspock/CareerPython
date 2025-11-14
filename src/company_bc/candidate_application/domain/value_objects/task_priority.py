"""
Task Priority Value Object
Phase 6: Calculates priority score for application tasks based on multiple factors
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class TaskPriority:
    """Value object representing the priority of a task

    Priority is calculated based on:
    - Base priority (default)
    - Deadline weight (closer deadlines = higher priority)
    - Time in stage weight (longer in stage = higher priority)
    - Position importance (optional future enhancement)
    - Candidate importance (optional future enhancement)
    """

    base_priority: int = 50  # Base score 0-100
    deadline_weight: int = 0  # 0-50 based on deadline proximity
    time_in_stage_weight: int = 0  # 0-30 based on time in current stage
    position_weight: int = 0  # 0-10 based on position importance (future)
    candidate_weight: int = 0  # 0-10 based on candidate score (future)

    @property
    def total_score(self) -> int:
        """Calculate total priority score (0-150)"""
        return (
                self.base_priority +
                self.deadline_weight +
                self.time_in_stage_weight +
                self.position_weight +
                self.candidate_weight
        )

    @property
    def priority_level(self) -> str:
        """Get priority level based on score"""
        score = self.total_score
        if score >= 120:
            return "critical"
        elif score >= 90:
            return "high"
        elif score >= 60:
            return "medium"
        else:
            return "low"

    @staticmethod
    def calculate(
            stage_deadline: Optional[datetime],
            stage_entered_at: Optional[datetime],
            current_time: Optional[datetime] = None
    ) -> 'TaskPriority':
        """Calculate priority for an application

        Args:
            stage_deadline: Deadline for current stage
            stage_entered_at: When application entered current stage
            current_time: Current time (defaults to now)

        Returns:
            TaskPriority value object with calculated weights
        """
        if current_time is None:
            current_time = datetime.utcnow()

        deadline_weight = TaskPriority._calculate_deadline_weight(stage_deadline, current_time)
        time_weight = TaskPriority._calculate_time_in_stage_weight(stage_entered_at, current_time)

        return TaskPriority(
            base_priority=50,
            deadline_weight=deadline_weight,
            time_in_stage_weight=time_weight,
            position_weight=0,  # Future enhancement
            candidate_weight=0  # Future enhancement
        )

    @staticmethod
    def _calculate_deadline_weight(deadline: Optional[datetime], now: datetime) -> int:
        """Calculate weight based on deadline proximity

        Returns 0-50:
        - Overdue: 50
        - < 24 hours: 40
        - < 3 days: 30
        - < 7 days: 20
        - < 14 days: 10
        - > 14 days: 0
        - No deadline: 0
        """
        if deadline is None:
            return 0

        time_until_deadline = deadline - now

        # Overdue
        if time_until_deadline.total_seconds() < 0:
            return 50

        hours_until = time_until_deadline.total_seconds() / 3600

        if hours_until < 24:
            return 40
        elif hours_until < 72:  # 3 days
            return 30
        elif hours_until < 168:  # 7 days
            return 20
        elif hours_until < 336:  # 14 days
            return 10
        else:
            return 0

    @staticmethod
    def _calculate_time_in_stage_weight(stage_entered_at: Optional[datetime], now: datetime) -> int:
        """Calculate weight based on time in current stage

        Returns 0-30:
        - > 14 days: 30
        - > 7 days: 20
        - > 3 days: 15
        - > 1 day: 10
        - < 1 day: 5
        - Not in stage: 0
        """
        if stage_entered_at is None:
            return 0

        time_in_stage = now - stage_entered_at
        hours_in_stage = time_in_stage.total_seconds() / 3600

        if hours_in_stage > 336:  # 14 days
            return 30
        elif hours_in_stage > 168:  # 7 days
            return 20
        elif hours_in_stage > 72:  # 3 days
            return 15
        elif hours_in_stage > 24:  # 1 day
            return 10
        else:
            return 5

    def __str__(self) -> str:
        return f"Priority({self.priority_level}, score={self.total_score})"

    def __repr__(self) -> str:
        return (
            f"TaskPriority(total={self.total_score}, level={self.priority_level}, "
            f"base={self.base_priority}, deadline={self.deadline_weight}, "
            f"time={self.time_in_stage_weight})"
        )
