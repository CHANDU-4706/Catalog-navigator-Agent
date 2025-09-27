import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_products():
    """Check the actual structure of products in your database"""
    
    connection_string = "mongodb+srv://chandu:chandu2005@cluster0.nq0kb1u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    try:
        client = AsyncIOMotorClient(connection_string)
        db = client["catalogDB"]
        products_collection = db["products"]
        
        # Get a sample product to see its structure
        sample_product = await products_collection.find_one({})
        print("📦 Sample Product Structure:")
        print("-" * 50)
        for key, value in sample_product.items():
            print(f"{key}: {value}")
        
        # Check if stock_quantity field exists
        print(f"\n🔍 Checking for stock_quantity field:")
        count_with_stock = await products_collection.count_documents({"stock_quantity": {"$exists": True}})
        print(f"Products with 'stock_quantity' field: {count_with_stock}")
        
        # Check for other possible stock field names
        stock_fields = ["stock", "quantity", "inventory", "units", "available"]
        for field in stock_fields:
            count = await products_collection.count_documents({field: {"$exists": True}})
            if count > 0:
                print(f"Products with '{field}' field: {count}")
        
        # Test the actual query
        print(f"\n🧪 Testing stock query:")
        stock_query = {"stock_quantity": {"$lt": 50}}
        count = await products_collection.count_documents(stock_query)
        print(f"Products with stock_quantity < 50: {count}")
        
        # Show some products with stock info
        print(f"\n📊 Products with stock information:")
        cursor = products_collection.find({}).limit(3)
        async for doc in cursor:
            print(f"ID: {doc.get('product_id', 'N/A')}")
            print(f"Name: {doc.get('name', 'N/A')}")
            print(f"Stock fields: {[k for k in doc.keys() if 'stock' in k.lower() or 'quantity' in k.lower()]}")
            print("-" * 30)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_products())
