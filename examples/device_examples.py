"""
Examples of working with devices and points in the Brick Backend API.
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def find_devices_by_type():
    """Example: Find all devices of a specific type using SPARQL"""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    
    SELECT ?device ?label ?location
    WHERE {
        ?device a brick:Temperature_Sensor .
        OPTIONAL { ?device rdfs:label ?label }
        OPTIONAL { 
            ?device brick:hasLocation ?location .
            ?location rdfs:label ?loc_label
        }
    }
    """
    response = requests.post(
        f"{BASE_URL}/query/",
        json={"query": query}
    )
    print("Temperature Sensors:", json.dumps(response.json(), indent=2))

def get_floor_devices(building_id: str, floor_id: str):
    """Example: Get all devices on a specific floor"""
    response = requests.get(
        f"{BASE_URL}/devices/floor/{building_id}/{floor_id}"
    )
    print(f"Devices on Floor {floor_id}:", json.dumps(response.json(), indent=2))

def find_connected_points():
    """Example: Find points connected to a specific device type"""
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    
    SELECT ?device ?point ?point_type
    WHERE {
        ?device a brick:VAV .
        ?device brick:hasPoint ?point .
        ?point a ?point_type .
    }
    """
    response = requests.post(
        f"{BASE_URL}/query/",
        json={"query": query}
    )
    print("VAV Points:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    # Example usage
    find_devices_by_type()
    get_floor_devices("campus_lab_1", "floor1")
    find_connected_points() 