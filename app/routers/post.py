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
from app import forms

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/")
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # posts = db.query(models.Post).all()

    # results = db.query(models.Post,models.Reaction.reaction_type ).join(models.Reaction, models.Reaction.post_id == models.Post.id, isouter=True)
    
    # print(results)
    # print(results.all())
    # print(posts)
    # # return [{"post": result} for result in results]
    # return results.all()

    results = db.query(
        models.Post,
        models.Reaction.reaction_type.label("reaction_type")
    ).join(
        models.Reaction, models.Reaction.post_id == models.Post.id, isouter=True
    ).group_by(
        models.Post.id
    ).all()
       
    posts_out = []
    for post, reaction in results:
        print(post, reaction, "\n")
        
        # serialize the owner_data else it returns sql alchemy object 
        owner_data = schemas.UserOut.from_orm(post.owner) if post.owner else None

        post_data = {
            "id": post.id,
            "description": post.description,
            "published": post.published,
            "location": post.location,
            "deleted": post.deleted,
            "image_url_front": post.image_url_front,
            "image_url_back": post.image_url_back,
            "created_at": post.created_at,
            "owner_id": post.owner_id,
            "owner": owner_data,
            "reaction_type": reaction if reaction is not None else 0  # Default value or handle None differently
        }
        posts_out.append(schemas.PostOut(**post_data))
    
    return posts_out

@router.get("/{id}", response_model= schemas.PostOut)
def get_post_by(id:int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

    return {"post": post}

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_post( post: forms.PostCreate = Depends(forms.PostCreate), front_image: UploadFile = File(...), back_image:UploadFile = File(...), db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    file_extension_front = "." + front_image.filename.split(".")[-1]
    file_extension_back = "." + back_image.filename.split(".")[-1]

    if file_extension_front in [".png", ".jpg", ".jpeg"] and file_extension_back in [".png", ".jpg", ".jpeg"]:
        front_image_url = await upload.save_upload_file(front_image, "media/images/uploads", "front", file_extension_front)
        back_image_url = await upload.save_upload_file(back_image, "media/images/uploads", "back", file_extension_back)

        post = post.dict()
        post['image_url_front'] = front_image_url
        post['image_url_back'] = back_image_url

        new_post = models.Post(owner_id= current_user.id ,**post)

        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()