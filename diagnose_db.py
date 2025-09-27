import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pprint import pprint

async def diagnose_database():
    """Diagnose what's actually in your MongoDB Atlas database"""
    
    # MongoDB Atlas connection string
    connection_string = "mongodb+srv://chandu:chandu2005@cluster0.nq0kb1u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(connection_string)
        
        # List all databases
        print("🗄️  Available Databases:")
        db_list = await client.list_database_names()
        for db_name in db_list:
            print(f"  • {db_name}")
        
        # Check catalog_navigator database
        db = client["catalog_navigator"]
        collections = await db.list_collection_names()
        print(f"\n📁 Collections in 'catalog_navigator' database:")
        for collection_name in collections:
            print(f"  • {collection_name}")
        
        # Check products collection
        products_collection = db["products"]
        total_count = await products_collection.count_documents({})
        print(f"\n📊 Total products in 'products' collection: {total_count}")
        
        # Show first few products
        print(f"\n🔍 First 5 products:")
        cursor = products_collection.find({}).limit(5)
        async for doc in cursor:
            print(f"  ID: {doc.get('product_id', 'N/A')}")
            print(f"  Name: {doc.get('name', 'N/A')}")
            print(f"  Brand: {doc.get('brand', 'N/A')}")
            print(f"  Category: {doc.get('category', 'N/A')}")
            print("  ---")
        
        # Check if there are other collections with products
        print(f"\n🔍 Checking other collections for products:")
        for collection_name in collections:
            if collection_name != "products":
                collection = db[collection_name]
                count = await collection.count_documents({})
                print(f"  • {collection_name}: {count} documents")
                
                # Check if this collection has product-like documents
                if count > 0:
                    sample = await collection.find_one({})
                    if sample and any(key in sample for key in ['name', 'product_id', 'brand', 'price']):
                        print(f"    ⚠️  This collection might contain products!")
                        print(f"    Sample: {sample.get('name', 'N/A')} - {sample.get('brand', 'N/A')}")
        
        # Check if products are in a different database
        print(f"\n🔍 Checking other databases for products:")
        for db_name in db_list:
            if db_name not in ['admin', 'local', 'config']:
                try:
                    other_db = client[db_name]
                    other_collections = await other_db.list_collection_names()
                    for collection_name in other_collections:
                        collection = other_db[collection_name]
                        count = await collection.count_documents({})
                        if count > 0:
                            sample = await collection.find_one({})
                            if sample and any(key in sample for key in ['name', 'product_id', 'brand', 'price']):
                                print(f"  • {db_name}.{collection_name}: {count} products found!")
                                print(f"    Sample: {sample.get('name', 'N/A')} - {sample.get('brand', 'N/A')}")
                except Exception as e:
                    print(f"  • {db_name}: Error accessing - {e}")
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(diagnose_database())

