import asyncio
from query_parser import QueryParser
from motor.motor_asyncio import AsyncIOMotorClient

async def test_ssd_query():
    """Test the SSD storage query"""
    
    # Test the parser
    parser = QueryParser()
    query = "Find laptops with 'SSD' storage."
    
    print(f"🔍 Testing Query: '{query}'")
    parsed = parser.parse_query(query)
    print(f"📝 Parsed: {parsed}")
    
    mongo_query = parser.build_mongo_query(parsed)
    print(f"🗄️  MongoDB Query: {mongo_query}")
    
    # Check what features are available in the database
    connection_string = "mongodb+srv://chandu:chandu2005@cluster0.nq0kb1u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    try:
        client = AsyncIOMotorClient(connection_string)
        db = client["catalogDB"]
        products_collection = db["products"]
        
        # Check laptop products and their features
        print(f"\n📊 Laptop Products in Database:")
        cursor = products_collection.find({"category": {"$regex": "Laptop", "$options": "i"}})
        laptops = []
        async for doc in cursor:
            laptops.append(doc)
        
        print(f"Found {len(laptops)} laptops")
        
        for laptop in laptops:
            print(f"\n💻 {laptop.get('name', 'N/A')}")
            print(f"   Features: {laptop.get('features', [])}")
            print(f"   Technical Details: {laptop.get('technical_details', {})}")
        
        # Test the actual query
        print(f"\n🧪 Testing SSD Query:")
        count = await products_collection.count_documents(mongo_query)
        print(f"Products matching query: {count}")
        
        if count > 0:
            cursor = products_collection.find(mongo_query).limit(3)
            async for doc in cursor:
                print(f"✅ {doc.get('name')} - Features: {doc.get('features', [])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_ssd_query())
