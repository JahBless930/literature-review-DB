#!/usr/bin/env python3
"""
Add missing columns to existing tables
"""
from sqlalchemy import text, inspect
from app.database import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_columns_if_not_exist():
    """Add missing columns to tables"""
    
    with engine.connect() as conn:
        inspector = inspect(engine)
        
        # Check and add columns to users table
        user_columns = [col['name'] for col in inspector.get_columns('users')]
        logger.info(f"Existing user columns: {user_columns}")
        
        user_columns_to_add = [
            ("about", "TEXT"),
            ("disciplines", "TEXT"),
            ("research_interests", "TEXT"),
            ("office_location", "VARCHAR(255)"),
            ("office_hours", "VARCHAR(255)"),
            ("profile_picture_filename", "VARCHAR"),
            ("profile_picture_size", "INTEGER"),
            ("profile_picture_data", "BYTEA"),  # PostgreSQL binary type
            ("profile_picture_content_type", "VARCHAR"),
            ("is_profile_public", "BOOLEAN DEFAULT TRUE"),
            ("profile_slug", "VARCHAR")
        ]
        
        for column_name, column_type in user_columns_to_add:
            if column_name not in user_columns:
                try:
                    conn.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"))
                    conn.commit()
                    logger.info(f"✅ Added column users.{column_name}")
                except Exception as e:
                    logger.warning(f"⚠️  Could not add users.{column_name}: {e}")
                    conn.rollback()
        
        # Check and add columns to projects table
        project_columns = [col['name'] for col in inspector.get_columns('projects')]
        logger.info(f"Existing project columns: {project_columns}")
        
        if 'supervisor_id' not in project_columns:
            try:
                conn.execute(text("ALTER TABLE projects ADD COLUMN supervisor_id INTEGER"))
                conn.commit()
                logger.info("✅ Added column projects.supervisor_id")
            except Exception as e:
                logger.warning(f"⚠️  Could not add projects.supervisor_id: {e}")
                conn.rollback()
        
        # Create project_figures table if it doesn't exist
        if 'project_figures' not in inspector.get_table_names():
            try:
                conn.execute(text("""
                    CREATE TABLE project_figures (
                        id SERIAL PRIMARY KEY,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                        title VARCHAR NOT NULL,
                        caption TEXT,
                        order_index INTEGER DEFAULT 0,
                        filename VARCHAR NOT NULL,
                        size INTEGER NOT NULL,
                        data BYTEA NOT NULL,
                        content_type VARCHAR NOT NULL,
                        width INTEGER,
                        height INTEGER,
                        uploaded_by_id INTEGER REFERENCES users(id)
                    )
                """))
                conn.commit()
                logger.info("✅ Created table project_figures")
                
                # Create index
                conn.execute(text("CREATE INDEX ix_project_figures_project_id ON project_figures(project_id)"))
                conn.commit()
                logger.info("✅ Created index on project_figures.project_id")
            except Exception as e:
                logger.warning(f"⚠️  Could not create project_figures table: {e}")
                conn.rollback()
        
        # Add unique index on profile_slug if not exists
        try:
            conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_profile_slug ON users(profile_slug)"))
            conn.commit()
            logger.info("✅ Created unique index on users.profile_slug")
        except Exception as e:
            logger.warning(f"⚠️  Could not create index on profile_slug: {e}")
            conn.rollback()
        
        # Add foreign key constraint for supervisor_id if not exists
        try:
            conn.execute(text("""
                ALTER TABLE projects 
                ADD CONSTRAINT fk_projects_supervisor 
                FOREIGN KEY (supervisor_id) 
                REFERENCES users(id)
            """))
            conn.commit()
            logger.info("✅ Added foreign key constraint for supervisor_id")
        except Exception as e:
            logger.warning(f"⚠️  Could not add foreign key constraint: {e}")
            conn.rollback()

if __name__ == "__main__":
    logger.info("🔧 Adding missing columns to database...")
    add_columns_if_not_exist()
    logger.info("✅ Database update completed!")
