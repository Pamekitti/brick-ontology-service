# Brick Backend Examples

This directory contains example scripts demonstrating how to use the Brick Backend API and generate building models.

## Files

- `query_examples.py`: Basic examples of querying buildings and executing SPARQL queries
- `device_examples.py`: Examples of working with devices and points
- `building_generator.py`: Utilities to generate Brick-compliant building descriptions

## Prerequisites

Install the required dependencies:
```bash
pip install requests rdflib brickschema
```

## Running the Examples

1. Make sure the Brick Backend server is running on `localhost:8000`

2. Run the example scripts:
```bash
python query_examples.py
python device_examples.py
```

3. Generate example buildings:
```bash
python building_generator.py
```

## Building Generator

The `building_generator.py` script provides utilities to generate Brick-compliant building descriptions in TTL format. It includes:

### Predefined Building Types
- Office buildings with multiple floors
- Laboratory buildings with specialized HVAC
- Hospital wings with critical zones
- Retail stores with open plans
- Multi-building campus settings

### Standard Equipment Templates
- Air Handler Units (AHU) with standard points
- Variable Air Volume (VAV) boxes
- Chillers and cooling systems
- Rooms and HVAC zones

### Custom Building Generation
You can create custom buildings using JSON configuration:

```json
{
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
    "chiller": true
}
```

## Example SPARQL Queries

### Find all VAV boxes
```sparql
SELECT ?vav ?label
WHERE {
    ?vav a brick:VAV .
    OPTIONAL { ?vav rdfs:label ?label }
}
```

### Find Temperature Sensors
```sparql
SELECT ?device ?label ?location
WHERE {
    ?device a brick:Temperature_Sensor .
    OPTIONAL { ?device rdfs:label ?label }
    OPTIONAL { 
        ?device brick:hasLocation ?location .
        ?location rdfs:label ?loc_label
    }
}
```

### Find Points Connected to VAVs
```sparql
SELECT ?device ?point ?point_type
WHERE {
    ?device a brick:VAV .
    ?device brick:hasPoint ?point .
    ?point a ?point_type .
}
``` 
