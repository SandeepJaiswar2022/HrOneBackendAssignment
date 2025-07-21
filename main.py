from fastapi import FastAPI,status
from routes.product_routes import router as product_router
from routes.order_routes import router as order_router

app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "Welcome to the E-commerce FAST_API! Append Order or Product to the URL to access respective endpoints."}

# Routes
app.include_router(product_router) # product router
app.include_router(order_router)  # order router
