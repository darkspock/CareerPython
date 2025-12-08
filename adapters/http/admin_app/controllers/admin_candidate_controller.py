"""
Admin controller for candidate and user management
"""
from datetime import datetime
from typing import List, Optional

from src.auth_bc.user.application.commands.create_user_command import CreateUserCommand
from src.auth_bc.user.application.commands.update_user_password_command import UpdateUserPasswordCommand
from src.auth_bc.user.application.queries.dtos.auth_dto import CurrentUserDto
from src.auth_bc.user.application.queries.get_user_by_email_query import GetUserByEmailQuery
from src.auth_bc.user.application.queries.get_user_by_id_query import GetUserByIdQuery
from src.auth_bc.user.domain.exceptions.user_exceptions import EmailAlreadyExistException
from src.auth_bc.user.domain.value_objects import UserId
from src.candidate_bc.candidate.application.queries.get_candidate_by_id import GetCandidateByIdQuery
from src.candidate_bc.candidate.application.queries.list_candidates import ListCandidatesQuery
from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate_bc.candidate.domain.value_objects import CandidateId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus


class AdminCandidateController:
    """Controller for administrative management of candidates and users"""

    def __init__(
            self,
            command_bus: CommandBus,
            query_bus: QueryBus
    ):
        self.command_bus = command_bus
        self.query_bus = query_bus

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

        # Get associated user information using query
        user_dto: Optional[CurrentUserDto] = None
        if candidate_dto.user_id:
            try:
                user_dto = self.query_bus.query(
                    GetUserByIdQuery(user_id=candidate_dto.user_id)
                )
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
                "id": user_dto.user_id if user_dto else None,
                "email": user_dto.email if user_dto else candidate_dto.email,
                "is_active": user_dto.is_active if user_dto else True,
                "created_at": None,  # User entity doesn't have created_at currently
                "last_login": None,  # User entity doesn't have last_login currently
                "has_password": user_dto.has_password if user_dto else False
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
        user_dto: Optional[CurrentUserDto] = None
        found_by_user_id = False
        if candidate_dto.user_id:
            try:
                result: Optional[CurrentUserDto] = self.query_bus.query(
                    GetUserByIdQuery(user_id=candidate_dto.user_id)
                )
                if result:
                    user_dto = result
                    found_by_user_id = True
            except Exception:
                pass  # User not found

        # If no user associated by user_id, check if one exists with the same email
        if not user_dto:
            try:
                user_dto = self.query_bus.query(
                    GetUserByEmailQuery(email=candidate_dto.email)
                )
            except Exception:
                pass  # User not found by email

        if user_dto:
            # User already exists, just update password
            command = UpdateUserPasswordCommand(
                user_id=UserId.from_string(user_dto.user_id),
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
            try:
                # Generate ID for new user
                new_user_id = UserId.generate()

                # Create user using command
                create_command = CreateUserCommand(
                    id=new_user_id,
                    email=candidate_dto.email,
                    password=new_password,
                    is_active=True
                )
                self.command_bus.dispatch(create_command)

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

            except EmailAlreadyExistException:
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
            except Exception as e:
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
