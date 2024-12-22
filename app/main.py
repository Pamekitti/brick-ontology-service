from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import buildings, query, floors, devices
from app.config import settings
from app.services.brick import BrickService

app = FastAPI(
    title="Brick API",
    description="REST API for interacting with Brick ontology",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Initialize the Brick graph at application startup"""
    try:
        # This will trigger the singleton initialization
        brick_service = BrickService()
        print(f"Application started with {brick_service.get_triple_count()} triples in graph")
    except Exception as e:
        print(f"Failed to initialize Brick graph: {str(e)}")
        raise

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query.router, prefix="/api/v1/query", tags=["query"])
app.include_router(buildings.router, prefix="/api/v1/buildings", tags=["building"])
app.include_router(floors.router, prefix="/api/v1/floors", tags=["floor"])
app.include_router(devices.router, prefix="/api/v1/devices", tags=["device"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 