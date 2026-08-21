from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/posts",
    tags=["Posts"]
)