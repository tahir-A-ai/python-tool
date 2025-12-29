from fastapi import APIRouter,Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/books",
    tags = ["Books"]
)

# --- ENDPOINT 1: GET ALL BOOKS (Public) ---
