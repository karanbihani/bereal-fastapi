from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app import schemas
from app.utils import auth
from app.db import models
from app.db.database import get_db
from app.auth import oauth2

router = APIRouter(
    tags=['Reactions'],
    prefix="/reactions",
)

# body has post id and reaction id ranging from 0 to x with 0 indicating they want to remove reaction

# instead leaving it to fronttend to figure out if delete then sep end point else, will check if update or create no sep end point for that
# nvm doing it

@router.post("/", status_code = status.HTTP_201_CREATED )
def reaction(reaction: schemas.Reaction ,db:  Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id==reaction.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id {reaction.post_id} does not exist")

    reaction_query = db.query(models.Reaction).filter(models.Reaction.post_id == reaction.post_id, models.Reaction.user_id == current_user.id)

    reaction_found = reaction_query.first()

    if reaction.dir != 0:
        if reaction_found:
            if reaction_found.reaction_type == reaction.dir:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"User with id: {current_user.id}, has already reacted on post {reaction.post_id} with the reaction: {reaction.dir}")
            else:
                reaction_query.update({"reaction_type":reaction.dir}, synchronize_session=False)
                db.commit()
                return{"message": "successfully updated vote"}

        else:
            new_reaction = models.Reaction(post_id = reaction.post_id, user_id = current_user.id , reaction_type = reaction.dir)

            db.add(new_reaction)
            db.commit()

            return{"message": "successfully added vote"}
    else:
        if not reaction_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Reaction does not exist")

        else:
            reaction_query.delete(synchronize_session=False)
            db.commit()

            return{"message": "Successfully deleted vot"}