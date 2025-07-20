from pydantic import BaseModel, Field
from typing import List


class SizeModel(BaseModel):
    size: str
    quantity: int


class ProductIn(BaseModel):
    name: str
    price: float
    sizes: List[SizeModel]


class ProductOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    price: float
