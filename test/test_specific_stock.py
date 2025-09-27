import asyncio
from catalog_navigator import CatalogNavigator

async def test_specific_stock():
    """Test specific stock queries that might be problematic"""
    
    navigator = CatalogNavigator()
    
    # Initialize
    if await navigator.initialize():
        print("✅ Navigator initialized successfully")
        
        # Test specific stock queries that might have issues
        specific_queries = [
            "products with stock quantity greater than 50",
            "show me items with stock under 25",
            "find products where stock is more than 100",
            "list all products with stock above 30",
            "products with stock less than 10 units",
            "show products with stock between 5 and 15"
        ]
        
        for query in specific_queries:
            print(f"\n🔍 Testing: '{query}'")
            response = await navigator.process_query(query)
            print(f"📊 Results: {response.count} products")
            
            if response.sample:
                print(f"📦 Sample products:")
                for i, product in enumerate(response.sample[:2], 1):
                    print(f"  {i}. {product.name} - Stock: {product.stock_quantity}")
            else:
                print("❌ No products found")
            
            print("-" * 40)
            
    else:
        print("❌ Failed to initialize navigator")

if __name__ == "__main__":
    asyncio.run(test_specific_stock())
