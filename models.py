from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

class TechnicalDetails(BaseModel):
    supported_databases: Optional[List[str]] = None
    version: Optional[str] = None
    min_system_requirements: Optional[str] = None

class Ratings(BaseModel):
    average: float
    review_count: int

class Product(BaseModel):
    product_id: str
    name: str
    category: str
    brand: str
    price: float
    stock_quantity: int
    features: List[str] = []
    technical_details: Optional[TechnicalDetails] = None
    ratings: Optional[Ratings] = None
    screen_size: Optional[int] = None
    color_swatches: List[str] = []

class QueryResponse(BaseModel):
    parsed: Dict[str, Any]
    mongo_query: Dict[str, Any]
    count: int
    sample: List[Product]
    summary: str

class CatalogNavigatorRequest(BaseModel):
    query: str

