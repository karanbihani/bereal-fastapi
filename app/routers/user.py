from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional


router = APIRouter(
    tags=['Users'],
    prefix="/users",
)
