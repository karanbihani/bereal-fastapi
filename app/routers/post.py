from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile, File

from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func 
# from sqlalchemy.sql.functions import func
from app.db import models
from app.db.database import get_db
from app import schemas
from app.auth import oauth2
from app.utils import upload

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return [{"post": post} for post in posts]

@router.get("/{id}", response_model= schemas.PostOut)
def get_post_by_id(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

    return {"post": post}

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_post( post: schemas.PostCreate, front_image: UploadFile = File(...), back_image:UploadFile = File(...), db:Session = Depends(get_db)):

    file_extension_front = "." + front_image.filename.split(".")[-1]
    file_extension_back = "." + back_image.filename.split(".")[-1]

    if file_extension_front in [".png", ".jpg", ".jpeg"] and file_extension_back in [".png", ".jpg", ".jpeg"]:
        front_image_url = await upload.save_upload_file(front_image, "media/images/uploads", "front", file_extension_front)
        print(front_image_url)
        back_image_url = await upload.save_upload_file(back_image, "media/images/uploads", "back", file_extension_back)
        print(back_image_url)

        post['image_url_front'] = front_image_url
        post['image_url_back'] = back_image_url

        new_post = models.Post(**post.dict())

        await db.add(new_post)
        await db.commit()
        await db.refresh(new_post)
        return new_post

# @router.post("/", response_model=schemas.Post, status_code=status.HTTP_204_NO_CONTENT)
# def update_post(post:schemas.PostUpdate,  db:Session = Depends(get_db)):
#     pass
