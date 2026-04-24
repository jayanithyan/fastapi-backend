from fastapi import FastAPI
app=FastAPI()
@app.get("/")
def root():
    return {"message":"Hello World"}
@app.get("/post")
def get_post():
    return {"message":"This is the list of posts"}