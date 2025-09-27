import asyncio
from query_parser import QueryParser

async def debug_query():
    """Debug the query generation step by step"""
    
    parser = QueryParser()
    query = "Find laptops with SSD storage"
    
    print(f"🔍 Query: '{query}'")
    parsed = parser.parse_query(query)
    print(f"📝 Parsed: {parsed}")
    
    # Check each field individually
    for field, value in parsed.items():
        print(f"  {field}: {value} (type: {type(value)})")
        if field == 'features':
            print(f"    Features empty check: {not value or len(value) == 0}")
    
    mongo_query = parser.build_mongo_query(parsed)
    print(f"🗄️  Final MongoDB Query: {mongo_query}")

if __name__ == "__main__":
    asyncio.run(debug_query())
