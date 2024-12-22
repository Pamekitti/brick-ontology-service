from fastapi import APIRouter, HTTPException
from typing import Dict
from pydantic import BaseModel

from app.services.brick import BrickService

router = APIRouter()
brick_service = BrickService()

class SPARQLQuery(BaseModel):
    query: str

@router.post("/", response_model=Dict)
async def execute_query(query: SPARQLQuery):
    """Execute a SPARQL query against the Brick graph"""
    try:
        return await brick_service.execute_query(query.query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query error: {str(e)}")

@router.get("/triples/count")
async def count_triples() -> Dict:
    """Get the total number of triples in the graph"""
    return {"count": brick_service.get_triple_count()}

@router.get("/namespaces")
async def get_namespaces() -> Dict:
    """Get all namespaces defined in the graph"""
    return {"namespaces": brick_service.get_namespaces()} 