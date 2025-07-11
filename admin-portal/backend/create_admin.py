import os
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal, engine
from app.models.user import User
from app.models.base import Base
from app.core.security import get_password_hash

def create_admin():
    """Create admin user if it doesn't exist"""
    
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Get admin credentials from environment or use defaults
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin24@H2")
        admin_email = os.getenv("ADMIN_EMAIL", "admin@literature-db.com")
        
        # Check if admin already exists (case-insensitive)
        admin = db.query(User).filter(
            func.lower(User.username) == admin_username.lower()
        ).first()
        
        if admin:
            print("✅ Admin user already exists")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   Role: {admin.role}")
            
            # Update role if needed
            if admin.role != "main_coordinator":
                admin.role = "main_coordinator"
                db.commit()
                print("   ✅ Updated role to main_coordinator")
            
            return
        
        # Also check by email
        admin_by_email = db.query(User).filter(
            func.lower(User.email) == admin_email.lower()
        ).first()
        
        if admin_by_email:
            print("✅ Admin user already exists (found by email)")
            print(f"   Username: {admin_by_email.username}")
            print(f"   Email: {admin_by_email.email}")
            print(f"   Role: {admin_by_email.role}")
            
            # Update role if needed
            if admin_by_email.role != "main_coordinator":
                admin_by_email.role = "main_coordinator"
                db.commit()
                print("   ✅ Updated role to main_coordinator")
            
            return
        
        # Create admin user
        admin_user = User(
            username=admin_username,
            email=admin_email,
            full_name="Main Administrator",
            hashed_password=get_password_hash(admin_password),
            role="main_coordinator",
            is_active=True,
            institution="Literature Review Database",
            department="Administration"
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("🎉 Admin user created successfully!")
        print(f"   Username: {admin_username}")
        print(f"   Email: {admin_email}")
        print(f"   Role: {admin_user.role}")
        print("")
        print("⚠️  IMPORTANT: Change the default password after first login!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        
        # Try to provide more helpful information
        try:
            # Check what users exist
            existing_users = db.query(User.username, User.email, User.role).all()
            print("\n📋 Existing users in database:")
            for user in existing_users[:5]:  # Show first 5 users
                print(f"   - Username: {user.username}, Email: {user.email}, Role: {user.role}")
            if len(existing_users) > 5:
                print(f"   ... and {len(existing_users) - 5} more users")
        except:
            pass
        
        # Don't fail the build if admin creation fails
        print("\n⚠️  Continuing with deployment...")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
