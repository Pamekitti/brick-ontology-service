from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Building(BaseModel):
    id: str = Field(..., description="Unique identifier for the building")
    name: str = Field(..., description="Name of the building")
    description: Optional[str] = Field(None, description="Building description")

class Floor(BaseModel):
    id: str = Field(..., description="Unique identifier for the floor")
    name: str = Field(..., description="Name of the floor")
    building_id: str = Field(..., description="ID of the building this floor belongs to")

class Device(BaseModel):
    id: str = Field(..., description="Unique identifier for the device")
    type: str = Field(..., description="Brick class type of the device")
    name: Optional[str] = Field(None, description="Name of the device")
    location: Optional[str] = Field(None, description="Location reference of the device")
    points: List[str] = Field(default_factory=list, description="List of point IDs associated with this device")

class Point(BaseModel):
    id: str = Field(..., description="Unique identifier for the point")
    type: str = Field(..., description="Brick class type of the point")
    name: Optional[str] = Field(None, description="Name of the point")
    device: Optional[str] = Field(None, description="Device ID this point belongs to")
    current_value: Optional[Dict] = Field(None, description="Current value and metadata") 