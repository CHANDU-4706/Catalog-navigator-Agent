import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test_mongo_direct():
    """Test the MongoDB query directly"""
    
    connection_string = "mongodb+srv://chandu:chandu2005@cluster0.nq0kb1u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    try:
        client = AsyncIOMotorClient(connection_string)
        db = client["catalogDB"]
        products_collection = db["products"]
        
        # Test the exact query from the parser
        query = {
            "category": {"$regex": "Laptop", "$options": "i"},
            "features": {"$in": ["storage", "ssd"]},
            "technical_details.storage": {"$regex": "SSD", "$options": "i"}
        }
        
        print(f"🧪 Testing query: {query}")
        count = await products_collection.count_documents(query)
        print(f"📊 Results: {count}")
        
        # Test without features
        query_no_features = {
            "category": {"$regex": "Laptop", "$options": "i"},
            "technical_details.storage": {"$regex": "SSD", "$options": "i"}
        }
        
        print(f"\n🧪 Testing without features: {query_no_features}")
        count2 = await products_collection.count_documents(query_no_features)
        print(f"📊 Results: {count2}")
        
        if count2 > 0:
            cursor = products_collection.find(query_no_features).limit(3)
            async for doc in cursor:
                print(f"✅ {doc.get('name')} - Storage: {doc.get('technical_details', {}).get('storage', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_mongo_direct())
