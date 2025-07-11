from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from PIL import Image
import io

from ..database import get_db
from ..models.user import User
from ..models.project import Project
from ..models.project_figure import ProjectFigure
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
    except Exception:  # Fixed: specify exception type
        width, height = None, None
    
    # Create figure record
    figure = ProjectFigure(
        project_id=project_id,
        title=title,
        caption=caption,
        order_index=order_index,
        filename=file.filename,
        size=len(image_data),
        data=image_data,
        content_type=file.content_type,
        width=width,
        height=height,
        uploaded_by_id=current_user.id
    )
    
    db.add(figure)
    db.commit()
    db.refresh(figure)
    
    # Add URL to response
    figure.url = f"/api/figures/{figure.id}/image"
    return figure

@router.get("/projects/{project_id}/figures", response_model=List[ProjectFigureResponse])
async def get_project_figures(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all figures for a project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(404, "Project not found")
    
    figures = db.query(ProjectFigure).filter(
        ProjectFigure.project_id == project_id
    ).order_by(ProjectFigure.order_index).all()
    
    # Add URLs
    for figure in figures:
        figure.url = f"/api/figures/{figure.id}/image"
    
    return figures

@router.get("/figures/{figure_id}/image")
async def get_figure_image(
    figure_id: int,
    db: Session = Depends(get_db)
):
    """Get figure image data"""
    figure = db.query(ProjectFigure).filter(ProjectFigure.id == figure_id).first()
    if not figure:
        raise HTTPException(404, "Figure not found")
    
    return StreamingResponse(
        io.BytesIO(figure.data),
        media_type=figure.content_type
    )

@router.delete("/figures/{figure_id}")
async def delete_figure(
    figure_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a figure"""
    figure = db.query(ProjectFigure).filter(ProjectFigure.id == figure_id).first()
    if not figure:
        raise HTTPException(404, "Figure not found")
    
    # Check permissions
    project = figure.project
    if current_user.role != "main_coordinator" and project.created_by_id != current_user.id:
                raise HTTPException(403, "Not authorized to delete this figure")
    
    db.delete(figure)
    db.commit()
    
    return {"message": "Figure deleted successfully"}

@router.put("/figures/{figure_id}")
async def update_figure(
    figure_id: int,
    title: Optional[str] = Form(None),
    caption: Optional[str] = Form(None),
    order_index: Optional[int] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update figure details"""
    figure = db.query(ProjectFigure).filter(ProjectFigure.id == figure_id).first()
    if not figure:
        raise HTTPException(404, "Figure not found")
    
    # Check permissions
    project = figure.project
    if current_user.role != "main_coordinator" and project.created_by_id != current_user.id:
        raise HTTPException(403, "Not authorized to update this figure")
    
    # Update fields
    if title is not None:
        figure.title = title
    if caption is not None:
        figure.caption = caption
    if order_index is not None:
        figure.order_index = order_index
    
    db.commit()
    db.refresh(figure)
    
    figure.url = f"/api/figures/{figure.id}/image"
    return figure
