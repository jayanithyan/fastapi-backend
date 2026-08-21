from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/posts",
    tags=["Posts"]
)
@router.get("/test")
def test_posts_router():
    return {
        "message": "Posts router is working"
    }