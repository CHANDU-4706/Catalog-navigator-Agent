import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from query_parser import QueryParser

async def test_stock_query():
    """Test the actual stock query that the system generates"""
    
    # Test the parser
    parser = QueryParser()
    query = "show the product where the stock is less than 50 units"
    
    print(f"🔍 Testing Query: '{query}'")
    parsed = parser.parse_query(query)
    print(f"📝 Parsed: {parsed}")
    
    mongo_query = parser.build_mongo_query(parsed)
    print(f"🗄️  MongoDB Query: {mongo_query}")
    
    # Test the actual database query
    connection_string = "mongodb+srv://chandu:chandu2005@cluster0.nq0kb1u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    try:
        client = AsyncIOMotorClient(connection_string)
        db = client["catalogDB"]
        products_collection = db["products"]
        
        # Execute the query
        count = await products_collection.count_documents(mongo_query)
        print(f"📊 Query Results: {count} products found")
        
        # Get sample products
        cursor = products_collection.find(mongo_query).limit(5)
        products = []
        async for doc in cursor:
            products.append(doc)
        
        print(f"\n📦 Sample Products:")
        for i, product in enumerate(products, 1):
            print(f"{i}. {product.get('name', 'N/A')} - Stock: {product.get('stock_quantity', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_stock_query())
