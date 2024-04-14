from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app import schemas
from app.utils import auth
from app.db import models
from app.db.database import get_db
from app.auth import oauth2

router = APIRouter(
    tags=['Comments'],
    prefix="/comments",
)

# get all comments for a particular post id

@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model= List[schemas.Comment])
def get_all_comments(post_id:int, db:  Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id {post_id} does nto exist")

    comments = db.query(models.Comments).filter(models.Comments.post_id == post_id).all()

    return comments

@router.post("/{post_id}", status_code = status.HTTP_201_CREATED, response_model=schemas.CommentOut)
def create_comment(post_id:int, comment: schemas.Comment ,db:  Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id {post_id} does not exist")

    # reaction_query = db.query(models.Reaction).filter(models.Reaction.post_id == reaction.post_id, models.Reaction.user_id == current_user.id)

    # reaction_found = reaction_query.first()

    # if reaction.dir != 0:
    #     if reaction_found:
    #         if reaction_found.reaction_type == reaction.dir:
    #             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"User with id: {current_user.id}, has already reacted on post {reaction.post_id} with the reaction: {reaction.dir}")
    #         else:
    #             reaction_query.update({"reaction_type":reaction.dir}, synchronize_session=False)
    #             db.commit()
    #             return{"message": "successfully updated vote"}

    new_comment = models.Comments(post_id = post_id, user_id = current_user.id , comment = comment.comment)

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@router.delete("/{comment_id}", status_code = status.HTTP_204_NO_CONTENT )
def delete_comment(comment_id: int ,db:  Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):

    comment_query = db.query(models.Comments).filter(models.Comments.id == comment_id)

    comment = comment_query.first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Comment with id {comment_id} does not exist")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    
    comment_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{comment_id}", status_code = status.HTTP_204_NO_CONTENT )
def update_comment(comment_id: int, new_comment: schemas.Comment , db:  Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):
    
    comment_query = db.query(models.Comments).filter(models.Comments.id == comment_id)
    comment = comment_query.first()

    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {comment_id} does not exist")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    comment_query.update(new_comment.dict(), synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)