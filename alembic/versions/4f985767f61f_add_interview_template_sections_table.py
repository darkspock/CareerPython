"""Add interview template sections table

Revision ID: 4f985767f61f
Revises: 1041d31a8631
Create Date: 2025-09-27 17:16:19.824705

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f985767f61f'
down_revision: Union[str, Sequence[str], None] = '1041d31a8631'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step 1: Create the interview_template_sections table
    op.create_table('interview_template_sections',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('interview_template_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('intro', sa.Text(), nullable=True),
        sa.Column('prompt', sa.Text(), nullable=True),
        sa.Column('goal', sa.Text(), nullable=True),
        sa.Column('section', sa.Enum('EXPERIENCE', 'EDUCATION', 'PROJECT', 'SOFT_SKILL', 'GENERAL', name='interviewtemplatesectionenum'), nullable=True),
        sa.ForeignKeyConstraint(['interview_template_id'], ['interview_templates.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_interview_template_sections_id', 'interview_template_sections', ['id'])
    op.create_index('ix_interview_template_sections_interview_template_id', 'interview_template_sections', ['interview_template_id'])
    op.create_index('ix_interview_template_sections_section', 'interview_template_sections', ['section'])

    # Step 2: Add interview_template_section_id column to questions table (nullable for now)
    op.add_column('interview_template_questions', sa.Column('interview_template_section_id', sa.String(), nullable=True))
    op.create_index('ix_interview_template_questions_interview_template_section_id', 'interview_template_questions', ['interview_template_section_id'])

    # Step 3: Create default sections for existing templates and migrate questions
    connection = op.get_bind()

    # Create default sections for each existing template
    connection.execute(sa.text("""
        INSERT INTO interview_template_sections (id, interview_template_id, name, intro, prompt, goal, section)
        SELECT
            gen_random_uuid()::text as id,
            id as interview_template_id,
            'Default Section' as name,
            intro,
            prompt,
            goal,
            section::text::interviewtemplatesectionenum
        FROM interview_templates
    """))

    # Update questions to reference the new sections
    connection.execute(sa.text("""
        UPDATE interview_template_questions
        SET interview_template_section_id = (
            SELECT s.id
            FROM interview_template_sections s
            WHERE s.interview_template_id = interview_template_questions.interview_template_id
            LIMIT 1
        )
    """))

    # Step 4: Make section_id non-nullable and finalize the migration
    op.alter_column('interview_template_questions', 'interview_template_section_id', nullable=False)

    # Add foreign key constraint
    op.create_foreign_key('fk_questions_section', 'interview_template_questions', 'interview_template_sections', ['interview_template_section_id'], ['id'])

    # Remove old foreign key and column
    op.drop_constraint('interview_template_questions_interview_template_id_fkey', 'interview_template_questions', type_='foreignkey')
    op.drop_column('interview_template_questions', 'interview_template_id')


def downgrade() -> None:
    """Downgrade schema."""
    # Re-add the old column
    op.add_column('interview_template_questions', sa.Column('interview_template_id', sa.String(), nullable=True))

    # Restore the old foreign key relationship
    connection = op.get_bind()
    connection.execute(sa.text("""
        UPDATE interview_template_questions
        SET interview_template_id = (
            SELECT s.interview_template_id
            FROM interview_template_sections s
            WHERE s.id = interview_template_questions.interview_template_section_id
        )
    """))

    op.alter_column('interview_template_questions', 'interview_template_id', nullable=False)
    op.create_foreign_key('interview_template_questions_interview_template_id_fkey', 'interview_template_questions', 'interview_templates', ['interview_template_id'], ['id'])

    # Remove new relationships and columns
    op.drop_constraint('fk_questions_section', 'interview_template_questions', type_='foreignkey')
    op.drop_index('ix_interview_template_questions_interview_template_section_id')
    op.drop_column('interview_template_questions', 'interview_template_section_id')

    # Drop the sections table
    op.drop_index('ix_interview_template_sections_section')
    op.drop_index('ix_interview_template_sections_interview_template_id')
    op.drop_index('ix_interview_template_sections_id')
    op.drop_table('interview_template_sections')
