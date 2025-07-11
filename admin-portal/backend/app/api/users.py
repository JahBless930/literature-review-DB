from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import io
import json
import re

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserResponse, UserProfileUpdate
from ..core.auth import get_current_active_user, require_main_coordinator
from ..core.security import get_password_hash
from ..core.config import settings

router = APIRouter()

def create_slug(text: str) -> str:
    """Create a URL-friendly slug from text"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace spaces and special characters with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    
    # Remove leading/trailing hyphens
    text = text.strip('-')
    
    return text

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    current_user: User = Depends(require_main_coordinator),
    db: Session = Depends(get_db)
):
    try:
        # Check if username already exists
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Check if email already exists
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Create new user
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=get_password_hash(user.password),
            institution=user.institution,
            department=user.department,
            phone=user.phone,
            role=user.role,
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database constraint violation. Username or email may already exist."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(require_main_coordinator),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user fields
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_main_coordinator),
    db: Session = Depends(get_db)
):
    # Prevent deleting yourself
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user"
        )

@router.patch("/{user_id}/toggle-status")
async def toggle_user_status(
    user_id: int,
    current_user: User = Depends(require_main_coordinator),
    db: Session = Depends(get_db)
):
    # Prevent deactivating yourself
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        user.is_active = not user.is_active
        db.commit()
        db.refresh(user)
        
        status_text = "activated" if user.is_active else "deactivated"
        return {
            "message": f"User {status_text} successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "is_active": user.is_active
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating user status"
        )

@router.put("/profile", response_model=UserResponse)
async def update_own_profile(
    about: Optional[str] = Form(None),
    disciplines: Optional[str] = Form(None),  # JSON string
    research_interests: Optional[str] = Form(None),
    office_location: Optional[str] = Form(None),
    office_hours: Optional[str] = Form(None),
    is_profile_public: Optional[bool] = Form(None),
    profile_picture: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    # Update profile fields
    if about is not None:
        current_user.about = about
    if disciplines is not None:
        current_user.disciplines = disciplines
    if research_interests is not None:
        current_user.research_interests = research_interests
    if office_location is not None:
        current_user.office_location = office_location
    if office_hours is not None:
        current_user.office_hours = office_hours
    if is_profile_public is not None:
        current_user.is_profile_public = is_profile_public
    
    # Generate profile slug if not exists
    if not current_user.profile_slug:
        base_slug = create_slug(current_user.full_name)
        slug = base_slug
        counter = 1
        while db.query(User).filter(User.profile_slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        current_user.profile_slug = slug
    
    # Handle profile picture upload
    if profile_picture and profile_picture.filename:
        # Validate image
        if profile_picture.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail="Invalid image type. Allowed types: JPEG, PNG, GIF, WebP"
            )
        
        # Read and store image
        image_data = await profile_picture.read()
        if len(image_data) > settings.MAX_PROFILE_PICTURE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"Profile picture too large. Max size: {settings.MAX_PROFILE_PICTURE_SIZE / 1024 / 1024}MB"
            )
        
        current_user.profile_picture_filename = profile_picture.filename
        current_user.profile_picture_size = len(image_data)
        current_user.profile_picture_data = image_data
        current_user.profile_picture_content_type = profile_picture.content_type
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/profile/picture")
async def get_profile_picture(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile picture"""
    if not current_user.profile_picture_data:
        raise HTTPException(404, "No profile picture found")
    
    return StreamingResponse(
        io.BytesIO(current_user.profile_picture_data),
        media_type=current_user.profile_picture_content_type or "image/jpeg"
    )

@router.get("/{user_id}/public-profile", response_model=UserResponse)
async def get_public_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get public profile of a faculty member"""
    user = db.query(User).filter(
        User.id == user_id,
        User.is_profile_public == True,
        User.role == "faculty"
    ).first()
    
    if not user:
        raise HTTPException(404, "Profile not found or not public")
    
    return user
