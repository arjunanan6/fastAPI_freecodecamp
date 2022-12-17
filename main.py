from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, Any
from random import randrange
import models
from database import engine, get_db
from sqlalchemy.orm import Session

import time
import os

# from dotenv import load_dotenv

# load_dotenv()

from logconfig import MyLoggingConnection, logger

import psycopg2
from psycopg2.extras import RealDictCursor

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Pydantic Basemodel: https://pydantic-docs.helpmanual.io/usage/models/


class Post(BaseModel):
    title: str
    content: str
    published: bool = (
        True  # Optional field where default value is true for post published.
    )


# Get ALL posts


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM POSTS """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return {"data": posts}


# post in the following is a model inherited from the Post class where our type validation is done.
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(
        **post.dict()
    )  # Using unpacked dict to avoid typing out each column individually.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # Similar to RETURNING

    return {"data": new_post}


# Get latest posts


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[len(my_posts) - 1]
    return {"detail": latest_post}


# Get post by ID


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found",
        )
    return {"post_detail": post}


# Delete specific post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post ID {id} not found."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, id),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {id} not found",
        )
    return {"data": updated_post}


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {f"data": posts}
