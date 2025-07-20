from pydantic import BaseModel,Field
from typing import List

class OrderItem(BaseModel):
    productId: str
    qty:int = Field(..., ge=1)

class OrderIn(BaseModel):
    userId: str
    items: List[OrderItem]
