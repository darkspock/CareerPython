from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.resume.domain.entities.resume import Resume
from src.resume.domain.repositories.resume_repository_interface import ResumeRepositoryInterface
from src.resume.domain.value_objects.resume_id import ResumeId
from src.shared.application.command_bus import Command, CommandHandler


class SectionAction(Enum):
    """Actions that can be performed on sections"""
    ADD = "add"
    UPDATE = "update"
    REMOVE = "remove"
    REORDER = "reorder"


@dataclass
class ManageVariableSectionCommand(Command):
    """Command to manage variable sections (add, update, remove, reorder)"""
    resume_id: ResumeId
    action: SectionAction
    # For add/update actions
    section_key: Optional[str] = None
    section_title: Optional[str] = None
    section_content: Optional[str] = None
    section_order: Optional[int] = None
    # For reorder action
    sections_order: Optional[list[dict]] = None  # [{"key": "experience", "order": 1}, ...]


class ManageVariableSectionCommandHandler(CommandHandler[ManageVariableSectionCommand]):
    """Handler for managing variable sections"""

    def __init__(self, resume_repository: ResumeRepositoryInterface):
        self.resume_repository = resume_repository

    def execute(self, command: ManageVariableSectionCommand) -> None:
        """Handle variable section management"""

        # 1. Get resume
        resume = self.resume_repository.get_by_id(command.resume_id)
        if not resume:
            raise ValueError(f"Resume with id {command.resume_id.value} not found")

        # 2. Check if resume can be edited
        if not resume.can_be_edited():
            raise ValueError(f"Resume cannot be edited in status {resume.status.value}")

        # 3. Execute action
        if command.action == SectionAction.ADD:
            self._add_section(resume, command)
        elif command.action == SectionAction.UPDATE:
            self._update_section(resume, command)
        elif command.action == SectionAction.REMOVE:
            self._remove_section(resume, command)
        elif command.action == SectionAction.REORDER:
            self._reorder_sections(resume, command)
        else:
            raise ValueError(f"Unknown action: {command.action}")

        # 4. Save changes
        self.resume_repository.update(resume)

    def _add_section(self, resume: Resume, command: ManageVariableSectionCommand) -> None:
        """Add a new variable section"""
        if not command.section_key or not command.section_title:
            raise ValueError("Section key and title are required for add action")

        # Check if section already exists
        if resume.get_variable_section(command.section_key):
            raise ValueError(f"Section with key '{command.section_key}' already exists")

        # Determine order (if not provided, append at the end)
        order = command.section_order
        if order is None:
            max_order = max([s.order for s in resume.content.variable_sections], default=0)
            order = max_order + 1

        resume.add_variable_section(
            key=command.section_key,
            title=command.section_title,
            content=command.section_content or "",
            order=order
        )

    def _update_section(self, resume: Resume, command: ManageVariableSectionCommand) -> None:
        """Update existing variable section"""
        if not command.section_key:
            raise ValueError("Section key is required for update action")

        # Check if section exists
        section = resume.get_variable_section(command.section_key)
        if not section:
            raise ValueError(f"Section with key '{command.section_key}' not found")

        # Update content and/or title
        resume.update_variable_section(
            key=command.section_key,
            content=command.section_content if command.section_content is not None else section.content,
            title=command.section_title if command.section_title is not None else section.title
        )

        # Update order if provided
        if command.section_order is not None:
            section.order = command.section_order
            # Re-sort sections
            resume.content.variable_sections.sort(key=lambda s: s.order)

    def _remove_section(self, resume: Resume, command: ManageVariableSectionCommand) -> None:
        """Remove a variable section"""
        if not command.section_key:
            raise ValueError("Section key is required for remove action")

        success = resume.remove_variable_section(command.section_key)
        if not success:
            raise ValueError(f"Section with key '{command.section_key}' not found")

    def _reorder_sections(self, resume: Resume, command: ManageVariableSectionCommand) -> None:
        """Reorder variable sections"""
        if not command.sections_order:
            raise ValueError("Sections order is required for reorder action")

        # Create a mapping of key to new order
        order_map = {item['key']: item['order'] for item in command.sections_order}

        # Update order for each section
        for section in resume.content.variable_sections:
            if section.key in order_map:
                section.order = order_map[section.key]

        # Sort sections by new order
        resume.content.variable_sections.sort(key=lambda s: s.order)


# Convenience command classes for specific actions
@dataclass
class AddVariableSectionCommand(Command):
    """Command to add a new variable section"""
    resume_id: ResumeId
    section_key: str
    section_title: str
    section_content: str = ""
    section_order: Optional[int] = None


@dataclass
class UpdateVariableSectionCommand(Command):
    """Command to update a variable section"""
    resume_id: ResumeId
    section_key: str
    section_content: Optional[str] = None
    section_title: Optional[str] = None
    section_order: Optional[int] = None


@dataclass
class RemoveVariableSectionCommand(Command):
    """Command to remove a variable section"""
    resume_id: ResumeId
    section_key: str


@dataclass
class ReorderVariableSectionsCommand(Command):
    """Command to reorder variable sections"""
    resume_id: ResumeId
    sections_order: list[dict]  # [{"key": "experience", "order": 1}, ...]


# Convenience handlers that delegate to the main handler
class AddVariableSectionCommandHandler(CommandHandler[AddVariableSectionCommand]):
    def __init__(self, resume_repository: ResumeRepositoryInterface):
        self.main_handler = ManageVariableSectionCommandHandler(resume_repository)

    def execute(self, command: AddVariableSectionCommand) -> None:
        main_command = ManageVariableSectionCommand(
            resume_id=command.resume_id,
            action=SectionAction.ADD,
            section_key=command.section_key,
            section_title=command.section_title,
            section_content=command.section_content,
            section_order=command.section_order
        )
        self.main_handler.execute(main_command)


class UpdateVariableSectionCommandHandler(CommandHandler[UpdateVariableSectionCommand]):
    def __init__(self, resume_repository: ResumeRepositoryInterface):
        self.main_handler = ManageVariableSectionCommandHandler(resume_repository)

    def execute(self, command: UpdateVariableSectionCommand) -> None:
        main_command = ManageVariableSectionCommand(
            resume_id=command.resume_id,
            action=SectionAction.UPDATE,
            section_key=command.section_key,
            section_title=command.section_title,
            section_content=command.section_content,
            section_order=command.section_order
        )
        self.main_handler.execute(main_command)


class RemoveVariableSectionCommandHandler(CommandHandler[RemoveVariableSectionCommand]):
    def __init__(self, resume_repository: ResumeRepositoryInterface):
        self.main_handler = ManageVariableSectionCommandHandler(resume_repository)

    def execute(self, command: RemoveVariableSectionCommand) -> None:
        main_command = ManageVariableSectionCommand(
            resume_id=command.resume_id,
            action=SectionAction.REMOVE,
            section_key=command.section_key
        )
        self.main_handler.execute(main_command)


class ReorderVariableSectionsCommandHandler(CommandHandler[ReorderVariableSectionsCommand]):
    def __init__(self, resume_repository: ResumeRepositoryInterface):
        self.main_handler = ManageVariableSectionCommandHandler(resume_repository)

    def execute(self, command: ReorderVariableSectionsCommand) -> None:
        main_command = ManageVariableSectionCommand(
            resume_id=command.resume_id,
            action=SectionAction.REORDER,
            sections_order=command.sections_order
        )
        self.main_handler.execute(main_command)
