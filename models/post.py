from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, func
from datetime import datetime
from database import Base


class Post(Base):
    """Post database model."""
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(String(5000), nullable=False)
    published = Column(Boolean, default=True, index=True)
    rating = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title='{self.title}', published={self.published})>"
