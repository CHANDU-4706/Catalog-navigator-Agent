from query_parser import QueryParser

# Test the stock parsing
parser = QueryParser()

test_queries = [
    "show the product where the stock is less than 50 units",
    "products with stock less than 50",
    "items with stock under 50",
    "show me products with stock below 50 units"
]

for query in test_queries:
    print(f"Query: '{query}'")
    parsed = parser.parse_query(query)
    print(f"Parsed: {parsed}")
    mongo_query = parser.build_mongo_query(parsed)
    print(f"MongoDB Query: {mongo_query}")
    print("-" * 50)
