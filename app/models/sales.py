"""
Sales data models using Pydantic.
Author: Victor Velazquez - Invntio SRL
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class SalesItem(BaseModel):
    """Sales item model."""
    product: str = Field(..., description="Product name", min_length=1)
    quantity: int = Field(..., description="Quantity sold", ge=1)
    price: float = Field(..., description="Unit price", ge=0)
    
    @validator('product')
    def validate_product(cls, v):
        return v.strip()
    
    @property
    def total(self) -> float:
        """Calculate total for this item."""
        return self.quantity * self.price

class SalesReport(BaseModel):
    """Sales report model."""
    items: List[SalesItem]
    generated_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def total_revenue(self) -> float:
        """Calculate total revenue."""
        return sum(item.total for item in self.items)
    
    @property
    def total_items(self) -> int:
        """Calculate total items sold."""
        return sum(item.quantity for item in self.items)

class ReportResponse(BaseModel):
    """Response model for report generation."""
    filename: str
    generated_at: datetime
    items_count: int
    total_revenue: float
    download_url: str