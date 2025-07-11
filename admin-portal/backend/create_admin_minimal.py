import os
from sqlalchemy import create_engine, Column, String, Boolean, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.security import get_password_hash
from app.core.config import settings

Base = declarative_base()

class UserMinimal(Base):
    """Minimal User model just for admin creation"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    institution = Column(String(255))
    department = Column(String(255))
    role = Column(String(50), default="faculty")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

def create_admin():
    """Create admin user if it doesn't exist"""
    
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(UserMinimal).filter(UserMinimal.username == "admin").first()
        if admin:
            print("✅ Admin user already exists")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   Role: {admin.role}")
            return
        
        # Get admin credentials from environment or use defaults
        admin_username = os.getenv("ADMIN_USERNAME", "admin")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin24@H2")
        admin_email = os.getenv("ADMIN_EMAIL", "admin@literature-db.com")
        
        # Create admin user
        admin_user = UserMinimal(
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
        
        print("🎉 Admin user created successfully!")
        print(f"   Username: {admin_username}")
        print(f"   Email: {admin_email}")
        print(f"   Role: main_coordinator")
        print("")
        print("⚠️  IMPORTANT: Change the default password after first login!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        print("⚠️  Continuing with deployment...")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
