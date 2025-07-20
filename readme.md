# 🛍️ FastAPI E-commerce API (Products & Orders)

This is a lightweight FastAPI backend service that supports creating and reading products and orders

##  Features


- 📤 Create Product
- 📰 Get Products (with limit & offset)
- 📊 Create Order (linked to products)
- 📱 Get Orders by User ID (with pagination)


## Tech Stack

- 🐍 Python 3.11+
- ⚡ FastAPI (Python Framework)
- 🌐 Uvicorn (Web Server)
- 🍃 MongoDB (Atlas or local DB) 
- 🔁 Motor (async MongoDB driver)
- 🧪 Pydantic


## Prerequisites

- Node.js 16+
- npm or yarn
- Firebase project
- NewsAPI key

## Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/fastapi-ecommerce-api.git
cd fastapi-ecommerce-api

```

2. Create a virtual environment:
```bash
python -m venv venv
```


3. Activate the environment:
```bash
windows   : venv\Scripts\activate
MAC/Linux : source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt //file in root folder if not found install these (fastapi, uvicorn, motor,python-dotenv, pydantic)
```

5. Add a .env file:
```bash
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority

MONGO_DB_NAME=mydatabase

```

6. Run the SERVER:
```bash
//make sure you are in virtual environment.....

uvicorn main:app --reload
```

##  API Endpoints

### 📘 Products

1.  Create Product : http://localhost:8000/products 
HTTP method : POST
```bash
//request body
{
  "name": "T-Shirt",
  "price": 1499.50,
  "sizes": [
     {
     "size": "M", "quantity": 12 
     }
   ]
}
```
2. Get Products with name, size, Pagination(limit, offset) :
http://localhost:8000/products?name=t-shirt&size=M&limit=5

HTTP method : POST
```bash
//response
{
    "data": [
        {
            "id": "687b3c559e9e8a3d062a0f87",
            "name": "T-Shirt",
            "price": 499.99
        },
        {
            "id": "687b3cb99e9e8a3d062a0f88",
            "name": "Traditional Kurti",
            "price": 799.99
        }
    ],
    "page": {
        "next": 2,
        "limit": 2,
        "previous": 0
    }
}
```


### 📦 Orders

1.  Create Order : http://localhost:8000/orders 
HTTP method : POST
```bash
//request body
{
  "userId": "user_1", //custom user ID
  "items": [
    {
      "productId": "687b3d2b936bb4799cdf3b70", //make sure productID already exist in the DB else will throw exception response
      "qty": 5
    },
    {
      "productId": "687b4c27e50c4add82896b76",//make sure productID already exist in the DB else will throw exception response
      "qty": 2
    }
  ]
}
```
2. Get Orders by UserID & Pagination(limit, offset) :
http://localhost:8000/orders/user_1?limit=1

HTTP method : POST
```bash
//response
{
    "data": [
        {
            "id": "687b7204506c02913e23c2f6",
            "items": [
                {
                    "productDetails": {
                        "name": "T-Shirt",
                        "id": "687b3c559e9e8a3d062a0f87"
                    },
                    "qty": 2
                },
                {
                    "productDetails": {
                        "name": "Traditional Kurti",
                        "id": "687b3cb99e9e8a3d062a0f88"
                    },
                    "qty": 1
                }
            ],
            "total": 1799.97
        }
    ],
    "page": {
        "next": 1,
        "limit": 1,
        "previous": 0
    }
}
```



