from fastapi import APIRouter
from random import randrange
from schemas.post import Post
from fastapi import status, HTTPException, Response


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


def find_post(post_id: int):
    for post in my_posts:
        if post["id"] == post_id:
            return post

    return None


@router.get("/{id}")
def get_post(id: int):
    post = find_post(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    return {
        "data": post
    }


def find_index_post(post_id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == post_id:
            return index

    return None


@router.delete("/{id}", status_code=204)
def delete_post(id: int):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    my_posts.pop(index)

    return Response(status_code=204)


@router.get("/count")
def get_post_count():
    return {
        "count": len(my_posts)
    }


@router.get("/latest")
def get_latest_post():
    if not my_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts available"
        )

    return {
        "data": my_posts[-1]
    }

@router.get("/published")
def get_published_posts():
    published_posts = []

    for post in my_posts:
        if post.get("published", True):
            published_posts.append(post)

    return {
        "data": published_posts
    }