import motor.motor_asyncio
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")

# Create MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]
product_collection = database.get_collection("products")
order_collection = database.get_collection("orders")
