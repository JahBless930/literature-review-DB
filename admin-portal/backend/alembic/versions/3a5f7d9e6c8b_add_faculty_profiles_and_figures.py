"""Add faculty profiles and figures tables

Revision ID: 3a5f7d9e6c8b
Revises: 8f7e9d2c4b5a
Create Date: 2024-01-XX

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '3a5f7d9e6c8b'
down_revision = '8f7e9d2c4b5a'
branch_labels = None
depends_on = None

def upgrade():
    # Add profile fields to users table
    op.add_column('users', sa.Column('about', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('disciplines', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('research_interests', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('office_location', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('office_hours', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('profile_picture_filename', sa.String(), nullable=True))
    op.add_column('users', sa.Column('profile_picture_size', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('profile_picture_data', sa.LargeBinary(), nullable=True))
    op.add_column('users', sa.Column('profile_picture_content_type', sa.String(), nullable=True))
    op.add_column('users', sa.Column('is_profile_public', sa.Boolean(), server_default='true'))
    op.add_column('users', sa.Column('profile_slug', sa.String(), nullable=True))
    
    # Create unique index for profile_slug
    op.create_index('ix_users_profile_slug', 'users', ['profile_slug'], unique=True)
    
    # Add supervisor_id to projects table
    op.add_column('projects', sa.Column('supervisor_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_projects_supervisor', 'projects', 'users', ['supervisor_id'], ['id'])
    
    # Create project_figures table
    op.create_table('project_figures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.Column('order_index', sa.Integer(), default=0),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('data', sa.LargeBinary(), nullable=False),
        sa.Column('content_type', sa.String(), nullable=False),
        sa.Column('width', sa.Integer(), nullable=True),
        sa.Column('height', sa.Integer(), nullable=True),
        sa.Column('uploaded_by_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['uploaded_by_id'], ['users.id'])
    )
    
    op.create_index('ix_project_figures_project_id', 'project_figures', ['project_id'])

def downgrade():
    op.drop_index('ix_project_figures_project_id', 'project_figures')
    op.drop_table('project_figures')
    
    op.drop_constraint('fk_projects_supervisor', 'projects', type_='foreignkey')
    op.drop_column('projects', 'supervisor_id')
    
    op.drop_index('ix_users_profile_slug', 'users')
    op.drop_column('users', 'profile_slug')
    op.drop_column('users', 'is_profile_public')
    op.drop_column('users', 'profile_picture_content_type')
    op.drop_column('users', 'profile_picture_data')
    op.drop_column('users', 'profile_picture_size')
    op.drop_column('users', 'profile_picture_filename')
    op.drop_column('users', 'office_hours')
    op.drop_column('users', 'office_location')
    op.drop_column('users', 'research_interests')
    op.drop_column('users', 'disciplines')
    op.drop_column('users', 'about')
