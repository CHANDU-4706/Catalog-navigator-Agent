import asyncio
from catalog_navigator import CatalogNavigator

async def test_stock_queries():
    """Test various stock queries to identify issues"""
    
    navigator = CatalogNavigator()
    
    # Initialize
    if await navigator.initialize():
        print("✅ Navigator initialized successfully")
        
        # Test different stock queries
        stock_queries = [
            "show products with stock less than 50",
            "find products with stock greater than 20",
            "list products with stock between 10 and 30",
            "show me products with low stock",
            "find products in stock"
        ]
        
        for query in stock_queries:
            print(f"\n🔍 Testing: '{query}'")
            response = await navigator.process_query(query)
            print(f"📊 Results: {response.count} products")
            print(f"📝 Summary: {response.summary}")
            
            if response.sample:
                print(f"📦 Sample products:")
                for i, product in enumerate(response.sample[:3], 1):
                    print(f"  {i}. {product.name} - Stock: {product.stock_quantity}")
            else:
                print("❌ No products found")
            
            print("-" * 50)
            
    else:
        print("❌ Failed to initialize navigator")

if __name__ == "__main__":
    asyncio.run(test_stock_queries())
