import asyncio
from database import MongoDBService
from models import Product

async def add_real_products():
    """Add real product data to your MongoDB database"""
    
    # Connect to your MongoDB Atlas database
    db_service = MongoDBService()
    await db_service.connect()
    
    # Example real products - replace these with your actual products
    real_products = [
        {
            "product_id": "REAL001",
            "name": "Samsung Galaxy S24 Ultra",
            "category": "Smartphone",
            "brand": "Samsung",
            "price": 1199.99,
            "stock_quantity": 45,
            "features": ["5G", "200MP Camera", "S Pen", "Titanium Build"],
            "technical_details": {
                "supported_databases": [],
                "version": "Android 14",
                "min_system_requirements": "5G Network"
            },
            "ratings": {
                "average": 4.8,
                "review_count": 320
            },
            "screen_size": 6,
            "color_swatches": ["titanium black", "titanium gray", "titanium violet"]
        },
        {
            "product_id": "REAL002",
            "name": "MacBook Air M3 15-inch",
            "category": "Laptop",
            "brand": "Apple",
            "price": 1299.99,
            "stock_quantity": 25,
            "features": ["M3 Chip", "15-inch Liquid Retina", "18-hour Battery", "Touch ID"],
            "technical_details": {
                "supported_databases": ["MongoDB", "PostgreSQL", "MySQL"],
                "version": "macOS Sonoma",
                "min_system_requirements": "8GB RAM"
            },
            "ratings": {
                "average": 4.9,
                "review_count": 180
            },
            "screen_size": 15,
            "color_swatches": ["midnight", "starlight", "space gray"]
        },
        {
            "product_id": "REAL003",
            "name": "Sony A7R V Camera",
            "category": "Camera",
            "brand": "Sony",
            "price": 3899.99,
            "stock_quantity": 12,
            "features": ["61MP Sensor", "8K Video", "AI Autofocus", "5-axis Stabilization"],
            "technical_details": {
                "supported_databases": [],
                "version": "Firmware 2.0",
                "min_system_requirements": "CFexpress Card"
            },
            "ratings": {
                "average": 4.7,
                "review_count": 95
            },
            "screen_size": None,
            "color_swatches": ["black"]
        }
    ]
    
    try:
        # Insert real products
        result = await db_service.products_collection.insert_many(real_products)
        print(f"✅ Added {len(result.inserted_ids)} real products to your database")
        
        # Show what was added
        print("\n📦 Added Products:")
        for product in real_products:
            print(f"  • {product['name']} - ${product['price']} ({product['stock_quantity']} in stock)")
        
    except Exception as e:
        print(f"❌ Error adding products: {e}")
    finally:
        await db_service.disconnect()

async def clear_sample_data():
    """Remove sample data from database"""
    db_service = MongoDBService()
    await db_service.connect()
    
    try:
        # Remove sample products (SKU001-SKU008)
        result = await db_service.products_collection.delete_many({
            "product_id": {"$regex": "^SKU"}
        })
        print(f"🗑️  Removed {result.deleted_count} sample products")
    except Exception as e:
        print(f"❌ Error clearing sample data: {e}")
    finally:
        await db_service.disconnect()

async def show_database_contents():
    """Show what's currently in your database"""
    db_service = MongoDBService()
    await db_service.connect()
    
    try:
        products = await db_service.get_all_products()
        print(f"\n📊 Your Database Contents ({len(products)} products):")
        print("-" * 50)
        
        for product in products:
            print(f"ID: {product.product_id}")
            print(f"Name: {product.name}")
            print(f"Brand: {product.brand}")
            print(f"Category: {product.category}")
            print(f"Price: ${product.price}")
            print(f"Stock: {product.stock_quantity}")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Error reading database: {e}")
    finally:
        await db_service.disconnect()

async def main():
    print("🗄️  MongoDB Database Manager")
    print("=" * 40)
    print("1. Show current database contents")
    print("2. Add real products")
    print("3. Clear sample data")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        await show_database_contents()
    elif choice == "2":
        await add_real_products()
    elif choice == "3":
        await clear_sample_data()
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())

