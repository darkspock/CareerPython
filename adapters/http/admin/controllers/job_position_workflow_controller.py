"""Job position workflow admin controller"""
import logging
from typing import List, Optional

from adapters.http.admin.schemas.job_position_workflow import (
    JobPositionWorkflowCreate, JobPositionWorkflowUpdate, JobPositionWorkflowResponse,
    MoveJobPositionToStageRequest, UpdateJobPositionCustomFieldsRequest
)
from src.job_position.application.commands.create_job_position_workflow import CreateJobPositionWorkflowCommand
from src.job_position.application.commands.update_job_position_workflow import UpdateJobPositionWorkflowCommand
from src.job_position.application.commands.move_job_position_to_stage import (
    MoveJobPositionToStageCommand,
    JobPositionValidationError
)
from src.job_position.application.commands.update_job_position_custom_fields import UpdateJobPositionCustomFieldsCommand
from src.job_position.application.queries.get_job_position_workflow import GetJobPositionWorkflowQuery
from src.job_position.application.queries.list_job_position_workflows import ListJobPositionWorkflowsQuery
from src.job_position.application.dtos.job_position_workflow_dto import JobPositionWorkflowDto
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.stage_id import StageId
from src.job_position.domain.value_objects.job_position_id import JobPositionId
from src.job_position.domain.enums.view_type import ViewTypeEnum
from src.job_position.domain.value_objects.workflow_stage import WorkflowStage
from src.job_position.domain.enums.job_position_status import JobPositionStatusEnum
from src.job_position.domain.enums.job_position_workflow_status import JobPositionWorkflowStatusEnum
from src.job_position.domain.enums.kanban_display import KanbanDisplayEnum
from src.company.domain.value_objects.company_id import CompanyId
from src.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus

logger = logging.getLogger(__name__)


class JobPositionWorkflowController:
    """Controller for job position workflow admin operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def create_workflow(self, request: JobPositionWorkflowCreate) -> JobPositionWorkflowResponse:
        """Create a new job position workflow"""
        workflow_id = JobPositionWorkflowId.generate()
        company_id = CompanyId.from_string(request.company_id)

        # Convert stages from request to WorkflowStage value objects
        stages = []
        for stage_data in request.stages:
            stage_id = StageId.from_string(stage_data.id)
            status_mapping = JobPositionStatusEnum(stage_data.status_mapping)
            kanban_display = KanbanDisplayEnum(stage_data.kanban_display)
            role = CompanyRoleId.from_string(stage_data.role) if stage_data.role else None

            stage = WorkflowStage.create(
                id=stage_id,
                name=stage_data.name,
                icon=stage_data.icon,
                background_color=stage_data.background_color,
                text_color=stage_data.text_color,
                status_mapping=status_mapping,
                kanban_display=kanban_display,
                role=role,
                field_visibility=stage_data.field_visibility,
                field_validation=stage_data.field_validation,
                field_candidate_visibility=stage_data.field_candidate_visibility,
            )
            stages.append(stage)

        default_view = ViewTypeEnum(request.default_view)

        command = CreateJobPositionWorkflowCommand(
            id=workflow_id,
            company_id=company_id,
            name=request.name,
            default_view=default_view,
            stages=stages,
            custom_fields_config=request.custom_fields_config,
        )

        self.command_bus.dispatch(command)

        # Return the created workflow
        query = GetJobPositionWorkflowQuery(workflow_id=workflow_id)
        workflow_dto: JobPositionWorkflowDto = self.query_bus.query(query)
        if not workflow_dto:
            raise ValueError("Failed to retrieve created workflow")

        return self._dto_to_response(workflow_dto)

    def update_workflow(self, workflow_id: str, request: JobPositionWorkflowUpdate) -> JobPositionWorkflowResponse:
        """Update a job position workflow"""
        workflow_id_vo = JobPositionWorkflowId.from_string(workflow_id)

        default_view = ViewTypeEnum(request.default_view) if request.default_view else None
        status = JobPositionWorkflowStatusEnum(request.status) if request.status else None

        # Convert stages from request to WorkflowStage value objects
        stages = None
        if request.stages is not None:
            from src.job_position.domain.value_objects.workflow_stage import WorkflowStage
            from src.job_position.domain.value_objects.stage_id import StageId
            from src.job_position.domain.enums.job_position_status import JobPositionStatusEnum
            from src.job_position.domain.enums.kanban_display import KanbanDisplayEnum
            from src.company_role.domain.value_objects.company_role_id import CompanyRoleId
            
            stages = []
            for stage_data in request.stages:
                stage_id = StageId.from_string(stage_data.id)
                status_mapping = JobPositionStatusEnum(stage_data.status_mapping)
                kanban_display = KanbanDisplayEnum(stage_data.kanban_display)
                role = CompanyRoleId.from_string(stage_data.role) if stage_data.role else None
                
                # Get field_candidate_visibility, defaulting to empty dict if not provided
                field_candidate_visibility = getattr(stage_data, 'field_candidate_visibility', None)
                if field_candidate_visibility is None:
                    field_candidate_visibility = {}
                
                stage = WorkflowStage.create(
                    id=stage_id,
                    name=stage_data.name,
                    icon=stage_data.icon,
                    background_color=stage_data.background_color,
                    text_color=stage_data.text_color,
                    status_mapping=status_mapping,
                    kanban_display=kanban_display,
                    role=role,
                    field_visibility=stage_data.field_visibility,
                    field_validation=stage_data.field_validation,
                    field_candidate_visibility=field_candidate_visibility,
                )
                stages.append(stage)

        command = UpdateJobPositionWorkflowCommand(
            id=workflow_id_vo,
            name=request.name,
            default_view=default_view,
            status=status,
            stages=stages,
            custom_fields_config=request.custom_fields_config,
        )

        self.command_bus.dispatch(command)

        # Return the updated workflow
        query = GetJobPositionWorkflowQuery(workflow_id=workflow_id_vo)
        workflow_dto: JobPositionWorkflowDto = self.query_bus.query(query)
        if not workflow_dto:
            raise ValueError("Failed to retrieve updated workflow")

        return self._dto_to_response(workflow_dto)

    def get_workflow(self, workflow_id: str) -> JobPositionWorkflowResponse:
        """Get a job position workflow by ID"""
        workflow_id_vo = JobPositionWorkflowId.from_string(workflow_id)
        query = GetJobPositionWorkflowQuery(workflow_id=workflow_id_vo)
        workflow_dto: JobPositionWorkflowDto = self.query_bus.query(query)

        if not workflow_dto:
            raise ValueError(f"Workflow with id {workflow_id} not found")

        return self._dto_to_response(workflow_dto)

    def list_workflows(self, company_id: str) -> List[JobPositionWorkflowResponse]:
        """List job position workflows for a company"""
        company_id_vo = CompanyId.from_string(company_id)

        query = ListJobPositionWorkflowsQuery(
            company_id=company_id_vo,
        )
        workflow_dtos: List[JobPositionWorkflowDto] = self.query_bus.query(query)

        return [self._dto_to_response(dto) for dto in workflow_dtos]

    def initialize_default_workflows(self, company_id: str) -> List[JobPositionWorkflowResponse]:
        """
        Initialize default job position workflows for a company.
        
        This will ARCHIVE all existing workflows and create new defaults.
        """
        company_id_vo = CompanyId.from_string(company_id)

        # Archive all existing workflows for this company
        query = ListJobPositionWorkflowsQuery(company_id=company_id_vo)
        existing_workflows: List[JobPositionWorkflowDto] = self.query_bus.query(query)
        
        if existing_workflows:
            logger.info(f"Archiving {len(existing_workflows)} existing workflows for company {company_id}")
            for workflow_dto in existing_workflows:
                # Only archive if not already deprecated
                if workflow_dto.status != JobPositionWorkflowStatusEnum.DEPRECATED.value:
                    update_command = UpdateJobPositionWorkflowCommand(
                        id=JobPositionWorkflowId.from_string(workflow_dto.id),
                        name=workflow_dto.name,
                        default_view=ViewTypeEnum(workflow_dto.default_view),
                        status=JobPositionWorkflowStatusEnum.DEPRECATED,
                        stages=None,  # Keep existing stages
                        custom_fields_config=None  # Keep existing config
                    )
                    self.command_bus.dispatch(update_command)

        # Create default workflows
        created_workflows = []

        # 1. Standard Hiring Workflow - Comprehensive hiring process
        workflow1_id = JobPositionWorkflowId.generate()
        stages1 = [
            WorkflowStage.create(
                id=StageId.generate(),
                name="Borrador",
                icon="📝",
                background_color="#E5E7EB",
                text_color="#374151",
                status_mapping=JobPositionStatusEnum.DRAFT,
                kanban_display=KanbanDisplayEnum.VERTICAL,
            ),
            WorkflowStage.create(
                id=StageId.generate(),
                name="Publicada",
                icon="🌐",
                background_color="#10B981",
                text_color="#FFFFFF",
                status_mapping=JobPositionStatusEnum.ACTIVE,
                kanban_display=KanbanDisplayEnum.VERTICAL,
            ),
            WorkflowStage.create(
                id=StageId.generate(),
                name="En Revisión",
                icon="🔍",
                background_color="#3B82F6",
                text_color="#FFFFFF",
                status_mapping=JobPositionStatusEnum.ACTIVE,
                kanban_display=KanbanDisplayEnum.VERTICAL,
            ),
            WorkflowStage.create(
                id=StageId.generate(),
                name="Pausada",
                icon="⏸️",
                background_color="#F59E0B",
                text_color="#FFFFFF",
                status_mapping=JobPositionStatusEnum.PAUSED,
                kanban_display=KanbanDisplayEnum.HORIZONTAL_BOTTOM,
            ),
            WorkflowStage.create(
                id=StageId.generate(),
                name="Cerrada",
                icon="🔒",
                background_color="#6B7280",
                text_color="#FFFFFF",
                status_mapping=JobPositionStatusEnum.CLOSED,
                kanban_display=KanbanDisplayEnum.HORIZONTAL_BOTTOM,
            ),
        ]

        command1 = CreateJobPositionWorkflowCommand(
            id=workflow1_id,
            company_id=company_id_vo,
            name="Proceso de Contratación Estándar",
            default_view=ViewTypeEnum.KANBAN,
            status=JobPositionWorkflowStatusEnum.PUBLISHED,  # Default workflows are published
            stages=stages1,
            custom_fields_config={},
        )
        self.command_bus.dispatch(command1)

        # Get and add to results
        query1 = GetJobPositionWorkflowQuery(workflow_id=workflow1_id)
        workflow_dto1: Optional[JobPositionWorkflowDto] = self.query_bus.query(query1)
        if workflow_dto1:
            created_workflows.append(self._dto_to_response(workflow_dto1))

        # 2. Simple Workflow - For quick job postings
        workflow2_id = JobPositionWorkflowId.generate()
        stages2 = [
            WorkflowStage.create(
                id=StageId.generate(),
                name="Borrador",
                icon="📝",
                background_color="#E5E7EB",
                text_color="#374151",
                status_mapping=JobPositionStatusEnum.DRAFT,
                kanban_display=KanbanDisplayEnum.VERTICAL,
            ),
            WorkflowStage.create(
                id=StageId.generate(),
                name="Activa",
                icon="✅",
                background_color="#10B981",
                text_color="#FFFFFF",
                status_mapping=JobPositionStatusEnum.ACTIVE,
                kanban_display=KanbanDisplayEnum.VERTICAL,
            ),
            WorkflowStage.create(
                id=StageId.generate(),
                name="Cerrada",
                icon="🔒",
                background_color="#6B7280",
                text_color="#FFFFFF",
                status_mapping=JobPositionStatusEnum.CLOSED,
                kanban_display=KanbanDisplayEnum.VERTICAL,
            ),
        ]

        command2 = CreateJobPositionWorkflowCommand(
            id=workflow2_id,
            company_id=company_id_vo,
            name="Flujo Simplificado",
            default_view=ViewTypeEnum.LIST,
            status=JobPositionWorkflowStatusEnum.PUBLISHED,  # Default workflows are published
            stages=stages2,
            custom_fields_config={},
        )
        self.command_bus.dispatch(command2)

        # Get and add to results
        query2 = GetJobPositionWorkflowQuery(workflow_id=workflow2_id)
        workflow_dto2: Optional[JobPositionWorkflowDto] = self.query_bus.query(query2)
        if workflow_dto2:
            created_workflows.append(self._dto_to_response(workflow_dto2))

        # 3. General Workflow - For approval process
        workflow3_id = JobPositionWorkflowId.generate()
        stages3 = [
            WorkflowStage.create(
                id=StageId.generate(),
                name="Borrador",
                icon="📝",
                background_color="#E5E7EB",
                text_color="#374151",
                status_mapping=JobPositionStatusEnum.DRAFT,
                kanban_display=KanbanDisplayEnum.VERTICAL,
            ),
            WorkflowStage.create(
                id=StageId.generate(),
                name="Pendiente de Aprobación",
                icon="⏳",
                background_color="#F59E0B",
                text_color="#FFFFFF",
                status_mapping=JobPositionStatusEnum.DRAFT,
                kanban_display=KanbanDisplayEnum.VERTICAL,
            ),
            WorkflowStage.create(
                id=StageId.generate(),
                name="Publicado",
                icon="🚀",
                background_color="#3B82F6",
                text_color="#FFFFFF",
                status_mapping=JobPositionStatusEnum.ACTIVE,
                kanban_display=KanbanDisplayEnum.VERTICAL,
            ),
            WorkflowStage.create(
                id=StageId.generate(),
                name="Descartado",
                icon="🗑️",
                background_color="#EF4444",
                text_color="#FFFFFF",
                status_mapping=JobPositionStatusEnum.CLOSED,
                kanban_display=KanbanDisplayEnum.HORIZONTAL_BOTTOM,
            ),
        ]

        command3 = CreateJobPositionWorkflowCommand(
            id=workflow3_id,
            company_id=company_id_vo,
            name="General",
            default_view=ViewTypeEnum.KANBAN,
            status=JobPositionWorkflowStatusEnum.PUBLISHED,  # Default workflows are published
            stages=stages3,
            custom_fields_config={},
        )
        self.command_bus.dispatch(command3)

        # Get and add to results
        query3 = GetJobPositionWorkflowQuery(workflow_id=workflow3_id)
        workflow_dto3: Optional[JobPositionWorkflowDto] = self.query_bus.query(query3)
        if workflow_dto3:
            created_workflows.append(self._dto_to_response(workflow_dto3))

        logger.info(f"Created {len(created_workflows)} default workflows for company {company_id}")
        return created_workflows

    def move_position_to_stage(self, position_id: str, request: MoveJobPositionToStageRequest) -> dict:
        """
        Move a job position to a new stage.
        
        Raises:
            JobPositionValidationError: If custom fields validation fails
        """
        position_id_vo = JobPositionId.from_string(position_id)
        stage_id_vo = StageId.from_string(request.stage_id)

        command = MoveJobPositionToStageCommand(
            id=position_id_vo,
            stage_id=stage_id_vo,
            comment=request.comment,
        )

        # This will raise JobPositionValidationError if validation fails
        self.command_bus.dispatch(command)

        return {"success": True, "message": "Job position moved to new stage", "position_id": position_id}

    def update_custom_fields(self, position_id: str, request: UpdateJobPositionCustomFieldsRequest) -> dict:
        """Update custom fields values for a job position"""
        position_id_vo = JobPositionId.from_string(position_id)

        command = UpdateJobPositionCustomFieldsCommand(
            id=position_id_vo,
            custom_fields_values=request.custom_fields_values,
        )

        self.command_bus.dispatch(command)

        return {"success": True, "message": "Custom fields updated", "position_id": position_id}

    def _dto_to_response(self, dto: JobPositionWorkflowDto) -> JobPositionWorkflowResponse:
        """Convert workflow DTO to response schema"""
        from adapters.http.admin.schemas.job_position_workflow import WorkflowStageResponse

        stages = [
            WorkflowStageResponse(
                id=stage.id,
                name=stage.name,
                icon=stage.icon,
                background_color=stage.background_color,
                text_color=stage.text_color,
                role=stage.role,
                status_mapping=stage.status_mapping,
                kanban_display=stage.kanban_display,
                field_visibility=stage.field_visibility,
                field_validation=stage.field_validation,
                field_candidate_visibility=stage.field_candidate_visibility,
            )
            for stage in dto.stages
        ]

        return JobPositionWorkflowResponse(
            id=dto.id,
            company_id=dto.company_id,
            name=dto.name,
            default_view=dto.default_view,
            status=dto.status,
            stages=stages,
            custom_fields_config=dto.custom_fields_config,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )

