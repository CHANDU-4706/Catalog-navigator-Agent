import re
from typing import Dict, Any, List, Optional, Tuple
from models import Product

class QueryParser:
    """Natural language query parser for product catalog"""
    
    # Whitelisted fields that can be queried
    WHITELISTED_FIELDS = {
        'category', 'brand', 'price', 'screen_size', 
        'color_swatches', 'features', 'stock_quantity', 'ratings'
    }
    
    def __init__(self):
        self.category_keywords = {
            'tv', 'television', 'smart tv', 'smart television',
            'laptop', 'notebook', 'computer',
            'phone', 'smartphone', 'mobile',
            'audio', 'speaker', 'headphone', 'earphone',
            'software', 'app', 'application',
            'home', 'kitchen', 'appliance'
        }
        
        self.brand_keywords = {
            'samsung', 'apple', 'sony', 'lg', 'dell', 'hp', 'lenovo',
            'bose', 'jbl', 'beats', 'microsoft', 'google', 'amazon'
        }
        
        self.color_keywords = {
            'black', 'white', 'red', 'blue', 'green', 'yellow', 'orange',
            'purple', 'pink', 'gray', 'grey', 'silver', 'gold', 'rose gold'
        }
        
        self.feature_keywords = {
            'ram', 'storage', 'battery', 'camera', 'display', 'screen',
            'bluetooth', 'wifi', 'wireless', 'waterproof', 'water resistant',
            'touch', 'voice', 'smart', 'ai', 'artificial intelligence',
            'ssd', 'hdd', 'hard drive', 'solid state'
        }

    def parse_query(self, query: str) -> Dict[str, Any]:
        """Parse natural language query and extract structured data"""
        query_lower = query.lower()
        parsed = {}
        
        # Extract category
        category = self._extract_category(query_lower)
        if category:
            parsed['category'] = category
            
        # Extract brand
        brand = self._extract_brand(query_lower)
        if brand:
            parsed['brand'] = brand
            
        # Extract price range
        price_range = self._extract_price_range(query_lower)
        if price_range:
            parsed['price'] = price_range
            
        # Extract screen size range
        screen_size_range = self._extract_screen_size_range(query_lower)
        if screen_size_range:
            parsed['screen_size'] = screen_size_range
            
        # Extract colors
        colors = self._extract_colors(query_lower)
        if colors:
            parsed['color_swatches'] = colors
            
        # Extract features
        features = self._extract_features(query_lower)
        if features:
            parsed['features'] = features
            
        # Extract stock quantity
        stock_range = self._extract_stock_range(query_lower)
        if stock_range:
            parsed['stock_quantity'] = stock_range
            
        # Extract ratings
        ratings = self._extract_ratings(query_lower)
        if ratings:
            parsed['ratings'] = ratings
            
        # Extract storage requirements
        storage = self._extract_storage(query_lower)
        if storage:
            parsed['storage'] = storage
            
        # Extract aggregation queries
        aggregation = self._extract_aggregation(query_lower)
        if aggregation:
            parsed['aggregation'] = aggregation
            
        return parsed

    def _extract_category(self, query: str) -> Optional[str]:
        """Extract category from query"""
        for keyword in self.category_keywords:
            if keyword in query:
                if 'tv' in keyword or 'television' in keyword:
                    return 'Smart TV'
                elif 'laptop' in keyword or 'notebook' in keyword:
                    return 'Laptop'
                elif 'phone' in keyword or 'smartphone' in keyword:
                    return 'Smartphone'
                elif 'audio' in keyword or 'speaker' in keyword:
                    return 'Audio'
                elif 'software' in keyword or 'app' in keyword:
                    return 'Software'
                elif 'home' in keyword or 'kitchen' in keyword:
                    return 'Home & Kitchen'
        return None

    def _extract_brand(self, query: str) -> Optional[str]:
        """Extract brand from query"""
        for brand in self.brand_keywords:
            if brand in query:
                return brand.title()
        return None

    def _extract_price_range(self, query: str) -> Optional[Dict[str, float]]:
        """Extract price range from query"""
        # Skip if query contains stock-related keywords
        if any(keyword in query.lower() for keyword in ['stock', 'units', 'quantity', 'inventory', 'available']):
            return None
        
        # Skip if query is ambiguous and doesn't contain price indicators
        if not any(indicator in query.lower() for indicator in ['$', 'price', 'cost', 'dollar', 'dollars']):
            # If it's ambiguous (just numbers without context), skip price parsing
            if re.search(r'\b(under|below|less than|over|above|more than|greater than|between)\s+\d+', query.lower()):
                if not any(context in query.lower() for context in ['$', 'price', 'cost', 'dollar']):
                    return None
            
        # Look for patterns like "under $1500", "between $100 and $500", "over $200"
        price_patterns = [
            r'under\s+\$?(\d+(?:\.\d+)?)',
            r'below\s+\$?(\d+(?:\.\d+)?)',
            r'less\s+than\s+\$?(\d+(?:\.\d+)?)',
            r'over\s+\$?(\d+(?:\.\d+)?)',
            r'above\s+\$?(\d+(?:\.\d+)?)',
            r'more\s+than\s+\$?(\d+(?:\.\d+)?)',
            r'greater\s+than\s+\$?(\d+(?:\.\d+)?)',
            r'prices?\s+greater\s+than\s+\$?(\d+(?:\.\d+)?)',
            r'price\s+(?:is\s+)?less\s+than\s+\$?(\d+(?:\.\d+)?)',
            r'price\s+(?:is\s+)?under\s+\$?(\d+(?:\.\d+)?)',
            r'price\s+(?:is\s+)?below\s+\$?(\d+(?:\.\d+)?)',
            r'price\s+(?:is\s+)?over\s+\$?(\d+(?:\.\d+)?)',
            r'price\s+(?:is\s+)?above\s+\$?(\d+(?:\.\d+)?)',
            r'between\s+\$?(\d+(?:\.\d+)?)\s+and\s+\$?(\d+(?:\.\d+)?)',
            r'from\s+\$?(\d+(?:\.\d+)?)\s+to\s+\$?(\d+(?:\.\d+)?)'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, query)
            if match:
                if 'between' in pattern or 'from' in pattern:
                    return {'$gte': float(match.group(1)), '$lte': float(match.group(2))}
                elif 'under' in pattern or 'below' in pattern or 'less' in pattern:
                    return {'$lt': float(match.group(1))}
                elif 'over' in pattern or 'above' in pattern or 'more' in pattern or 'greater' in pattern:
                    return {'$gt': float(match.group(1))}
        
        return None

    def _extract_screen_size_range(self, query: str) -> Optional[Dict[str, int]]:
        """Extract screen size range from query"""
        # Look for patterns like "between 55 and 65 inches", "55 inch", "over 50 inches"
        size_patterns = [
            r'(\d+)\s*inch',
            r'between\s+(\d+)\s+and\s+(\d+)\s*inch',
            r'from\s+(\d+)\s+to\s+(\d+)\s*inch',
            r'over\s+(\d+)\s*inch',
            r'under\s+(\d+)\s*inch'
        ]
        
        for pattern in size_patterns:
            match = re.search(pattern, query)
            if match:
                if 'between' in pattern or 'from' in pattern:
                    return {'$gte': int(match.group(1)), '$lte': int(match.group(2))}
                elif 'over' in pattern:
                    return {'$gt': int(match.group(1))}
                elif 'under' in pattern:
                    return {'$lt': int(match.group(1))}
                else:
                    # Exact size
                    size = int(match.group(1))
                    return {'$gte': size - 2, '$lte': size + 2}  # Allow some tolerance
        
        return None

    def _extract_colors(self, query: str) -> Optional[List[str]]:
        """Extract colors from query"""
        colors = []
        for color in self.color_keywords:
            if color in query:
                colors.append(color)
        return colors if colors else None

    def _extract_features(self, query: str) -> Optional[List[str]]:
        """Extract features from query"""
        features = []
        for feature in self.feature_keywords:
            if feature in query:
                features.append(feature)
        return features if features else None

    def _extract_stock_range(self, query: str) -> Optional[Dict[str, int]]:
        """Extract stock quantity range from query"""
        # Look for patterns like "in stock", "low stock", "out of stock"
        if 'in stock' in query:
            return {'$gt': 0}
        elif 'low stock' in query:
            return {'$lte': 10, '$gt': 0}
        elif 'out of stock' in query:
            return {'$eq': 0}
        
        # Look for numeric stock patterns
        stock_patterns = [
            r'stock\s+(?:is\s+)?less\s+than\s+(\d+)',
            r'stock\s+(?:is\s+)?under\s+(\d+)',
            r'stock\s+(?:is\s+)?below\s+(\d+)',
            r'stock\s+(?:is\s+)?more\s+than\s+(\d+)',
            r'stock\s+(?:is\s+)?over\s+(\d+)',
            r'stock\s+(?:is\s+)?above\s+(\d+)',
            r'stock\s+(?:is\s+)?greater\s+than\s+(\d+)',
            r'stock\s+(?:is\s+)?between\s+(\d+)\s+and\s+(\d+)',
            r'stock\s+(?:is\s+)?from\s+(\d+)\s+to\s+(\d+)',
            r'stock\s+(?:is\s+)?less\s+than\s+(\d+)\s+units?',
            r'stock\s+(?:is\s+)?under\s+(\d+)\s+units?',
            r'stock\s+(?:is\s+)?below\s+(\d+)\s+units?'
        ]
        
        # Handle ambiguous queries (when no explicit stock/price context)
        ambiguous_patterns = [
            r'(?:items?|products?)\s+(?:with\s+)?(?:stock\s+)?(?:less\s+than|under|below)\s+(\d+)',
            r'(?:items?|products?)\s+(?:with\s+)?(?:stock\s+)?(?:more\s+than|over|above|greater\s+than)\s+(\d+)',
            r'(?:items?|products?)\s+(?:with\s+)?(?:stock\s+)?(?:between)\s+(\d+)\s+and\s+(\d+)',
            r'(?:items?|products?)\s+(?:with\s+)?(?:stock\s+)?(?:from)\s+(\d+)\s+to\s+(\d+)'
        ]
        
        for pattern in stock_patterns:
            match = re.search(pattern, query)
            if match:
                if 'between' in pattern or 'from' in pattern:
                    return {'$gte': int(match.group(1)), '$lte': int(match.group(2))}
                elif 'less' in pattern or 'under' in pattern or 'below' in pattern:
                    return {'$lt': int(match.group(1))}
                elif 'more' in pattern or 'over' in pattern or 'above' in pattern or 'greater' in pattern:
                    return {'$gt': int(match.group(1))}
        
        # Handle ambiguous patterns (assume stock if no price context)
        for pattern in ambiguous_patterns:
            match = re.search(pattern, query)
            if match:
                if 'between' in pattern or 'from' in pattern:
                    return {'$gte': int(match.group(1)), '$lte': int(match.group(2))}
                elif 'less' in pattern or 'under' in pattern or 'below' in pattern:
                    return {'$lt': int(match.group(1))}
                elif 'more' in pattern or 'over' in pattern or 'above' in pattern or 'greater' in pattern:
                    return {'$gt': int(match.group(1))}
        
        return None

    def _extract_ratings(self, query: str) -> Optional[Dict[str, float]]:
        """Extract rating requirements from query"""
        # Look for patterns like "4+ stars", "highly rated", "5 star"
        rating_patterns = [
            r'(\d+(?:\.\d+)?)\+?\s*star',
            r'highly\s+rated',
            r'(\d+(?:\.\d+)?)\s*rating'
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, query)
            if match:
                if 'highly rated' in pattern:
                    return {'$gte': 4.0}
                else:
                    return {'$gte': float(match.group(1))}
        
        return None

    def _extract_storage(self, query: str) -> Optional[Dict[str, Any]]:
        """Extract storage requirements from query"""
        storage_patterns = [
            r'ssd',
            r'solid\s+state',
            r'hdd',
            r'hard\s+drive',
            r'(\d+)\s*gb\s*ssd',
            r'(\d+)\s*tb\s*ssd',
            r'(\d+)\s*gb\s*hdd',
            r'(\d+)\s*tb\s*hdd'
        ]
        
        for pattern in storage_patterns:
            if re.search(pattern, query):
                if 'ssd' in pattern or 'solid state' in pattern:
                    return {'type': 'SSD'}
                elif 'hdd' in pattern or 'hard drive' in pattern:
                    return {'type': 'HDD'}
        
        return None

    def _extract_aggregation(self, query: str) -> Optional[Dict[str, Any]]:
        """Extract aggregation queries like 'summarize', 'average', 'count'"""
        aggregation_patterns = [
            r'summarize\s+average\s+rating',
            r'average\s+rating',
            r'summarize\s+rating',
            r'count\s+products',
            r'total\s+products',
            r'summarize\s+products'
        ]
        
        for pattern in aggregation_patterns:
            if re.search(pattern, query):
                if 'average rating' in query or 'summarize rating' in query:
                    return {'type': 'average_rating'}
                elif 'count' in query or 'total' in query:
                    return {'type': 'count'}
        
        return None

    def build_mongo_query(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Build MongoDB query from parsed data"""
        mongo_query = {}
        
        for field, value in parsed.items():
            if field == 'category':
                mongo_query['category'] = {'$regex': value, '$options': 'i'}
            elif field == 'brand':
                mongo_query['brand'] = {'$regex': value, '$options': 'i'}
            elif field == 'price':
                mongo_query['price'] = value
            elif field == 'screen_size':
                mongo_query['screen_size'] = value
            elif field == 'color_swatches':
                mongo_query['color_swatches'] = {'$in': value}
            elif field == 'features':
                # Skip features query for storage-related queries since storage is in technical_details
                # Also skip for aggregation queries since features array is empty
                if 'storage' not in value or 'ssd' not in value:
                    if value and len(value) > 0:  # Check if features array is not empty
                        mongo_query['features'] = {'$in': value}
            elif field == 'stock_quantity':
                mongo_query['stock_quantity'] = value
            elif field == 'ratings':
                mongo_query['ratings.average'] = value
            elif field == 'storage':
                # Look for storage type in technical_details.storage
                if value.get('type') == 'SSD':
                    mongo_query['technical_details.storage'] = {'$regex': 'SSD', '$options': 'i'}
                elif value.get('type') == 'HDD':
                    mongo_query['technical_details.storage'] = {'$regex': 'HDD', '$options': 'i'}
        
        return mongo_query

    def generate_summary(self, parsed: Dict[str, Any], count: int) -> str:
        """Generate human-readable summary of results"""
        conditions = []
        
        if 'category' in parsed:
            conditions.append(f"category '{parsed['category']}'")
        if 'brand' in parsed:
            conditions.append(f"brand '{parsed['brand']}'")
        if 'price' in parsed:
            price = parsed['price']
            if '$gte' in price and '$lte' in price:
                conditions.append(f"price between ${price['$gte']} and ${price['$lte']}")
            elif '$lt' in price:
                conditions.append(f"price under ${price['$lt']}")
            elif '$gt' in price:
                conditions.append(f"price over ${price['$gt']}")
        if 'screen_size' in parsed:
            size = parsed['screen_size']
            if '$gte' in size and '$lte' in size:
                conditions.append(f"screen size between {size['$gte']} and {size['$lte']} inches")
            elif '$gt' in size:
                conditions.append(f"screen size over {size['$gt']} inches")
            elif '$lt' in size:
                conditions.append(f"screen size under {size['$lt']} inches")
        if 'color_swatches' in parsed:
            colors = ', '.join(parsed['color_swatches'])
            conditions.append(f"colors: {colors}")
        if 'features' in parsed:
            features = ', '.join(parsed['features'])
            conditions.append(f"features: {features}")
        if 'ratings' in parsed:
            rating = parsed['ratings']
            if '$gte' in rating:
                conditions.append(f"rating {rating['$gte']}+ stars")
        
        if conditions:
            condition_str = " and ".join(conditions)
            return f"Found {count} products matching: {condition_str}"
        else:
            return f"Found {count} products"

