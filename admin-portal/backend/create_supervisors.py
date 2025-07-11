import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.user import User
from app.models.base import Base
from app.core.security import get_password_hash
from app.core.constants import SUPERVISORS, get_institution_by_id
import re

def create_slug(name: str) -> str:
    """Create a URL-friendly slug from name"""
    slug = re.sub(r'[^\w\s-]', '', name.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def create_supervisors():
    """Create supervisor accounts if they don't exist"""
    
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    created_count = 0
    existing_count = 0
    
    try:
        # Get default password from environment or use default
        default_password = os.getenv("SUPERVISOR_DEFAULT_PASSWORD", "faculty2024@UHAS")
        
        print("🔄 Creating supervisor accounts...")
        print(f"   Default password: {default_password}")
        print("")
        
        for supervisor in SUPERVISORS:
            # Skip the "others" option
            if supervisor["id"] == "others":
                continue
            
            # Check if user already exists by email
            existing_user = db.query(User).filter(
                User.email == supervisor["email"]
            ).first()
            
            if existing_user:
                existing_count += 1
                print(f"✓ Supervisor already exists: {supervisor['name']}")
                
                # Update profile slug if missing
                if not existing_user.profile_slug:
                    base_slug = create_slug(existing_user.full_name)
                    slug = base_slug
                    counter = 1
                    while db.query(User).filter(User.profile_slug == slug).first():
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    existing_user.profile_slug = slug
                    db.commit()
                    print(f"  → Added profile slug: {slug}")
                
                continue
            
            # Extract username from email
            username = supervisor["email"].split("@")[0]
            
            # Check if username already exists
            if db.query(User).filter(User.username == username).first():
                # Add number suffix if username exists
                counter = 1
                while db.query(User).filter(User.username == f"{username}{counter}").first():
                    counter += 1
                username = f"{username}{counter}"
            
            # Create profile slug
            base_slug = create_slug(supervisor["name"])
            slug = base_slug
            counter = 1
            while db.query(User).filter(User.profile_slug == slug).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Create supervisor user
            supervisor_user = User(
                username=username,
                email=supervisor["email"],
                full_name=supervisor["name"],
                hashed_password=get_password_hash(default_password),
                role="faculty",
                is_active=True,
                institution=supervisor["institution"],
                department=supervisor["institution"],  # Using institution as department for now
                profile_slug=slug,
                is_profile_public=True
            )
            
            db.add(supervisor_user)
            db.commit()
            db.refresh(supervisor_user)
            
            created_count += 1
            print(f"✅ Created supervisor: {supervisor['name']}")
            print(f"   Username: {username}")
            print(f"   Email: {supervisor['email']}")
            print(f"   Institution: {supervisor['institution']}")
            print(f"   Profile URL: /supervisors/{slug}")
            print("")
        
        print("=" * 50)
        print(f"🎉 Supervisor creation completed!")
        print(f"   Created: {created_count} new supervisors")
        print(f"   Existing: {existing_count} supervisors")
        print(f"   Total: {created_count + existing_count} supervisors")
        print("")
        print("⚠️  IMPORTANT: All new supervisors have the default password.")
        print("   They should change it after first login!")
        
    except Exception as e:
        print(f"❌ Error creating supervisors: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_supervisors()
