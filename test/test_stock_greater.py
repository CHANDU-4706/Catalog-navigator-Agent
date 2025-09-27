import asyncio
from catalog_navigator import CatalogNavigator

async def test_stock_greater():
    """Test stock greater than 50 query"""
    
    navigator = CatalogNavigator()
    
    # Initialize
    if await navigator.initialize():
        print("✅ Navigator initialized successfully")
        
        # Test stock greater than 50 query
        query = "List products with stock greater than 50"
        print(f"\n🔍 Testing stock query: '{query}'")
        
        response = await navigator.process_query(query)
        print(f"📊 Response count: {response.count}")
        print(f"📦 Sample products: {len(response.sample)}")
        
        if response.sample:
            print(f"\n📦 Products with Stock > 50:")
            for i, product in enumerate(response.sample, 1):
                print(f"{i}. {product.name} - Stock: {product.stock_quantity}")
        else:
            print("❌ No products found with stock > 50")
            
        # Show the formatted response
        print(f"\n📝 Formatted Response:")
        print(navigator.format_response(response))
            
    else:
        print("❌ Failed to initialize navigator")

if __name__ == "__main__":
    asyncio.run(test_stock_greater())
