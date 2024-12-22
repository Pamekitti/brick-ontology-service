from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import Device
from app.services.brick import BrickService

router = APIRouter()
brick_service = BrickService()

@router.get("/building/{building_id}", response_model=List[Device])
async def get_building_devices(building_id: str):
    """Get all devices in a specific building"""
    try:
        devices = await brick_service.get_building_devices(building_id)
        if not devices:
            raise HTTPException(
                status_code=404,
                detail=f"No devices found in building {building_id}"
            )
        return devices
    except Exception as e:
        if "No devices found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/floor/{building_id}/{floor_id}", response_model=List[Device])
async def get_floor_devices(building_id: str, floor_id: str):
    """Get all devices in a specific floor"""
    try:
        devices = await brick_service.get_floor_devices(building_id, floor_id)
        if not devices:
            raise HTTPException(
                status_code=404,
                detail=f"No devices found on floor {floor_id} in building {building_id}"
            )
        return devices
    except Exception as e:
        if "No devices found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e)) 