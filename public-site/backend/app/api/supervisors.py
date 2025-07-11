from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Project
from app.models.user import User  # Import from admin models

router = APIRouter()

@router.get("/supervisors/profile/{slug}")
async def get_supervisor_profile(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get public supervisor profile"""
    # Query the admin database for user profile
    user = db.query(User).filter(
        User.profile_slug == slug,
        User.is_profile_public == True,
        User.role == "faculty"
    ).first()
    
    if not user:
        raise HTTPException(404, "Profile not found")
    
    # Get supervised projects
    projects = db.query(Project).filter(
        Project.supervisor_id == user.id,
        Project.is_published == True
    ).order_by(Project.publication_date.desc()).limit(10).all()
    
    return {
        "profile": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "institution": user.institution,
            "department": user.department,
            "about": user.about,
            "disciplines": user.disciplines.split(',') if user.disciplines else [],
            "research_interests": user.research_interests,
            "office_location": user.office_location,
            "office_hours": user.office_hours,
            "profile_picture_url": f"/api/supervisors/{user.id}/picture" if user.profile_picture_data else None
        },
        "projects": projects
    }

@router.get("/supervisors/{user_id}/picture")
async def get_supervisor_picture(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get supervisor profile picture"""
    user = db.query(User).filter(
        User.id == user_id,
        User.is_profile_public == True
    ).first()
    
    if not user or not user.profile_picture_data:
        raise HTTPException(404, "Picture not found")
    
    return StreamingResponse(
        io.BytesIO(user.profile_picture_data),
        media_type=user.profile_picture_content_type or "image/jpeg"
    )
