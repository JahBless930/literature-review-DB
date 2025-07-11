from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from PIL import Image
import io

from ..database import get_db
from ..models import User, Project, ProjectFigure
from ..schemas.project_figure import ProjectFigureCreate, ProjectFigureResponse
from ..core.auth import get_current_active_user
from ..core.config import settings

router = APIRouter()

@router.post("/projects/{project_id}/figures", response_model=ProjectFigureResponse)
async def upload_figure(
    project_id: int,
    title: str = Form(...),
    caption: Optional[str] = Form(None),
    order_index: int = Form(0),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload a figure to a project"""
    # Check project exists and user has permission
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    
    if current_user.role != "main_coordinator" and project.created_by_id != current_user.id:
        raise HTTPException(403, "Not authorized to add figures to this project")
    
    # Check figure limit
    figure_count = db.query(ProjectFigure).filter(ProjectFigure.project_id == project_id).count()
    if figure_count >= settings.MAX_FIGURES_PER_PROJECT:
        raise HTTPException(400, f"Maximum {settings.MAX_FIGURES_PER_PROJECT} figures allowed per project")
    
    # Validate image
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(400, "Invalid image type")
    
    # Read and process image
    image_data = await file.read()
    if len(image_data) > settings.MAX_IMAGE_SIZE:
        raise HTTPException(413, "Image too large")
    
    # Get image dimensions
    try:
        img = Image.open(io.BytesIO(image_data))
        width, height = img.size
    except:
