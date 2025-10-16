"""
Admin controller for candidate and user management
"""
from datetime import datetime
from typing import List, Optional

from src.candidate.application.queries.get_candidate_by_id import GetCandidateByIdQuery
from src.candidate.application.queries.list_candidates import ListCandidatesQuery
from src.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate.domain.value_objects import CandidateId
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.user.application.commands.update_user_password_command import UpdateUserPasswordCommand
from src.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.user.domain.services.password_service import PasswordService
from src.user.domain.value_objects.UserId import UserId


class AdminCandidateController:
    """Controller for administrative management of candidates and users"""

    def __init__(
            self,
            command_bus: CommandBus,
            query_bus: QueryBus,
            user_repository: UserRepositoryInterface,
            candidate_repository: CandidateRepositoryInterface
    ):
        self.command_bus = command_bus
        self.query_bus = query_bus
        self.user_repository = user_repository
        self.candidate_repository = candidate_repository

    def list_candidates(
            self,
            search_term: Optional[str] = None,
            status: Optional[str] = None,
            limit: int = 10,
            offset: int = 0
    ) -> dict:
        """List candidates with filters for admin"""

        # Use existing candidates query
        candidates_dto: List[CandidateDto] = self.query_bus.query(
            ListCandidatesQuery(name=search_term, phone=None)
        )

        # Apply additional filters if needed
        if status:
            # Status filtering can be implemented in the query if needed
            pass

        # Apply manual pagination (ideally this should be in the query)
        total_count = len(candidates_dto)
        paginated_candidates = candidates_dto[offset:offset + limit]

        # Enrich with associated user information
        enriched_candidates = []
        for candidate_dto in paginated_candidates:
            candidate_data = {
                "id": candidate_dto.id,
                "name": candidate_dto.name,
                "email": candidate_dto.email,
                "phone": candidate_dto.phone,
                "city": candidate_dto.city,
                "country": candidate_dto.country,
                "job_category": candidate_dto.job_category.value if candidate_dto.job_category else None,
                "created_at": candidate_dto.created_at.isoformat() if candidate_dto.created_at else None,
                "status": "active",  # Default, can be improved
                "has_resume": False,  # Can be obtained from resumes query if needed
                "years_of_experience": None  # Can be calculated if available
            }
            enriched_candidates.append(candidate_data)

        return {
            "candidates": enriched_candidates,
            "total_count": total_count,
            "has_more": offset + limit < total_count
        }

    def get_candidate_with_user(self, candidate_id: str) -> dict:
        """Get complete details of candidate and associated user"""

        candidate_dto: Optional[CandidateDto] = self.query_bus.query(
            GetCandidateByIdQuery(CandidateId.from_string(candidate_id))
        )

        if not candidate_dto:
            raise ValueError(f"Candidate with id {candidate_id} not found")

        # Get associated user information using repository
        user = None
        if candidate_dto.user_id:
            try:
                user = self.user_repository.get_by_id(candidate_dto.user_id)
            except Exception:
                pass  # User not found or error

        return {
            "candidate": {
                "id": candidate_dto.id,
                "name": candidate_dto.name,
                "email": candidate_dto.email,
                "phone": candidate_dto.phone,
                "city": candidate_dto.city,
                "country": candidate_dto.country,
                "job_category": candidate_dto.job_category.value if candidate_dto.job_category else None,
                "date_of_birth": candidate_dto.date_of_birth.isoformat() if candidate_dto.date_of_birth else None,
                "created_at": candidate_dto.created_at.isoformat() if candidate_dto.created_at else None,
            },
            "user": {
                "id": user.id.value if user else None,
                "email": user.email if user else candidate_dto.email,
                "is_active": user.is_active if user else True,
                "created_at": None,  # User entity doesn't have created_at currently
                "last_login": None,  # User entity doesn't have last_login currently
                "has_password": bool(user.hashed_password) if user else False
            }
        }

    def update_user_password(self, candidate_id: str, new_password: str, admin_id: str) -> dict:
        """Update user password from admin, creating account if it doesn't exist"""

        # Get the candidate
        candidate_dto: Optional[CandidateDto] = self.query_bus.query(
            GetCandidateByIdQuery(CandidateId.from_string(candidate_id))
        )

        if not candidate_dto:
            raise ValueError(f"Candidate with id {candidate_id} not found")

        # Check if candidate already has an associated user via user_id
        user = None
        found_by_user_id = False
        if candidate_dto.user_id:
            try:
                # candidate_dto.user_id is already a UserId object, no conversion needed
                user = self.user_repository.get_by_id(candidate_dto.user_id)
                if user:
                    found_by_user_id = True
            except Exception:
                pass  # User not found

        # If no user associated by user_id, check if one exists with the same email
        if not user:
            try:
                user = self.user_repository.get_by_email(candidate_dto.email)
            except Exception:
                pass  # User not found by email

        if user:
            # User already exists, just update password
            command = UpdateUserPasswordCommand(
                user_id=user.id,
                new_password=new_password,
                updated_by_admin_id=admin_id
            )

            self.command_bus.dispatch(command)

            return {
                "success": True,
                "message": (
                    f"Password updated successfully. User "
                    f"{'found by email match' if not found_by_user_id else 'already linked to candidate'}."
                ),
                "updated_at": datetime.utcnow().isoformat(),
                "updated_by": admin_id,
                "user_created": False,
                "user_found_by": "user_id" if found_by_user_id else "email"
            }
        else:
            # Candidate has no associated user, create a new one
            # Use candidate's email as user's login email
            from src.user.domain.entities.user import User

            try:
                # Generate ID for new user
                new_user_id = UserId.generate()

                # Hash password using PasswordService
                hashed_password = PasswordService.hash_password(new_password)

                # Create user using candidate's email as access email
                new_user = User(
                    id=new_user_id,
                    email=candidate_dto.email,  # Candidate's email becomes login email
                    hashed_password=hashed_password,
                    is_active=True
                )

                # Create user in repository
                self.user_repository.create(new_user)

                # TODO: Update candidate.user_id relationship when method is implemented
                # For now user is created but relationship is not automatically established
                # This will require a specific command to update the relationship

                return {
                    "success": True,
                    "message": "User account created and password set successfully. Login email will be the candidate's contact email.",
                    "updated_at": datetime.utcnow().isoformat(),
                    "updated_by": admin_id,
                    "user_created": True,
                    "login_email": candidate_dto.email
                }

            except Exception as e:
                # If there's an error (like duplicate email), try to find existing user with that email
                error_message = str(e).lower()
                if ("already exists" in error_message or
                        "unique constraint" in error_message or
                        "ya está registrado" in error_message or
                        "email already" in error_message):
                    # Duplicate email - handle more clearly for admin
                    return {
                        "success": False,
                        "message": (
                            f"A user account with email '{candidate_dto.email}' already exists. "
                            "This candidate's contact email is already being used as a login email by another user. "
                            "Please either: 1) Use a different email for the candidate's contact info, or "
                            "2) Contact system administrator to resolve the email conflict."
                        ),
                        "error": "duplicate_email",
                        "candidate_email": candidate_dto.email,
                        "suggested_action": "check_existing_users_or_change_candidate_email"
                    }

                # General error
                raise ValueError(f"Failed to create user account: {str(e)}")

    def get_candidates_stats(self) -> dict:
        """Get candidate statistics for admin"""

        # Basic statistics for now
        # In a complete implementation, this would be a specific query
        candidates_dto: List[CandidateDto] = self.query_bus.query(
            ListCandidatesQuery(name=None, phone=None)
        )

        total_candidates = len(candidates_dto)

        # Basic statistics
        stats = {
            "total_candidates": total_candidates,
            "active_candidates": total_candidates,  # Simplified
            "pending_candidates": 0,
            "candidates_with_resumes": 0,  # Can be implemented
            "candidates_this_month": 0,  # Can be implemented with date filters
            "generated_at": datetime.utcnow().isoformat()
        }

        return stats
