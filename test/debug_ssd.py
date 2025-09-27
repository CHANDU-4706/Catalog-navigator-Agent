import asyncio
from query_parser import QueryParser
from motor.motor_asyncio import AsyncIOMotorClient

async def debug_ssd():
    """Debug the SSD query step by step"""
    
    parser = QueryParser()
    query = "Find laptops with SSD storage"
    
    print(f"🔍 Query: '{query}'")
    parsed = parser.parse_query(query)
    print(f"📝 Parsed: {parsed}")
    
    mongo_query = parser.build_mongo_query(parsed)
    print(f"🗄️  MongoDB Query: {mongo_query}")
    
    # Test just the storage part
    storage_query = {"technical_details.storage": {"$regex": "SSD", "$options": "i"}}
    print(f"\n🧪 Testing storage query: {storage_query}")
    
    connection_string = "mongodb+srv://chandu:chandu2005@cluster0.nq0kb1u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    try:
        client = AsyncIOMotorClient(connection_string)
        db = client["catalogDB"]
        products_collection = db["products"]
        
        # Test storage query only
        count = await products_collection.count_documents(storage_query)
        print(f"📊 Products with SSD storage: {count}")
        
        if count > 0:
            cursor = products_collection.find(storage_query).limit(3)
            async for doc in cursor:
                print(f"✅ {doc.get('name')} - Storage: {doc.get('technical_details', {}).get('storage', 'N/A')}")
        
        # Test category + storage query
        combined_query = {
            "category": {"$regex": "Laptop", "$options": "i"},
            "technical_details.storage": {"$regex": "SSD", "$options": "i"}
        }
        print(f"\n🧪 Testing combined query: {combined_query}")
        count2 = await products_collection.count_documents(combined_query)
        print(f"📊 Laptops with SSD storage: {count2}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(debug_ssd())
