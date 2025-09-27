import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import List, Dict, Any, Optional
from models import Product
import asyncio

class MongoDBService:
    """MongoDB service for product catalog operations"""
    
    def __init__(self, connection_string: str = None, database_name: str = "catalogDB"):
        self.connection_string = connection_string or "mongodb+srv://chandu:chandu2005@cluster0.nq0kb1u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.database_name = database_name
        self.client = None
        self.db = None
        self.products_collection = None
        
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(self.connection_string)
            self.db = self.client[self.database_name]
            self.products_collection = self.db.products
            
            # Test connection
            await self.client.admin.command('ping')
            print(f"✅ Connected to MongoDB: {self.database_name}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            print("🔌 Disconnected from MongoDB")
    
    async def insert_sample_data(self):
        """Insert sample product data"""
        sample_products = [
            {
                "product_id": "SKU001",
                "name": "Samsung 55-inch Smart TV",
                "category": "Smart TV",
                "brand": "Samsung",
                "price": 899.99,
                "stock_quantity": 25,
                "features": ["4K", "HDR", "Smart TV", "Voice Control"],
                "technical_details": {
                    "supported_databases": ["MongoDB"],
                    "version": "2023.1",
                    "min_system_requirements": "WiFi"
                },
                "ratings": {
                    "average": 4.5,
                    "review_count": 120
                },
                "screen_size": 55,
                "color_swatches": ["black", "silver"]
            },
            {
                "product_id": "SKU002",
                "name": "Apple MacBook Pro 16-inch",
                "category": "Laptop",
                "brand": "Apple",
                "price": 2499.99,
                "stock_quantity": 15,
                "features": ["16GB RAM", "512GB SSD", "Touch Bar", "Retina Display"],
                "technical_details": {
                    "supported_databases": ["MongoDB", "PostgreSQL"],
                    "version": "macOS Monterey",
                    "min_system_requirements": "16GB RAM"
                },
                "ratings": {
                    "average": 4.8,
                    "review_count": 95
                },
                "screen_size": 16,
                "color_swatches": ["silver", "space gray"]
            },
            {
                "product_id": "SKU003",
                "name": "Sony WH-1000XM4 Headphones",
                "category": "Audio",
                "brand": "Sony",
                "price": 349.99,
                "stock_quantity": 50,
                "features": ["Noise Cancelling", "Wireless", "30-hour Battery", "Quick Charge"],
                "technical_details": {
                    "supported_databases": [],
                    "version": "1.0",
                    "min_system_requirements": "Bluetooth 5.0"
                },
                "ratings": {
                    "average": 4.6,
                    "review_count": 200
                },
                "screen_size": None,
                "color_swatches": ["black", "silver"]
            },
            {
                "product_id": "SKU004",
                "name": "LG 65-inch OLED Smart TV",
                "category": "Smart TV",
                "brand": "LG",
                "price": 1599.99,
                "stock_quantity": 8,
                "features": ["OLED", "4K", "HDR", "Smart TV", "WebOS"],
                "technical_details": {
                    "supported_databases": [],
                    "version": "WebOS 6.0",
                    "min_system_requirements": "WiFi"
                },
                "ratings": {
                    "average": 4.7,
                    "review_count": 85
                },
                "screen_size": 65,
                "color_swatches": ["black"]
            },
            {
                "product_id": "SKU005",
                "name": "Dell XPS 13 Laptop",
                "category": "Laptop",
                "brand": "Dell",
                "price": 1299.99,
                "stock_quantity": 30,
                "features": ["13-inch Display", "8GB RAM", "256GB SSD", "Windows 11"],
                "technical_details": {
                    "supported_databases": ["MongoDB", "MySQL"],
                    "version": "Windows 11",
                    "min_system_requirements": "8GB RAM"
                },
                "ratings": {
                    "average": 4.3,
                    "review_count": 150
                },
                "screen_size": 13,
                "color_swatches": ["silver", "rose gold"]
            },
            {
                "product_id": "SKU006",
                "name": "Bose QuietComfort 35 II",
                "category": "Audio",
                "brand": "Bose",
                "price": 299.99,
                "stock_quantity": 40,
                "features": ["Noise Cancelling", "Wireless", "20-hour Battery", "Google Assistant"],
                "technical_details": {
                    "supported_databases": [],
                    "version": "1.0",
                    "min_system_requirements": "Bluetooth"
                },
                "ratings": {
                    "average": 4.4,
                    "review_count": 180
                },
                "screen_size": None,
                "color_swatches": ["black", "silver"]
            },
            {
                "product_id": "SKU007",
                "name": "iPhone 14 Pro",
                "category": "Smartphone",
                "brand": "Apple",
                "price": 999.99,
                "stock_quantity": 60,
                "features": ["5G", "A16 Bionic", "Pro Camera", "Face ID"],
                "technical_details": {
                    "supported_databases": [],
                    "version": "iOS 16",
                    "min_system_requirements": "5G Network"
                },
                "ratings": {
                    "average": 4.9,
                    "review_count": 300
                },
                "screen_size": 6,
                "color_swatches": ["space black", "silver", "gold", "deep purple"]
            },
            {
                "product_id": "SKU008",
                "name": "Samsung Galaxy S23",
                "category": "Smartphone",
                "brand": "Samsung",
                "price": 799.99,
                "stock_quantity": 45,
                "features": ["5G", "Snapdragon 8 Gen 2", "50MP Camera", "Wireless Charging"],
                "technical_details": {
                    "supported_databases": [],
                    "version": "Android 13",
                    "min_system_requirements": "5G Network"
                },
                "ratings": {
                    "average": 4.6,
                    "review_count": 250
                },
                "screen_size": 6,
                "color_swatches": ["black", "white", "green", "purple"]
            }
        ]
        
        try:
            # Check if sample data already exists
            existing_sample = await self.products_collection.find_one({"product_id": "SKU001"})
            if existing_sample:
                print("✅ Sample data already exists in database")
                return True
            
            # Insert sample data
            result = await self.products_collection.insert_many(sample_products)
            print(f"✅ Inserted {len(result.inserted_ids)} sample products")
            return True
        except Exception as e:
            print(f"❌ Failed to insert sample data: {e}")
            return False
    
    async def query_products(self, mongo_query: Dict[str, Any], limit: int = 20) -> tuple[List[Product], int]:
        """Query products from MongoDB"""
        try:
            # Get total count
            count = await self.products_collection.count_documents(mongo_query)
            
            # Get sample products
            cursor = self.products_collection.find(mongo_query).limit(limit)
            products = []
            
            async for doc in cursor:
                # Convert MongoDB document to Product model
                product = Product(**doc)
                products.append(product)
            
            return products, count
        except Exception as e:
            print(f"❌ Query failed: {e}")
            return [], 0
    
    async def get_all_products(self) -> List[Product]:
        """Get all products for debugging"""
        try:
            cursor = self.products_collection.find({})
            products = []
            
            async for doc in cursor:
                product = Product(**doc)
                products.append(product)
            
            return products
        except Exception as e:
            print(f"❌ Failed to get all products: {e}")
            return []
    
    async def calculate_average_rating(self, mongo_query: Dict[str, Any]) -> tuple[float, int]:
        """Calculate average rating for products matching the query"""
        try:
            cursor = self.products_collection.find(mongo_query)
            total_rating = 0
            count = 0
            
            async for doc in cursor:
                if doc.get('ratings', {}).get('average'):
                    total_rating += doc['ratings']['average']
                    count += 1
            
            if count > 0:
                return total_rating / count, count
            else:
                return 0.0, 0
        except Exception as e:
            print(f"❌ Failed to calculate average rating: {e}")
            return 0.0, 0
