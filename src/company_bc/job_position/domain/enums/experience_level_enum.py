import enum


class ExperienceLevelEnum(str, enum.Enum):
    """Experience level required for a job position"""
    INTERNSHIP = "internship"   # Student/intern level
    ENTRY = "entry"             # Entry level / Junior
    MID = "mid"                 # Mid level
    SENIOR = "senior"           # Senior level
    LEAD = "lead"               # Lead / Principal
    EXECUTIVE = "executive"     # Director / VP / C-level
