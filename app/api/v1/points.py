from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import Point
from app.services.brick import BrickService

router = APIRouter()
brick_service = BrickService()

@router.get("/", response_model=List[Point])
async def get_points():
    try:
        # TODO: Implement get_all_points in BrickService
        points = []  # brick_service.get_all_points()
        return points
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 