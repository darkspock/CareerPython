#!/usr/bin/env python3
"""
Fixture script to delete all interview templates and create a comprehensive discovery template
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import settings
from src.interview.interview_template.infrastructure.models.interview_template import InterviewTemplateModel
from src.interview.interview_template.infrastructure.models.interview_template_section import InterviewTemplateSectionModel
from src.interview.interview_template.infrastructure.models.interview_template_question import InterviewTemplateQuestionModel
from src.interview.interview_template.domain.enums import (
    InterviewTemplateTypeEnum,
    InterviewTemplateStatusEnum,
    InterviewTemplateSectionEnum
)
from src.interview.interview_template.domain.enums.interview_template_section import InterviewTemplateSectionStatusEnum
from src.interview.interview_template.domain.enums.interview_template_question import (
    InterviewTemplateQuestionStatusEnum,
    InterviewTemplateQuestionDataTypeEnum,
    InterviewTemplateQuestionScopeEnum
)
from src.framework.domain.entities.base import generate_id


def delete_all_templates(session):
    """Delete all existing interview templates"""
    try:
        # Get all templates
        templates = session.query(InterviewTemplateModel).all()
        template_count = len(templates)

        if template_count == 0:
            print("ℹ️  No existing templates to delete")
            return 0

        # Delete in proper order: questions -> sections -> templates
        print(f"🗑️  Found {template_count} templates to delete...")

        for template in templates:
            # Delete questions first
            for section in template.sections:
                question_count = len(section.questions)
                if question_count > 0:
                    for question in section.questions:
                        session.delete(question)
                    print(f"    - Deleted {question_count} questions from section '{section.name}'")

            # Delete sections
            section_count = len(template.sections)
            if section_count > 0:
                for section in template.sections:
                    session.delete(section)
                print(f"    - Deleted {section_count} sections from template '{template.name}'")

            # Delete template
            session.delete(template)
            print(f"  ✓ Deleted template: {template.name}")

        session.commit()
        print(f"🗑️  Successfully deleted {template_count} templates")
        return template_count
    except Exception as e:
        session.rollback()
        print(f"❌ Error deleting templates: {e}")
        raise


def create_discovery_template(session, admin_id: str):
    """Create a comprehensive profile discovery interview template"""

    # Create the main template
    template = InterviewTemplateModel(
        id=generate_id(),
        name="Comprehensive Profile Discovery Interview",
        intro="""Welcome to your profile discovery interview. This interview is designed to uncover valuable information
that might not be obvious from your resume. We'll explore your experiences, education, projects, and soft skills
in depth to build a complete picture of your professional profile.""",
        prompt="""This interview aims to discover hidden details and context about the candidate's professional background.
Focus on extracting specific examples, measurable achievements, and contextual information that adds depth to their resume.
Pay attention to skills used, challenges overcome, and impact created.""",
        goal="""To gather comprehensive information about the candidate's professional journey that goes beyond what's
written in their resume, including specific achievements, technical skills, soft skills, and career motivations.""",
        type=InterviewTemplateTypeEnum.EXTENDED_PROFILE,
        status=InterviewTemplateStatusEnum.ENABLED,
        job_category=None,  # Generic template for all categories
        allow_ai_questions=True,
        legal_notice="""The information you provide will be used to enhance your professional profile.
All data will be handled in accordance with our privacy policy and data protection regulations.""",
        created_by=admin_id,
        tags=["discovery", "profile", "comprehensive", "generic"]
    )

    session.add(template)
    session.flush()

    print(f"✅ Created template: {template.name}")

    # Section 1: Experience Discovery
    experience_section = InterviewTemplateSectionModel(
        id=generate_id(),
        interview_template_id=template.id,
        name="Professional Experience Discovery",
        intro="Let's dive deep into your professional experiences and uncover the details that make your work unique.",
        prompt="Focus on extracting specific technical skills, methodologies used, team dynamics, and measurable outcomes.",
        goal="Discover hidden technical skills, leadership experiences, and quantifiable achievements from work history.",
        section=InterviewTemplateSectionEnum.EXPERIENCE,
        sort_order=1,
        status=InterviewTemplateSectionStatusEnum.ENABLED,
        allow_ai_questions=True,
        allow_ai_override_questions=True
    )
    session.add(experience_section)
    session.flush()

    # Experience questions
    experience_questions = [
        {
            "name": "Can you describe a specific technical challenge you faced in your most recent role and how you solved it?",
            "description": "Seeking specific problem-solving examples, technologies used, and approach taken",
            "code": "EXP_TECH_CHALLENGE",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.ITEM
        },
        {
            "name": "What tools, frameworks, or methodologies did you use regularly that might not be listed on your resume?",
            "description": "Discovering unlisted technical skills and tools",
            "code": "EXP_HIDDEN_SKILLS",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.ITEM
        },
        {
            "name": "Can you quantify the impact of your work in any of your roles? (e.g., performance improvements, cost savings, user growth)",
            "description": "Extracting measurable achievements and business impact",
            "code": "EXP_MEASURABLE_IMPACT",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.ITEM
        }
    ]

    for idx, q in enumerate(experience_questions, start=1):
        question = InterviewTemplateQuestionModel(
            id=generate_id(),
            interview_template_section_id=experience_section.id,
            sort_order=idx,
            name=q["name"],
            description=q["description"],
            status=InterviewTemplateQuestionStatusEnum.ENABLED,
            data_type=q["data_type"],
            scope=q["scope"],
            code=q["code"],
            allow_ai_followup=True
        )
        session.add(question)

    print(f"  ✅ Added section: {experience_section.name} with {len(experience_questions)} questions")

    # Section 2: Education Discovery
    education_section = InterviewTemplateSectionModel(
        id=generate_id(),
        interview_template_id=template.id,
        name="Educational Background Discovery",
        intro="Let's explore your educational journey and the skills and knowledge you gained.",
        prompt="Focus on practical skills learned, notable projects, and how education applies to their career.",
        goal="Uncover practical skills from education, academic achievements, and relevant coursework not on resume.",
        section=InterviewTemplateSectionEnum.EDUCATION,
        sort_order=2,
        status=InterviewTemplateSectionStatusEnum.ENABLED,
        allow_ai_questions=True,
        allow_ai_override_questions=True
    )
    session.add(education_section)
    session.flush()

    # Education questions
    education_questions = [
        {
            "name": "What were the most valuable skills or knowledge areas you gained from your education that you use professionally?",
            "description": "Connecting education to practical professional skills",
            "code": "EDU_PRACTICAL_SKILLS",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.ITEM
        },
        {
            "name": "Did you complete any significant academic projects, thesis, or research? Please describe.",
            "description": "Discovering academic achievements and research experience",
            "code": "EDU_PROJECTS_RESEARCH",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.ITEM
        },
        {
            "name": "Were there any specialized courses, certifications, or training programs that particularly enhanced your professional capabilities?",
            "description": "Identifying additional qualifications and specialized training",
            "code": "EDU_SPECIALIZED_TRAINING",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.ITEM
        }
    ]

    for idx, q in enumerate(education_questions, start=1):
        question = InterviewTemplateQuestionModel(
            id=generate_id(),
            interview_template_section_id=education_section.id,
            sort_order=idx,
            name=q["name"],
            description=q["description"],
            status=InterviewTemplateQuestionStatusEnum.ENABLED,
            data_type=q["data_type"],
            scope=q["scope"],
            code=q["code"],
            allow_ai_followup=True
        )
        session.add(question)

    print(f"  ✅ Added section: {education_section.name} with {len(education_questions)} questions")

    # Section 3: Projects Discovery
    projects_section = InterviewTemplateSectionModel(
        id=generate_id(),
        interview_template_id=template.id,
        name="Projects and Side Work Discovery",
        intro="Tell us about projects you've worked on - whether professional, personal, or open source.",
        prompt="Explore technical depth, problem-solving approaches, and technologies used in projects.",
        goal="Discover projects that showcase technical skills, initiative, and passion for technology.",
        section=InterviewTemplateSectionEnum.PROJECT,
        sort_order=3,
        status=InterviewTemplateSectionStatusEnum.ENABLED,
        allow_ai_questions=True,
        allow_ai_override_questions=True
    )
    session.add(projects_section)
    session.flush()

    # Project questions
    project_questions = [
        {
            "name": "Describe a project you're particularly proud of. What was your role and what technologies did you use?",
            "description": "Identifying standout projects and technical contributions",
            "code": "PRJ_PROUD_PROJECT",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.ITEM
        },
        {
            "name": "Have you contributed to any open-source projects or maintained personal coding projects? Please elaborate.",
            "description": "Discovering open source contributions and personal initiative",
            "code": "PRJ_OPENSOURCE_PERSONAL",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.ITEM
        },
        {
            "name": "What was the most technically challenging aspect of any project you've worked on, and how did you overcome it?",
            "description": "Assessing problem-solving skills and technical depth",
            "code": "PRJ_TECHNICAL_CHALLENGE",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.ITEM
        }
    ]

    for idx, q in enumerate(project_questions, start=1):
        question = InterviewTemplateQuestionModel(
            id=generate_id(),
            interview_template_section_id=projects_section.id,
            sort_order=idx,
            name=q["name"],
            description=q["description"],
            status=InterviewTemplateQuestionStatusEnum.ENABLED,
            data_type=q["data_type"],
            scope=q["scope"],
            code=q["code"],
            allow_ai_followup=True
        )
        session.add(question)

    print(f"  ✅ Added section: {projects_section.name} with {len(project_questions)} questions")

    # Section 4: Soft Skills Discovery
    soft_skills_section = InterviewTemplateSectionModel(
        id=generate_id(),
        interview_template_id=template.id,
        name="Soft Skills and Work Style Discovery",
        intro="Let's understand your work style, collaboration approach, and interpersonal skills.",
        prompt="Look for examples of leadership, teamwork, communication, and adaptability.",
        goal="Identify soft skills, leadership qualities, and cultural fit indicators.",
        section=InterviewTemplateSectionEnum.SOFT_SKILL,
        sort_order=4,
        status=InterviewTemplateSectionStatusEnum.ENABLED,
        allow_ai_questions=True,
        allow_ai_override_questions=True
    )
    session.add(soft_skills_section)
    session.flush()

    # Soft skills questions
    soft_skills_questions = [
        {
            "name": "Describe a situation where you had to lead a team or mentor others. What was your approach?",
            "description": "Assessing leadership and mentoring capabilities",
            "code": "SOFT_LEADERSHIP",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.GLOBAL
        },
        {
            "name": "Tell me about a time you had to collaborate with difficult stakeholders or team members. How did you handle it?",
            "description": "Evaluating conflict resolution and communication skills",
            "code": "SOFT_COLLABORATION",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.GLOBAL
        },
        {
            "name": "Describe how you stay current with industry trends and continue learning in your field.",
            "description": "Understanding learning mindset and professional development approach",
            "code": "SOFT_CONTINUOUS_LEARNING",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.GLOBAL
        }
    ]

    for idx, q in enumerate(soft_skills_questions, start=1):
        question = InterviewTemplateQuestionModel(
            id=generate_id(),
            interview_template_section_id=soft_skills_section.id,
            sort_order=idx,
            name=q["name"],
            description=q["description"],
            status=InterviewTemplateQuestionStatusEnum.ENABLED,
            data_type=q["data_type"],
            scope=q["scope"],
            code=q["code"],
            allow_ai_followup=True
        )
        session.add(question)

    print(f"  ✅ Added section: {soft_skills_section.name} with {len(soft_skills_questions)} questions")

    # Section 5: General Discovery
    general_section = InterviewTemplateSectionModel(
        id=generate_id(),
        interview_template_id=template.id,
        name="General Profile and Career Goals",
        intro="Finally, let's discuss your overall career journey and future aspirations.",
        prompt="Understand career motivations, goals, and what drives the candidate professionally.",
        goal="Discover career motivations, professional goals, and culture fit indicators.",
        section=InterviewTemplateSectionEnum.GENERAL,
        sort_order=5,
        status=InterviewTemplateSectionStatusEnum.ENABLED,
        allow_ai_questions=True,
        allow_ai_override_questions=True
    )
    session.add(general_section)
    session.flush()

    # General questions
    general_questions = [
        {
            "name": "What motivated your career transitions or key decisions in your professional journey?",
            "description": "Understanding career drivers and decision-making process",
            "code": "GEN_CAREER_MOTIVATION",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.GLOBAL
        },
        {
            "name": "What type of work environment and company culture brings out your best performance?",
            "description": "Assessing culture fit and work environment preferences",
            "code": "GEN_WORK_ENVIRONMENT",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.GLOBAL
        },
        {
            "name": "Where do you see your career heading in the next 3-5 years? What skills or experiences do you want to develop?",
            "description": "Understanding career goals and growth mindset",
            "code": "GEN_CAREER_GOALS",
            "data_type": InterviewTemplateQuestionDataTypeEnum.LARGE_STRING,
            "scope": InterviewTemplateQuestionScopeEnum.GLOBAL
        }
    ]

    for idx, q in enumerate(general_questions, start=1):
        question = InterviewTemplateQuestionModel(
            id=generate_id(),
            interview_template_section_id=general_section.id,
            sort_order=idx,
            name=q["name"],
            description=q["description"],
            status=InterviewTemplateQuestionStatusEnum.ENABLED,
            data_type=q["data_type"],
            scope=q["scope"],
            code=q["code"],
            allow_ai_followup=True
        )
        session.add(question)

    print(f"  ✅ Added section: {general_section.name} with {len(general_questions)} questions")

    return template


def main():
    """Main execution function"""
    print("=" * 80)
    print("Interview Template Fixture Script")
    print("=" * 80)

    # Database connection
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        # Get admin user ID
        from src.auth_bc.user.infrastructure.models.user_model import UserModel
        admin_user = session.query(UserModel).filter(UserModel.email == "admin@careerpython.com").first()
        admin_id = admin_user.id if admin_user else "system"

        # Step 1: Delete all existing templates
        print("\n📋 Step 1: Deleting existing templates...")
        deleted_count = delete_all_templates(session)

        # Step 2: Create new discovery template
        print("\n📋 Step 2: Creating comprehensive discovery template...")
        template = create_discovery_template(session, admin_id)

        # Commit all changes
        session.commit()

        print("\n" + "=" * 80)
        print("✅ SUCCESS! Interview template fixture completed")
        print("=" * 80)
        print(f"\n📊 Summary:")
        print(f"  - Deleted: {deleted_count} templates")
        print(f"  - Created: 1 new template")
        print(f"  - Template Name: {template.name}")
        print(f"  - Template ID: {template.id}")
        print(f"  - Sections: 5 (Experience, Education, Projects, Soft Skills, General)")
        print(f"  - Total Questions: 15 (3 per section)")
        print(f"\n🌐 You can now use this template in the admin panel:")
        print(f"   http://localhost:5173/admin/interview-templates")
        print()

    except Exception as e:
        session.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
