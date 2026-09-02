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


my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "fav food",
        "content": "briyani",
        "id": 3
    }
]


@router.get("/")
def get_posts():
    return {
        "data": my_posts
    }