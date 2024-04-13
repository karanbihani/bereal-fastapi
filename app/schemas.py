from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class ORMBase(BaseModel):
    """ Base for ORM models"""

    class Config:
        """ Configuring ORM mode to true"""
        orm_mode = True

class UserOut(ORMBase):
    
    id: int
    fullname: str
    username:str
    email: EmailStr
    created_at: datetime

# Posts

class PostBase(BaseModel):
    description: Optional[str] = None
    published: bool = True
    location: Optional[str]
    deleted: bool = False
    # image_url_front: str
    # image_url_back: str

# class PostCreate(PostBase):
#     pass    
    
class PostUpdate(BaseModel):

    description: Optional[str] = None 
    published: Optional[bool] = True
    location: Optional[str] = None
    deleted: Optional[bool] = False

class Post(PostBase):
    id: int
    image_url_front: str
    image_url_back: str
    created_at: datetime
    owner_id : int
    owner: UserOut

    class Config:
        """ Configuring ORM mode to true"""
        orm_mode = True

class PostOut(ORMBase):
    post: Post

# User

class UserCreate(BaseModel):

    fullname: str
    username: str
    email: EmailStr
    password: str
    bio: Optional[str]

class UserUpdate(BaseModel):

    fullname: Optional[str]
    email: Optional[EmailStr]
    username: Optional[str]
    bio: Optional[str]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None