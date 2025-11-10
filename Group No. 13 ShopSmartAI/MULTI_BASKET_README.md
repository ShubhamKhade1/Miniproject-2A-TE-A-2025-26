# 🛒 Multi-Basket Support for ShopSmart AI

## Overview
The ShopSmart AI application has been enhanced to support multiple saved baskets per user, enabling proper data collection for Apriori algorithm analysis. Each basket save now creates a new transaction in the database instead of replacing the previous one.

## 🚀 New Features

### 1. **Multiple Baskets Per User**
- Each "Save Basket" action creates a new row in `user_carts` table
- Unique `cart_id` for each saved basket
- Basket naming system for better organization
- Historical basket data preserved for analysis

### 2. **Enhanced Database Schema**
- Added `cart_type` field: 'active', 'saved', 'completed'
- Added `total_amount` and `item_count` for quick statistics
- Added performance indexes for better query speed
- Maintains all existing functionality

### 3. **Improved User Interface**
- Basket naming modal for better organization
- New "Saved Baskets" tab to view all saved baskets
- Load saved baskets back to cart functionality
- Enhanced cart management with basket history

### 4. **Apriori Algorithm Ready**
- Each basket represents a transaction
- Items in each basket represent itemset
- Perfect for market basket analysis
- Historical data collection for pattern mining

## 📁 Files Modified

### Backend Changes
- **`simple_app.py`**: Updated `save_cart` endpoint to create new baskets
- **`simple_database.sql`**: Enhanced schema with new columns and indexes
- **`update_database.py`**: Script to update existing databases

### Frontend Changes
- **`dashboard.html`**: Added basket naming modal and saved baskets tab
- **`test_multi_basket.py`**: Test script for multi-basket functionality

## 🛠️ Setup Instructions

### 1. Update Database Schema
```bash
# Run the database update script
python update_database.py
```

### 2. Start the Application
```bash
# Start the Flask backend
python simple_app.py

# Open the frontend in browser
# Navigate to index.html
```

### 3. Test Multi-Basket Functionality
```bash
# Run the test script
python test_multi_basket.py
```

## 🎯 How It Works

### Saving a Basket
1. User adds items to cart
2. Clicks "Save Basket" button
3. Basket naming modal appears
4. User enters basket name (e.g., "Weekly Groceries")
5. New row created in `user_carts` with unique `cart_id`
6. All items saved to `cart_items` linked to new `cart_id`

### Viewing Saved Baskets
1. Navigate to "Saved Baskets" tab
2. View all previously saved baskets
3. See basket details: name, date, items, total
4. Load any basket back to current cart
5. Delete unwanted baskets

### Database Structure
```sql
user_carts:
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- cart_name (VARCHAR)
- cart_type (ENUM: 'active', 'saved', 'completed')
- total_amount (DECIMAL)
- item_count (INT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

cart_items:
- id (PRIMARY KEY)
- cart_id (FOREIGN KEY to user_carts.id)
- food_name (VARCHAR)
- food_id (VARCHAR)
- price (DECIMAL)
- quantity (INT)
- [nutrition fields...]
- added_at (TIMESTAMP)
```

## 🔍 API Endpoints

### Save Basket
```http
POST /api/cart/save
Content-Type: application/json

{
    "user_id": 1,
    "cart_name": "Weekly Groceries",
    "items": [
        {
            "food": "Apples",
            "food_id": "apples_1",
            "price": 50.0,
            "quantity": 2,
            "caloric_value": 52,
            "protein": 0.3,
            "fat": 0.2,
            "nutrition_density": 8.5
        }
    ]
}
```

### Get Saved Baskets
```http
GET /api/cart/saved-baskets?user_id=1
```

## 📊 Apriori Algorithm Integration

### Transaction Data Format
Each saved basket represents a transaction:
```python
transactions = [
    ['Apples', 'Bananas', 'Milk'],      # Basket 1
    ['Chicken', 'Rice', 'Vegetables'],  # Basket 2
    ['Apples', 'Milk', 'Bread'],        # Basket 3
    # ... more baskets
]
```

### Example Usage
```python
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# Convert baskets to transaction format
# Run Apriori algorithm
frequent_itemsets = apriori(transactions_df, min_support=0.1, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)
```

## 🧪 Testing

### Manual Testing
1. Login to the application
2. Add items to cart from any tab
3. Click "Save Basket" and enter a name
4. Repeat with different items and names
5. Go to "Saved Baskets" tab to view all saved baskets
6. Test loading baskets back to cart

### Automated Testing
```bash
python test_multi_basket.py
```

## 🎨 User Interface

### New Elements
- **Basket Naming Modal**: Clean interface for naming baskets
- **Saved Baskets Tab**: Comprehensive view of all saved baskets
- **Load to Cart**: One-click loading of saved baskets
- **Basket Statistics**: Item count, total amount, creation date

### Keyboard Shortcuts
- `Ctrl+7`: Switch to Saved Baskets tab
- `Escape`: Close modals
- `Ctrl+1-6`: Navigate between tabs

## 🔧 Troubleshooting

### Common Issues
1. **Database Connection Error**: Check MySQL credentials in `simple_app.py`
2. **Modal Not Showing**: Check browser console for JavaScript errors
3. **Baskets Not Saving**: Verify user is logged in and cart is not empty
4. **API Errors**: Check Flask server is running on port 5000

### Debug Steps
1. Check browser console (F12) for errors
2. Verify database connection
3. Test API endpoints directly
4. Check user authentication status

## 📈 Benefits for Apriori Algorithm

### Data Collection
- **Multiple Transactions**: Each basket is a separate transaction
- **Item Sets**: Items in each basket form an itemset
- **User Segmentation**: Data can be analyzed per user or globally
- **Temporal Analysis**: Time-based pattern analysis possible

### Pattern Mining
- **Frequent Itemsets**: Find commonly bought together items
- **Association Rules**: Discover "if A then B" patterns
- **Recommendation Engine**: Suggest items based on basket history
- **Market Analysis**: Understand shopping patterns and trends

## 🚀 Future Enhancements

### Planned Features
- **Basket Categories**: Organize baskets by type (grocery, health, etc.)
- **Basket Sharing**: Share baskets with family members
- **Smart Recommendations**: AI-powered basket suggestions
- **Analytics Dashboard**: Visual insights into shopping patterns
- **Export Functionality**: Export basket data for external analysis

### Apriori Enhancements
- **Real-time Analysis**: Live pattern mining
- **Confidence Scoring**: Advanced rule confidence metrics
- **Seasonal Patterns**: Time-based pattern analysis
- **User Clustering**: Group users by shopping behavior

## 📝 Notes

- **Backward Compatibility**: All existing functionality preserved
- **Performance**: Optimized with database indexes
- **Scalability**: Designed to handle large numbers of baskets
- **Security**: User data properly isolated and protected

---

**Ready for Apriori Algorithm!** 🎉

Your ShopSmart AI application now collects proper transaction data for market basket analysis. Each saved basket represents a transaction, and items within each basket form itemsets - perfect for discovering shopping patterns and building recommendation systems.
