from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, Any
from random import randrange

app = FastAPI()

#Pydantic Basemodel: https://pydantic-docs.helpmanual.io/usage/models/

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # Optional field where default value is true for post published.
    rating: Optional[int] = None

my_posts: dict[str | Any] = [{"title": "Title of post 1", "content": "Post 1", "id": 1},
 {"title": "Title of post 2", "content": "Post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        # Do not use else statement here as it fails to iterate over rows.
        if p["id"] == id:
            return p
        

@app.get("/")
def root():
    return {"message": "Hello testing"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# post in the following is a model inherited from the Post class where our type validation is done.
@app.post("/posts")
def create_posts(post: Post):
    # Doing this because there is no transactional database (yet). 
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000000)
    my_posts.append(post_dict)  #Every pydantic model can be converted to a dictionary if needed with dict()
    return {"data": post_dict}

@app.get("/posts/{id}")

def get_post(id: int):

    post = find_post(id) # Don't forget to convert to int! 
    print(post)
    return {"post_detail": post}
