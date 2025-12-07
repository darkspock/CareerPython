"""add application questions tables

Revision ID: c3d4e5f6a7b8
Revises: bdc7f8f711e4
Create Date: 2025-12-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'bdc7f8f711e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create application_questions table
    op.create_table(
        'application_questions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workflow_id', sa.String(), nullable=False),
        sa.Column('company_id', sa.String(), nullable=False),
        sa.Column('field_key', sa.String(100), nullable=False),
        sa.Column('label', sa.String(500), nullable=False),
        sa.Column('description', sa.String(1000), nullable=True),
        sa.Column('field_type', sa.String(20), nullable=False),
        sa.Column('options', sa.JSON(), nullable=True),
        sa.Column('is_required_default', sa.Boolean(), nullable=False, default=False),
        sa.Column('validation_rules', sa.JSON(), nullable=True),
        sa.Column('sort_order', sa.Integer(), nullable=False, default=0),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflows.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_application_questions_id', 'application_questions', ['id'])
    op.create_index('ix_application_questions_workflow_id', 'application_questions', ['workflow_id'])
    op.create_index('ix_application_questions_company_id', 'application_questions', ['company_id'])
    op.create_index('ix_application_questions_is_active', 'application_questions', ['is_active'])
    # Unique constraint on workflow_id + field_key
    op.create_unique_constraint(
        'uq_workflow_field_key',
        'application_questions',
        ['workflow_id', 'field_key']
    )

    # Create position_question_configs table
    op.create_table(
        'position_question_configs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('position_id', sa.String(), nullable=False),
        sa.Column('question_id', sa.String(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_required_override', sa.Boolean(), nullable=True),
        sa.Column('sort_order_override', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['position_id'], ['job_positions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_id'], ['application_questions.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('position_id', 'question_id', name='uq_position_question'),
    )
    op.create_index('ix_position_question_configs_id', 'position_question_configs', ['id'])
    op.create_index('ix_position_question_configs_position_id', 'position_question_configs', ['position_id'])
    op.create_index('ix_position_question_configs_question_id', 'position_question_configs', ['question_id'])


def downgrade() -> None:
    # Drop position_question_configs table
    op.drop_index('ix_position_question_configs_question_id', table_name='position_question_configs')
    op.drop_index('ix_position_question_configs_position_id', table_name='position_question_configs')
    op.drop_index('ix_position_question_configs_id', table_name='position_question_configs')
    op.drop_table('position_question_configs')

    # Drop application_questions table
    op.drop_constraint('uq_workflow_field_key', 'application_questions', type_='unique')
    op.drop_index('ix_application_questions_is_active', table_name='application_questions')
    op.drop_index('ix_application_questions_company_id', table_name='application_questions')
    op.drop_index('ix_application_questions_workflow_id', table_name='application_questions')
    op.drop_index('ix_application_questions_id', table_name='application_questions')
    op.drop_table('application_questions')
