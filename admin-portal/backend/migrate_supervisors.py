"""
Script to migrate existing supervisor string data to user relationships
"""
from sqlalchemy.orm import Session
from sqlalchemy import text, inspect
from app.database import SessionLocal, engine
from app.models.project import Project
from app.models.user import User
from app.core.constants import SUPERVISORS

def check_supervisor_id_column():
    """Check if supervisor_id column exists"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('projects')]
    return 'supervisor_id' in columns

def migrate_supervisors():
    """Link existing projects to supervisor user accounts"""
    
    # First check if supervisor_id column exists
    if not check_supervisor_id_column():
        print("⚠️  supervisor_id column doesn't exist yet. Run add_missing_columns.py first.")
        return
    
    db = SessionLocal()
    
    try:
        print("🔄 Starting supervisor data migration...")
        
        # Create a mapping of supervisor names to user IDs
        supervisor_map = {}
        
        # First, build the mapping
        for supervisor_info in SUPERVISORS:
            if supervisor_info["id"] == "others":
                continue
                
            # Find user by email
            user = db.query(User).filter(
                User.email == supervisor_info["email"]
            ).first()
            
            if user:
                supervisor_map[supervisor_info["name"]] = user.id
                # Also map variations of the name
                supervisor_map[supervisor_info["name"].lower()] = user.id
                supervisor_map[supervisor_info["name"].upper()] = user.id
        
        print(f"✓ Found {len(supervisor_map)} supervisor accounts")
        
        # Get all projects with supervisor strings but no supervisor_id
        projects = db.query(Project).filter(
            Project.supervisor.isnot(None),
            Project.supervisor_id.is_(None)
        ).all()
        
        print(f"📊 Found {len(projects)} projects to migrate")
        
        migrated_count = 0
        not_found = []
        
        for project in projects:
            supervisor_name = project.supervisor.strip()
            
            # Try exact match first
            if supervisor_name in supervisor_map:
                project.supervisor_id = supervisor_map[supervisor_name]
                migrated_count += 1
                print(f"✓ Linked project '{project.title[:50]}...' to supervisor ID {project.supervisor_id}")
            else:
                # Try case-insensitive match
                found = False
                for name, user_id in supervisor_map.items():
                    if name.lower() == supervisor_name.lower():
                        project.supervisor_id = user_id
                        migrated_count += 1
                        found = True
                        print(f"✓ Linked project '{project.title[:50]}...' to supervisor ID {user_id} (case-insensitive match)")
                        break
                
                if not found:
                    not_found.append((project.id, project.title, supervisor_name))
        
        db.commit()
        
        print("\n" + "=" * 50)
        print(f"🎉 Migration completed!")
        print(f"   Migrated: {migrated_count} projects")
        print(f"   Not found: {len(not_found)} supervisors")
        
        if not_found:
            print("\n⚠️  Projects with unmatched supervisors:")
            for proj_id, title, supervisor in not_found[:10]:  # Show first 10
                print(f"   - Project {proj_id}: '{title[:40]}...' → '{supervisor}'")
            if len(not_found) > 10:
                print(f"   ... and {len(not_found) - 10} more")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    migrate_supervisors()
