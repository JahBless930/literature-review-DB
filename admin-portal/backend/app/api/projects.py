from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import os
import uuid
from datetime import datetime
import io

from ..database import get_db
from ..models.user import User
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from ..core.auth import get_current_active_user
from ..core.config import settings
from ..core.constants import RESEARCH_AREAS, DEGREE_TYPES, ACADEMIC_YEARS, INSTITUTIONS
from ..services.database_storage import database_storage

router = APIRouter()

def create_slug(title: str) -> str:
    """Create a URL-friendly slug from title"""
    import re
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    research_area: Optional[str] = None,
    degree_type: Optional[str] = None,
    is_published: Optional[bool] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    query = db.query(Project)
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                Project.title.ilike(f"%{search}%"),
                Project.abstract.ilike(f"%{search}%"),
                Project.author_name.ilike(f"%{search}%"),
                Project.keywords.ilike(f"%{search}%")
            )
        )
    
    if research_area:
        query = query.filter(Project.research_area == research_area)
    
    if degree_type:
        query = query.filter(Project.degree_type == degree_type)
    
    if is_published is not None:
        query = query.filter(Project.is_published == is_published)
    
    # If user is not main coordinator, only show their projects
    if current_user.role != "main_coordinator":
        query = query.filter(Project.created_by_id == current_user.id)
    
    projects = query.offset(skip).limit(limit).all()
    return projects

@router.post("/", response_model=ProjectResponse)
async def create_project(
    title: str = Form(...),
    abstract: Optional[str] = Form(None),
    keywords: Optional[str] = Form(None),
    research_area: Optional[str] = Form(None),
    custom_research_area: Optional[str] = Form(None),
    degree_type: Optional[str] = Form(None),
    custom_degree_type: Optional[str] = Form(None),
    academic_year: Optional[str] = Form(None),
    institution: Optional[str] = Form(None),
    custom_institution: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    supervisor: Optional[str] = Form(None),
    author_name: str = Form(...),
    author_email: Optional[str] = Form(None),
    meta_description: Optional[str] = Form(None),
    meta_keywords: Optional[str] = Form(None),
    is_published: bool = Form(True),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Handle custom fields
    final_research_area = custom_research_area if research_area == "Others" else research_area
    final_degree_type = custom_degree_type if degree_type == "Others" else degree_type
    final_institution = custom_institution if institution == "Others" else institution
    
    # Validate custom fields
    if research_area == "Others" and not custom_research_area:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Custom research area is required when 'Others' is selected"
        )
    
    if degree_type == "Others" and not custom_degree_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Custom degree type is required when 'Others' is selected"
        )
    
    if institution == "Others" and not custom_institution:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Custom institution is required when 'Others' is selected"
        )
    
    # Generate slug
    base_slug = create_slug(title)
    slug = base_slug
    counter = 1
    while db.query(Project).filter(Project.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    # Handle file upload
    document_filename = None
    document_size = None
    document_data = None
    document_content_type = None
    document_storage = "database"
    
    if file and file.filename:
        try:
            # Process file for database storage
            file_result = await database_storage.upload_file(file)
            
            document_filename = file_result["filename"]
            document_size = file_result["size"]
            document_data = file_result["data"]
            document_content_type = file_result["content_type"]
            document_storage = file_result["storage"]
            
            print(f"✅ File processed for database storage: {document_filename}")
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process uploaded file: {str(e)}"
            )
    
    # Create project
    db_project = Project(
        title=title,
        slug=slug,
        abstract=abstract,
        keywords=keywords,
        research_area=final_research_area,
        degree_type=final_degree_type,
        academic_year=academic_year,
        institution=final_institution or current_user.institution,
        department=department or current_user.department,
        supervisor=supervisor,
        author_name=author_name,
        author_email=author_email,
        meta_description=meta_description,
        meta_keywords=meta_keywords,
        is_published=is_published,
        document_filename=document_filename,
        document_size=document_size,
        document_data=document_data,
        document_content_type=document_content_type,
        document_storage=document_storage,
        created_by_id=current_user.id
    )
    
    try:
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        print(f"✅ Project created successfully: {db_project.title}")
        return db_project
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project"
        )

@router.get("/{project_id}/download")
async def download_project_file(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Download project file from database"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check permissions
    if current_user.role != "main_coordinator" and project.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to download this file"
        )
    
    if not project.document_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No file available for download"
        )
    
    # Increment download counter
    project.download_count = (project.download_count or 0) + 1
    db.commit()
    
    # Create file stream
    file_stream = io.BytesIO(project.document_data)
    
    # Return file as streaming response
    return StreamingResponse(
        io.BytesIO(project.document_data),
        media_type=project.document_content_type or "application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename=\"{project.document_filename}\""
        }
    )

@router.get("/{project_id}/view")
async def view_project_file(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """View project file in browser"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
                        detail="Project not found"
        )
    
    # Check permissions
    if current_user.role != "main_coordinator" and project.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to view this file"
        )
    
    if not project.document_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No file available for viewing"
        )
    
    # Increment view counter
    project.view_count = (project.view_count or 0) + 1
    db.commit()
    
    # Return file for inline viewing
    return StreamingResponse(
        io.BytesIO(project.document_data),
        media_type=project.document_content_type or "application/pdf",
        headers={
            "Content-Disposition": f"inline; filename=\"{project.document_filename}\""
        }
    )

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    title: Optional[str] = Form(None),
    abstract: Optional[str] = Form(None),
    keywords: Optional[str] = Form(None),
    research_area: Optional[str] = Form(None),
    custom_research_area: Optional[str] = Form(None),
    degree_type: Optional[str] = Form(None),
    custom_degree_type: Optional[str] = Form(None),
    academic_year: Optional[str] = Form(None),
    institution: Optional[str] = Form(None),
    custom_institution: Optional[str] = Form(None),
    department: Optional[str] = Form(None),
    supervisor: Optional[str] = Form(None),
    author_name: Optional[str] = Form(None),
    author_email: Optional[str] = Form(None),
    meta_description: Optional[str] = Form(None),
    meta_keywords: Optional[str] = Form(None),
    is_published: Optional[bool] = Form(None),
    file: Optional[UploadFile] = File(None),
    remove_file: Optional[bool] = Form(False),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check permissions
    if current_user.role != "main_coordinator" and project.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this project"
        )
    
    # Handle custom fields
    if research_area is not None:
        final_research_area = custom_research_area if research_area == "Others" else research_area
        if research_area == "Others" and not custom_research_area:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Custom research area is required when 'Others' is selected"
            )
        project.research_area = final_research_area
    
    if degree_type is not None:
        final_degree_type = custom_degree_type if degree_type == "Others" else degree_type
        if degree_type == "Others" and not custom_degree_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Custom degree type is required when 'Others' is selected"
            )
        project.degree_type = final_degree_type
    
    if institution is not None:
        final_institution = custom_institution if institution == "Others" else institution
        if institution == "Others" and not custom_institution:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Custom institution is required when 'Others' is selected"
            )
        project.institution = final_institution
    
    # Update other fields
    if title is not None:
        project.title = title
        # Update slug if title changed
        base_slug = create_slug(title)
        slug = base_slug
        counter = 1
        while db.query(Project).filter(and_(Project.slug == slug, Project.id != project_id)).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        project.slug = slug
    
    if abstract is not None:
        project.abstract = abstract
    if keywords is not None:
        project.keywords = keywords
    if academic_year is not None:
        project.academic_year = academic_year
    if department is not None:
        project.department = department
    if supervisor is not None:
        project.supervisor = supervisor
    if author_name is not None:
        project.author_name = author_name
    if author_email is not None:
        project.author_email = author_email
    if meta_description is not None:
        project.meta_description = meta_description
    if meta_keywords is not None:
        project.meta_keywords = meta_keywords
    if is_published is not None:
        project.is_published = is_published
    
    # Handle file removal
    if remove_file:
        project.document_filename = None
        project.document_size = None
        project.document_data = None
        project.document_content_type = None
        project.document_storage = "database"
        print(f"🗑️  File removed from project: {project.title}")
    
    # Handle new file upload
    if file and file.filename:
        try:
            # Process new file for database storage
            file_result = await database_storage.upload_file(file)
            
            project.document_filename = file_result["filename"]
            project.document_size = file_result["size"]
            project.document_data = file_result["data"]
            project.document_content_type = file_result["content_type"]
            project.document_storage = file_result["storage"]
            
            print(f"✅ File updated for project: {project.title}")
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process uploaded file: {str(e)}"
            )
    
    try:
        db.commit()
        db.refresh(project)
        return project
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project"
        )

@router.delete("/{project_id}/file")
async def delete_project_file(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check permissions
    if current_user.role != "main_coordinator" and project.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete file"
        )
    
    if not project.document_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No file to delete"
        )
    
    # Clear file fields in database
    project.document_filename = None
    project.document_size = None
    project.document_data = None
    project.document_content_type = None
    project.document_storage = "database"
    
    try:
        db.commit()
        return {"message": "File deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete file"
        )

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check permissions
    if current_user.role != "main_coordinator" and project.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this project"
        )
    
    try:
        db.delete(project)
        db.commit()
        return {"message": "Project deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project"
        )

# Keep existing endpoints
@router.get("/research-areas/list")
async def get_research_areas(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get predefined research areas"""
    return RESEARCH_AREAS

@router.get("/degree-types/list")
async def get_degree_types(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get predefined degree types"""
    return DEGREE_TYPES

@router.patch("/{project_id}/toggle-publish")
async def toggle_project_publish_status(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Check permissions
    if current_user.role != "main_coordinator" and project.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify this project"
        )
    
    project.is_published = not project.is_published
    
    try:
        db.commit()
        db.refresh(project)
        status_text = "published" if project.is_published else "unpublished"
        return {
            "message": f"Project {status_text} successfully",
            "project": {
                "id": project.id,
                "title": project.title,
                "is_published": project.is_published
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project status"
        )
