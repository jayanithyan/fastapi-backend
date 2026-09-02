from fastapi import APIRouter
from random import randrange
from schemas.post import Post

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

@router.post("/", status_code=201)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000000)

    my_posts.append(post_dict)

    return {
        "data": post_dict
    }