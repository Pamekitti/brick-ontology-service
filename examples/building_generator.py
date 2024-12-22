"""
Building Generator for Brick Schema

This script provides utilities to generate Brick-compliant building descriptions
in TTL format for various types of buildings including offices, labs, hospitals,
and retail spaces.
"""

from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD
from typing import Dict, List, Optional
import json
import os

# Templates for standard equipment points
AHU_POINTS = [
    {
        "name": "Supply_Air_Temp",
        "type": "Supply_Air_Temperature_Sensor",
        "label": "Supply Air Temp"
    },
    {
        "name": "Return_Air_Temp",
        "type": "Return_Air_Temperature_Sensor",
        "label": "Return Air Temp"
    },
    {
        "name": "Mixed_Air_Temp",
        "type": "Mixed_Air_Temperature_Sensor",
        "label": "Mixed Air Temp"
    },
    {
        "name": "Outside_Air_Temp",
        "type": "Outside_Air_Temperature_Sensor",
        "label": "Outside Air Temp"
    },
    {
        "name": "Supply_Air_Pressure",
        "type": "Supply_Air_Static_Pressure_Sensor",
        "label": "Supply Air Pressure"
    },
    {
        "name": "CCV",
        "type": ["Cooling_Command", "Valve_Command"],
        "label": "CCV"
    },
    {
        "name": "Cooling_Valve_Output",
        "type": ["Cooling_Command", "Valve_Command"],
        "label": "Cooling Valve Output"
    },
    {
        "name": "Supply_Air_Temp_Setpoint",
        "type": "Supply_Air_Temperature_Setpoint",
        "label": "Supply Air Temp Setpoint"
    }
]

VAV_POINTS = [
    {
        "name": "Zone_Air_Temp",
        "type": "Zone_Air_Temperature_Sensor",
        "label": "Zone Air Temp"
    },
    {
        "name": "Zone_Air_Temp_Setpoint",
        "type": "Zone_Air_Temperature_Setpoint",
        "label": "Zone Air Temp Setpoint"
    },
    {
        "name": "Zone_Air_Control_Temp",
        "type": "Zone_Air_Temperature_Setpoint",
        "label": "Zone Air Control Temp"
    },
    {
        "name": "Zone_Air_Damper_Command",
        "type": "Damper_Position_Setpoint",
        "label": "Zone Air Damper Command"
    },
    {
        "name": "Zone_Heating_Mode",
        "type": "Heating_Command",
        "label": "Zone Heating Mode"
    },
    {
        "name": "Zone_Percent_Air_Flow",
        "type": "Air_Flow_Sensor",
        "label": "Zone Percent Air Flow"
    },
    {
        "name": "Zone_Supply_Air_Flow",
        "type": "Supply_Air_Flow_Sensor",
        "label": "Zone Supply Air Flow"
    },
    {
        "name": "Zone_Supply_Air_Temp",
        "type": "Supply_Air_Temperature_Sensor",
        "label": "Zone Supply Air Temp"
    },
    {
        "name": "Zone_Reheat_Valve_Command",
        "type": "Command",
        "label": "Zone Reheat Valve Command"
    }
]

CHILLER_POINTS = [
    {
        "name": "Building_Chilled_Water_Supply_Temp",
        "type": "Chilled_Water_Supply_Temperature_Sensor",
        "label": "Building Chilled Water Supply Temp"
    },
    {
        "name": "Building_Chilled_Water_Return_Temp",
        "type": "Chilled_Water_Return_Temperature_Sensor",
        "label": "Building Chilled Water Return Temp"
    },
    {
        "name": "Loop_Chilled_Water_Supply_Temp",
        "type": "Chilled_Water_Supply_Temperature_Sensor",
        "label": "Loop Chilled Water Supply Temp"
    },
    {
        "name": "Loop_Chilled_Water_Return_Temp",
        "type": "Chilled_Water_Return_Temperature_Sensor",
        "label": "Loop Chilled Water Return Temp"
    },
    {
        "name": "ECONOMIZER",
        "type": "Damper_Position_Command",
        "label": "ECONOMIZER"
    }
]

class BrickGenerator:
    def __init__(self, building_name: str):
        self.g = Graph()
        # Define namespaces
        self.BRICK = Namespace("https://brickschema.org/schema/Brick#")
        self.BUILDING = Namespace(f"http://buildsys.org/ontologies/{building_name}#")
        self.REF = Namespace("https://brickschema.org/schema/Brick/ref#")
        self.UNIT = Namespace("http://qudt.org/vocab/unit/")
        
        # Bind prefixes
        self.g.bind("brick", self.BRICK)
        self.g.bind(building_name, self.BUILDING)
        self.g.bind("ref", self.REF)
        self.g.bind("unit", self.UNIT)
        self.g.bind("owl", OWL)
        self.g.bind("rdfs", RDFS)
        
        self.building_name = building_name

    def add_point(self, equipment_uri: URIRef, point: Dict, equipment_type: str, equipment_id: str):
        """Helper method to add a point to equipment"""
        point_uri = self.BUILDING[f"{self.building_name}.{equipment_type}.{equipment_id}.{point['name']}"]
        
        # Handle multiple types
        if isinstance(point['type'], list):
            for type_name in point['type']:
                self.g.add((point_uri, RDF.type, self.BRICK[type_name]))
        else:
            self.g.add((point_uri, RDF.type, self.BRICK[point['type']]))
            
        self.g.add((equipment_uri, self.BRICK.hasPoint, point_uri))
        self.g.add((point_uri, RDFS.label, Literal(f"{self.building_name}.{equipment_type}.{equipment_id}.{point['label']}")))
        
        return point_uri

    def create_ahu(self, ahu_id: str, feeds_vavs: List[str], fed_by: Optional[str] = None):
        """Create AHU using standard template"""
        ahu = self.BUILDING[f"AHU{ahu_id}"]
        self.g.add((ahu, RDF.type, self.BRICK.Air_Handler_Unit))
        
        # Add points and relationships
        for point in AHU_POINTS:
            self.add_point(ahu, point, "AHU", f"AHU{ahu_id}")
        
        for vav in feeds_vavs:
            self.g.add((ahu, self.BRICK.feeds, self.BUILDING[vav]))
        
        if fed_by:
            self.g.add((ahu, self.BRICK.isFedBy, self.BUILDING[fed_by]))
            
        return ahu

    def create_building_system(self, config: Dict):
        """Create entire building system from configuration"""
        # Create building
        building = self.BUILDING[self.building_name]
        self.g.add((building, RDF.type, self.BRICK.Building))
        if 'area' in config:
            area_blank = URIRef(f"{str(building)}_area")
            self.g.add((building, self.BRICK.area, area_blank))
            self.g.add((area_blank, self.BRICK.hasUnits, self.UNIT.FT_2))
            self.g.add((area_blank, self.BRICK.value, Literal(f"{config['area']}^^{XSD.integer}")))

        # Create floors
        for floor_number in config['floors']:
            floor = self.BUILDING[f"floor{floor_number}"]
            self.g.add((floor, RDF.type, self.BRICK.Floor))
            self.g.add((building, self.BRICK.hasPart, floor))

        # Create AHUs and VAVs
        for ahu_config in config['ahus']:
            self.create_ahu(
                ahu_config['id'],
                ahu_config['feeds_vavs'],
                ahu_config.get('fed_by')
            )
            
            for vav_id in ahu_config['feeds_vavs']:
                room_id = vav_id.replace('VAVRM', '')
                self.create_vav_and_room(vav_id, room_id, f"AHU{ahu_config['id']}", floor)

        if 'chiller' in config:
            self.create_chiller()

    def create_vav_and_room(self, vav_id: str, room_id: str, ahu_id: str, floor: URIRef):
        """Create VAV and associated room"""
        vav = self.BUILDING[vav_id]
        self.g.add((vav, RDF.type, self.BRICK.VAV))
        
        for point in VAV_POINTS:
            self.add_point(vav, point, f"ZONE.{ahu_id}.RM{room_id}", "")

        # Create damper
        damper = self.BUILDING[f"damper{vav_id}"]
        self.g.add((damper, RDF.type, self.BRICK.Damper))
        self.g.add((damper, self.BRICK.isPartOf, vav))

        # Create room and zone
        room = self.BUILDING[f"RM{room_id}_room"]
        self.g.add((room, RDF.type, self.BRICK.Room))
        self.g.add((floor, self.BRICK.hasPart, room))

        zone = self.BUILDING[f"RM{room_id}"]
        self.g.add((zone, RDF.type, self.BRICK.HVAC_Zone))
        self.g.add((zone, self.BRICK.hasPart, room))
        self.g.add((vav, self.BRICK.feeds, zone))

    def create_chiller(self):
        """Create chiller with standard points"""
        chiller = self.BUILDING["chiller"]
        self.g.add((chiller, RDF.type, self.BRICK.Chiller))
        
        for point in CHILLER_POINTS:
            self.add_point(chiller, point, "CHW", "")

    def save_model(self, filename: str):
        """Save the model to a TTL file"""
        # Ensure .assets directory exists
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.assets')
        os.makedirs(assets_dir, exist_ok=True)
        
        # Save to .assets directory
        filepath = os.path.join(assets_dir, filename)
        with open(filepath, 'w') as f:
            f.write(self.g.serialize(format='turtle'))
        print(f"Saved model to {filepath}")

def generate_office_building():
    """Generate a typical office building with multiple floors"""
    config = {
        "building_name": "office_building_1",
        "area": 150000,
        "floors": ["1", "2", "3"],
        "ahus": [
            {
                "id": "01",
                "feeds_vavs": [
                    "VAVRM101", "VAVRM102", "VAVRM103", "VAVRM104",
                    "VAVRM105", "VAVRM106", "VAVRM107", "VAVRM108"
                ],
                "fed_by": "chiller1"
            },
            {
                "id": "02",
                "feeds_vavs": [
                    "VAVRM201", "VAVRM202", "VAVRM203", "VAVRM204",
                    "VAVRM205", "VAVRM206", "VAVRM207", "VAVRM208"
                ],
                "fed_by": "chiller1"
            }
        ],
        "chiller": True
    }
    
    generator = BrickGenerator(config["building_name"])
    generator.create_building_system(config)
    generator.save_model("office_building_1.ttl")

def generate_lab_building():
    """Generate a laboratory building with specialized HVAC requirements"""
    config = {
        "building_name": "lab_building_1",
        "area": 75000,
        "floors": ["1", "2"],
        "ahus": [
            {
                "id": "01",
                "feeds_vavs": ["VAVRM101", "VAVRM102", "VAVRM103"],
                "fed_by": "chiller1"
            },
            {
                "id": "02",
                "feeds_vavs": ["VAVRM201", "VAVRM202", "VAVRM203"],
                "fed_by": "chiller1"
            },
            {
                "id": "03",
                "feeds_vavs": ["VAVRM301", "VAVRM302"],
                "fed_by": "chiller2"
            }
        ],
        "chiller": True
    }
    
    generator = BrickGenerator(config["building_name"])
    generator.create_building_system(config)
    generator.save_model("lab_building_1.ttl")

def generate_hospital_wing():
    """Generate a hospital wing with critical HVAC zones"""
    config = {
        "building_name": "hospital_wing_east",
        "area": 100000,
        "floors": ["1", "2", "3", "4"],
        "ahus": [
            {
                "id": "01",
                "feeds_vavs": [
                    "VAVRM_OR101", "VAVRM_OR102", 
                    "VAVRM_OR103", "VAVRM_OR104"
                ],
                "fed_by": "chiller1"
            },
            {
                "id": "02",
                "feeds_vavs": [
                    "VAVRM_PR201", "VAVRM_PR202", "VAVRM_PR203",
                    "VAVRM_PR204", "VAVRM_PR205", "VAVRM_PR206"
                ],
                "fed_by": "chiller1"
            },
            {
                "id": "03",
                "feeds_vavs": [
                    "VAVRM_ICU301", "VAVRM_ICU302",
                    "VAVRM_ICU303", "VAVRM_ICU304"
                ],
                "fed_by": "chiller2"
            }
        ],
        "chiller": True
    }
    
    generator = BrickGenerator(config["building_name"])
    generator.create_building_system(config)
    generator.save_model("hospital_wing_east.ttl")

def generate_retail_store():
    """Generate a retail store with open-plan HVAC zones"""
    config = {
        "building_name": "retail_store_1",
        "area": 50000,
        "floors": ["1"],
        "ahus": [
            {
                "id": "01",
                "feeds_vavs": [
                    "VAVRM_SHOP1", "VAVRM_SHOP2", 
                    "VAVRM_SHOP3", "VAVRM_SHOP4"
                ],
                "fed_by": "chiller1"
            },
            {
                "id": "02",
                "feeds_vavs": [
                    "VAVRM_STORAGE1", "VAVRM_STORAGE2",
                    "VAVRM_OFFICE1", "VAVRM_OFFICE2"
                ],
                "fed_by": "chiller1"
            }
        ],
        "chiller": True
    }
    
    generator = BrickGenerator(config["building_name"])
    generator.create_building_system(config)
    generator.save_model("retail_store_1.ttl")

def generate_multi_building_campus():
    """Generate multiple buildings in a campus setting"""
    buildings = [
        {
            "building_name": "campus_office_1",
            "area": 120000,
            "floors": ["1", "2", "3", "4"],
            "ahus": [
                {
                    "id": "01",
                    "feeds_vavs": [f"VAVRM{i:03d}" for i in range(101, 111)],
                    "fed_by": "chiller1"
                },
                {
                    "id": "02",
                    "feeds_vavs": [f"VAVRM{i:03d}" for i in range(201, 211)],
                    "fed_by": "chiller1"
                }
            ],
            "chiller": True
        },
        {
            "building_name": "campus_lab_1",
            "area": 80000,
            "floors": ["1", "2"],
            "ahus": [
                {
                    "id": "01",
                    "feeds_vavs": [f"VAVRM_LAB{i:03d}" for i in range(1, 6)],
                    "fed_by": "chiller1"
                }
            ],
            "chiller": True
        }
    ]
    
    for building in buildings:
        generator = BrickGenerator(building["building_name"])
        generator.create_building_system(building)
        generator.save_model(f"{building['building_name']}.ttl")

def generate_building_from_json(json_file: str):
    """Generate building model from JSON configuration file"""
    with open(json_file, 'r') as f:
        config = json.load(f)
    
    generator = BrickGenerator(config["building_name"])
    generator.create_building_system(config)
    generator.save_model(f"{config['building_name']}.ttl")

if __name__ == "__main__":
    # Generate all example buildings
    generate_office_building()
    generate_lab_building()
    generate_hospital_wing()
    generate_retail_store()
    generate_multi_building_campus()
    
    # Example of custom building from config
    sample_config = {
        "building_name": "custom_building_1",
        "area": 75000,
        "floors": ["1", "2"],
        "ahus": [
            {
                "id": "01",
                "feeds_vavs": ["VAVRM101", "VAVRM102", "VAVRM103"],
                "fed_by": "chiller1"
            }
        ],
        "chiller": True
    }
    
    # Save sample config
    with open('sample_building_config.json', 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    # Generate from config
    generate_building_from_json('sample_building_config.json') 