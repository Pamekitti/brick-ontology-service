from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import Floor
from app.services.brick import BrickService

router = APIRouter()
brick_service = BrickService()

@router.get("/{building_id}", response_model=List[Floor])
async def get_building_floors(building_id: str):
    """Get all floors in a specific building"""
    try:
        floors = await brick_service.get_building_floors(building_id)
        if not floors:
            raise HTTPException(
                status_code=404,
                detail=f"No floors found for building {building_id}"
            )
        return floors
    except Exception as e:
        if "No floors found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
