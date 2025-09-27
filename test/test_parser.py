from query_parser import QueryParser

# Test the price parsing
parser = QueryParser()

test_queries = [
    "prices greater than 100000 dollars",
    "products over $100000",
    "items above 100000",
    "show me products over 100000 dollars"
]

for query in test_queries:
    print(f"Query: '{query}'")
    parsed = parser.parse_query(query)
    print(f"Parsed: {parsed}")
    mongo_query = parser.build_mongo_query(parsed)
    print(f"MongoDB Query: {mongo_query}")
    print("-" * 50)
