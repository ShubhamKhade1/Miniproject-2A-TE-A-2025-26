# 🚀 ShopSmart AI - Simple Login Backend Setup

## 📋 Prerequisites
- Python 3.7+ installed
- MySQL server running
- Basic knowledge of command line

## 🗄️ Step 1: Setup MySQL Database

1. **Open MySQL command line or MySQL Workbench**
2. **Run the database setup script:**
   ```sql
   source simple_database.sql
   ```
   Or copy-paste the contents of `simple_database.sql`

3. **Verify the database was created:**
   ```sql
   SHOW DATABASES;
   USE shopsmart_ai;
   SHOW TABLES;
   ```

## 🐍 Step 2: Setup Python Backend

1. **Install Python dependencies:**
   ```bash
   pip install -r simple_requirements.txt
   ```

2. **Update database configuration in `simple_app.py`:**
   ```python
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = 'Mysql#@22'
   ```

3. **Run the backend:**
   ```bash
   python simple_app.py
   ```

4. **Test the backend:**
   - Open browser and go to: `http://localhost:5000`
   - You should see: `{"message": "ShopSmart AI Simple Backend - Login Only"}`

## 🧪 Step 3: Test Login & Signup

1. **Open `index.html` in your browser**
2. **Test Signup:**
   - Click "Sign Up" button
   - Fill in name, email, and password (min 6 chars)
   - Submit and check console for debugging info
3. **Test Login:**
   - Click "Login" button
   - Use your created account or test credentials:
     - Email: `test@example.com`
     - Password: `test123`
4. **Check browser console (F12) for debugging info**

## 🧪 Step 4: Test Budget Optimization & Cart

1. **Login to dashboard**
2. **Test Budget Optimization:**
   - Go to "Budget Optimizer" tab
   - Enter budget amount and family size
   - Click "Optimize My Budget"
   - View real food items from dataset within 90% of budget
   - See detailed nutrition information (calories, protein, fat, carbs, fiber)
3. **Test Cart Functionality:**
   - Click "Add to Cart" on recommended items
   - Go to "Cart" tab to see added items
   - Items are saved to database per user

## 🔍 Troubleshooting

### Backend won't start?
- Check if MySQL is running
- Verify database credentials in `simple_app.py`
- Check if port 5000 is available

### Login not working?
- Check browser console (F12) for errors
- Verify backend is running on `http://localhost:5000`
- Check if database and users table exist

### Database connection error?
- Verify MySQL server is running
- Check username/password in `simple_app.py`
- Ensure `shopsmart_ai` database exists

## 📁 Files Created
- `simple_database.sql` - Database setup script
- `simple_app.py` - Basic Flask backend
- `simple_requirements.txt` - Python dependencies
- `SIMPLE_SETUP.md` - This setup guide

## 🎯 What's Working
- ✅ User login with database
- ✅ User signup with database
- ✅ Password hashing and verification
- ✅ Basic authentication
- ✅ Frontend-backend connection
- ✅ Test user account
- ✅ Budget optimization with real CSV dataset
- ✅ Shopping cart functionality
- ✅ Add items to cart from recommendations
- ✅ Real nutrition data with prices

## 🚧 What's Next
- User registration
- Password hashing
- JWT tokens
- Cart functionality
- User preferences
