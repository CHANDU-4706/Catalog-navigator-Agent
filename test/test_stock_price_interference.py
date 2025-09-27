import asyncio
from query_parser import QueryParser

async def test_stock_price_interference():
    """Test if stock queries are interfering with price parsing"""
    
    parser = QueryParser()
    
    # Test queries that might have interference
    test_queries = [
        "products with stock less than 50",
        "find items with stock greater than 20",
        "show products with stock between 10 and 30",
        "products with stock under 25",
        "items with stock above 100"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        parsed = parser.parse_query(query)
        print(f"📝 Parsed: {parsed}")
        
        # Check if price is being incorrectly parsed
        if 'price' in parsed:
            print(f"❌ PRICE INTERFERENCE: {parsed['price']}")
        else:
            print(f"✅ No price interference")
        
        mongo_query = parser.build_mongo_query(parsed)
        print(f"🗄️  MongoDB Query: {mongo_query}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_stock_price_interference())
