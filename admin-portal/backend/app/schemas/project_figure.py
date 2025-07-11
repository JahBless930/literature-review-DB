from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectFigureBase(BaseModel):
    title: str
    caption: Optional[str] = None
    order_index: int = 0

class ProjectFigureCreate(ProjectFigureBase):
    pass

class ProjectFigureUpdate(BaseModel):
    title: Optional[str] = None
    caption: Optional[str] = None
    order_index: Optional[int] = None

class ProjectFigureResponse(ProjectFigureBase):
    id: int
    project_id: int
    filename: str
    size: int
    content_type: str
    width: Optional[int] = None
    height: Optional[int] = None
    url: str
    created_at: datetime
    
    class Config:
        from_attributes = True
