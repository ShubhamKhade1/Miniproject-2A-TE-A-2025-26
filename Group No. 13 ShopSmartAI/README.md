# ShopSmart AI - Smart Market Basket Optimizer

A comprehensive web application that uses AI-powered algorithms to optimize your grocery shopping experience, providing personalized nutrition recommendations, budget optimization, and healthier food alternatives.

## Features

### 🧠 AI-Powered Features
- **Budget Optimizer**: Maximize nutrition while staying within your budget
- **Nutrition Filter**: Filter foods based on specific nutritional requirements
- **Healthier Swaps**: Find healthier alternatives using KNN algorithm
- **Smart Cart**: Manage shopping cart with real-time nutrition tracking

### 💰 Budget Management
- Monthly budget planning
- Family size considerations
- Cost optimization algorithms
- Savings calculations

### 🥗 Nutrition Intelligence
- Comprehensive food database
- Nutritional value analysis
- Dietary preference filtering
- Health score calculations

## Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No backend server required (demo mode with simulated data)

### Installation
1. Clone or download the project files
2. Open `index.html` in your web browser
3. Use the demo login or create an account to get started

### Demo Mode
For testing purposes, you can use the **Demo Login** button which will:
- Skip authentication
- Provide sample data
- Allow full functionality testing

## Usage Guide

### 1. Landing Page (index.html)
- **Login/Signup**: Access your account or create a new one
- **Demo Login**: Quick access for testing without authentication
- **Navigation**: Smooth scrolling to different sections

### 2. Dashboard (dashboard.html)
The dashboard is organized into several functional tabs:

#### Overview Tab
- Quick access to all features
- Statistics display (items saved, budget used)
- Navigation buttons to other tabs

#### Budget Optimizer Tab
- Enter monthly budget amount
- Select family size
- Get AI-optimized food recommendations
- View cost breakdown and savings

#### Items List Tab
- Browse comprehensive food database
- Search functionality
- Add items directly to cart
- View nutritional information

#### Nutrition Filter Tab
- Filter by calories, protein, fat, and sugars
- Quick preset filters (Low Calorie, High Protein, etc.)
- Real-time filtering results
- Add filtered items to cart

#### Healthier Swaps Tab
- Enter food item to find alternatives
- AI-powered similarity scoring
- Nutrition density comparisons
- Healthier option recommendations

#### Cart Tab
- View all selected items
- Adjust quantities
- Remove items
- Save basket for later
- Clear entire cart

### 3. Key Functions

#### Adding Items to Cart
- Click "Add to Cart" on any food item
- Items are automatically added with quantity 1
- Duplicate items increase quantity
- Real-time cart updates

#### Cart Management
- **Quantity Controls**: +/- buttons to adjust amounts
- **Remove Items**: Click × to remove individual items
- **Save Basket**: Store your cart for future reference
- **Clear Cart**: Remove all items (with confirmation)

#### Notifications
- Success messages for completed actions
- Error messages for failed operations
- Info messages for general updates
- Auto-dismissing after 3 seconds

## Technical Details

### Frontend Technologies
- **HTML5**: Semantic markup and structure
- **CSS3**: Tailwind CSS for styling
- **JavaScript**: ES6+ for functionality
- **Local Storage**: Cart and user data persistence

### Demo Data
The application includes comprehensive demo data:
- Sample food items with nutritional information
- Realistic pricing (in Indian Rupees ₹)
- Nutrition density scores
- Similarity calculations for swaps

### Responsive Design
- Mobile-first approach
- Responsive grid layouts
- Touch-friendly interface
- Cross-browser compatibility

## File Structure

```
ShopSmartAI/
├── index.html          # Landing page with authentication
├── dashboard.html      # Main application dashboard
├── auth.js            # Authentication and user management
├── dashboard.js       # Dashboard functionality (legacy)
└── README.md          # This documentation
```

## Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## Future Enhancements

- Backend API integration
- User authentication system
- Database connectivity
- Advanced AI algorithms
- Mobile app development
- Social sharing features

## Support

For questions or issues:
1. Check the browser console for error messages
2. Ensure JavaScript is enabled
3. Try refreshing the page
4. Use demo mode for testing

## License

This project is for educational and demonstration purposes.

---

**Note**: This is a frontend demonstration application. In production, it would connect to backend services for real data processing and user management.

