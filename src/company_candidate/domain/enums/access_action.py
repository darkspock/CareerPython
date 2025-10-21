from enum import Enum


class AccessAction(str, Enum):
    """Actions that can be logged when accessing candidate data"""
    VIEW_PROFILE = "view_profile"
    VIEW_EDUCATION = "view_education"
    VIEW_EXPERIENCE = "view_experience"
    VIEW_PROJECTS = "view_projects"
    ADD_COMMENT = "add_comment"
    UPDATE_TAGS = "update_tags"
    UPDATE_NOTES = "update_notes"
    CHANGE_STAGE = "change_stage"
