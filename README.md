# Brick Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-blue?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)](https://www.python.org)
[![RDFLib](https://img.shields.io/badge/RDFLib-6.0+-blue?style=flat)](https://rdflib.readthedocs.io)
[![BrickSchema](https://img.shields.io/badge/BrickSchema-0.7+-blue?style=flat)](https://brickschema.org)
[![Tests](https://img.shields.io/badge/Tests-Pytest-green?style=flat&logo=pytest)](https://docs.pytest.org)

This repository contains the backend server implementation for the Brick project, a RESTful API service that manages and queries building data using the Brick schema ontology.

## About Brick

Brick is a standardized ontology-based schema for describing building components, their relationships, and their operations. This backend implementation provides a FastAPI-based service that simplifies RDF data management.

The project includes:
- RESTful API for querying building data
- Building model generation utilities
- Support for multiple building types (office, lab, hospital, retail)
- Standard equipment templates (AHU, VAV, Chiller)

## Project Structure

```
├── app/            # Main application directory
│   ├── api/        # API endpoints and routes
│   ├── models/     # Data models and schemas
│   └── services/   # Business logic and services
├── examples/       # Example scripts and usage demos
│   ├── query_examples.py     # API query examples
│   ├── device_examples.py    # Device interaction examples
│   └── building_generator.py # Building model generator
├── tests/          # Test files
├── .assets/        # Asset files (TTL files)
├── .env           # Environment variables (not tracked in git)
├── requirements.txt # Python dependencies
└── run.py         # Application entry point
```

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env` (if available)
   - Configure your environment variables

## Running the Application

To start the server:
```bash
python run.py
```

## Examples

Check out the `examples/` directory for sample code and usage demonstrations:
- Basic API queries
- Working with devices and points
- SPARQL query examples
- Building data exploration
- Building model generation

The building generator supports various building types:
- Office buildings with multiple floors
- Laboratory buildings with specialized HVAC
- Hospital wings with critical zones
- Retail stores with open plans
- Multi-building campus settings

See [examples/README.md](examples/README.md) for detailed information.

## Testing

To run tests:
```bash
pytest
```

## Development

- The main application code is in the `app/` directory
- Tests are located in the `tests/` directory
- Environment variables should be configured in `.env`
- Building data is stored in TTL files in the `.assets/` directory
- Use the building generator to create new building models

## References

- [Brick Schema](https://brickschema.org/) - Official Brick Schema documentation
- [FastAPI](https://fastapi.tiangolo.com/) - FastAPI framework
- [RDFLib](https://rdflib.readthedocs.io/) - RDF library for Python
- [BrickSchema Python](https://github.com/BrickSchema/py-brickschema) - Python library for Brick
