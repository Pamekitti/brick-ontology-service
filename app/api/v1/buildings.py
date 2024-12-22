from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import Building
from app.services.brick import BrickService

router = APIRouter()
brick_service = BrickService()

@router.get("/", response_model=List[Building])
async def get_buildings():
    """Get all buildings from the Brick graph"""
    try:
        buildings = await brick_service.get_buildings()
        if not buildings:
            raise HTTPException(status_code=404, detail="No buildings found")
        return buildings
    except Exception as e:
        if "No buildings found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))