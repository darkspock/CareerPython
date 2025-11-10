from typing import Optional, List

from fastapi import HTTPException

from adapters.http.admin.schemas.interview_template import InterviewTemplateResponse, InterviewTemplateCreate
from adapters.http.admin.schemas.interview_template import (
    InterviewTemplateSectionCreate, InterviewTemplateSectionUpdate, InterviewTemplateQuestionCreate,
    InterviewTemplateQuestionUpdate, InterviewTemplateQuestionResponse
)
from src.company_bc.company.domain.value_objects import CompanyId
from src.interview.interview_template.application.commands import CreateInterviewTemplateCommand
from src.interview.interview_template.application.commands.create_interview_template_question import \
    CreateInterviewTemplateQuestionCommand
from src.interview.interview_template.application.commands.create_interview_template_section import \
    CreateInterviewTemplateSectionCommand
from src.interview.interview_template.application.commands.delete_interview_template_question import \
    DeleteInterviewTemplateQuestionCommand
from src.interview.interview_template.application.commands.disable_interview_template import \
    DisableInterviewTemplateCommand
from src.interview.interview_template.application.commands.disable_interview_template_question import \
    DisableInterviewTemplateQuestionCommand
from src.interview.interview_template.application.commands.disable_interview_template_section import \
    DisableInterviewTemplateSectionCommand
from src.interview.interview_template.application.commands.enable_interview_template import \
    EnableInterviewTemplateCommand
from src.interview.interview_template.application.commands.enable_interview_template_question import \
    EnableInterviewTemplateQuestionCommand
from src.interview.interview_template.application.commands.enable_interview_template_section import \
    EnableInterviewTemplateSectionCommand
from src.interview.interview_template.application.commands.update_interview_template import \
    UpdateInterviewTemplateCommand
from src.interview.interview_template.application.commands.update_interview_template_question import \
    UpdateInterviewTemplateQuestionCommand
from src.interview.interview_template.application.commands.update_interview_template_section import \
    UpdateInterviewTemplateSectionCommand
from src.interview.interview_template.application.queries import ListInterviewTemplatesQuery
from src.interview.interview_template.application.queries.dtos.interview_template_full_dto import \
    InterviewTemplateQuestionDto, InterviewTemplateFullDto
from src.interview.interview_template.application.queries.dtos.interview_template_list_dto import \
    InterviewTemplateListDto
from src.interview.interview_template.application.queries.get_interview_template_full_by_id import \
    GetInterviewTemplateFullByIdQuery
from src.interview.interview_template.domain.enums import InterviewTemplateTypeEnum, InterviewTemplateStatusEnum, \
    InterviewTemplateSectionEnum, InterviewTemplateQuestionScopeEnum, InterviewTemplateQuestionDataTypeEnum
from src.interview.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.framework.domain.enums.job_category import JobCategoryEnum


class InterviewTemplateController:
    def __init__(self, query_bus: QueryBus, command_bus: CommandBus):
        self.query_bus = query_bus
        self.command_bus = command_bus

    def list_interview_templates(
            self,
            search_term: Optional[str] = None,
            type: Optional[str] = None,
            status: Optional[str] = None,
            job_category: Optional[str] = None,
            section: Optional[str] = None,
            page: Optional[int] = None,
            page_size: Optional[int] = None
    ) -> List[InterviewTemplateResponse]:
        # Convert string parameters to enums
        type_enum = None
        if type:
            try:
                type_enum = InterviewTemplateTypeEnum(type)
            except ValueError:
                pass

        status_enum = None
        if status:
            try:
                status_enum = InterviewTemplateStatusEnum(status)
            except ValueError:
                pass

        job_category_enum = None
        if job_category:
            try:
                job_category_enum = JobCategoryEnum(job_category)
            except ValueError:
                pass

        section_enum = None
        if section:
            try:
                section_enum = InterviewTemplateSectionEnum(section)
            except ValueError:
                pass

        query = ListInterviewTemplatesQuery(
            search_term=search_term,
            type=type_enum,
            status=status_enum,
            job_category=job_category_enum,
            section=section_enum,
            page=page,
            page_size=page_size
        )
        templates_dto: List[InterviewTemplateListDto] = self.query_bus.query(query)
        return [InterviewTemplateResponse.from_list_dto(dto) for dto in templates_dto]

    def create_interview_template(self,
                                  template_data: InterviewTemplateCreate,
                                  current_admin_id: str) -> InterviewTemplateResponse:
        # Generate ID before creating the command
        template_id = InterviewTemplateId.generate()

        command = CreateInterviewTemplateCommand(
            id=template_id,
            company_id=None,  # Set to None for now - can be enhanced later
            name=template_data.name,
            intro=template_data.intro,
            prompt=template_data.prompt,
            goal=template_data.goal,
            template_type=template_data.type,
            job_category=template_data.job_category,
            allow_ai_questions=template_data.allow_ai_questions or False,
            legal_notice=template_data.legal_notice,
            created_by=current_admin_id,
            tags=template_data.tags,
            template_metadata=template_data.template_metadata
        )

        # Execute command (no return value)
        self.command_bus.dispatch(command)

        # Handle sections if provided during creation
        if template_data.sections is not None:
            for section_data in template_data.sections:
                # Create new section
                section_create_command = CreateInterviewTemplateSectionCommand(
                    id=InterviewTemplateSectionId.generate(),
                    company_id=None,
                    interview_template_id=template_id,
                    name=section_data.get('name', ''),
                    intro=section_data.get('intro', ''),
                    prompt=section_data.get('prompt', ''),
                    goal=section_data.get('goal', ''),
                    section=InterviewTemplateSectionEnum(
                        section_data['section']) if section_data.get('section') else None,
                    allow_ai_questions=section_data.get('allow_ai_questions', False),
                    allow_ai_override_questions=section_data.get('allow_ai_override_questions', False),
                    legal_notice=section_data.get('legal_notice'),
                    created_by=current_admin_id
                )
                self.command_bus.dispatch(section_create_command)

        # Query the created entity with sections
        query = GetInterviewTemplateFullByIdQuery(template_id)
        template_dto: Optional[InterviewTemplateFullDto] = self.query_bus.query(query)

        if template_dto is None:
            raise Exception(f"Failed to retrieve created interview template with id {template_id}")

        return InterviewTemplateResponse.from_full_dto(template_dto)

    def get_interview_template(
            self,
            template_id: str,
    ) -> InterviewTemplateResponse:
        """
        Get a specific interview template by ID with sections
        """
        query = GetInterviewTemplateFullByIdQuery(id=InterviewTemplateId.from_string(template_id))
        template_dto: Optional[InterviewTemplateFullDto] = self.query_bus.query(query)

        if not template_dto:
            raise HTTPException(status_code=404, detail="Interview template not found")
        return InterviewTemplateResponse.from_full_dto(template_dto)

    def update_interview_template(
            self,
            template_id: str,
            template_data: InterviewTemplateCreate,
            current_admin_id: str
    ) -> InterviewTemplateResponse:
        """
        Update an existing interview template and its sections
        """
        # Update the main template
        command = UpdateInterviewTemplateCommand(
            template_id=InterviewTemplateId.from_string(template_id),
            name=template_data.name,
            intro=template_data.intro,
            prompt=template_data.prompt,
            goal=template_data.goal,
            type=template_data.type,
            job_category=template_data.job_category,
            section=template_data.section,
            allow_ai_questions=template_data.allow_ai_questions,
            legal_notice=template_data.legal_notice,
            tags=template_data.tags,
            template_metadata=template_data.template_metadata
        )
        self.command_bus.dispatch(command)

        # Handle sections if provided
        if template_data.sections is not None:
            # For now, we'll just create/update sections as they come
            # This is a simplified implementation - in a real system you'd want to handle
            # updates, deletes, and proper synchronization
            for section_data in template_data.sections:
                if 'id' in section_data and not section_data['id'].startswith('temp-'):
                    # Update existing section
                    section_update_command = UpdateInterviewTemplateSectionCommand(
                        section_id=InterviewTemplateSectionId.from_string(section_data['id']),
                        name=section_data.get('name', ''),
                        intro=section_data.get('intro', ''),
                        prompt=section_data.get('prompt', ''),
                        goal=section_data.get('goal', ''),
                        section=InterviewTemplateSectionEnum(
                            section_data['section']) if section_data.get('section') else None,
                        allow_ai_questions=section_data.get('allow_ai_questions'),
                        allow_ai_override_questions=section_data.get('allow_ai_override_questions'),
                        legal_notice=section_data.get('legal_notice'),
                        updated_by=current_admin_id
                    )
                    self.command_bus.dispatch(section_update_command)
                else:
                    # Create new section
                    section_create_command = CreateInterviewTemplateSectionCommand(
                        id=InterviewTemplateSectionId.generate(),
                        company_id=None,
                        interview_template_id=InterviewTemplateId.from_string(template_id),
                        name=section_data.get('name', ''),
                        intro=section_data.get('intro', ''),
                        prompt=section_data.get('prompt', ''),
                        goal=section_data.get('goal', ''),
                        section=InterviewTemplateSectionEnum(
                            section_data['section']) if section_data.get('section') else None,
                        allow_ai_questions=section_data.get('allow_ai_questions', False),
                        allow_ai_override_questions=section_data.get('allow_ai_override_questions', False),
                        legal_notice=section_data.get('legal_notice'),
                        created_by=current_admin_id
                    )
                    self.command_bus.dispatch(section_create_command)

        # Return the full template with sections
        query = GetInterviewTemplateFullByIdQuery(id=InterviewTemplateId.from_string(template_id))
        template_dto: Optional[InterviewTemplateFullDto] = self.query_bus.query(query)
        if not template_dto:
            raise HTTPException(status_code=404, detail="Interview template not found after update")
        return InterviewTemplateResponse.from_full_dto(template_dto)

    def enable_interview_template(
            self,
            template_id: str,
            current_admin_id: str,
            enable_reason: Optional[str] = None
    ) -> dict:
        """
        Enable an interview template
        """
        command = EnableInterviewTemplateCommand(
            template_id=InterviewTemplateId.from_string(template_id),
            enabled_by=current_admin_id,
            enable_reason=enable_reason
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template enabled successfully"}

    def disable_interview_template(
            self,
            template_id: str,
            current_admin_id: str,
            disable_reason: Optional[str] = None,
            force_disable: bool = False
    ) -> dict:
        """
        Disable an interview template
        """
        command = DisableInterviewTemplateCommand(
            template_id=InterviewTemplateId.from_string(template_id),
            disabled_by=current_admin_id,
            disable_reason=disable_reason,
            force_disable=force_disable
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template disabled successfully"}

    def delete_interview_template(
            self,
            template_id: str,
            current_admin_id: str,
            delete_reason: Optional[str] = None,
            force_delete: bool = False
    ) -> dict:
        """
        Delete an interview template (only if disabled)
        """
        from src.interview.interview_template.application.commands.delete_interview_template import \
            DeleteInterviewTemplateCommand

        command = DeleteInterviewTemplateCommand(
            template_id=InterviewTemplateId.from_string(template_id),
            deleted_by=current_admin_id,
            delete_reason=delete_reason,
            force_delete=force_delete
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template deleted successfully"}

    # Interview Template Section Methods
    def create_interview_template_section(
            self,
            section_data: InterviewTemplateSectionCreate,
            current_admin_id: str
    ) -> dict:
        """
        Create a new interview template section
        """
        section_id = InterviewTemplateSectionId.generate()

        command = CreateInterviewTemplateSectionCommand(
            id=section_id,
            company_id=CompanyId.from_string(section_data.company_id) if section_data.company_id else None,
            interview_template_id=InterviewTemplateId.from_string(section_data.interview_template_id),
            section=section_data.section,
            name=section_data.name,
            intro=section_data.intro,
            prompt=section_data.prompt,
            goal=section_data.goal,
            sort_order=getattr(section_data, 'sort_order', 0),
            allow_ai_questions=getattr(section_data, 'allow_ai_questions', False),
            allow_ai_override_questions=getattr(section_data, 'allow_ai_override_questions', False),
            legal_notice=getattr(section_data, 'legal_notice', None),
            created_by=current_admin_id
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template section created successfully", "id": str(section_id)}

    def update_interview_template_section(
            self,
            section_id: str,
            section_data: InterviewTemplateSectionUpdate,
            current_admin_id: str
    ) -> dict:
        """
        Update an interview template section
        """
        command = UpdateInterviewTemplateSectionCommand(
            section_id=InterviewTemplateSectionId.from_string(section_id),
            name=section_data.name,
            intro=section_data.intro,
            prompt=section_data.prompt,
            goal=section_data.goal,
            section=section_data.section,
            allow_ai_questions=getattr(section_data, 'allow_ai_questions', None),
            allow_ai_override_questions=getattr(section_data, 'allow_ai_override_questions', None),
            legal_notice=getattr(section_data, 'legal_notice', None),
            updated_by=current_admin_id
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template section updated successfully"}

    def enable_interview_template_section(
            self,
            section_id: str,
            current_admin_id: str
    ) -> dict:
        """
        Enable an interview template section
        """
        command = EnableInterviewTemplateSectionCommand(
            section_id=InterviewTemplateSectionId.from_string(section_id),
            enabled_by=current_admin_id
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template section enabled successfully"}

    def disable_interview_template_section(
            self,
            section_id: str,
            current_admin_id: str
    ) -> dict:
        """
        Disable an interview template section
        """
        command = DisableInterviewTemplateSectionCommand(
            section_id=InterviewTemplateSectionId.from_string(section_id),
            disabled_by=current_admin_id
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template section disabled successfully"}

    def delete_interview_template_section(
            self,
            section_id: str,
            current_admin_id: str
    ) -> dict:
        """
        Delete an interview template section (only if disabled)
        """
        from src.interview.interview_template.application.commands.delete_interview_template_section import \
            DeleteInterviewTemplateSectionCommand

        command = DeleteInterviewTemplateSectionCommand(
            section_id=InterviewTemplateSectionId.from_string(section_id),
            deleted_by=current_admin_id
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template section deleted successfully"}

    def move_section_up(
            self,
            section_id: str,
            current_admin_id: str
    ) -> dict:
        """
        Move a section up in the order
        """
        from src.interview.interview_template.application.commands.move_section_up import MoveSectionUpCommand

        command = MoveSectionUpCommand(
            section_id=InterviewTemplateSectionId.from_string(section_id),
            moved_by=current_admin_id
        )
        self.command_bus.dispatch(command)
        return {"message": "Section moved up successfully"}

    def move_section_down(
            self,
            section_id: str,
            current_admin_id: str
    ) -> dict:
        """
        Move a section down in the order
        """
        from src.interview.interview_template.application.commands.move_section_down import MoveSectionDownCommand

        command = MoveSectionDownCommand(
            section_id=InterviewTemplateSectionId.from_string(section_id),
            moved_by=current_admin_id
        )
        self.command_bus.dispatch(command)
        return {"message": "Section moved down successfully"}

    def get_questions_by_section(self, section_id: str) -> List[InterviewTemplateQuestionResponse]:
        """
        Get all questions for a specific section
        """
        from src.interview.interview_template.application.queries.get_questions_by_section import \
            GetQuestionsBySectionQuery

        query = GetQuestionsBySectionQuery(
            section_id=InterviewTemplateSectionId.from_string(section_id)
        )
        questions_dtos: List[InterviewTemplateQuestionDto] = self.query_bus.query(query)

        # Convert DTOs to response format using Pydantic schema
        return [
            InterviewTemplateQuestionResponse(
                id=dto.id.value,
                name=dto.name,
                description=dto.description,
                code=dto.code,
                sort_order=dto.sort_order,
                interview_template_section_id=dto.interview_template_section_id.value,
                scope=dto.scope.value if dto.scope else "",
                data_type=dto.data_type.value if dto.data_type else "",
                status=dto.status.value if dto.status else "",
                allow_ai_followup=dto.allow_ai_followup,
                legal_notice=dto.legal_notice
            )
            for dto in questions_dtos
        ]

    # Interview Template Question Methods
    def create_interview_template_question(
            self,
            question_data: InterviewTemplateQuestionCreate
    ) -> dict:
        """
        Create a new interview template question
        """
        question_id = InterviewTemplateQuestionId.generate()

        command = CreateInterviewTemplateQuestionCommand(
            id=question_id,
            interview_template_section_id=InterviewTemplateSectionId.from_string(
                question_data.interview_template_section_id),
            scope=InterviewTemplateQuestionScopeEnum(question_data.scope),
            sort_order=question_data.sort_order,
            name=question_data.name,
            description=question_data.description,
            code=question_data.code,
            data_type=InterviewTemplateQuestionDataTypeEnum(question_data.data_type),
            allow_ai_followup=getattr(question_data, 'allow_ai_followup', False),
            legal_notice=getattr(question_data, 'legal_notice', None)
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template question created successfully", "id": str(question_id)}

    def update_interview_template_question(
            self,
            question_id: str,
            question_data: InterviewTemplateQuestionUpdate,
            current_admin_id: str
    ) -> dict:
        """
        Update an interview template question
        """
        command = UpdateInterviewTemplateQuestionCommand(
            question_id=InterviewTemplateQuestionId.from_string(question_id),
            interview_template_section_id=InterviewTemplateSectionId.from_string(
                question_data.interview_template_section_id),
            scope=InterviewTemplateQuestionScopeEnum(question_data.scope),
            sort_order=question_data.sort_order,
            name=question_data.name,
            description=question_data.description,
            code=question_data.code,
            data_type=InterviewTemplateQuestionDataTypeEnum(question_data.data_type),
            allow_ai_followup=getattr(question_data, 'allow_ai_followup', None),
            legal_notice=getattr(question_data, 'legal_notice', None),
            updated_by=current_admin_id
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template question updated successfully"}

    def enable_interview_template_question(
            self,
            question_id: str,
            current_admin_id: str
    ) -> dict:
        """
        Enable an interview template question
        """
        command = EnableInterviewTemplateQuestionCommand(
            question_id=InterviewTemplateQuestionId.from_string(question_id),
            enabled_by=current_admin_id
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template question enabled successfully"}

    def disable_interview_template_question(
            self,
            question_id: str,
            current_admin_id: str
    ) -> dict:
        """
        Disable an interview template question
        """
        command = DisableInterviewTemplateQuestionCommand(
            question_id=InterviewTemplateQuestionId.from_string(question_id),
            disabled_by=current_admin_id
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template question disabled successfully"}

    def delete_interview_template_question(
            self,
            question_id: str,
            current_admin_id: str
    ) -> dict:
        """
        Delete an interview template question
        """

        command = DeleteInterviewTemplateQuestionCommand(
            question_id=InterviewTemplateQuestionId.from_string(question_id),
            deleted_by=current_admin_id
        )
        self.command_bus.dispatch(command)
        return {"message": "Interview template question deleted successfully"}
