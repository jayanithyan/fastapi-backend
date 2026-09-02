from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    """Base schema for posts."""
    title: str = Field(..., min_length=1, max_length=255, description="Post title")
    content: str = Field(..., min_length=1, max_length=5000, description="Post content")
    published: bool = Field(default=True, description="Publication status")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Post rating between 0 and 5")


class PostCreate(PostBase):
    """Schema for creating a post."""
    pass


class PostUpdate(BaseModel):
    """Schema for updating a post."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1, max_length=5000)
    published: Optional[bool] = None
    rating: Optional[float] = Field(None, ge=0, le=5)


class PostResponse(PostBase):
    """Schema for post response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    """Schema for post list response."""
    items: List[PostResponse]
    total: int
    skip: int
    limit: int
    
    class Config:
        from_attributes = True
