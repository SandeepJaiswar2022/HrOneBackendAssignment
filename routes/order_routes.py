from fastapi import APIRouter, HTTPException, status
from models.order_model import OrderIn
from bson import ObjectId
from db.mongo import order_collection, product_collection


router = APIRouter()


@router.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderIn):
    try:
        # Convert productId strings to ObjectId
        product_object_ids = [ObjectId(item.productId) for item in order.items]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product Does not Exist : One or more productId are invalid"
        )

    # Query to get existing products
    existing_products = await product_collection.find(
        {"_id": {"$in": product_object_ids}}
    ).to_list(length=len(product_object_ids))

    # Extract found ObjectIds
    existing_ids = {str(product["_id"]) for product in existing_products}

    # Compare with original string productIds
    original_ids = [item.productId for item in order.items]
    missing_ids = [pid for pid in original_ids if pid not in existing_ids]

    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid productId(s): {', '.join(missing_ids)}"
        )

    # Proceed with inserting the order
    order_dict = order.model_dump()
    result = await order_collection.insert_one(order_dict)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Order not created")

    return {"id": str(result.inserted_id)}


@router.get("/orders/{user_id}")
async def get_orders(user_id: str, limit: int = 3, offset: int = 0):
    orders_cursor = order_collection.find({"userId": user_id}).skip(offset).limit(limit)

    orders = []
    all_product_ids = []

    raw_orders = []
    async for order in orders_cursor:
        raw_orders.append(order)
        for item in order["items"]:
            all_product_ids.append(ObjectId(item["productId"]))

    # Remove duplicates
    unique_product_ids = list(set(all_product_ids))

    # Batch fetch all product data
    products_cursor = product_collection.find({"_id": {"$in": unique_product_ids}})
    product_map = {}
    async for product in products_cursor:
        product_map[str(product["_id"])] = {
            "name": product.get("name"),
            "id": str(product.get("_id")),
            "price": product.get("price", 0)
        }

    # Now build final orders response
    for order in raw_orders:
        items = []
        total = 0
        for item in order["items"]:
            product_id = item["productId"]
            product = product_map.get(product_id)
            if product:
                items.append({
                    "productDetails": {
                        "name": product["name"],
                        "id": product["id"]
                    },
                    "qty": item["qty"]
                })
                total += product["price"] * item["qty"]

        orders.append({
            "id": str(order["_id"]),
            "items": items,
            "total": total
        })

    total_orders = await order_collection.count_documents({"userId": user_id})
    next_offset = offset + limit if offset + limit < total_orders else None

    return {
        "data": orders,
        "page": {
            "next": next_offset,
            "limit": len(orders),
            "previous": max(0, offset - limit)
        }
    }