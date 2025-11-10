"""Delete Company With All Data Command - Elimina una empresa con toda su información relacionada"""
from dataclasses import dataclass
import logging

from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.company.domain.value_objects.company_id import CompanyId
from src.company_bc.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company_bc.company.domain.exceptions.company_exceptions import CompanyNotFoundError
from src.company_bc.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company_bc.company.domain.infrastructure.company_user_invitation_repository_interface import CompanyUserInvitationRepositoryInterface
from src.company_role.domain.infrastructure.company_role_repository_interface import CompanyRoleRepositoryInterface
from src.company_bc.company_page.domain.infrastructure.company_page_repository_interface import CompanyPageRepositoryInterface
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import CompanyCandidateRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.shared_bc.customization.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.company_bc.job_position.domain.repositories.job_position_repository_interface import JobPositionRepositoryInterface
from src.customization.domain.interfaces.entity_customization_repository_interface import EntityCustomizationRepositoryInterface
from src.customization.domain.enums.entity_customization_type_enum import EntityCustomizationTypeEnum
from core.database import SQLAlchemyDatabase

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeleteCompanyWithAllDataCommand(Command):
    """Command to delete a company with all its related data
    
    This command deletes:
    - CompanyCandidate relationships (NOT the candidates themselves)
    - JobPositions and their related data (stages, comments)
    - Workflows and their stages
    - Phases
    - EntityCustomizations related to the company
    - CompanyRoles
    - CompanyPages
    - CompanyUsers
    - CompanyUserInvitations
    - TalentPoolEntries
    - Finally, the Company itself
    
    Note: Candidates are NOT deleted as they don't belong to a company.
    """
    company_id: CompanyId


class DeleteCompanyWithAllDataCommandHandler(CommandHandler[DeleteCompanyWithAllDataCommand]):
    """Handler for deleting a company with all its related data"""
    
    def __init__(
        self,
        company_repository: CompanyRepositoryInterface,
        company_user_repository: CompanyUserRepositoryInterface,
        company_user_invitation_repository: CompanyUserInvitationRepositoryInterface,
        company_role_repository: CompanyRoleRepositoryInterface,
        company_page_repository: CompanyPageRepositoryInterface,
        company_candidate_repository: CompanyCandidateRepositoryInterface,
        workflow_repository: WorkflowRepositoryInterface,
        workflow_stage_repository: WorkflowStageRepositoryInterface,
        phase_repository: PhaseRepositoryInterface,
        job_position_repository: JobPositionRepositoryInterface,
        entity_customization_repository: EntityCustomizationRepositoryInterface,
        database: SQLAlchemyDatabase,
    ):
        self.company_repository = company_repository
        self.company_user_repository = company_user_repository
        self.company_user_invitation_repository = company_user_invitation_repository
        self.company_role_repository = company_role_repository
        self.company_page_repository = company_page_repository
        self.company_candidate_repository = company_candidate_repository
        self.workflow_repository = workflow_repository
        self.workflow_stage_repository = workflow_stage_repository
        self.phase_repository = phase_repository
        self.job_position_repository = job_position_repository
        self.entity_customization_repository = entity_customization_repository
        self.database = database
    
    def execute(self, command: DeleteCompanyWithAllDataCommand) -> None:
        """Execute the command to delete company with all related data"""
        company_id = command.company_id
        
        # Verify company exists
        company = self.company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundError(f"Company with id {company_id.value} not found")
        
        log.info(f"Starting deletion of company {company_id.value} with all related data")
        
        try:
            # Step 1: Delete CompanyCandidate relationships (NOT the candidates)
            # These may reference workflows, so delete them first
            self._delete_company_candidates(company_id)
            
            # Step 2: Delete JobPositions (and their stages/comments are handled by CASCADE or manually)
            # These may reference workflows, so delete them before workflows
            self._delete_job_positions(company_id)
            
            # Step 3: Delete EntityCustomizations (may reference workflows/phases/job_positions)
            # Delete before workflows/phases to avoid foreign key issues
            self._delete_entity_customizations(company_id)
            
            # Step 4: Delete WorkflowStages (before workflows)
            self._delete_workflow_stages(company_id)
            
            # Step 5: Delete Workflows (may reference phases)
            self._delete_workflows(company_id)
            
            # Step 6: Delete Phases
            self._delete_phases(company_id)
            
            # Step 7: Delete CompanyRoles
            self._delete_company_roles(company_id)
            
            # Step 8: Delete CompanyPages
            self._delete_company_pages(company_id)
            
            # Step 9: Delete CompanyUsers (CASCADE will handle some, but we do it explicitly)
            self._delete_company_users(company_id)
            
            # Step 10: Delete CompanyUserInvitations (CASCADE will handle, but we do it explicitly)
            self._delete_company_user_invitations(company_id)
            
            # Step 11: Delete TalentPoolEntries (CASCADE will handle, but we do it explicitly)
            self._delete_talent_pool_entries(company_id)
            
            # Step 12: Finally, delete the Company itself
            self.company_repository.delete(company_id)
            
            log.info(f"Successfully deleted company {company_id.value} with all related data")
            
        except Exception as e:
            log.error(f"Error deleting company {company_id.value}: {str(e)}")
            raise
    
    def _delete_company_candidates(self, company_id: CompanyId) -> None:
        """Delete all CompanyCandidate relationships for the company"""
        log.debug(f"Deleting CompanyCandidate relationships for company {company_id.value}")
        company_candidates = self.company_candidate_repository.list_by_company(company_id)
        for company_candidate in company_candidates:
            self.company_candidate_repository.delete(company_candidate.id)
        log.debug(f"Deleted {len(company_candidates)} CompanyCandidate relationships")
    
    def _delete_job_positions(self, company_id: CompanyId) -> None:
        """Delete all JobPositions for the company"""
        log.debug(f"Deleting JobPositions for company {company_id.value}")
        # Use find_by_filters to get all job positions for the company
        job_positions = self.job_position_repository.find_by_filters(
            company_id=company_id.value,
            limit=10000  # Large limit to get all
        )
        for job_position in job_positions:
            self.job_position_repository.delete(job_position.id)
        log.debug(f"Deleted {len(job_positions)} JobPositions")
    
    def _delete_workflow_stages(self, company_id: CompanyId) -> None:
        """Delete all WorkflowStages for workflows belonging to the company"""
        log.debug(f"Deleting WorkflowStages for company {company_id.value}")
        workflows = self.workflow_repository.list_by_company(company_id)
        total_stages_deleted = 0
        for workflow in workflows:
            stages = self.workflow_stage_repository.list_by_workflow(workflow.id)
            for stage in stages:
                self.workflow_stage_repository.delete(stage.id)
                total_stages_deleted += 1
        log.debug(f"Deleted {total_stages_deleted} WorkflowStages")
    
    def _delete_workflows(self, company_id: CompanyId) -> None:
        """Delete all Workflows for the company"""
        log.debug(f"Deleting Workflows for company {company_id.value}")
        workflows = self.workflow_repository.list_by_company(company_id)
        for workflow in workflows:
            self.workflow_repository.delete(workflow.id)
        log.debug(f"Deleted {len(workflows)} Workflows")
    
    def _delete_phases(self, company_id: CompanyId) -> None:
        """Delete all Phases for the company"""
        log.debug(f"Deleting Phases for company {company_id.value}")
        phases = self.phase_repository.list_by_company(company_id)
        for phase in phases:
            self.phase_repository.delete(phase.id)
        log.debug(f"Deleted {len(phases)} Phases")
    
    def _delete_entity_customizations(self, company_id: CompanyId) -> None:
        """Delete all EntityCustomizations related to the company"""
        log.debug(f"Deleting EntityCustomizations for company {company_id.value}")
        # Delete customizations where entity_type is Company and entity_id is the company_id
        with self.database.get_session() as session:
            from src.customization.infrastructure.models.entity_customization_model import EntityCustomizationModel

            # Get all workflow IDs for this company
            workflows = self.workflow_repository.list_by_company(company_id)
            workflow_ids = {str(w.id.value) for w in workflows}
            
            # Delete customizations for:
            # 1. Workflow entity type with workflow_ids from this company
            # 2. JobPosition entity type with job_position_ids from this company
            # 3. CandidateApplication entity type (these are linked to workflows/positions)

            # Get all job position IDs for this company
            job_positions = self.job_position_repository.find_by_filters(
                company_id=company_id.value,
                limit=10000
            )
            job_position_ids = {str(jp.id.value) for jp in job_positions}
            
            # Get all company candidate IDs (for CandidateApplication customizations)
            company_candidates = self.company_candidate_repository.list_by_company(company_id)
            company_candidate_ids = {str(cc.id.value) for cc in company_candidates}
            
            # Delete Workflow customizations
            if workflow_ids:
                session.query(EntityCustomizationModel).filter(
                    EntityCustomizationModel.entity_type == EntityCustomizationTypeEnum.WORKFLOW.value,
                    EntityCustomizationModel.entity_id.in_(workflow_ids)
                ).delete(synchronize_session=False)
            
            # Delete JobPosition customizations
            if job_position_ids:
                session.query(EntityCustomizationModel).filter(
                    EntityCustomizationModel.entity_type == EntityCustomizationTypeEnum.JOB_POSITION.value,
                    EntityCustomizationModel.entity_id.in_(job_position_ids)
                ).delete(synchronize_session=False)
            
            # Delete CandidateApplication customizations (linked to company candidates)
            if company_candidate_ids:
                session.query(EntityCustomizationModel).filter(
                    EntityCustomizationModel.entity_type == EntityCustomizationTypeEnum.CANDIDATE_APPLICATION.value,
                    EntityCustomizationModel.entity_id.in_(company_candidate_ids)
                ).delete(synchronize_session=False)
            
            session.commit()
        log.debug("Deleted EntityCustomizations")
    
    def _delete_company_roles(self, company_id: CompanyId) -> None:
        """Delete all CompanyRoles for the company"""
        log.debug(f"Deleting CompanyRoles for company {company_id.value}")
        roles = self.company_role_repository.list_by_company(company_id, active_only=False)
        for role in roles:
            self.company_role_repository.delete(role.id)
        log.debug(f"Deleted {len(roles)} CompanyRoles")
    
    def _delete_company_pages(self, company_id: CompanyId) -> None:
        """Delete all CompanyPages for the company"""
        log.debug(f"Deleting CompanyPages for company {company_id.value}")
        pages = self.company_page_repository.list_by_company(company_id)
        for page in pages:
            self.company_page_repository.delete(page.id)
        log.debug(f"Deleted {len(pages)} CompanyPages")
    
    def _delete_company_users(self, company_id: CompanyId) -> None:
        """Delete all CompanyUsers for the company"""
        log.debug(f"Deleting CompanyUsers for company {company_id.value}")
        company_users = self.company_user_repository.list_by_company(company_id)
        for company_user in company_users:
            self.company_user_repository.delete(company_user.id)
        log.debug(f"Deleted {len(company_users)} CompanyUsers")
    
    def _delete_company_user_invitations(self, company_id: CompanyId) -> None:
        """Delete all CompanyUserInvitations for the company"""
        log.debug(f"Deleting CompanyUserInvitations for company {company_id.value}")
        with self.database.get_session() as session:
            from src.company_bc.company.infrastructure.models.company_user_invitation_model import CompanyUserInvitationModel
            deleted_count = session.query(CompanyUserInvitationModel).filter_by(
                company_id=str(company_id.value)
            ).delete(synchronize_session=False)
            session.commit()
        log.debug(f"Deleted {deleted_count} CompanyUserInvitations")
    
    def _delete_talent_pool_entries(self, company_id: CompanyId) -> None:
        """Delete all TalentPoolEntries for the company"""
        log.debug(f"Deleting TalentPoolEntries for company {company_id.value}")
        with self.database.get_session() as session:
            from src.company_bc.talent_pool.infrastructure.models.talent_pool_entry_model import TalentPoolEntryModel
            deleted_count = session.query(TalentPoolEntryModel).filter_by(
                company_id=str(company_id.value)
            ).delete(synchronize_session=False)
            session.commit()
        log.debug(f"Deleted {deleted_count} TalentPoolEntries")

