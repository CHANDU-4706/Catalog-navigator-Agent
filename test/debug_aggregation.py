import re

query = "Summarize average rating of Smart TVs"
query_lower = query.lower()

print(f"Query: {query}")
print(f"Query lower: {query_lower}")

# Test the regex patterns
aggregation_patterns = [
    r'summarize\s+average\s+rating',
    r'average\s+rating',
    r'summarize\s+rating',
    r'count\s+products',
    r'total\s+products',
    r'summarize\s+products'
]

for i, pattern in enumerate(aggregation_patterns):
    match = re.search(pattern, query_lower)
    print(f"Pattern {i+1}: {pattern}")
    print(f"  Match: {match}")
    if match:
        print(f"  ✅ Found match!")
    print()
