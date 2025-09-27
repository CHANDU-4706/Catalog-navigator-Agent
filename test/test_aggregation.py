from query_parser import QueryParser

# Test the aggregation parser
parser = QueryParser()
query = "Summarize average rating of Smart TVs"

print(f"🔍 Query: '{query}'")
parsed = parser.parse_query(query)
print(f"📝 Parsed: {parsed}")

# Check if aggregation is detected
if 'aggregation' in parsed:
    print(f"✅ Aggregation detected: {parsed['aggregation']}")
else:
    print("❌ No aggregation detected")

mongo_query = parser.build_mongo_query(parsed)
print(f"🗄️  MongoDB Query: {mongo_query}")
