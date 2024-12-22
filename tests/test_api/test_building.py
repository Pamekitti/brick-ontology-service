from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.services.brick import BrickService

client = TestClient(app)

def test_get_buildings():
    """Test getting all buildings"""
    response = client.get("/api/v1/buildings/")
    assert response.status_code == 200
    buildings = response.json()
    
    # Check response structure
    assert isinstance(buildings, list)
    if len(buildings) > 0:
        building = buildings[0]
        assert "id" in building
        assert "name" in building
        assert isinstance(building["id"], str)
        assert isinstance(building["name"], str)
        
        # Check if name is not None (as per our fix)
        assert building["name"] is not None

def test_get_buildings_data():
    """Test actual building data"""
    response = client.get("/api/v1/buildings/")
    assert response.status_code == 200
    buildings = response.json()
    
    # Check for specific test buildings
    building_ids = [b["id"] for b in buildings]
    expected_buildings = ["campus_lab_1", "campus_office_1"]
    
    for expected_id in expected_buildings:
        assert any(expected_id in bid for bid in building_ids), f"Expected building {expected_id} not found" 