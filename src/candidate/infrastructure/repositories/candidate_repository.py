from typing import List, Optional, Any

from core.database import DatabaseInterface
from src.candidate.domain.entities.candidate import Candidate
from src.candidate.domain.enums.candidate_enums import CandidateStatusEnum, LanguageEnum, \
    LanguageLevelEnum, PositionRoleEnum, WorkModalityEnum
from src.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate.infrastructure.models.candidate_model import CandidateModel
from src.shared.infrastructure.helpers.mixed_helper import MixedHelper
from src.shared.infrastructure.repositories.base import BaseRepository
from src.user.domain.value_objects.UserId import UserId


class SQLAlchemyCandidateRepository(CandidateRepositoryInterface):
    """Implementación de repositorio de candidatos con SQLAlchemy"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, CandidateModel)

    def _to_domain(self, model: CandidateModel) -> Candidate:
        """Convierte modelo de SQLAlchemy a entidad de dominio"""
        # Convert work_modality JSON to enum list
        work_modality_enums = []
        if model.work_modality:
            work_modality_enums = [WorkModalityEnum(wm) for wm in model.work_modality]

        # Convert languages JSON to enum dict
        languages_dict = {}
        if model.languages:
            for lang, level in model.languages.items():
                languages_dict[LanguageEnum(lang)] = LanguageLevelEnum(level)

        # Convert current_roles JSON to enum list
        current_roles_enums = []
        if model.current_roles:
            current_roles_enums = [PositionRoleEnum(role) for role in model.current_roles]

        # Convert expected_roles JSON to enum list
        expected_roles_enums = []
        if model.expected_roles:
            expected_roles_enums = [PositionRoleEnum(role) for role in model.expected_roles]

        # Convert skills JSON to list of strings
        skills_list = model.skills or []

        # Convert job level strings to enums - DISABLED until migration
        current_job_level_enum = None
        expected_job_level_enum = None
        # if hasattr(model, 'current_job_level') and model.current_job_level:
        #     current_job_level_enum = JobPositionLevelEnum(model.current_job_level)
        # if hasattr(model, 'expected_job_level') and model.expected_job_level:
        #     expected_job_level_enum = JobPositionLevelEnum(model.expected_job_level)

        return Candidate(
            id=CandidateId.from_string(model.id),
            name=model.name,
            date_of_birth=model.date_of_birth,
            city=model.city,
            country=model.country,
            phone=model.phone,
            email=model.email,
            user_id=UserId.from_string(model.user_id),
            status=model.status,
            job_category=model.job_category,
            candidate_type=model.candidate_type,
            expected_annual_salary=model.expected_annual_salary,
            current_annual_salary=model.current_annual_salary,
            currency=model.currency,
            relocation=model.relocation,
            work_modality=work_modality_enums,
            languages=languages_dict,
            other_languages=model.other_languages,
            linkedin_url=model.linkedin_url,
            data_consent=model.data_consent,
            data_consent_on=model.data_consent_on,
            current_roles=current_roles_enums,
            expected_roles=expected_roles_enums,
            current_job_level=current_job_level_enum,
            expected_job_level=expected_job_level_enum,
            skills=skills_list,
            created_on=model.created_on,
            updated_on=model.updated_on,
            timezone=model.timezone,
            candidate_notes=model.candidate_notes
        )

    def _to_model(self, domain: Candidate) -> CandidateModel:
        """Convierte entidad de dominio a modelo de SQLAlchemy"""
        # Convert work_modality enum list to JSON
        work_modality_values = MixedHelper.enum_list_to_string_list(domain.work_modality)

        # Convert languages enum dict to JSON
        languages_dict = {}
        if domain.languages:
            for lang, level in domain.languages.items():
                languages_dict[lang.value] = level.value

        # Convert current_roles enum list to JSON
        current_roles_values = MixedHelper.enum_list_to_string_list(domain.current_roles)

        # Convert expected_roles enum list to JSON
        expected_roles_values = MixedHelper.enum_list_to_string_list(domain.expected_roles)

        model = CandidateModel(
            id=domain.id.value,
            name=domain.name,
            date_of_birth=domain.date_of_birth,
            city=domain.city,
            country=domain.country,
            phone=domain.phone,
            email=domain.email,
            user_id=domain.user_id.value,
            status=domain.status,
            job_category=domain.job_category,
            candidate_type=domain.candidate_type,
            expected_annual_salary=domain.expected_annual_salary,
            current_annual_salary=domain.current_annual_salary,
            currency=domain.currency,
            relocation=domain.relocation,
            work_modality=work_modality_values,
            languages=languages_dict,
            other_languages=domain.other_languages,
            linkedin_url=domain.linkedin_url,
            data_consent=domain.data_consent,
            data_consent_on=domain.data_consent_on,
            current_roles=current_roles_values,
            expected_roles=expected_roles_values,
            # current_job_level=domain.current_job_level.value if domain.current_job_level else None,  # DISABLED until migration
            # expected_job_level=domain.expected_job_level.value if domain.expected_job_level else None,  # DISABLED until migration
            skills=domain.skills,
            created_on=domain.created_on,
            updated_on=domain.updated_on,
            timezone=domain.timezone,
            candidate_notes=domain.candidate_notes
        )
        return model

    def create(self, candidate: Candidate) -> None:
        model = self._to_model(candidate)
        self.base_repo.create(model)

    def get_by_id(self, candidate_id: CandidateId) -> Optional[Candidate]:
        with self.database.get_session() as session:
            model = session.query(CandidateModel).filter(CandidateModel.id == candidate_id.value).first()
            if model:
                return self._to_domain(model)
            return None

    def get_all(self, name: Optional[str] = None, phone: Optional[str] = None) -> List[Candidate]:
        with self.database.get_session() as session:
            query = session.query(CandidateModel)

            if name:
                query = query.filter(CandidateModel.name.ilike(f"%{name}%"))
            if phone:
                query = query.filter(CandidateModel.phone.ilike(f"%{phone}%"))

            models = query.all()
            return [self._to_domain(model) for model in models]

    def get_by_user_id(self, id: UserId) -> Optional[Candidate]:
        with self.database.get_session() as session:
            model = session.query(CandidateModel).filter(CandidateModel.user_id == id.value).first()
            if model:
                return self._to_domain(model)
            return None

    def update(self, candidate: Candidate) -> None:
        with self.database.get_session() as session:
            model = session.query(CandidateModel).filter(CandidateModel.id == candidate.id.value).first()
            if model:
                # Update all fields from the entity
                model.name = candidate.name
                model.date_of_birth = candidate.date_of_birth
                model.city = candidate.city
                model.country = candidate.country
                model.phone = candidate.phone
                model.email = candidate.email
                model.user_id = candidate.user_id.value
                model.status = candidate.status
                model.job_category = candidate.job_category
                model.candidate_type = candidate.candidate_type
                model.expected_annual_salary = candidate.expected_annual_salary
                model.current_annual_salary = candidate.current_annual_salary
                model.currency = candidate.currency
                model.relocation = candidate.relocation

                # Convert work_modality enum list to JSON
                model.work_modality = [wm.value for wm in candidate.work_modality] if candidate.work_modality else []

                # Convert languages enum dict to JSON
                languages_dict = {}
                if candidate.languages:
                    for lang, level in candidate.languages.items():
                        languages_dict[lang.value] = level.value
                model.languages = languages_dict

                model.other_languages = candidate.other_languages
                model.linkedin_url = candidate.linkedin_url
                model.data_consent = candidate.data_consent
                model.data_consent_on = candidate.data_consent_on

                # Convert roles enum lists to JSON
                model.current_roles = [role.value for role in
                                       candidate.current_roles] if candidate.current_roles else []
                model.expected_roles = [role.value for role in
                                        candidate.expected_roles] if candidate.expected_roles else []

                # model.current_job_level = candidate.current_job_level.value if candidate.current_job_level else None  # DISABLED until migration
                # model.expected_job_level = candidate.expected_job_level.value if candidate.expected_job_level else None  # DISABLED until migration
                model.skills = candidate.skills
                model.created_on = candidate.created_on
                model.updated_on = candidate.updated_on
                model.timezone = candidate.timezone
                model.candidate_notes = candidate.candidate_notes

                session.commit()
                return

            raise ValueError(f"Candidate with id {candidate.id.value} not found")

    def delete(self, candidate_id: CandidateId) -> bool:
        return self.base_repo.delete(candidate_id)

    # Admin-specific methods for advanced filtering and stats
    def admin_find_by_filters(self, name: Optional[str] = None,
                              email: Optional[str] = None,
                              phone: Optional[str] = None,
                              status: Optional[Any] = None,
                              job_category: Optional[Any] = None,
                              location: Optional[str] = None,
                              years_of_experience_min: Optional[int] = None,
                              years_of_experience_max: Optional[int] = None,
                              created_after: Optional[Any] = None,
                              created_before: Optional[Any] = None,
                              search_term: Optional[str] = None,
                              has_resume: Optional[bool] = None,
                              limit: int = 50, offset: int = 0) -> List[Candidate]:
        """Advanced filtering for admin panel"""
        from sqlalchemy import or_

        with self.database.get_session() as session:
            query = session.query(CandidateModel)

            # Apply basic filters
            if name:
                query = query.filter(CandidateModel.name.ilike(f"%{name}%"))

            if email:
                query = query.filter(CandidateModel.email.ilike(f"%{email}%"))

            if phone:
                query = query.filter(CandidateModel.phone.ilike(f"%{phone}%"))

            if status:
                query = query.filter(CandidateModel.status == status)

            if job_category:
                query = query.filter(CandidateModel.job_category == job_category)

            if location:
                query = query.filter(
                    or_(
                        CandidateModel.city.ilike(f"%{location}%"),
                        CandidateModel.country.ilike(f"%{location}%")
                    )
                )

            # Date range filters
            if created_after:
                query = query.filter(CandidateModel.created_at >= created_after)

            if created_before:
                query = query.filter(CandidateModel.created_at <= created_before)

            # Global search term
            if search_term:
                query = query.filter(
                    or_(
                        CandidateModel.name.ilike(f"%{search_term}%"),
                        CandidateModel.email.ilike(f"%{search_term}%"),
                        CandidateModel.phone.ilike(f"%{search_term}%"),
                        CandidateModel.city.ilike(f"%{search_term}%"),
                        CandidateModel.country.ilike(f"%{search_term}%")
                    )
                )

            # Order by created_at desc
            query = query.order_by(CandidateModel.created_at.desc())

            # Apply pagination
            query = query.offset(offset).limit(limit)

            models = query.all()
            return [self._to_domain(model) for model in models]

    def count_by_status(self, status: Any) -> int:
        """Count candidates by status"""
        with self.database.get_session() as session:
            return session.query(CandidateModel).filter(CandidateModel.status == status).count()

    def count_total(self) -> int:
        """Count total candidates"""
        with self.database.get_session() as session:
            return session.query(CandidateModel).count()

    def count_recent(self, days: int = 30) -> int:
        """Count candidates created in the last N days"""
        from datetime import datetime, timedelta

        with self.database.get_session() as session:
            since_date = datetime.utcnow() - timedelta(days=days)
            return session.query(CandidateModel).filter(
                CandidateModel.created_at >= since_date
            ).count()

    def count_active(self) -> int:
        """Count active candidates (not inactive)"""

        with self.database.get_session() as session:
            return session.query(CandidateModel).filter(
                CandidateModel.status == CandidateStatusEnum.COMPLETE
            ).count()

    def count_all(self) -> int:
        """Count all candidates"""
        with self.database.get_session() as session:
            return session.query(CandidateModel).count()

    def count_with_resume(self) -> int:
        """Count candidates with resume - simplified implementation"""
        # For now, return 0 since we don't have resume relationships
        # This can be implemented later when resume functionality is needed
        return 0
