"""Add course tables

Revision ID: d6776bae9ccb
Revises: 937f76ad8c2d
Create Date: 2025-09-01 21:36:29.551759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6776bae9ccb'
down_revision: Union[str, Sequence[str], None] = '937f76ad8c2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 创建课程表
    op.create_table('courses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.Enum('BASIC', 'SEASONAL', 'DIET', 'MASSAGE', 'HERB', 'DISEASE_FOCUSED', 'COMPREHENSIVE', name='coursecategory'), nullable=False),
        sa.Column('duration', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('is_free', sa.Boolean(), nullable=True, default=False),
        sa.Column('is_published', sa.Boolean(), nullable=True, default=False),
        sa.Column('instructor', sa.String(), nullable=True),
        sa.Column('total_lessons', sa.Integer(), nullable=True, default=0),
        sa.Column('total_duration', sa.Integer(), nullable=True, default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)
    
    # 创建课程内容表
    op.create_table('lessons',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('video_url', sa.String(), nullable=True),
        sa.Column('video_id', sa.String(), nullable=True),
        sa.Column('file_id', sa.String(), nullable=True),
        sa.Column('cover_url', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('PROCESSING', 'READY', 'ERROR', name='videostatus'), nullable=True, default='PROCESSING'),
        sa.Column('is_free', sa.Boolean(), nullable=True, default=False),
        sa.Column('transcript', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lessons_id'), 'lessons', ['id'], unique=False)
    
    # 创建课程注册表
    op.create_table('enrollments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('progress', sa.Float(), nullable=True, default=0.0),
        sa.Column('completed_lessons', sa.Integer(), nullable=True, default=0),
        sa.Column('total_watch_time', sa.Integer(), nullable=True, default=0),
        sa.Column('last_watched_lesson_id', sa.Integer(), nullable=True),
        sa.Column('enrolled_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.ForeignKeyConstraint(['last_watched_lesson_id'], ['lessons.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_enrollments_id'), 'enrollments', ['id'], unique=False)
    
    # 创建观看记录表
    op.create_table('watch_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('lesson_id', sa.Integer(), nullable=False),
        sa.Column('watch_time', sa.Integer(), nullable=True, default=0),
        sa.Column('last_position', sa.Integer(), nullable=True, default=0),
        sa.Column('is_completed', sa.Boolean(), nullable=True, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_watch_records_id'), 'watch_records', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # 删除表（按依赖关系逆序）
    op.drop_index(op.f('ix_watch_records_id'), table_name='watch_records')
    op.drop_table('watch_records')
    
    op.drop_index(op.f('ix_enrollments_id'), table_name='enrollments')
    op.drop_table('enrollments')
    
    op.drop_index(op.f('ix_lessons_id'), table_name='lessons')
    op.drop_table('lessons')
    
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_table('courses')
