import asyncio
from catalog_navigator import CatalogNavigator

async def test_stock_query():
    """Test the stock query with Catalog Navigator"""
    
    navigator = CatalogNavigator()
    
    # Initialize
    if await navigator.initialize():
        print("✅ Navigator initialized successfully")
        
        # Test stock query
        query = "show the product where the stock is less than 50 units"
        print(f"\n🔍 Testing stock query: '{query}'")
        
        response = await navigator.process_query(query)
        print(f"📊 Response count: {response.count}")
        print(f"📦 Sample products: {len(response.sample)}")
        
        if response.sample:
            print(f"\n📦 Sample Products:")
            for i, product in enumerate(response.sample[:3], 1):
                print(f"{i}. {product.name} - Stock: {product.stock_quantity}")
        else:
            print("❌ No products found")
            
        # Show the formatted response
        print(f"\n📝 Formatted Response:")
        print(navigator.format_response(response))
            
    else:
        print("❌ Failed to initialize navigator")

if __name__ == "__main__":
    asyncio.run(test_stock_query())
