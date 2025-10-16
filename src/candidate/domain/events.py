from core.event import Event


class ExperienceCreatedEvent(Event):
    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id


class ExperienceDeletedEvent(Event):
    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id


class EducationCreatedEvent(Event):
    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id


class EducationDeletedEvent(Event):
    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id


class ProjectCreatedEvent(Event):
    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id


class ProjectDeletedEvent(Event):
    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id


class CandidateCreatedEvent(Event):
    def __init__(self, candidate_id: str):
        self.candidate_id = candidate_id
