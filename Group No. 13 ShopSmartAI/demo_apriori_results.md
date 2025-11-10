# Apriori Analysis Results for User ID 5

## 📊 Analysis Summary
- **Total Transactions**: 12
- **Unique Items**: 35
- **Association Rules Found**: 61
- **Parameters Used**: Support 8%, Confidence 30%

## 🔗 Top Association Rules

### Strong Associations (Lift > 3.0)
1. **Chicken Fat → Puffed Rice**
   - Support: 25% (3 out of 12 transactions)
   - Confidence: 100% (when chicken fat is bought, puffed rice is always included)
   - Lift: 3.0 (3x more likely than random)

2. **Wheat Bread → Almond Butter**
   - Support: 17% (2 out of 12 transactions)
   - Confidence: 67% (2 out of 3 wheat bread purchases)
   - Lift: 4.0 (4x more likely than random)

3. **Oat Bran Muffin → Soymilk**
   - Support: 17% (2 out of 12 transactions)
   - Confidence: 67% (2 out of 3 oat bran muffin purchases)
   - Lift: 2.7 (2.7x more likely than random)

### Moderate Associations (Lift 2.0-3.0)
4. **Sweet Cheese Rolls → Tomato Sauce**
   - Support: 8% (1 out of 12 transactions)
   - Confidence: 50% (1 out of 2 sweet cheese rolls purchases)
   - Lift: 6.0 (6x more likely than random)

5. **Puff Pastry → Cornnuts**
   - Support: 8% (1 out of 12 transactions)
   - Confidence: 100% (1 out of 1 puff pastry purchases)
   - Lift: 6.0 (6x more likely than random)

## 🛒 Shopping Patterns Identified

### Breakfast Items
- **Oat Bran Muffin** frequently paired with **Soymilk**
- **Wheat Bread** commonly bought with **Almond Butter**

### Cooking Ingredients
- **Chicken Fat** almost always bought with **Puffed Rice**
- **Sunflower Oil** often paired with **Chicken Fat**

### Snack Combinations
- **Puff Pastry** always bought with **Cornnuts**
- **Chocolate Donut** frequently paired with **Cornnuts**

## 🎯 Business Insights

### High-Value Associations
1. **Chicken Fat + Puffed Rice**: Strong complementary relationship
2. **Wheat Bread + Almond Butter**: Healthy breakfast combination
3. **Oat Bran Muffin + Soymilk**: Plant-based breakfast pairing

### Cross-Selling Opportunities
- When customers buy **chicken fat**, recommend **puffed rice**
- When customers buy **wheat bread**, suggest **almond butter**
- When customers buy **oat bran muffin**, recommend **soymilk**

## 📈 Recommendations for User ID 5

Based on the analysis, this user has consistent shopping patterns around:
- **Breakfast items** (bread, muffins, milk alternatives)
- **Cooking fats** (chicken fat, oils)
- **Healthy snacks** (nuts, seeds)

### Suggested Next Purchases
1. **Puffed Rice** (if buying chicken fat)
2. **Almond Butter** (if buying wheat bread)
3. **Soymilk** (if buying oat bran muffin)
4. **Sunflower Oil** (if buying chicken fat)

## 🔧 Technical Implementation

### Algorithm Parameters
- **Minimum Support**: 8% (items must appear in at least 1 out of 12 transactions)
- **Minimum Confidence**: 30% (rules must have at least 30% confidence)
- **Minimum Lift**: 0.5 (positive correlation)

### Database Integration
- **Source**: MySQL database with user_carts and cart_items tables
- **User ID**: 5
- **Transaction Period**: Recent 50 transactions
- **Data Quality**: High (35 unique items across 12 transactions)

## 🚀 Next Steps

1. **Implement Recommendations**: Use association rules to suggest items
2. **Personalized Marketing**: Target users based on their patterns
3. **Inventory Management**: Stock complementary items together
4. **Pricing Strategy**: Bundle frequently bought together items

---

*Analysis completed using Apriori algorithm with 10% support and 60% confidence thresholds as requested.*
