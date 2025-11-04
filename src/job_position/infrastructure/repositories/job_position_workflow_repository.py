from typing import Optional, List, Dict, Any

from core.database import DatabaseInterface
from src.job_position.domain.entities.job_position_workflow import JobPositionWorkflow
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.workflow_stage import WorkflowStage
from src.job_position.domain.value_objects.stage_id import StageId
from src.job_position.domain.enums.view_type import ViewTypeEnum
from src.job_position.domain.enums.workflow_type import WorkflowTypeEnum
from src.job_position.domain.enums.job_position_status import JobPositionStatusEnum
from src.job_position.domain.enums.kanban_display import KanbanDisplayEnum
from src.job_position.domain.infrastructure.job_position_workflow_repository_interface import JobPositionWorkflowRepositoryInterface
from src.job_position.infrastructure.models.job_position_workflow_model import JobPositionWorkflowModel
from src.company.domain.value_objects.company_id import CompanyId
from src.company_role.domain.value_objects.company_role_id import CompanyRoleId


class JobPositionWorkflowRepository(JobPositionWorkflowRepositoryInterface):
    """Repository implementation for job position workflow operations"""

    def __init__(self, database: DatabaseInterface) -> None:
        self._database = database

    def save(self, workflow: JobPositionWorkflow) -> None:
        """Save or update a workflow"""
        model = self._to_model(workflow)
        with self._database.get_session() as session:
            existing = session.query(JobPositionWorkflowModel).filter_by(id=str(workflow.id)).first()
            if existing:
                # Update existing
                self._update_model_from_entity(existing, workflow)
            else:
                # Create new
                session.add(model)
            session.commit()

    def get_by_id(self, workflow_id: JobPositionWorkflowId) -> Optional[JobPositionWorkflow]:
        """Get workflow by ID"""
        with self._database.get_session() as session:
            model = session.query(JobPositionWorkflowModel).filter_by(id=str(workflow_id)).first()
            if model:
                return self._to_domain(model)
            return None

    def get_by_company_id(self, company_id: CompanyId) -> List[JobPositionWorkflow]:
        """Get all workflows for a company"""
        with self._database.get_session() as session:
            models = session.query(JobPositionWorkflowModel).filter_by(company_id=str(company_id)).all()
            return [self._to_domain(model) for model in models]

    def get_by_company_and_type(
        self,
        company_id: CompanyId,
        workflow_type: WorkflowTypeEnum
    ) -> List[JobPositionWorkflow]:
        """Get workflows by company and type"""
        with self._database.get_session() as session:
            models = session.query(JobPositionWorkflowModel).filter_by(
                company_id=str(company_id),
                workflow_type=workflow_type.value
            ).all()
            return [self._to_domain(model) for model in models]

    def delete(self, workflow_id: JobPositionWorkflowId) -> None:
        """Delete a workflow"""
        with self._database.get_session() as session:
            session.query(JobPositionWorkflowModel).filter_by(id=str(workflow_id)).delete()
            session.commit()

    def _to_domain(self, model: JobPositionWorkflowModel) -> JobPositionWorkflow:
        """Convert model to domain entity"""
        # Deserialize stages from JSON
        stages = []
        if model.stages:
            for stage_dict in model.stages:
                stage = self._stage_from_dict(stage_dict)
                if stage:
                    stages.append(stage)

        return JobPositionWorkflow(
            id=JobPositionWorkflowId.from_string(model.id),
            company_id=CompanyId.from_string(model.company_id),
            name=model.name,
            workflow_type=WorkflowTypeEnum(model.workflow_type),
            default_view=ViewTypeEnum(model.default_view),
            stages=stages,
            custom_fields_config=model.custom_fields_config or {},
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: JobPositionWorkflow) -> JobPositionWorkflowModel:
        """Convert domain entity to model"""
        # Serialize stages to JSON
        stages_json = []
        for stage in entity.stages:
            stages_json.append(self._stage_to_dict(stage))

        return JobPositionWorkflowModel(
            id=str(entity.id),
            company_id=str(entity.company_id),
            name=entity.name,
            workflow_type=entity.workflow_type.value,
            default_view=entity.default_view.value,
            stages=stages_json,
            custom_fields_config=entity.custom_fields_config,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def _update_model_from_entity(self, model: JobPositionWorkflowModel, entity: JobPositionWorkflow) -> None:
        """Update model with entity data"""
        # Serialize stages to JSON
        stages_json = []
        for stage in entity.stages:
            stages_json.append(self._stage_to_dict(stage))

        model.name = entity.name
        model.workflow_type = entity.workflow_type.value
        model.default_view = entity.default_view.value
        model.stages = stages_json
        model.custom_fields_config = entity.custom_fields_config
        model.updated_at = entity.updated_at

    def _stage_to_dict(self, stage: WorkflowStage) -> Dict[str, Any]:
        """Convert WorkflowStage value object to dictionary for JSON serialization"""
        stage_dict = {
            "id": stage.id.value,
            "name": stage.name,
            "icon": stage.icon,
            "background_color": stage.background_color,
            "text_color": stage.text_color,
            "status_mapping": stage.status_mapping.value,
            "kanban_display": stage.kanban_display.value,
            "field_visibility": stage.field_visibility,
            "field_validation": stage.field_validation,
        }
        if stage.role:
            stage_dict["role"] = stage.role.value
        return stage_dict

    def _stage_from_dict(self, stage_dict: Dict[str, Any]) -> Optional[WorkflowStage]:
        """Convert dictionary to WorkflowStage value object from JSON deserialization"""
        try:
            stage_id = StageId.from_string(stage_dict["id"])
            status_mapping = JobPositionStatusEnum(stage_dict["status_mapping"])
            kanban_display = KanbanDisplayEnum(stage_dict["kanban_display"])
            
            role = None
            if "role" in stage_dict and stage_dict["role"]:
                role = CompanyRoleId.from_string(stage_dict["role"])

            return WorkflowStage.create(
                id=stage_id,
                name=stage_dict["name"],
                icon=stage_dict["icon"],
                background_color=stage_dict["background_color"],
                text_color=stage_dict["text_color"],
                status_mapping=status_mapping,
                kanban_display=kanban_display,
                role=role,
                field_visibility=stage_dict.get("field_visibility", {}),
                field_validation=stage_dict.get("field_validation", {}),
            )
        except (KeyError, ValueError) as e:
            # Log error and return None if stage cannot be deserialized
            # This allows the workflow to load even if one stage is invalid
            return None

