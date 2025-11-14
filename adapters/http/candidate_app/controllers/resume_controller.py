from typing import Optional, List, Dict, Any

from fastapi import HTTPException, status

from adapters.http.candidate_app.mappers.resume_mapper import ResumeMapper
from adapters.http.candidate_app.schemas.resume_dto import ResumeDto
from adapters.http.candidate_app.schemas.resume_request import CreateGeneralResumeRequest, UpdateResumeContentRequest, \
    AddVariableSectionRequest, UpdateVariableSectionRequest, RemoveVariableSectionRequest, \
    ReorderVariableSectionsRequest
from adapters.http.candidate_app.schemas.resume_response import ResumeListResponse, ResumeResponse, \
    ResumeStatisticsResponse
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.resume.application import UpdateResumeContentCommand, GetResumeStatisticsQuery
from src.candidate_bc.resume.application.commands.create_general_resume_command import CreateGeneralResumeCommand
from src.candidate_bc.resume.application.commands.delete_resume_command import DeleteResumeCommand
from src.candidate_bc.resume.application.commands.manage_variable_section_command import (
    AddVariableSectionCommand,
    UpdateVariableSectionCommand,
    RemoveVariableSectionCommand,
    ReorderVariableSectionsCommand
)
from src.candidate_bc.resume.application.queries.get_resume_by_id_query import GetResumeByIdQuery
from src.candidate_bc.resume.application.queries.get_resumes_by_candidate_query import GetResumesByCandidateQuery
from src.candidate_bc.resume.domain.enums.resume_type import ResumeType
from src.candidate_bc.resume.domain.value_objects.resume_id import ResumeId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus


class ResumeController:
    """Controlador para operaciones de Resume"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def get_resumes(
            self,
            candidate_id: str,
            resume_type: Optional[str] = None,
            limit: Optional[int] = None
    ) -> ResumeListResponse:
        """Obtiene resumes por candidato"""
        try:
            candidate_id_vo = CandidateId.from_string(candidate_id)
            resume_type_enum = ResumeType(resume_type) if resume_type else None

            query = GetResumesByCandidateQuery(
                candidate_id=candidate_id_vo,
                resume_type=resume_type_enum,
                limit=limit
            )

            resume_dtos: List[ResumeDto] = self.query_bus.query(query)
            return ResumeMapper.dtos_to_list_response(resume_dtos)

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve resumes: {str(e)}"
            )

    def get_resume_by_id(self, resume_id: str) -> ResumeResponse:
        """Obtiene un resume por ID"""
        try:
            resume_id_vo = ResumeId.from_string(resume_id)
            query = GetResumeByIdQuery(resume_id=resume_id_vo)

            resume_dto: Optional[ResumeDto] = self.query_bus.query(query)
            if not resume_dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Resume with id {resume_id} not found"
                )

            return ResumeMapper.dto_to_response(resume_dto)

        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve resume: {str(e)}"
            )

    def create_general_resume(self, candidate_id: str, request: CreateGeneralResumeRequest) -> ResumeResponse:
        """Crea un resume general"""
        try:
            candidate_id_vo = CandidateId.from_string(candidate_id)

            command = CreateGeneralResumeCommand(
                candidate_id=candidate_id_vo,
                name=request.name,
                include_ai_enhancement=request.include_ai_enhancement,
                general_data=request.general_data
            )

            self.command_bus.dispatch(command)

            # Obtener el resume creado
            # Nota: En una implementación real, el command handler podría devolver el ID
            # Por ahora, obtenemos el último resume creado por el candidato
            query = GetResumesByCandidateQuery(
                candidate_id=candidate_id_vo,
                limit=1
            )
            resume_dtos: List[ResumeDto] = self.query_bus.query(query)

            if not resume_dtos:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Resume was created but could not be retrieved"
                )

            return ResumeMapper.dto_to_response(resume_dtos[0])

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create resume: {str(e)}"
            )

    def update_resume_content(
            self,
            resume_id: str,
            request: UpdateResumeContentRequest
    ) -> ResumeResponse:
        """Actualiza el contenido de un resume with hybrid structure support"""
        try:
            resume_id_vo = ResumeId.from_string(resume_id)

            # Prepare data for command - support both new and legacy structures
            general_data_dict = None
            if request.general_data:
                general_data_dict = {
                    'cv_title': request.general_data.cv_title,
                    'name': request.general_data.name,
                    'email': request.general_data.email,
                    'phone': request.general_data.phone
                }

            variable_sections_list = None
            if request.variable_sections:
                variable_sections_list = [
                    {
                        'key': section.key,
                        'title': section.title,
                        'content': section.content,
                        'order': section.order
                    }
                    for section in request.variable_sections
                ]

            command = UpdateResumeContentCommand(
                resume_id=resume_id_vo,
                # New hybrid structure
                general_data=general_data_dict,
                variable_sections=variable_sections_list,
                # Legacy compatibility fields
                experiencia_profesional=request.experiencia_profesional,
                educacion=request.educacion,
                proyectos=request.proyectos,
                habilidades=request.habilidades,
                datos_personales=request.datos_personales,
                # Common fields
                custom_content=request.custom_content,
                preserve_ai_content=request.preserve_ai_content
            )

            self.command_bus.dispatch(command)

            # Obtener el resume actualizado
            query = GetResumeByIdQuery(resume_id=resume_id_vo)
            resume_dto: Optional[ResumeDto] = self.query_bus.query(query)

            if not resume_dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Resume with id {resume_id} not found"
                )

            return ResumeMapper.dto_to_response(resume_dto)

        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update resume content: {str(e)}"
            )

    def delete_resume(self, resume_id: str) -> dict:
        """Elimina un resume"""
        try:
            resume_id_vo = ResumeId.from_string(resume_id)

            command = DeleteResumeCommand(resume_id=resume_id_vo)
            self.command_bus.dispatch(command)

            return {
                "id": resume_id,
                "message": "Resume deleted successfully",
                "status": "deleted"
            }

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete resume: {str(e)}"
            )

    def get_resume_statistics(self, candidate_id: str) -> ResumeStatisticsResponse:
        """Obtiene estadísticas de resumes"""
        try:
            candidate_id_vo = CandidateId.from_string(candidate_id)

            query = GetResumeStatisticsQuery(candidate_id=candidate_id_vo)
            statistics: Dict[str, Any] = self.query_bus.query(query)

            return ResumeMapper.statistics_to_response(statistics)

        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve statistics: {str(e)}"
            )

    # Variable Section Management Methods
    def add_variable_section(
            self,
            resume_id: str,
            request: AddVariableSectionRequest
    ) -> ResumeResponse:
        """Adds a new variable section to a resume"""
        try:
            resume_id_vo = ResumeId.from_string(resume_id)

            command = AddVariableSectionCommand(
                resume_id=resume_id_vo,
                section_key=request.section_key,
                section_title=request.section_title,
                section_content=request.section_content,
                section_order=request.section_order
            )

            self.command_bus.dispatch(command)

            # Get updated resume
            query = GetResumeByIdQuery(resume_id=resume_id_vo)
            resume_dto: Optional[ResumeDto] = self.query_bus.query(query)

            if not resume_dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Resume with id {resume_id} not found"
                )

            return ResumeMapper.dto_to_response(resume_dto)

        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to add variable section: {str(e)}"
            )

    def update_variable_section(
            self,
            resume_id: str,
            request: UpdateVariableSectionRequest
    ) -> ResumeResponse:
        """Updates an existing variable section"""
        try:
            resume_id_vo = ResumeId.from_string(resume_id)

            command = UpdateVariableSectionCommand(
                resume_id=resume_id_vo,
                section_key=request.section_key,
                section_content=request.section_content,
                section_title=request.section_title,
                section_order=request.section_order
            )

            self.command_bus.dispatch(command)

            # Get updated resume
            query = GetResumeByIdQuery(resume_id=resume_id_vo)
            resume_dto: Optional[ResumeDto] = self.query_bus.query(query)

            if not resume_dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Resume with id {resume_id} not found"
                )

            return ResumeMapper.dto_to_response(resume_dto)

        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update variable section: {str(e)}"
            )

    def remove_variable_section(
            self,
            resume_id: str,
            request: RemoveVariableSectionRequest
    ) -> ResumeResponse:
        """Removes a variable section from resume"""
        try:
            resume_id_vo = ResumeId.from_string(resume_id)

            command = RemoveVariableSectionCommand(
                resume_id=resume_id_vo,
                section_key=request.section_key
            )

            self.command_bus.dispatch(command)

            # Get updated resume
            query = GetResumeByIdQuery(resume_id=resume_id_vo)
            resume_dto: Optional[ResumeDto] = self.query_bus.query(query)

            if not resume_dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Resume with id {resume_id} not found"
                )

            return ResumeMapper.dto_to_response(resume_dto)

        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to remove variable section: {str(e)}"
            )

    def reorder_variable_sections(
            self,
            resume_id: str,
            request: ReorderVariableSectionsRequest
    ) -> ResumeResponse:
        """Reorders variable sections in resume"""
        try:
            resume_id_vo = ResumeId.from_string(resume_id)

            command = ReorderVariableSectionsCommand(
                resume_id=resume_id_vo,
                sections_order=request.sections_order
            )

            self.command_bus.dispatch(command)

            # Get updated resume
            query = GetResumeByIdQuery(resume_id=resume_id_vo)
            resume_dto: Optional[ResumeDto] = self.query_bus.query(query)

            if not resume_dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Resume with id {resume_id} not found"
                )

            return ResumeMapper.dto_to_response(resume_dto)

        except HTTPException:
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to reorder variable sections: {str(e)}"
            )
