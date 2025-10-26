"""
Talent Pool Entry Entity
Phase 8: Domain entity for company talent pool
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.talent_pool.domain.value_objects.talent_pool_entry_id import TalentPoolEntryId
from src.talent_pool.domain.enums.talent_pool_status import TalentPoolStatus


@dataclass
class TalentPoolEntry:
    """
    Domain entity representing a candidate in a company's talent pool.

    Business rules:
    - Each candidate can appear only once per company in the talent pool
    - Rating must be between 1-5 if provided
    - Tags are used for categorization and search
    - Status tracks the current state of the talent pool entry
    """

    id: TalentPoolEntryId
    company_id: str
    candidate_id: str
    source_application_id: Optional[str]
    source_position_id: Optional[str]
    added_reason: Optional[str]
    tags: List[str]
    rating: Optional[int]
    notes: Optional[str]
    status: TalentPoolStatus
    added_by_user_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        company_id: str,
        candidate_id: str,
        added_reason: Optional[str] = None,
        tags: Optional[List[str]] = None,
        rating: Optional[int] = None,
        notes: Optional[str] = None,
        status: TalentPoolStatus = TalentPoolStatus.ACTIVE,
        source_application_id: Optional[str] = None,
        source_position_id: Optional[str] = None,
        added_by_user_id: Optional[str] = None,
    ) -> "TalentPoolEntry":
        """
        Factory method to create a new talent pool entry.

        Args:
            company_id: The company ID
            candidate_id: The candidate ID
            added_reason: Reason for adding to talent pool
            tags: List of tags for categorization
            rating: Rating from 1-5
            notes: Additional notes
            status: Entry status (default: ACTIVE)
            source_application_id: Original application ID if from application
            source_position_id: Original position ID if from application
            added_by_user_id: User who added the entry

        Returns:
            New TalentPoolEntry instance

        Raises:
            ValueError: If validation fails
        """
        # Validate required fields
        if not company_id or not isinstance(company_id, str):
            raise ValueError("company_id must be a non-empty string")
        if not candidate_id or not isinstance(candidate_id, str):
            raise ValueError("candidate_id must be a non-empty string")

        # Validate rating if provided
        if rating is not None:
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("rating must be an integer between 1 and 5")

        # Validate tags
        if tags is not None and not isinstance(tags, list):
            raise ValueError("tags must be a list")

        # Ensure tags is a list
        final_tags = tags if tags is not None else []

        # Generate timestamps
        now = datetime.utcnow()

        return cls(
            id=TalentPoolEntryId.generate(),
            company_id=company_id,
            candidate_id=candidate_id,
            source_application_id=source_application_id,
            source_position_id=source_position_id,
            added_reason=added_reason,
            tags=final_tags,
            rating=rating,
            notes=notes,
            status=status,
            added_by_user_id=added_by_user_id,
            created_at=now,
            updated_at=now,
        )

    @classmethod
    def _from_repository(
        cls,
        id: TalentPoolEntryId,
        company_id: str,
        candidate_id: str,
        source_application_id: Optional[str],
        source_position_id: Optional[str],
        added_reason: Optional[str],
        tags: List[str],
        rating: Optional[int],
        notes: Optional[str],
        status: TalentPoolStatus,
        added_by_user_id: Optional[str],
        created_at: datetime,
        updated_at: datetime,
    ) -> "TalentPoolEntry":
        """
        Factory method for repository to reconstruct entity from persistence.

        This method bypasses factory validations as we trust data from DB.
        """
        return cls(
            id=id,
            company_id=company_id,
            candidate_id=candidate_id,
            source_application_id=source_application_id,
            source_position_id=source_position_id,
            added_reason=added_reason,
            tags=tags,
            rating=rating,
            notes=notes,
            status=status,
            added_by_user_id=added_by_user_id,
            created_at=created_at,
            updated_at=updated_at,
        )

    def update(
        self,
        added_reason: Optional[str] = None,
        tags: Optional[List[str]] = None,
        rating: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> None:
        """
        Update talent pool entry details.

        Args:
            added_reason: Updated reason for being in talent pool
            tags: Updated tags list
            rating: Updated rating (1-5)
            notes: Updated notes

        Raises:
            ValueError: If validation fails
        """
        # Validate rating if provided
        if rating is not None:
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("rating must be an integer between 1 and 5")

        # Validate tags
        if tags is not None and not isinstance(tags, list):
            raise ValueError("tags must be a list")

        # Update fields
        if added_reason is not None:
            self.added_reason = added_reason
        if tags is not None:
            self.tags = tags
        if rating is not None:
            self.rating = rating
        if notes is not None:
            self.notes = notes

        # Update timestamp
        self.updated_at = datetime.utcnow()

    def change_status(self, new_status: TalentPoolStatus) -> None:
        """
        Change the status of the talent pool entry.

        Args:
            new_status: The new status
        """
        if not isinstance(new_status, TalentPoolStatus):
            raise ValueError("new_status must be a TalentPoolStatus enum value")

        self.status = new_status
        self.updated_at = datetime.utcnow()

    def add_tag(self, tag: str) -> None:
        """
        Add a tag to the entry.

        Args:
            tag: Tag to add
        """
        if not tag or not isinstance(tag, str):
            raise ValueError("tag must be a non-empty string")

        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()

    def remove_tag(self, tag: str) -> None:
        """
        Remove a tag from the entry.

        Args:
            tag: Tag to remove
        """
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()

    def update_rating(self, rating: int) -> None:
        """
        Update the rating.

        Args:
            rating: New rating (1-5)

        Raises:
            ValueError: If rating is invalid
        """
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("rating must be an integer between 1 and 5")

        self.rating = rating
        self.updated_at = datetime.utcnow()

    def archive(self) -> None:
        """Archive this talent pool entry"""
        self.status = TalentPoolStatus.ARCHIVED
        self.updated_at = datetime.utcnow()

    def reactivate(self) -> None:
        """Reactivate this talent pool entry"""
        self.status = TalentPoolStatus.ACTIVE
        self.updated_at = datetime.utcnow()

    def mark_as_contacted(self) -> None:
        """Mark entry as contacted for a position"""
        self.status = TalentPoolStatus.CONTACTED
        self.updated_at = datetime.utcnow()

    def mark_as_hired(self) -> None:
        """Mark entry as hired from the talent pool"""
        self.status = TalentPoolStatus.HIRED
        self.updated_at = datetime.utcnow()

    def mark_as_not_interested(self) -> None:
        """Mark entry as not interested"""
        self.status = TalentPoolStatus.NOT_INTERESTED
        self.updated_at = datetime.utcnow()
