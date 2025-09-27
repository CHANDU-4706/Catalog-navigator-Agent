from query_parser import QueryParser

# Test the query parser directly
parser = QueryParser()
query = "Find laptops with SSD storage"

print(f"Query: {query}")
parsed = parser.parse_query(query)
print(f"Parsed: {parsed}")

# Test the MongoDB query building
mongo_query = parser.build_mongo_query(parsed)
print(f"MongoDB Query: {mongo_query}")

# Test just the storage part
storage_only = {"storage": {"type": "SSD"}}
storage_query = parser.build_mongo_query(storage_only)
print(f"Storage only query: {storage_query}")
