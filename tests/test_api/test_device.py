from fastapi.testclient import TestClient
import pytest

from app.main import app

client = TestClient(app)

def test_get_building_devices():
    """Test getting devices for a specific building"""
    building_id = "campus_lab_1"
    response = client.get(f"/api/v1/devices/building/{building_id}")
    assert response.status_code == 200
    devices = response.json()
    
    # Check response structure
    assert isinstance(devices, list)
    if len(devices) > 0:
        device = devices[0]
        assert "id" in device
        assert "type" in device
        assert "name" in device
        assert "location" in device
        assert "points" in device
        assert isinstance(device["id"], str)
        assert isinstance(device["type"], str)
        assert isinstance(device["name"], str)
        assert isinstance(device["points"], list)
        
        # Check if required fields are not None
        assert device["name"] is not None
        assert device["type"] is not None

def test_get_floor_devices():
    """Test getting devices for a specific floor"""
    building_id = "campus_lab_1"
    floor_id = "floor1"
    response = client.get(f"/api/v1/devices/floor/{building_id}/{floor_id}")
    assert response.status_code == 200
    devices = response.json()
    
    # Check response structure
    assert isinstance(devices, list)
    if len(devices) > 0:
        device = devices[0]
        assert "id" in device
        assert "type" in device
        assert "name" in device
        assert "location" in device
        assert "points" in device
        
        # Check if location matches floor_id
        assert device["location"] == floor_id

def test_get_building_devices_invalid_building():
    """Test getting devices for a non-existent building"""
    building_id = "non_existent_building"
    response = client.get(f"/api/v1/devices/building/{building_id}")
    assert response.status_code == 404

def test_get_floor_devices_invalid_floor():
    """Test getting devices for a non-existent floor"""
    building_id = "campus_lab_1"
    floor_id = "non_existent_floor"
    response = client.get(f"/api/v1/devices/floor/{building_id}/{floor_id}")
    assert response.status_code == 404

def test_get_floor_devices_data():
    """Test actual device data for a specific floor"""
    building_id = "campus_lab_1"
    floor_id = "floor1"
    response = client.get(f"/api/v1/devices/floor/{building_id}/{floor_id}")
    assert response.status_code == 200
    devices = response.json()
    
    # Verify we have devices and they have expected types
    if len(devices) > 0:
        device_types = {d["type"] for d in devices}
        # Check for common Brick equipment types
        brick_types = {"VAV", "AHU", "Thermostat", "Sensor"}
        assert any(brick_type in device_types for brick_type in brick_types), \
            "No expected Brick equipment types found" 