from fastapi import FastAPI

import os
from dotenv import load_dotenv

from .db import models

from .db.database import engine
from .routers import post, user, auth, reaction, comment, friend

load_dotenv()

POSTGRES_PWD = os.getenv('POSTGRES_PWD')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(reaction.router)
app.include_router(comment.router)
app.include_router(friend.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
