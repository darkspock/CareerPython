"""Resume application module - exports queries and commands"""

# Commands
from .commands.analyze_pdf_resume_command import (
    AnalyzePDFResumeCommand,
    AnalyzePDFResumeCommandHandler,
)
from .commands.create_general_resume_command import (
    CreateGeneralResumeCommand,
    CreateGeneralResumeCommandHandler,
)
from .commands.delete_resume_command import DeleteResumeCommand, DeleteResumeCommandHandler
from .commands.manage_variable_section_command import (
    ManageVariableSectionCommand,
    ManageVariableSectionCommandHandler,
    AddVariableSectionCommand,
    AddVariableSectionCommandHandler,
    UpdateVariableSectionCommand,
    UpdateVariableSectionCommandHandler,
    RemoveVariableSectionCommand,
    RemoveVariableSectionCommandHandler,
    ReorderVariableSectionsCommand,
    ReorderVariableSectionsCommandHandler,
)
from .commands.update_resume_content_command import (
    UpdateResumeContentCommand,
    UpdateResumeContentCommandHandler,
)
# Queries
from .queries.get_pdf_analysis_results_query import (
    GetPDFAnalysisResultsQuery,
    GetPDFAnalysisResultsQueryHandler,
)
from .queries.get_pdf_analysis_status_query import (
    GetPDFAnalysisStatusQuery,
    GetPDFAnalysisStatusQueryHandler,
    GetPDFAnalysisStatusByAssetQuery,
    GetPDFAnalysisStatusByAssetQueryHandler,
)
from .queries.get_resume_by_id_query import GetResumeByIdQuery, GetResumeByIdQueryHandler
from .queries.get_resume_statistics_query import (
    GetResumeStatisticsQuery,
    GetResumeStatisticsQueryHandler,
)
from .queries.get_resumes_by_candidate_query import (
    GetResumesByCandidateQuery,
    GetResumesByCandidateQueryHandler,
)

__all__ = [
    # Queries
    "GetPDFAnalysisResultsQuery",
    "GetPDFAnalysisResultsQueryHandler",
    "GetPDFAnalysisStatusQuery",
    "GetPDFAnalysisStatusQueryHandler",
    "GetPDFAnalysisStatusByAssetQuery",
    "GetPDFAnalysisStatusByAssetQueryHandler",
    "GetResumeByIdQuery",
    "GetResumeByIdQueryHandler",
    "GetResumeStatisticsQuery",
    "GetResumeStatisticsQueryHandler",
    "GetResumesByCandidateQuery",
    "GetResumesByCandidateQueryHandler",
    # Commands
    "AnalyzePDFResumeCommand",
    "AnalyzePDFResumeCommandHandler",
    "CreateGeneralResumeCommand",
    "CreateGeneralResumeCommandHandler",
    "DeleteResumeCommand",
    "DeleteResumeCommandHandler",
    "ManageVariableSectionCommand",
    "ManageVariableSectionCommandHandler",
    "AddVariableSectionCommand",
    "AddVariableSectionCommandHandler",
    "UpdateVariableSectionCommand",
    "UpdateVariableSectionCommandHandler",
    "RemoveVariableSectionCommand",
    "RemoveVariableSectionCommandHandler",
    "ReorderVariableSectionsCommand",
    "ReorderVariableSectionsCommandHandler",
    "UpdateResumeContentCommand",
    "UpdateResumeContentCommandHandler",
]
