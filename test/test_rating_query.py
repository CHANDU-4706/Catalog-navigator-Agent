import asyncio
from query_parser import QueryParser
from motor.motor_asyncio import AsyncIOMotorClient

async def test_rating_query():
    """Test the average rating query for Smart TVs"""
    
    # Test the parser
    parser = QueryParser()
    query = "Summarize average rating of Smart TVs"
    
    print(f"🔍 Testing Query: '{query}'")
    parsed = parser.parse_query(query)
    print(f"📝 Parsed: {parsed}")
    
    mongo_query = parser.build_mongo_query(parsed)
    print(f"🗄️  MongoDB Query: {mongo_query}")
    
    # Check Smart TVs in database
    connection_string = "mongodb+srv://chandu:chandu2005@cluster0.nq0kb1u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    try:
        client = AsyncIOMotorClient(connection_string)
        db = client["catalogDB"]
        products_collection = db["products"]
        
        # Get all Smart TVs
        print(f"\n📊 Smart TVs in Database:")
        cursor = products_collection.find({"category": {"$regex": "Smart TV", "$options": "i"}})
        smart_tvs = []
        async for doc in cursor:
            smart_tvs.append(doc)
        
        print(f"Found {len(smart_tvs)} Smart TVs")
        
        if smart_tvs:
            # Calculate average rating
            total_rating = 0
            count_with_ratings = 0
            
            for tv in smart_tvs:
                print(f"\n📺 {tv.get('name', 'N/A')}")
                print(f"   Rating: {tv.get('ratings', {}).get('average', 'N/A')}")
                print(f"   Review Count: {tv.get('ratings', {}).get('review_count', 'N/A')}")
                
                if tv.get('ratings', {}).get('average'):
                    total_rating += tv['ratings']['average']
                    count_with_ratings += 1
            
            if count_with_ratings > 0:
                average_rating = total_rating / count_with_ratings
                print(f"\n📊 Average Rating of Smart TVs: {average_rating:.2f}")
                print(f"📈 Based on {count_with_ratings} Smart TVs with ratings")
            else:
                print("❌ No Smart TVs with ratings found")
        
        # Test the actual query
        print(f"\n🧪 Testing Smart TV Query:")
        count = await products_collection.count_documents(mongo_query)
        print(f"Products matching query: {count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_rating_query())
