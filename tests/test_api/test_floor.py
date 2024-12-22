from fastapi.testclient import TestClient
import pytest

from app.main import app

client = TestClient(app)

def test_get_building_floors():
    """Test getting floors for a specific building"""
    building_id = "campus_lab_1"
    response = client.get(f"/api/v1/floors/{building_id}")
    assert response.status_code == 200
    floors = response.json()
    
    # Check response structure
    assert isinstance(floors, list)
    if len(floors) > 0:
        floor = floors[0]
        assert "id" in floor
        assert "name" in floor
        assert "building_id" in floor
        assert isinstance(floor["id"], str)
        assert isinstance(floor["name"], str)
        assert isinstance(floor["building_id"], str)
        
        # Check if name is not None
        assert floor["name"] is not None
        # Check if building_id matches request
        assert floor["building_id"] == building_id

def test_get_building_floors_data():
    """Test actual floor data for a specific building"""
    building_id = "campus_lab_1"
    response = client.get(f"/api/v1/floors/{building_id}")
    assert response.status_code == 200
    floors = response.json()
    
    # Check for expected floors
    floor_ids = [f["id"] for f in floors]
    expected_floors = ["floor1", "floor2"]
    
    for expected_id in expected_floors:
        assert expected_id in floor_ids, f"Expected floor {expected_id} not found"

def test_get_building_floors_invalid_building():
    """Test getting floors for a non-existent building"""
    building_id = "non_existent_building"
    response = client.get(f"/api/v1/floors/{building_id}")
    assert response.status_code == 404 