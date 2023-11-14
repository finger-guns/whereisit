from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/movie",
    tags=["movie"],
)
