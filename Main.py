from fastapi import FastAPI
from fastapi.params import Body



app=FastAPI()
@app.get("/")
def root():
    return {"message":"Hello World"}



@app.get("/posts")
def get_posts():
    return {"message":"This is the list of posts"}



@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message":"Post created successfully"}