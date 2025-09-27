import asyncio
from catalog_navigator import CatalogNavigator

async def test_rating_navigator():
    """Test average rating query with Catalog Navigator"""
    
    navigator = CatalogNavigator()
    
    # Initialize
    if await navigator.initialize():
        print("✅ Navigator initialized successfully")
        
        # Test average rating query
        query = "Summarize average rating of Smart TVs"
        print(f"\n🔍 Testing rating query: '{query}'")
        
        response = await navigator.process_query(query)
        print(f"📊 Response count: {response.count}")
        print(f"📝 Summary: {response.summary}")
        
        # Show the formatted response
        print(f"\n📝 Formatted Response:")
        print(navigator.format_response(response))
            
    else:
        print("❌ Failed to initialize navigator")

if __name__ == "__main__":
    asyncio.run(test_rating_navigator())
