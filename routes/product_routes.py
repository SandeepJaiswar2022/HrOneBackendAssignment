from fastapi import Query
from models.product import ProductOut
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from pymongo import ASCENDING
from fastapi import APIRouter, HTTPException,status
from models.product import ProductIn
from db.mongo import product_collection


router = APIRouter()

@router.post("/products",status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductIn):
    product_dict = product.model_dump()
    result = await product_collection.insert_one(product_dict)
    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Product not created")
    # return {"id": str(result.inserted_id), "message": "Product created successfully"}
    return {"id": str(result.inserted_id)}



@router.get("/products", response_model=dict)
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0)
):
    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    if size:
        query["sizes.size"] = size

    cursor = product_collection.find(query).sort("_id", ASCENDING).skip(offset).limit(limit)
    products_raw = await cursor.to_list(length=limit)

    # Format output
    products = [
        {"id": str(prod["_id"]), "name": prod["name"], "price": prod["price"]}
        for prod in products_raw
    ]

    next_offset = offset + limit if len(products) == limit else None
    previous_offset = max(0, offset - limit)

    return {
        "data": products,
        "page": {
            "next": next_offset,
            "limit": len(products),
            "previous": previous_offset
        }
    }
