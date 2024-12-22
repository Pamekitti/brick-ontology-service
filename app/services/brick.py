from rdflib import Graph, Namespace, URIRef
from rdflib.plugins.sparql.processor import SPARQLResult
import brickschema
from typing import List, Optional, Dict

from app.config import settings
from app.models.schemas import Building, Device, Point, Floor


class BrickService:
    _instance = None
    _initialized = False
    BASE_URI = "http://buildsys.org/ontologies"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrickService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.g = None
            self._initialize_graph()
            BrickService._initialized = True

    def _get_simple_id(self, full_uri: str) -> str:
        """Extract simple ID from a full URI"""
        return full_uri.split('#')[-1]

    def _initialize_graph(self):
        """Initialize the Brick graph with schema and building data"""
        try:
            print("Initializing Brick graph...")
            self.g = brickschema.Graph(load_brick=True)
            
            # Load building data
            for file in settings.BUILDING_TTL_FILES:
                self.g.load_file(file)
            
            # Commented out for faster initialization
            # self.g.expand(profile="owlrl")
            # self.g.expand(profile="shacl")
            print(f"Brick graph initialized with {len(self.g)} triples")
        except Exception as e:
            print(f"Error loading Brick graph: {str(e)}")
            raise

    async def execute_query(self, query: str) -> Dict:
        """Execute a SPARQL query and return processed results"""
        try:
            results = self.g.query(query)
            
            if isinstance(results, SPARQLResult):
                processed_results = []
                for row in results:
                    processed_row = {}
                    for var_idx, var in enumerate(results.vars):
                        if var_idx < len(row):
                            value = row[var_idx]
                            processed_row[str(var)] = str(value) if value is not None else None
                        else:
                            processed_row[str(var)] = None
                    processed_results.append(processed_row)
                return {"results": processed_results}
            else:
                return {"results": [{"result": bool(results)}]}
                
        except Exception as e:
            print(f"Query error details: {str(e)}")
            raise

    def get_triple_count(self) -> int:
        """Return the total number of triples in the graph"""
        return len(self.g)

    def get_namespaces(self) -> Dict:
        """Return all namespaces in the graph"""
        return dict(self.g.namespaces())

    async def get_buildings(self) -> List[Building]:
        """Get all buildings from the Brick graph"""
        query = """
        PREFIX brick: <https://brickschema.org/schema/Brick#>
        
        SELECT ?id ?name
        WHERE {
            ?id a brick:Building .
            OPTIONAL { ?id rdfs:label ?name }
        }
        """
        try:
            result = await self.execute_query(query)
            buildings = []
            for row in result["results"]:
                building_id = row["id"]
                simple_id = building_id.split('#')[-1]
                
                building = Building(
                    id=simple_id,
                    name=row.get("name") or simple_id,
                    description=None  # We can add description later if needed
                )
                buildings.append(building)
            return buildings
        except Exception as e:
            print(f"Error getting buildings: {str(e)}")
            raise

    async def get_building_floors(self, building_id: str) -> List[Floor]:
        """Get all floors in a specific building"""
        full_building_uri = f"{self.BASE_URI}/{building_id}#{building_id}"
        query = f"""
        SELECT DISTINCT ?id ?name
        WHERE {{
            ?id a brick:Floor .
            <{full_building_uri}> brick:hasPart ?id .
            OPTIONAL {{ ?id rdfs:label ?name }}
        }}
        ORDER BY ?id
        """
        try:
            result = await self.execute_query(query)
            floors = []
            for row in result["results"]:
                floor_id = row["id"]
                simple_id = floor_id.split('#')[-1]
                
                floor = Floor(
                    id=simple_id,
                    name=row.get("name") or simple_id,
                    building_id=building_id
                )
                floors.append(floor)
            return floors
        except Exception as e:
            print(f"Error getting floors: {str(e)}")
            raise

    async def get_building_devices(self, building_id: str) -> List[Device]:
        """Get all devices in a specific building"""
        full_building_uri = f"{self.BASE_URI}/{building_id}#{building_id}"
        query = f"""
        SELECT DISTINCT ?id ?type ?name ?location
        WHERE {{
            ?id a ?type .
            <{full_building_uri}> brick:hasPart* ?location .
            ?location brick:hasPart* ?id .
            FILTER EXISTS {{
                ?type rdfs:subClassOf* brick:Equipment
            }}
            OPTIONAL {{ ?id rdfs:label ?name }}
        }}
        ORDER BY ?id
        """
        try:
            result = await self.execute_query(query)
            devices = []
            for row in result["results"]:
                device_id = row["id"]
                simple_id = device_id.split('#')[-1]
                
                device = Device(
                    id=simple_id,
                    type=self._get_simple_id(row["type"]),
                    name=row.get("name", simple_id),
                    location=self._get_simple_id(row["location"]) if row.get("location") else None,
                    points=[]  # TODO: Points will be populated by a separate query if needed
                )
                devices.append(device)
            return devices
        except Exception as e:
            print(f"Error getting building devices: {str(e)}")
            raise

    async def get_floor_devices(self, building_id: str, floor_id: str) -> List[Device]:
        """Get all devices in a specific floor"""
        full_floor_uri = f"{self.BASE_URI}/{building_id}#{floor_id}"
        query = f"""
        SELECT DISTINCT ?id ?type ?name
        WHERE {{
            ?id a ?type .
            <{full_floor_uri}> brick:hasPart* ?id .
            FILTER EXISTS {{
                ?type rdfs:subClassOf* brick:Equipment
            }}
            OPTIONAL {{ ?id rdfs:label ?name }}
        }}
        ORDER BY ?id
        """
        try:
            result = await self.execute_query(query)
            devices = []
            for row in result["results"]:
                device_id = row["id"]
                simple_id = device_id.split('#')[-1]
                
                device = Device(
                    id=simple_id,
                    type=self._get_simple_id(row["type"]),
                    name=row.get("name", simple_id),
                    location=floor_id,
                    points=[]  # TODO: Points will be populated by a separate query if needed
                )
                devices.append(device)
            return devices
        except Exception as e:
            print(f"Error getting floor devices: {str(e)}")
            raise