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


def find_post(post_id: int):
    for post in my_posts:
        if post["id"] == post_id:
            return post
    return None