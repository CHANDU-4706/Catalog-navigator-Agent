import asyncio
from catalog_navigator import CatalogNavigator

async def test_ssd_final():
    """Test SSD query with the actual Catalog Navigator"""
    
    navigator = CatalogNavigator()
    
    # Initialize
    if await navigator.initialize():
        print("✅ Navigator initialized successfully")
        
        # Test SSD query
        query = "Find laptops with SSD storage"
        print(f"\n🔍 Testing SSD query: '{query}'")
        
        response = await navigator.process_query(query)
        print(f"📊 Response count: {response.count}")
        print(f"📦 Sample products: {len(response.sample)}")
        
        if response.sample:
            print(f"\n📦 SSD Laptops Found:")
            for i, product in enumerate(response.sample, 1):
                print(f"{i}. {product.name}")
                storage_info = "N/A"
                if product.technical_details and hasattr(product.technical_details, 'storage'):
                    storage_info = getattr(product.technical_details, 'storage', 'N/A')
                print(f"   Storage: {storage_info}")
        else:
            print("❌ No SSD laptops found")
            
    else:
        print("❌ Failed to initialize navigator")

if __name__ == "__main__":
    asyncio.run(test_ssd_final())
