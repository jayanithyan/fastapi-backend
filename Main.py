from typing import Optional
from urllib import response
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange



app=FastAPI()


class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating: Optional[int]=None


my_posts=[{"title":"title of post 1","content":"content of post 1","id":1},{"title":"fav food","content":"briyani","id":3}]



def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p



def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"]==id:
            return i



@app.get("/")
def root():
    return {"message":"Hello World"}



@app.get("/posts")
def get_posts():
    return {"message":my_posts}



@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict=post.dict()
    post_dict["id"]=randrange(0,100000000)
    my_posts.append(post_dict)
    return{"data":post_dict}



@app.get("/posts/{id}")
def get_post(id:int):
    post=find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return{"post_detail":f"post with id: {id}"}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index=find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
@app.get("/posts/count")
def get_post_count():
    return {"count": len(my_posts)}
@app.get("/posts/latest")
def get_latest_post():
    if not my_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts available"
        )

    return {"data": my_posts[-1]}
@app.get("/posts/first")
def get_first_post():
    if not my_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts available"
        )

    return {"data": my_posts[0]}
@app.get("/posts/published")
def get_published_posts():
    published_posts = []

    for post in my_posts:
        if post.get("published", True):
            published_posts.append(post)

    return {"data": published_posts}
@app.get("/posts/unpublished")
def get_unpublished_posts():
    unpublished_posts = []

    for post in my_posts:
        if not post.get("published", True):
            unpublished_posts.append(post)

    return {"data": unpublished_posts}
@app.get("/posts/rating/{rating}")
def get_posts_by_rating(rating: int):
    posts = []

    for post in my_posts:
        if post.get("rating") == rating:
            posts.append(post)

    return {"data": posts}
@app.get("/posts/top")
def get_top_post():
    if not my_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts available"
        )

    rated_posts = [
        post for post in my_posts
        if post.get("rating") is not None
    ]

    if not rated_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No rated posts available"
        )

    top_post = max(rated_posts, key=lambda post: post["rating"])

    return {"data": top_post}
@app.get("/posts/title/{title}")
def search_by_title(title: str):
    results = []

    for post in my_posts:
        if title.lower() in post["title"].lower():
            results.append(post)

    return {"data": results}
@app.get("/posts/content/{keyword}")
def search_by_content(keyword: str):
    results = []

    for post in my_posts:
        if keyword.lower() in post["content"].lower():
            results.append(post)

    return {"data": results}
@app.get("/posts/{id}/exists")
def post_exists(id: int):
    post = find_post(id)

    return {
        "id": id,
        "exists": post is not None
    }
@app.get("/posts/limit")
def get_posts_limit(limit: int = 10):
    return {"data": my_posts[:limit]}
@app.get("/posts/skip")
def get_posts_skip(skip: int = 0):
    return {"data": my_posts[skip:]}
@app.get("/posts/page")
def get_posts_page(skip: int = 0, limit: int = 10):
    return {
        "data": my_posts[skip:skip + limit],
        "skip": skip,
        "limit": limit
    }
@app.get("/posts/filter/rating")
def filter_by_rating(min_rating: int):
    results = []

    for post in my_posts:
        rating = post.get("rating")

        if rating is not None and rating >= min_rating:
            results.append(post)

    return {"data": results}
@app.get("/posts/filter/rating")
def filter_by_rating(min_rating: int):
    results = []

    for post in my_posts:
        rating = post.get("rating")

        if rating is not None and rating >= min_rating:
            results.append(post)

    return {"data": results}
@app.get("/posts/sort/rating")
def sort_posts_by_rating():
    results = sorted(
        my_posts,
        key=lambda post: post.get("rating") or 0,
        reverse=True
    )

    return {"data": results}
def post_id_exists(id):
    for post in my_posts:
        if post["id"] == id:
            return True

    return False
def generate_post_id():
    new_id = randrange(0, 100000000)

    while post_id_exists(new_id):
        new_id = randrange(0, 100000000)

    return new_id
def title_exists(title):
    for post in my_posts:
        if post["title"].lower() == title.lower():
            return True

    return False
@app.get("/posts/title-available")
def check_title(title: str):
    return {
        "title": title,
        "available": not title_exists(title)
    }
@app.get("/posts/stats/published")
def published_count():
    count = 0

    for post in my_posts:
        if post.get("published", True):
            count += 1

    return {
        "published_posts": count
    }
@app.get("/posts/stats/unpublished")
def unpublished_count():
    count = 0

    for post in my_posts:
        if not post.get("published", True):
            count += 1

    return {
        "unpublished_posts": count
    }
@app.get("/posts/stats/rating")
def rating_statistics():
    ratings = []

    for post in my_posts:
        if post.get("rating") is not None:
            ratings.append(post["rating"])

    if not ratings:
        return {
            "count": 0,
            "average": 0
        }

    return {
        "count": len(ratings),
        "average": sum(ratings) / len(ratings)
    }
@app.get("/posts/stats")
def post_statistics():
    published = 0
    unpublished = 0
    rated = 0

    for post in my_posts:
        if post.get("published", True):
            published += 1
        else:
            unpublished += 1

        if post.get("rating") is not None:
            rated += 1

    return {
        "total_posts": len(my_posts),
        "published_posts": published,
        "unpublished_posts": unpublished,
        "rated_posts": rated
    }
@app.get("/posts/sort/title")
def sort_posts_by_title():
    results = sorted(
        my_posts,
        key=lambda post: post["title"].lower()
    )

    return {
        "data": results
    }
@app.get("/posts/sort/title/reverse")
def sort_posts_by_title_reverse():
    results = sorted(
        my_posts,
        key=lambda post: post["title"].lower(),
        reverse=True
    )

    return {
        "data": results
    }