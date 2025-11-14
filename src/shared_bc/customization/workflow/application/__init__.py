"""Workflow application module - exports queries and commands"""

# Queries - Workflow
from .queries.workflow.get_workflow_by_id import GetWorkflowByIdQuery, GetWorkflowByIdQueryHandler
from .queries.workflow.list_workflows_by_company import (
    ListWorkflowsByCompanyQuery,
    ListWorkflowsByCompanyQueryHandler,
)
from .queries.workflow.list_workflows_by_phase import (
    ListWorkflowsByPhaseQuery,
    ListWorkflowsByPhaseQueryHandler,
)

# Queries - Stage
from .queries.stage.get_final_stages import GetFinalStagesQuery, GetFinalStagesQueryHandler
from .queries.stage.get_initial_stage import GetInitialStageQuery, GetInitialStageQueryHandler
from .queries.stage.get_stage_by_id import GetStageByIdQuery, GetStageByIdQueryHandler
from .queries.stage.list_stages_by_phase import (
    ListStagesByPhaseQuery,
    ListStagesByPhaseQueryHandler,
)
from .queries.stage.list_stages_by_workflow import (
    ListStagesByWorkflowQuery,
    ListStagesByWorkflowQueryHandler,
)

# Commands - Workflow
from .commands.workflow.activate_workflow_command import (
    ActivateWorkflowCommand,
    ActivateWorkflowCommandHandler,
)
from .commands.workflow.archive_workflow_command import (
    ArchiveWorkflowCommand,
    ArchiveWorkflowCommandHandler,
)
from .commands.workflow.create_workflow_command import (
    CreateWorkflowCommand,
    CreateWorkflowCommandHandler,
)
from .commands.workflow.deactivate_workflow_command import (
    DeactivateWorkflowCommand,
    DeactivateWorkflowCommandHandler,
)
from .commands.workflow.delete_workflow_command import (
    DeleteWorkflowCommand,
    DeleteWorkflowCommandHandler,
)
from .commands.workflow.set_as_default_workflow_command import (
    SetAsDefaultWorkflowCommand,
    SetAsDefaultWorkflowCommandHandler,
)
from .commands.workflow.unset_as_default_workflow_command import (
    UnsetAsDefaultWorkflowCommand,
    UnsetAsDefaultWorkflowCommandHandler,
)
from .commands.workflow.update_workflow_command import (
    UpdateWorkflowCommand,
    UpdateWorkflowCommandHandler,
)

# Commands - Stage
from .commands.stage.activate_stage_command import (
    ActivateStageCommand,
    ActivateStageCommandHandler,
)
from .commands.stage.create_stage_command import CreateStageCommand, CreateStageCommandHandler
from .commands.stage.deactivate_stage_command import (
    DeactivateStageCommand,
    DeactivateStageCommandHandler,
)
from .commands.stage.delete_stage_command import DeleteStageCommand, DeleteStageCommandHandler
from .commands.stage.reorder_stages_command import (
    ReorderStagesCommand,
    ReorderStagesCommandHandler,
)
from .commands.stage.update_stage_command import UpdateStageCommand, UpdateStageCommandHandler

__all__ = [
    # Queries - Workflow
    "GetWorkflowByIdQuery",
    "GetWorkflowByIdQueryHandler",
    "ListWorkflowsByCompanyQuery",
    "ListWorkflowsByCompanyQueryHandler",
    "ListWorkflowsByPhaseQuery",
    "ListWorkflowsByPhaseQueryHandler",
    # Queries - Stage
    "GetFinalStagesQuery",
    "GetFinalStagesQueryHandler",
    "GetInitialStageQuery",
    "GetInitialStageQueryHandler",
    "GetStageByIdQuery",
    "GetStageByIdQueryHandler",
    "ListStagesByPhaseQuery",
    "ListStagesByPhaseQueryHandler",
    "ListStagesByWorkflowQuery",
    "ListStagesByWorkflowQueryHandler",
    # Commands - Workflow
    "ActivateWorkflowCommand",
    "ActivateWorkflowCommandHandler",
    "ArchiveWorkflowCommand",
    "ArchiveWorkflowCommandHandler",
    "CreateWorkflowCommand",
    "CreateWorkflowCommandHandler",
    "DeactivateWorkflowCommand",
    "DeactivateWorkflowCommandHandler",
    "DeleteWorkflowCommand",
    "DeleteWorkflowCommandHandler",
    "SetAsDefaultWorkflowCommand",
    "SetAsDefaultWorkflowCommandHandler",
    "UnsetAsDefaultWorkflowCommand",
    "UnsetAsDefaultWorkflowCommandHandler",
    "UpdateWorkflowCommand",
    "UpdateWorkflowCommandHandler",
    # Commands - Stage
    "ActivateStageCommand",
    "ActivateStageCommandHandler",
    "CreateStageCommand",
    "CreateStageCommandHandler",
    "DeactivateStageCommand",
    "DeactivateStageCommandHandler",
    "DeleteStageCommand",
    "DeleteStageCommandHandler",
    "ReorderStagesCommand",
    "ReorderStagesCommandHandler",
    "UpdateStageCommand",
    "UpdateStageCommandHandler",
]

