from fastapi import FastAPI
from fastapi import Body



app=FastAPI()
@app.get("/")
def root():
    return {"message":"Hello World"}



@app.get("/post")
def get_post():
    return {"message":"This is the list of posts"}



@app.post("/createposts")
def create_post(payLoad: dict =Body(...)):
    return {"message":"Post created successfully"}