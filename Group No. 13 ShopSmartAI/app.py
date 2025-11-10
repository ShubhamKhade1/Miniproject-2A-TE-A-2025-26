from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_mysqldb import MySQL
import bcrypt
import jwt
import datetime
import os
import csv
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Enable CORS for frontend
CORS(app, supports_credentials=True)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'Mysql#@22'   # Change to your MySQL password
app.config['MYSQL_DB'] = 'shopsmart_ai'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# JWT Configuration
JWT_SECRET = 'your-jwt-secret-key'  # Change this in production
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION = 24 * 60 * 60  # 24 hours

# Data source for items (CSV)
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'nutrition_with_co2_with_refined_categories.csv')
CATEGORIZED_DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'nutrition_with_co2_with_refined_categories.csv')
_ITEMS_CACHE = None
_CATEGORIZED_ITEMS_CACHE = None

def _to_number(value, num_type=float):
    try:
        if value is None or value == '':
            return None
        return num_type(value)
    except Exception:
        return None

def _load_items_from_csv():
    global _ITEMS_CACHE
    if _ITEMS_CACHE is not None:
        return _ITEMS_CACHE

    items = []
    try:
        with open(DATA_FILE_PATH, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item = {
                    'food_id': _to_number(row.get('food_id'), int),
                    'food': row.get('food'),
                    'caloric_value': _to_number(row.get('caloric_value'), float),
                    'fat': _to_number(row.get('fat'), float),
                    'saturated_fats': _to_number(row.get('saturated_fats'), float),
                    'carbohydrates': _to_number(row.get('carbohydrates'), float),
                    'sugars': _to_number(row.get('sugars'), float),
                    'protein': _to_number(row.get('protein'), float),
                    'dietary_fiber': _to_number(row.get('dietary_fiber'), float),
                    'cholesterol': _to_number(row.get('cholesterol'), float),
                    'sodium': _to_number(row.get('sodium'), float),
                    'calcium': _to_number(row.get('calcium'), float),
                    'iron': _to_number(row.get('iron'), float),
                    'nutrition_density': _to_number(row.get('nutrition_density'), float),
                    'price': _to_number(row.get('price'), float),
                }
                items.append(item)
    except FileNotFoundError:
        items = []
    _ITEMS_CACHE = items
    return _ITEMS_CACHE

def _load_categorized_items_from_csv():
    global _CATEGORIZED_ITEMS_CACHE
    if _CATEGORIZED_ITEMS_CACHE is not None:
        return _CATEGORIZED_ITEMS_CACHE

    items = []
    try:
        with open(CATEGORIZED_DATA_FILE_PATH, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item = {
                    'food_id': _to_number(row.get('food_id'), int),
                    'food': row.get('food'),
                    'caloric_value': _to_number(row.get('caloric_value'), float),
                    'fat': _to_number(row.get('fat'), float),
                    'saturated_fats': _to_number(row.get('saturated_fats'), float),
                    'carbohydrates': _to_number(row.get('carbohydrates'), float),
                    'sugars': _to_number(row.get('sugars'), float),
                    'protein': _to_number(row.get('protein'), float),
                    'dietary_fiber': _to_number(row.get('dietary_fiber'), float),
                    'cholesterol': _to_number(row.get('cholesterol'), float),
                    'sodium': _to_number(row.get('sodium'), float),
                    'calcium': _to_number(row.get('calcium'), float),
                    'iron': _to_number(row.get('iron'), float),
                    'nutrition_density': _to_number(row.get('nutrition_density'), float),
                    'price': _to_number(row.get('price'), float),
                    'CO2_emissions_kg_per_kg': _to_number(row.get('CO2_emissions_kg_per_kg'), float),
                    'refined_category': row.get('refined_category'),
                }
                items.append(item)
    except FileNotFoundError:
        items = []
    _CATEGORIZED_ITEMS_CACHE = items
    return _CATEGORIZED_ITEMS_CACHE

def token_required(f):
    """Decorator to check if user is authenticated"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

@app.route('/')
def home():
    return jsonify({'message': 'ShopSmart AI Backend API'})

@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        items = _load_items_from_csv()
        # Optionally support simple search via ?q=
        query = request.args.get('q', type=str)
        if query:
            q_lower = query.lower()
            items = [item for item in items if isinstance(item.get('food'), str) and q_lower in item['food'].lower()]

        return jsonify({'success': True, 'items': items}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to load items'}), 500

@app.route('/api/items/csv-data', methods=['GET'])
def get_csv_data():
    try:
        items = _load_categorized_items_from_csv()
        return jsonify({'success': True, 'items': items}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to load CSV data'}), 500

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not all([name, email, password]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        cur = mysql.connection.cursor()
        
        # Check if user already exists
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Insert new user
        cur.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, password_hash.decode('utf-8'))
        )
        mysql.connection.commit()
        
        user_id = cur.lastrowid
        
        # Create default cart for user
        cur.execute(
            "INSERT INTO user_carts (user_id, cart_name) VALUES (%s, %s)",
            (user_id, 'Default Cart')
        )
        mysql.connection.commit()
        
        # Create default preferences
        cur.execute(
            "INSERT INTO user_preferences (user_id, family_size) VALUES (%s, %s)",
            (user_id, 1)
        )
        mysql.connection.commit()
        
        cur.close()
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'id': user_id,
                'name': name,
                'email': email
            }
        }), 201
        
    except Exception as e:
        print(f"Signup error: {str(e)}")
        return jsonify({'success': False, 'message': 'Registration failed'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400
        
        cur = mysql.connection.cursor()
        
        # Get user by email
        cur.execute("SELECT id, name, email, password_hash FROM users WHERE email = %s AND is_active = TRUE", (email,))
        user = cur.fetchone()
        
        if not user:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Check password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Update last login
        cur.execute("UPDATE users SET last_login = NOW() WHERE id = %s", (user['id'],))
        mysql.connection.commit()
        
        # Generate JWT token
        token_data = {
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION)
        }
        token = jwt.encode(token_data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        cur.close()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            },
            'token': token
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'success': False, 'message': 'Login failed'}), 500

@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(current_user_id):
    try:
        # In a real application, you might want to blacklist the token
        return jsonify({'success': True, 'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Logout failed'}), 500

@app.route('/api/user/profile', methods=['GET'])
@token_required
def get_profile(current_user_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, created_at, last_login FROM users WHERE id = %s", (current_user_id,))
        user = cur.fetchone()
        cur.close()
        
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to get profile'}), 500

@app.route('/api/user/preferences', methods=['GET', 'PUT'])
@token_required
def manage_preferences(current_user_id):
    try:
        cur = mysql.connection.cursor()
        
        if request.method == 'GET':
            cur.execute("SELECT * FROM user_preferences WHERE user_id = %s", (current_user_id,))
            preferences = cur.fetchone()
            cur.close()
            
            return jsonify({
                'success': True,
                'preferences': preferences
            }), 200
            
        elif request.method == 'PUT':
            data = request.get_json()
            
            cur.execute("""
                UPDATE user_preferences 
                SET dietary_restrictions = %s, budget_limit = %s, family_size = %s, preferred_cuisine = %s
                WHERE user_id = %s
            """, (
                data.get('dietary_restrictions'),
                data.get('budget_limit'),
                data.get('family_size', 1),
                data.get('preferred_cuisine'),
                current_user_id
            ))
            mysql.connection.commit()
            cur.close()
            
            return jsonify({
                'success': True,
                'message': 'Preferences updated successfully'
            }), 200
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to manage preferences'}), 500

@app.route('/api/cart', methods=['GET', 'POST'])
@token_required
def manage_cart(current_user_id):
    try:
        cur = mysql.connection.cursor()
        
        if request.method == 'GET':
            # Get user's cart and items
            cur.execute("SELECT * FROM user_carts WHERE user_id = %s", (current_user_id,))
            cart = cur.fetchone()
            
            if cart:
                cur.execute("SELECT * FROM cart_items WHERE cart_id = %s", (cart['id'],))
                items = cur.fetchall()
                cart['items'] = items
            else:
                cart = {'items': []}
            
            cur.close()
            
            return jsonify({
                'success': True,
                'cart': cart
            }), 200
            
        elif request.method == 'POST':
            data = request.get_json()
            
            # Get or create user's cart
            cur.execute("SELECT id FROM user_carts WHERE user_id = %s LIMIT 1", (current_user_id,))
            cart = cur.fetchone()
            
            if not cart:
                cur.execute("INSERT INTO user_carts (user_id) VALUES (%s)", (current_user_id,))
                mysql.connection.commit()
                cart_id = cur.lastrowid
            else:
                cart_id = cart['id']
            
            # Add item to cart
            cur.execute("""
                INSERT INTO cart_items (cart_id, food_name, food_id, price, quantity, caloric_value, protein, fat, nutrition_density)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                cart_id,
                data['food_name'],
                data.get('food_id'),
                data['price'],
                data.get('quantity', 1),
                data.get('caloric_value'),
                data.get('protein'),
                data.get('fat'),
                data.get('nutrition_density')
            ))
            mysql.connection.commit()
            cur.close()
            
            return jsonify({
                'success': True,
                'message': 'Item added to cart successfully'
            }), 201
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to manage cart'}), 500

@app.route('/api/cart/items/<int:item_id>', methods=['PUT', 'DELETE'])
@token_required
def manage_cart_item(current_user_id, item_id):
    try:
        cur = mysql.connection.cursor()
        
        if request.method == 'PUT':
            data = request.get_json()
            quantity = data.get('quantity', 1)
            
            if quantity <= 0:
                # Delete item if quantity is 0 or negative
                cur.execute("DELETE FROM cart_items WHERE id = %s", (item_id,))
            else:
                cur.execute("UPDATE cart_items SET quantity = %s WHERE id = %s", (quantity, item_id))
            
            mysql.connection.commit()
            cur.close()
            
            return jsonify({
                'success': True,
                'message': 'Cart item updated successfully'
            }), 200
            
        elif request.method == 'DELETE':
            cur.execute("DELETE FROM cart_items WHERE id = %s", (item_id,))
            mysql.connection.commit()
            cur.close()
            
            return jsonify({
                'success': True,
                'message': 'Item removed from cart successfully'
            }), 200
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to manage cart item'}), 500

@app.route('/api/cart/clear', methods=['POST'])
@token_required
def clear_cart(current_user_id):
    try:
        cur = mysql.connection.cursor()
        
        # Get user's cart
        cur.execute("SELECT id FROM user_carts WHERE user_id = %s", (current_user_id,))
        cart = cur.fetchone()
        
        if cart:
            # Clear all items from cart
            cur.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart['id'],))
            mysql.connection.commit()
        
        cur.close()
        
        return jsonify({
            'success': True,
            'message': 'Cart cleared successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to clear cart'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

