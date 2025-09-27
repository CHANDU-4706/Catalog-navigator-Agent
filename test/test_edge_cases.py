import asyncio
from query_parser import QueryParser

async def test_edge_cases():
    """Test edge cases where stock and price might interfere"""
    
    parser = QueryParser()
    
    # Test edge cases that might cause interference
    edge_cases = [
        "products with stock less than $50",  # This might confuse price vs stock
        "find items under 50",  # Ambiguous - could be price or stock
        "show products between 10 and 30",  # Ambiguous
        "items greater than 100",  # Ambiguous
        "products with stock under $25",  # Mixed stock and price symbols
        "find stock less than 50 dollars"  # Mixed terminology
    ]
    
    for query in edge_cases:
        print(f"\n🔍 Testing: '{query}'")
        parsed = parser.parse_query(query)
        print(f"📝 Parsed: {parsed}")
        
        # Check for both price and stock
        has_price = 'price' in parsed
        has_stock = 'stock_quantity' in parsed
        
        if has_price and has_stock:
            print(f"❌ BOTH PRICE AND STOCK DETECTED!")
            print(f"   Price: {parsed['price']}")
            print(f"   Stock: {parsed['stock_quantity']}")
        elif has_price:
            print(f"💰 Only PRICE detected: {parsed['price']}")
        elif has_stock:
            print(f"📦 Only STOCK detected: {parsed['stock_quantity']}")
        else:
            print(f"❓ Neither price nor stock detected")
        
        mongo_query = parser.build_mongo_query(parsed)
        print(f"🗄️  MongoDB Query: {mongo_query}")
        print("-" * 60)

if __name__ == "__main__":
    asyncio.run(test_edge_cases())
