import asyncio
import json
from typing import Dict, Any
from models import QueryResponse, Product
from query_parser import QueryParser
from database import MongoDBService

class CatalogNavigator:
    """Main Catalog Navigator class that handles natural language queries"""
    
    def __init__(self, connection_string: str = None):
        self.parser = QueryParser()
        self.db_service = MongoDBService(connection_string)
        self.connected = False
    
    async def initialize(self):
        """Initialize the catalog navigator"""
        print("🚀 Initializing Catalog Navigator...")
        
        # Connect to database
        self.connected = await self.db_service.connect()
        if not self.connected:
            return False
        
        # Check existing data in database
        existing_count = await self.db_service.products_collection.count_documents({})
        print(f"📊 Found {existing_count} products in your MongoDB database")
        print("✅ Catalog Navigator ready!")
        return True
    
    async def process_query(self, query: str) -> QueryResponse:
        """Process a natural language query and return results"""
        if not self.connected:
            return QueryResponse(
                parsed={},
                mongo_query={},
                count=0,
                sample=[],
                summary="❌ Not connected to database"
            )
        
        try:
            
            parsed = self.parser.parse_query(query)
            
            
            mongo_query = self.parser.build_mongo_query(parsed)
            
            # Check if this is an aggregation query
            if 'aggregation' in parsed:
                if parsed['aggregation'].get('type') == 'average_rating':
                    # For aggregation queries, remove features filter since features array is empty
                    aggregation_query = {k: v for k, v in mongo_query.items() if k != 'features'}
                    # Calculate average rating
                    avg_rating, rating_count = await self.db_service.calculate_average_rating(aggregation_query)
                    products = []
                    count = rating_count
                    summary = f"Average rating: {avg_rating:.2f} (based on {rating_count} products with ratings)"
                else:
                    # Regular query
                    products, count = await self.db_service.query_products(mongo_query, limit=20)
                    summary = self.parser.generate_summary(parsed, count)
            else:
                # Regular query
                products, count = await self.db_service.query_products(mongo_query, limit=20)
                summary = self.parser.generate_summary(parsed, count)
            
            return QueryResponse(
                parsed=parsed,
                mongo_query=mongo_query,
                count=count,
                sample=products,
                summary=summary
            )
        except Exception as e:
            return QueryResponse(
                parsed={},
                mongo_query={},
                count=0,
                sample=[],
                summary=f"❌ Error processing query: {str(e)}"
            )
    
    def format_response(self, response: QueryResponse) -> str:
        """Format the response for CLI output"""
        output = []
        output.append("=" * 60)
        output.append("🔍 CATALOG NAVIGATOR RESULTS")
        output.append("=" * 60)
        output.append(f"📊 {response.summary}")
        output.append(f"📈 Total matches: {response.count}")
        output.append("")
        
        if response.parsed:
            output.append("🔍 Parsed Query:")
            for key, value in response.parsed.items():
                output.append(f"  • {key}: {value}")
            output.append("")
        
        if response.mongo_query:
            output.append("🗄️  MongoDB Query:")
            output.append(f"  {json.dumps(response.mongo_query, indent=2)}")
            output.append("")
        
        if response.sample:
            output.append("📦 Sample Products:")
            for i, product in enumerate(response.sample, 1):
                output.append(f"  {i}. {product.name}")
                output.append(f"     ID: {product.product_id}")
                output.append(f"     Brand: {product.brand}")
                output.append(f"     Category: {product.category}")
                output.append(f"     Price: ${product.price}")
                if product.screen_size:
                    output.append(f"     Screen Size: {product.screen_size}\"")
                if product.color_swatches:
                    output.append(f"     Colors: {', '.join(product.color_swatches)}")
                if product.features:
                    output.append(f"     Features: {', '.join(product.features[:3])}...")
                if product.ratings:
                    output.append(f"     Rating: {product.ratings.average}⭐ ({product.ratings.review_count} reviews)")
                output.append(f"     Stock: {product.stock_quantity} units")
                output.append("")
        else:
            output.append("❌ No products found matching your criteria")
        
        output.append("=" * 60)
        return "\n".join(output)
    
    async def run_cli(self):
        """Run the CLI interface"""
        print("🎯 Welcome to Catalog Navigator!")
        print("Type your natural language queries to search the product catalog.")
        print("Type 'quit', 'exit', or 'q' to stop.")
        print("Type 'help' for example queries.")
        print("=" * 60)
        
        while True:
            try:
                query = input("\n🔍 Enter your query: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif query.lower() == 'help':
                    self.show_help()
                    continue
                elif not query:
                    print("❌ Please enter a query.")
                    continue
                
                print("\n⏳ Processing query...")
                response = await self.process_query(query)
                print(self.format_response(response))
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        

        await self.db_service.disconnect()
    
    def show_help(self):
        """Show help with example queries"""
        examples = [
            "How many Smart TVs between 55 and 65 inches from Samsung?",
            "Show all laptops with 16GB RAM under $1500",
            "List all audio products with color black or white",
            "Find products with 4+ star ratings",
            "Show all smartphones from Apple",
            "List products with wireless features",
            "Find laptops with touch features under $2000"
        ]
        
        print("\n📚 Example Queries:")
        print("-" * 40)
        for i, example in enumerate(examples, 1):
            print(f"{i}. {example}")
        print("\n💡 Tips:")
        print("• Use specific categories: Smart TV, Laptop, Smartphone, Audio")
        print("• Mention brands: Samsung, Apple, Sony, LG, Dell")
        print("• Use price ranges: 'under $1000', 'between $500 and $1500'")
        print("• Specify screen sizes: '55 inch', 'between 13 and 16 inches'")
        print("• Mention colors: black, white, silver, gold")
        print("• Use features: wireless, touch, 4K, noise cancelling")

async def main():
    """Main function to run the Catalog Navigator"""
    navigator = CatalogNavigator()
    
    # Initialize the system
    if await navigator.initialize():
        # Run the CLI
        await navigator.run_cli()
    else:
        print("❌ Failed to initialize Catalog Navigator")

if __name__ == "__main__":
    asyncio.run(main())
