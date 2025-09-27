import asyncio
from catalog_navigator import CatalogNavigator

async def test_simple():
    """Test the Catalog Navigator with a simple query"""
    
    navigator = CatalogNavigator()
    
    # Initialize
    if await navigator.initialize():
        print("✅ Navigator initialized successfully")
        
        # Test a simple query
        query = "list all products"
        print(f"\n🔍 Testing query: '{query}'")
        
        response = await navigator.process_query(query)
        print(f"📊 Response count: {response.count}")
        print(f"📦 Sample products: {len(response.sample)}")
        
        if response.sample:
            print(f"\n📦 First product: {response.sample[0].name}")
        else:
            print("❌ No products found")
            
    else:
        print("❌ Failed to initialize navigator")

if __name__ == "__main__":
    asyncio.run(test_simple())
