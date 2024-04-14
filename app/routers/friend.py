from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app import schemas
from app.utils import auth
from app.db import models
from app.db.database import get_db
from app.auth import oauth2

router = APIRouter(
    tags=['Friend'],
    prefix="/friends",
)

# Send, delete and view freind requests you sent

@router.get("/{id}/request", status_code=status.HTTP_200_OK)
def send_request(id: int, db:  Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):
    pass

@router.post("/{id}/request", status_code=status.HTTP_201_CREATED)
def send_request(id: int, db:  Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):
    pass

@router.delete("/{id}/request", status_code=status.HTTP_204_NO_CONTENT)
def send_request(id: int, db:  Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):
    pass

# View requests you have recieved

@router.get("/request", status_code=status.HTTP_201_CREATED)
def send_request(id: int, db:  Session = Depends(get_db), current_user : int =  Depends(oauth2.get_current_user)):
    pass
