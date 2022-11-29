from fastapi import FastAPI, Response, status, HTTPException
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
            return i # Return just the index here.

def find_post_index(id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i     

@app.get("/")
def root():
    return {"message": "Hello testing"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# post in the following is a model inherited from the Post class where our type validation is done.
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # Doing this because there is no transactional database (yet). 
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000000)
    my_posts.append(post_dict)  #Every pydantic model can be converted to a dictionary if needed with dict()
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[len(my_posts)-1]
    return {"detail": latest_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post ID: {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"post_detail": f"Post ID {id} not found"}
    print(post)
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)  # Default status code for delete.
def delete_post(id: int):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post ID {id} not found.")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)