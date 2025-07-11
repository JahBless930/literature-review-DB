from sqlalchemy import Column, String, Text, Integer, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from .base import BaseModel

class ProjectFigure(BaseModel):
    __tablename__ = "project_figures"
    
    # Relationships
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Project", back_populates="figures")
    
    # Figure Details
    title = Column(String, nullable=False)
    caption = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)
    
    # File Storage
    filename = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    data = Column(LargeBinary, nullable=False)
    content_type = Column(String, nullable=False)
    
    # Metadata
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    uploaded_by_id = Column(Integer, ForeignKey("users.id"))
    uploaded_by = relationship("User")
