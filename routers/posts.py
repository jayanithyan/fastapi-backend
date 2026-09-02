from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from database import get_db
from models.post import Post
from schemas.post import PostCreate, PostUpdate, PostResponse, PostListResponse

router = APIRouter(
    prefix="/api/v1/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new post",
    description="Creates a new post in the database",
)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
) -> PostResponse:
    """Create a new post."""
    db_post = Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.get(
    "",
    response_model=PostListResponse,
    summary="Get all posts with pagination",
    description="Retrieves all posts with optional filtering and pagination",
)
def list_posts(
    skip: int = Query(0, ge=0, description="Number of posts to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of posts to return"),
    published: Optional[bool] = Query(None, description="Filter by published status"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Filter by minimum rating"),
    db: Session = Depends(get_db),
) -> PostListResponse:
    """Get all posts with optional filtering."""
    query = db.query(Post)
    
    if published is not None:
        query = query.filter(Post.published == published)
    
    if min_rating is not None:
        query = query.filter(Post.rating >= min_rating)
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return PostListResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{post_id}",
    response_model=PostResponse,
    summary="Get a post by ID",
    description="Retrieves a specific post by its ID",
)
def get_post(
    post_id: int = Query(..., gt=0, description="Post ID"),
    db: Session = Depends(get_db),
) -> PostResponse:
    """Get a post by ID."""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    return post


@router.put(
    "/{post_id}",
    response_model=PostResponse,
    summary="Update a post",
    description="Updates a specific post by its ID",
)
def update_post(
    post_id: int = Query(..., gt=0, description="Post ID"),
    post_update: PostUpdate = None,
    db: Session = Depends(get_db),
) -> PostResponse:
    """Update a post."""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    
    update_data = post_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a post",
    description="Deletes a specific post by its ID",
)
def delete_post(
    post_id: int = Query(..., gt=0, description="Post ID"),
    db: Session = Depends(get_db),
) -> None:
    """Delete a post."""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found",
        )
    
    db.delete(db_post)
    db.commit()


@router.get(
    "/published/list",
    response_model=PostListResponse,
    summary="Get published posts",
    description="Retrieves only published posts",
)
def get_published_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PostListResponse:
    """Get all published posts."""
    query = db.query(Post).filter(Post.published == True)
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return PostListResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/stats/summary",
    summary="Get post statistics",
    description="Retrieves statistics about posts",
)
def get_post_stats(db: Session = Depends(get_db)) -> dict:
    """Get post statistics."""
    total_posts = db.query(Post).count()
    published_posts = db.query(Post).filter(Post.published == True).count()
    unpublished_posts = db.query(Post).filter(Post.published == False).count()
    rated_posts = db.query(Post).filter(Post.rating.isnot(None)).count()
    
    avg_rating = db.query(Post.rating).filter(Post.rating.isnot(None)).first()
    
    return {
        "total_posts": total_posts,
        "published_posts": published_posts,
        "unpublished_posts": unpublished_posts,
        "rated_posts": rated_posts,
    }


@router.get(
    "/top/rated",
    response_model=PostResponse,
    summary="Get top rated post",
    description="Retrieves the highest rated post",
)
def get_top_rated_post(db: Session = Depends(get_db)) -> PostResponse:
    """Get the top rated post."""
    post = db.query(Post).filter(Post.rating.isnot(None)).order_by(desc(Post.rating)).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No rated posts found",
        )
    return post


@router.get(
    "/search/title",
    response_model=PostListResponse,
    summary="Search posts by title",
    description="Search for posts by title (case-insensitive)",
)
def search_posts_by_title(
    query_str: str = Query(..., min_length=1, description="Search term"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PostListResponse:
    """Search posts by title."""
    search_query = db.query(Post).filter(Post.title.ilike(f"%{query_str}%"))
    total = search_query.count()
    items = search_query.offset(skip).limit(limit).all()
    
    return PostListResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit,
    )
