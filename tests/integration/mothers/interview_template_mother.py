"""
InterviewTemplate Object Mother for tests
"""
from typing import Optional
import factory
from faker import Faker

from src.shared.domain.enums.job_category import JobCategoryEnum
from src.interview.interview_template.domain.enums import InterviewTemplateStatusEnum, InterviewTemplateTypeEnum
from src.interview.interview_template.infrastructure.models.interview_template import InterviewTemplateModel
from tests.integration.mothers.base_mother import BaseMother

fake = Faker()


class InterviewTemplateMother(BaseMother):
    """Object Mother for InterviewTemplate test data"""

    def build(self, **kwargs) -> InterviewTemplateModel:
        """Build InterviewTemplate model with fake data"""
        defaults = {
            'name': kwargs.get('name', fake.sentence(nb_words=3)),
            'intro': kwargs.get('intro', fake.paragraph()),
            'prompt': kwargs.get('prompt', fake.text()),
            'goal': kwargs.get('goal', fake.sentence()),
            'status': kwargs.get('status', InterviewTemplateStatusEnum.ENABLED),
            'type': kwargs.get('type', InterviewTemplateTypeEnum.EXTENDED_PROFILE),
            'job_category': kwargs.get('job_category', fake.random_element(list(JobCategoryEnum))),
            'created_by': kwargs.get('created_by', fake.email()),
            'tags': kwargs.get('tags', [fake.word() for _ in range(2)]),
            'template_metadata': kwargs.get('template_metadata', {'test': True})
        }

        return InterviewTemplateModel(**defaults)

    @classmethod
    def create_enabled(cls, database, **kwargs) -> InterviewTemplateModel:
        """Create an enabled interview template"""
        mother = cls(database)
        return mother.create_in_db(status=InterviewTemplateStatusEnum.ENABLED, **kwargs)

    @classmethod
    def create_draft(cls, database, **kwargs) -> InterviewTemplateModel:
        """Create a draft interview template"""
        mother = cls(database)
        return mother.create_in_db(status=InterviewTemplateStatusEnum.DRAFT, **kwargs)

    @classmethod
    def create_disabled(cls, database, **kwargs) -> InterviewTemplateModel:
        """Create a disabled interview template"""
        mother = cls(database)
        return mother.create_in_db(status=InterviewTemplateStatusEnum.DISABLED, **kwargs)

    @classmethod
    def create_for_job_category(cls, database, job_category: JobCategoryEnum, **kwargs) -> InterviewTemplateModel:
        """Create template for specific job category"""
        mother = cls(database)
        return mother.create_in_db(job_category=job_category, **kwargs)