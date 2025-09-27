# Catalog Navigator

An intelligent assistant that helps product managers and marketing teams query an e-commerce product catalog stored in MongoDB using natural language queries.

## Features

- 🗣️ **Natural Language Processing**: Query products using plain English
- 🔍 **Smart Query Parsing**: Extracts categories, brands, prices, features, and more
- 📊 **MongoDB Integration**: Direct queries to MongoDB with optimized filters
- 🎯 **Whitelisted Fields**: Secure querying with only allowed fields
- 📱 **CLI Interface**: Easy-to-use command-line interface
- 📈 **Rich Results**: Detailed product information with ratings and stock

## Supported Query Types

### Categories
- Smart TV, Laptop, Smartphone, Audio, Software, Home & Kitchen

### Brands
- Samsung, Apple, Sony, LG, Dell, HP, Lenovo, Bose, JBL, Microsoft, Google, Amazon

### Price Ranges
- "under $1000", "between $500 and $1500", "over $2000"

### Screen Sizes
- "55 inch", "between 13 and 16 inches", "over 50 inches"

### Colors
- black, white, silver, gold, space gray, rose gold, etc.

### Features
- wireless, touch, 4K, noise cancelling, voice control, etc.

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start MongoDB:**
   ```bash
   # Make sure MongoDB is running on localhost:27017
   # Or update the connection string in the code
   ```

3. **Run the Catalog Navigator:**
   ```bash
   python catalog_navigator.py
   ```

## Usage Examples

```
🔍 Enter your query: How many Smart TVs between 55 and 65 inches from Samsung?

🔍 Enter your query: Show all laptops with 16GB RAM under $1500

🔍 Enter your query: List all audio products with color black or white

🔍 Enter your query: Find products with 4+ star ratings

🔍 Enter your query: Show all smartphones from Apple
```

## Project Structure

```
catalog_navigator/
├── catalog_navigator.py    # Main CLI application
├── models.py               # Pydantic data models
├── query_parser.py         # Natural language query parser
├── database.py             # MongoDB service
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Query Processing Flow

1. **Parse Query**: Extract structured data from natural language
2. **Build MongoDB Query**: Convert parsed data to MongoDB filter
3. **Execute Query**: Search the product catalog
4. **Format Results**: Return human-readable summary with samples

## Sample Product Schema

```json
{
  "product_id": "SKU789012",
  "name": "E-commerce Product Navigator",
  "category": "Software",
  "brand": "Innovate AI Co.",
  "price": 499.99,
  "stock_quantity": 150,
  "features": ["natural_language_query", "data_integration"],
  "technical_details": {
    "supported_databases": ["MongoDB", "DocumentDB"],
    "version": "1.2.0",
    "min_system_requirements": "8GB RAM"
  },
  "ratings": {
    "average": 4.5,
    "review_count": 85
  },
  "screen_size": 55,
  "color_swatches": ["black", "white"]
}
```

## Commands

- `help` - Show example queries
- `quit`, `exit`, `q` - Exit the application

## Requirements

- Python 3.8+
- MongoDB 4.4+
- FastAPI, Motor, Pydantic, PyMongo

## License

MIT License

