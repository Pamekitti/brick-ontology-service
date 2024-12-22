"""
Examples of using the Brick Backend API for querying building data.
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def get_all_buildings():
    """Example: Get all buildings"""
    response = requests.get(f"{BASE_URL}/buildings/")
    print("All Buildings:", json.dumps(response.json(), indent=2))

def get_building_floors(building_id: str):
    """Example: Get floors in a specific building"""
    response = requests.get(f"{BASE_URL}/floors/{building_id}")
    print(f"Floors in Building {building_id}:", json.dumps(response.json(), indent=2))

def get_building_devices(building_id: str):
    """Example: Get devices in a specific building"""
    response = requests.get(f"{BASE_URL}/devices/building/{building_id}")
    print(f"Devices in Building {building_id}:", json.dumps(response.json(), indent=2))

def execute_sparql_query():
    """Example: Execute a SPARQL query"""
    # Example query to find all VAV boxes
    query = """
    PREFIX brick: <https://brickschema.org/schema/Brick#>
    
    SELECT ?vav ?label
    WHERE {
        ?vav a brick:VAV .
        OPTIONAL { ?vav rdfs:label ?label }
    }
    """
    response = requests.post(
        f"{BASE_URL}/query/",
        json={"query": query}
    )
    print("SPARQL Query Results:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    # Example usage
    get_all_buildings()
    get_building_floors("campus_lab_1")
    get_building_devices("campus_lab_1")
    execute_sparql_query() 