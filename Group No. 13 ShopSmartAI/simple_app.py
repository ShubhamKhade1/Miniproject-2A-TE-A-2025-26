from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import bcrypt
import pandas as pd
import os
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pickle

app = Flask(__name__)

# Enable CORS for frontend
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'Mysql#@22'   # Change to your MySQL password
app.config['MYSQL_DB'] = 'shopsmart_ai'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

# Global variables for KNN model
knn_model = None
scaler = None
nutrition_features = None
food_names = None

# Load nutrition dataset
def load_nutrition_dataset():
    try:
        csv_path = 'nutrition_with_co2_with_refined_categories.csv'
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Convert to list of dictionaries for easier processing
            dataset = df.to_dict('records')
            print(f"Loaded {len(dataset)} food items from dataset")
            return dataset
        else:
            print(f"Dataset file not found: {csv_path}")
            return []
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        return []

# Train KNN model for healthier swaps
def train_knn_model():
    """
    Train KNN model on nutrition dataset for finding healthier alternatives
    Uses nutritional values to find similar foods with better nutrition density
    """
    global knn_model, scaler, nutrition_features, food_names
    
    try:
        csv_path = 'nutrition_with_co2_with_refined_categories.csv'
        if not os.path.exists(csv_path):
            print("Dataset not found for KNN training")
            return False
        
        # Load dataset
        df = pd.read_csv(csv_path)
        print(f"Training KNN model on {len(df)} food items...")
        
        # Select nutritional features for similarity calculation
        # These features will be used to find similar foods
        feature_columns = [
            'caloric_value', 'protein', 'fat', 'carbohydrates', 
            'dietary_fiber', 'sugars', 'saturated_fats', 'cholesterol', 
            'sodium', 'calcium', 'iron'
        ]
        
        # Fill missing values with 0 for training
        df[feature_columns] = df[feature_columns].fillna(0)
        
        # Extract features and food names
        nutrition_features = df[feature_columns].values
        food_names = df['food'].values
        
        # Standardize features for better KNN performance
        scaler = StandardScaler()
        nutrition_features_scaled = scaler.fit_transform(nutrition_features)
        
        # Train KNN model with 6 neighbors (5 alternatives + original)
        # Using cosine similarity for better nutritional similarity
        knn_model = NearestNeighbors(
            n_neighbors=6, 
            algorithm='auto', 
            metric='cosine'
        )
        knn_model.fit(nutrition_features_scaled)
        
        print("KNN model trained successfully!")
        print(f"Features used: {feature_columns}")
        print(f"Model type: {type(knn_model).__name__}")
        
        return True
        
    except Exception as e:
        print(f"Error training KNN model: {str(e)}")
        return False

# Find healthier alternatives using KNN
def find_healthier_alternatives(input_food_name, top_k=5):
    """
    Find healthier alternatives to the input food using trained KNN model
    
    Args:
        input_food_name (str): Name of the food to find alternatives for
        top_k (int): Number of alternatives to return
    
    Returns:
        list: List of healthier alternatives with nutrition info
    """
    global knn_model, scaler, nutrition_features, food_names
    
    if knn_model is None or scaler is None:
        print("KNN model not trained yet")
        return []
    
    try:
        # Find the input food in our dataset
        input_food_idx = None
        for i, name in enumerate(food_names):
            if input_food_name.lower() in name.lower():
                input_food_idx = i
                break
        
        if input_food_idx is None:
            print(f"Food '{input_food_name}' not found in dataset")
            return []
        
        # Get input food's features
        input_features = nutrition_features[input_food_idx:input_food_idx+1]
        input_features_scaled = scaler.transform(input_features)
        
        # Find nearest neighbors (similar foods)
        distances, indices = knn_model.kneighbors(input_features_scaled)
        
        # Get the input food's nutrition density for comparison
        input_nutrition_density = nutrition_features[input_food_idx][-1] if len(nutrition_features[input_food_idx]) > 10 else 0
        
        # Load full dataset for detailed information
        df = pd.read_csv('nutrition_with_co2_with_refined_categories.csv')
        
        alternatives = []
        for idx in indices[0][1:]:  # Skip first (original food)
            if idx < len(df):
                food_item = df.iloc[idx]
                
                # Calculate health improvement score
                current_nutrition_density = food_item.get('nutrition_density', 0)
                health_improvement = current_nutrition_density - input_nutrition_density
                
                # Get CO₂ emission data from dataset
                co2_emissions = food_item.get('CO2_emissions_kg_per_kg', 0)
                co2_data = {
                    'emission_level': 'high' if co2_emissions > 10 else 'medium' if co2_emissions > 2 else 'low',
                    'emission_value': float(co2_emissions) if pd.notna(co2_emissions) else 0.0,
                    'color': '#dc2626' if co2_emissions > 10 else '#f59e0b' if co2_emissions > 2 else '#10b981',
                    'description': 'High CO₂ emissions' if co2_emissions > 10 else 'Medium CO₂ emissions' if co2_emissions > 2 else 'Low CO₂ emissions'
                }
                
                # Create alternative item with all necessary info
                # Convert numpy types to Python native types for JSON serialization
                alternative = {
                    'food_id': str(food_item.get('food_id', idx)),
                    'food': str(food_item.get('food', '')),
                    'price': float(food_item.get('price', 0)),
                    'caloric_value': int(food_item.get('caloric_value', 0)) if pd.notna(food_item.get('caloric_value')) else 0,
                    'protein': float(food_item.get('protein', 0)) if pd.notna(food_item.get('protein')) else 0.0,
                    'fat': float(food_item.get('fat', 0)) if pd.notna(food_item.get('fat')) else 0.0,
                    'carbohydrates': float(food_item.get('carbohydrates', 0)) if pd.notna(food_item.get('carbohydrates')) else 0.0,
                    'dietary_fiber': float(food_item.get('dietary_fiber', 0)) if pd.notna(food_item.get('dietary_fiber')) else 0.0,
                    'sugars': float(food_item.get('sugars', 0)) if pd.notna(food_item.get('sugars')) else 0.0,
                    'nutrition_density': float(current_nutrition_density) if pd.notna(current_nutrition_density) else 0.0,
                    'health_improvement': round(float(health_improvement), 2),
                    'similarity_score': round(float(1 - distances[0][list(indices[0]).index(idx)]), 3),
                    'co2_emissions': co2_data
                }
                
                alternatives.append(alternative)
                
                if len(alternatives) >= top_k:
                    break
        
        # Sort by health improvement (healthier alternatives first)
        alternatives.sort(key=lambda x: x['health_improvement'], reverse=True)
        
        print(f"Found {len(alternatives)} healthier alternatives for '{input_food_name}'")
        return alternatives
        
    except Exception as e:
        print(f"Error finding alternatives: {str(e)}")
        return []

# Load dataset on startup
nutrition_dataset = load_nutrition_dataset()

# Train KNN model on startup
print("Initializing KNN model for healthier swaps...")
knn_training_success = train_knn_model()
if knn_training_success:
    print("✅ KNN model ready for healthier swaps!")
else:
    print("❌ KNN model training failed!")

# CO₂ emission classification data
CO2_EMISSION_DATA = {
    # High CO₂ emissions (>10 kg CO₂e per kg)
    'high': {
        'keywords': ['beef', 'lamb', 'mutton', 'cheese', 'butter', 'cream', 'lard', 'pork', 'veal'],
        'emission_range': (10, 60),  # kg CO₂e per kg
        'color': '#dc2626',  # red
        'description': 'High CO₂ emissions'
    },
    # Medium CO₂ emissions (2-10 kg CO₂e per kg)
    'medium': {
        'keywords': ['chicken', 'turkey', 'fish', 'salmon', 'tuna', 'rice', 'chocolate', 'milk', 'yogurt', 'eggs', 'bread', 'pasta'],
        'emission_range': (2, 10),
        'color': '#f59e0b',  # amber
        'description': 'Medium CO₂ emissions'
    },
    # Low CO₂ emissions (<2 kg CO₂e per kg)
    'low': {
        'keywords': ['apple', 'banana', 'orange', 'tomato', 'potato', 'carrot', 'onion', 'lettuce', 'spinach', 'broccoli', 'oatmeal', 'beans', 'lentils', 'nuts', 'seeds'],
        'emission_range': (0.1, 2),
        'color': '#10b981',  # green
        'description': 'Low CO₂ emissions'
    }
}

def classify_co2_emissions(food_name):
    """
    Classify food items based on their CO₂ emission levels
    Returns: dict with emission_level, emission_value, color, description
    """
    if not food_name:
        return {
            'emission_level': 'unknown',
            'emission_value': 0,
            'color': '#6b7280',  # gray
            'description': 'Unknown CO₂ emissions'
        }
    
    food_lower = food_name.lower()
    
    # Check each emission category
    for level, data in CO2_EMISSION_DATA.items():
        for keyword in data['keywords']:
            if keyword in food_lower:
                # Generate a realistic emission value within the range
                import random
                min_emission, max_emission = data['emission_range']
                emission_value = round(random.uniform(min_emission, max_emission), 2)
                
                return {
                    'emission_level': level,
                    'emission_value': emission_value,
                    'color': data['color'],
                    'description': data['description']
                }
    
    # Default to medium if no specific match found
    return {
        'emission_level': 'medium',
        'emission_value': 5.0,
        'color': '#f59e0b',
        'description': 'Medium CO₂ emissions'
    }

# Nutrition categorization function
def categorize_nutrition(value, nutrient_type):
    """Categorize nutritional values as low, medium, or high"""
    if pd.isna(value) or value == 0:
        return "any"
    
    value = float(value)
    
    if nutrient_type == "calories":
        if value <= 50:
            return "low"
        elif value <= 150:
            return "medium"
        else:
            return "high"
    elif nutrient_type == "protein":
        if value <= 5:
            return "low"
        elif value <= 15:
            return "medium"
        else:
            return "high"
    elif nutrient_type == "fat":
        if value <= 5:
            return "low"
        elif value <= 15:
            return "medium"
        else:
            return "high"
    elif nutrient_type == "sugars":
        if value <= 5:
            return "low"
        elif value <= 15:
            return "medium"
        else:
            return "high"
    else:
        return "any"

@app.route('/')
def home():
    return jsonify({'message': 'ShopSmart AI Simple Backend - Login Only'})

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
        
        cur = mysql.connection.cursor()
        
        # Check if user already exists
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert new user
        cur.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, password_hash.decode('utf-8'))
        )
        mysql.connection.commit()
        
        user_id = cur.lastrowid
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
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400
        
        cur = mysql.connection.cursor()
        
        # Get user by email
        cur.execute("SELECT id, name, email, password_hash FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        
        if not user:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        # Check password (for demo, accept 'test123' for test@example.com)
        if email == 'test@example.com' and password == 'test123':
            # Demo login - bypass password check
            pass
        else:
            # Real password check
            if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        
        cur.close()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'success': False, 'message': 'Login failed'}), 500

@app.route('/api/budget/optimize', methods=['POST'])
def optimize_budget():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        budget = data.get('budget')
        family_size = data.get('family_size', 1)
        
        if not budget:
            return jsonify({'success': False, 'message': 'Budget is required'}), 400
        
        # Calculate 90% of budget for recommendations
        available_budget = float(budget) * 0.9
        
        if not nutrition_dataset:
            return jsonify({'success': False, 'message': 'Nutrition dataset not available'}), 500
        
        # Filter items within budget and adjust for family size
        affordable_items = []
        total_cost = 0
        
        # Sort items by nutrition density (highest first) for better recommendations
        sorted_dataset = sorted(nutrition_dataset, key=lambda x: x.get('nutrition_density', 0), reverse=True)
        
        for item in sorted_dataset:
            # Get price from dataset (assuming price is in the last column)
            item_price = float(item.get('price', 0))
            
            if item_price > 0:  # Only include items with valid prices
                item_cost = item_price * family_size
                
                if total_cost + item_cost <= available_budget:
                    # Get CO₂ emission data from dataset
                    co2_emissions = item.get('CO2_emissions_kg_per_kg', 0)
                    co2_data = {
                        'emission_level': 'high' if co2_emissions > 10 else 'medium' if co2_emissions > 2 else 'low',
                        'emission_value': float(co2_emissions) if pd.notna(co2_emissions) else 0.0,
                        'color': '#dc2626' if co2_emissions > 10 else '#f59e0b' if co2_emissions > 2 else '#10b981',
                        'description': 'High CO₂ emissions' if co2_emissions > 10 else 'Medium CO₂ emissions' if co2_emissions > 2 else 'Low CO₂ emissions'
                    }
                    
                    # Format item for frontend
                    formatted_item = {
                        'food_id': str(item.get('food_id', '')),
                        'food': item.get('food', ''),
                        'price': item_price,
                        'caloric_value': item.get('caloric_value', 0),
                        'protein': item.get('protein', 0),
                        'fat': item.get('fat', 0),
                        'nutrition_density': item.get('nutrition_density', 0),
                        'carbohydrates': item.get('carbohydrates', 0),
                        'dietary_fiber': item.get('dietary_fiber', 0),
                        'sugars': item.get('sugars', 0),
                        'saturated_fats': item.get('saturated_fats', 0),
                        'cholesterol': item.get('cholesterol', 0),
                        'sodium': item.get('sodium', 0),
                        'calcium': item.get('calcium', 0),
                        'iron': item.get('iron', 0),
                        'co2_emissions': co2_data
                    }
                    
                    affordable_items.append({
                        **formatted_item,
                        'price': item_cost,
                        'quantity': family_size
                    })
                    total_cost += item_cost
                    
                    # Limit to top 20 recommendations for better performance
                    if len(affordable_items) >= 20:
                        break
        
        return jsonify({
            'success': True,
            'message': 'Budget optimization completed',
            'recommendations': affordable_items,
            'total_cost': total_cost,
            'available_budget': available_budget,
            'saved_amount': max(0.0, float(budget) - float(total_cost)),
            'total_items': len(affordable_items)
        }), 200
        
    except Exception as e:
        print(f"Budget optimization error: {str(e)}")
        return jsonify({'success': False, 'message': 'Budget optimization failed'}), 500

@app.route('/api/cart', methods=['GET', 'POST'])
def manage_cart():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'message': 'User ID is required'}), 400
        
        if request.method == 'GET':
            # Get user's cart and items
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM user_carts WHERE user_id = %s", (user_id,))
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
            # Add item to cart
            item_data = data.get('item')
            if not item_data:
                return jsonify({'success': False, 'message': 'Item data is required'}), 400
            
            cur = mysql.connection.cursor()
            
            # Get or create user's cart
            cur.execute("SELECT id FROM user_carts WHERE user_id = %s LIMIT 1", (user_id,))
            cart = cur.fetchone()
            
            if not cart:
                cur.execute("INSERT INTO user_carts (user_id) VALUES (%s)", (user_id,))
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
                item_data['food'],
                item_data.get('food_id'),
                item_data['price'],
                item_data.get('quantity', 1),
                item_data.get('caloric_value'),
                item_data.get('protein'),
                item_data.get('fat'),
                item_data.get('nutrition_density')
            ))
            mysql.connection.commit()
            cur.close()
            
            return jsonify({
                'success': True,
                'message': 'Item added to cart successfully'
            }), 201
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to manage cart'}), 500

@app.route('/api/cart/save', methods=['POST'])
def save_cart():
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        items = data.get('items', [])
        cart_name = data.get('cart_name', 'Saved Basket')

        if not user_id:
            return jsonify({'success': False, 'message': 'User ID is required'}), 400

        if not isinstance(items, list):
            return jsonify({'success': False, 'message': 'Items must be a list'}), 400

        if not items:
            return jsonify({'success': False, 'message': 'Cannot save empty cart'}), 400

        cur = mysql.connection.cursor()

        # Calculate total amount and item count
        total_amount = sum(float(item.get('price', 0)) * int(item.get('quantity', 1)) for item in items)
        item_count = sum(int(item.get('quantity', 1)) for item in items)

        # Create a new saved basket (don't replace existing ones)
        cur.execute(
            """
            INSERT INTO user_carts (user_id, cart_name, cart_type, total_amount, item_count) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, cart_name, 'saved', total_amount, item_count)
        )
        mysql.connection.commit()
        cart_id = cur.lastrowid

        # Insert all items for this new basket
        inserted = 0
        for item in items:
            # Basic required fields
            food_name = item.get('food') or item.get('food_name') or ''
            price = item.get('price') if item.get('price') is not None else 0
            quantity = item.get('quantity') if item.get('quantity') is not None else 1

            # Optional nutrition fields
            caloric_value = item.get('caloric_value')
            protein = item.get('protein')
            fat = item.get('fat')
            nutrition_density = item.get('nutrition_density')

            # CO₂ emission data
            co2_emissions = item.get('co2_emissions', {})
            co2_emission_value = co2_emissions.get('emission_value', 0) if co2_emissions else 0
            co2_emission_level = co2_emissions.get('emission_level', 'low') if co2_emissions else 'low'
            co2_emission_color = co2_emissions.get('color', '#10b981') if co2_emissions else '#10b981'

            cur.execute(
                """
                INSERT INTO cart_items (
                    cart_id, food_name, food_id, price, quantity, caloric_value, protein, fat, nutrition_density,
                    co2_emission_value, co2_emission_level, co2_emission_color
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    cart_id,
                    food_name,
                    item.get('food_id'),
                    price,
                    quantity,
                    caloric_value,
                    protein,
                    fat,
                    nutrition_density,
                    co2_emission_value,
                    co2_emission_level,
                    co2_emission_color,
                ),
            )
            inserted += 1

        mysql.connection.commit()
        cur.close()

        return jsonify({
            'success': True,
            'message': f'Basket "{cart_name}" saved successfully',
            'cart_id': cart_id,
            'cart_name': cart_name,
            'items_saved': inserted,
            'total_amount': total_amount,
            'item_count': item_count
        }), 200

    except Exception as e:
        print(f"Save cart error: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to save cart'}), 500

@app.route('/api/cart/saved-baskets', methods=['GET'])
def get_saved_baskets():
    """Get all saved baskets for a user"""
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'message': 'User ID is required'}), 400

        cur = mysql.connection.cursor()
        
        # Get all saved baskets for the user
        cur.execute("""
            SELECT id, cart_name, cart_type, total_amount, item_count, created_at, updated_at
            FROM user_carts 
            WHERE user_id = %s AND cart_type = 'saved'
            ORDER BY created_at DESC
        """, (user_id,))
        
        baskets = cur.fetchall()
        
        # Get items for each basket
        for basket in baskets:
            cur.execute("""
                SELECT food_name, food_id, price, quantity, caloric_value, protein, fat, nutrition_density,
                       co2_emission_value, co2_emission_level, co2_emission_color
                FROM cart_items 
                WHERE cart_id = %s
                ORDER BY added_at
            """, (basket['id'],))
            items = cur.fetchall()
            
            # Format items with CO₂ emission data
            formatted_items = []
            for item in items:
                formatted_item = dict(item)
                if item['co2_emission_value'] is not None:
                    formatted_item['co2_emissions'] = {
                        'emission_value': float(item['co2_emission_value']),
                        'emission_level': item['co2_emission_level'],
                        'color': item['co2_emission_color']
                    }
                formatted_items.append(formatted_item)
            
            basket['items'] = formatted_items
        
        cur.close()
        
        return jsonify({
            'success': True,
            'baskets': baskets,
            'total_baskets': len(baskets)
        }), 200
        
    except Exception as e:
        print(f"Get saved baskets error: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to retrieve saved baskets'}), 500

@app.route('/api/cart/saved-baskets/<int:basket_id>', methods=['DELETE'])
def delete_saved_basket(basket_id: int):
    """Delete a saved basket and its items"""
    try:
        cur = mysql.connection.cursor()
        # Ensure basket exists and is of type 'saved'
        cur.execute("SELECT id FROM user_carts WHERE id = %s AND cart_type = 'saved'", (basket_id,))
        basket = cur.fetchone()
        if not basket:
            cur.close()
            return jsonify({'success': False, 'message': 'Saved basket not found'}), 404

        # Delete items then the basket
        cur.execute("DELETE FROM cart_items WHERE cart_id = %s", (basket_id,))
        cur.execute("DELETE FROM user_carts WHERE id = %s", (basket_id,))
        mysql.connection.commit()
        cur.close()

        return jsonify({'success': True, 'message': 'Saved basket deleted successfully', 'id': basket_id}), 200
    except Exception as e:
        print(f"Delete saved basket error: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to delete saved basket'}), 500

@app.route('/api/nutrition/filter', methods=['POST'])
def filter_nutrition():
    try:
        data = request.get_json()
        filters = data.get('filters', {})
        
        if not nutrition_dataset:
            return jsonify({'success': False, 'message': 'Nutrition dataset not available'}), 500
        
        # Apply filters
        filtered_items = []
        
        for item in nutrition_dataset:
            # Check if item matches all applied filters
            matches_filters = True
            
            # Calories filter
            if filters.get('calories') and filters['calories'] != "":
                item_category = categorize_nutrition(item.get('caloric_value', 0), "calories")
                if item_category != filters['calories']:
                    matches_filters = False
            
            # Protein filter
            if filters.get('protein') and filters['protein'] != "":
                item_category = categorize_nutrition(item.get('protein', 0), "protein")
                if item_category != filters['protein']:
                    matches_filters = False
            
            # Fat filter
            if filters.get('fat') and filters['fat'] != "":
                item_category = categorize_nutrition(item.get('fat', 0), "fat")
                if item_category != filters['fat']:
                    matches_filters = False
            
            # Sugars filter
            if filters.get('sugars') and filters['sugars'] != "":
                item_category = categorize_nutrition(item.get('sugars', 0), "sugars")
                if item_category != filters['sugars']:
                    matches_filters = False
            
            # CO₂ emissions filter
            if filters.get('co2_emissions') and filters['co2_emissions'] != "":
                co2_emissions = item.get('CO2_emissions_kg_per_kg', 0)
                co2_level = 'high' if co2_emissions > 10 else 'medium' if co2_emissions > 2 else 'low'
                if co2_level != filters['co2_emissions']:
                    matches_filters = False
            
            if matches_filters:
                # Get CO₂ emission data from dataset
                co2_emissions = item.get('CO2_emissions_kg_per_kg', 0)
                co2_data = {
                    'emission_level': 'high' if co2_emissions > 10 else 'medium' if co2_emissions > 2 else 'low',
                    'emission_value': float(co2_emissions) if pd.notna(co2_emissions) else 0.0,
                    'color': '#dc2626' if co2_emissions > 10 else '#f59e0b' if co2_emissions > 2 else '#10b981',
                    'description': 'High CO₂ emissions' if co2_emissions > 10 else 'Medium CO₂ emissions' if co2_emissions > 2 else 'Low CO₂ emissions'
                }
                
                # Format item for frontend
                formatted_item = {
                    'food_id': str(item.get('food_id', '')),
                    'food': item.get('food', ''),
                    'price': float(item.get('price', 0)),
                    'caloric_value': item.get('caloric_value', 0),
                    'protein': item.get('protein', 0),
                    'fat': item.get('fat', 0),
                    'carbohydrates': item.get('carbohydrates', 0),
                    'sugars': item.get('sugars', 0),
                    'nutrition_density': item.get('nutrition_density', 0),
                    'dietary_fiber': item.get('dietary_fiber', 0),
                    'saturated_fats': item.get('saturated_fats', 0),
                    'cholesterol': item.get('cholesterol', 0),
                    'sodium': item.get('sodium', 0),
                    'calcium': item.get('calcium', 0),
                    'iron': item.get('iron', 0),
                    'co2_emissions': co2_data
                }
                filtered_items.append(formatted_item)
        
        # Limit results to top 50 for performance
        filtered_items = filtered_items[:50]
        
        return jsonify({
            'success': True,
            'message': f'Found {len(filtered_items)} items matching your filters',
            'items': filtered_items,
            'total_count': len(filtered_items)
        }), 200
        
    except Exception as e:
        print(f"Nutrition filtering error: {str(e)}")
        return jsonify({'success': False, 'message': 'Nutrition filtering failed'}), 500

@app.route('/api/items', methods=['GET'])
def get_items():
    try:
        if not nutrition_dataset:
            return jsonify({'success': True, 'items': [], 'total': 0}), 200
        
        # Query params
        q = (request.args.get('q') or '').strip().lower()
        limit_param = request.args.get('limit')
        try:
            limit = int(limit_param) if limit_param is not None else 50
        except ValueError:
            limit = 50
        if limit <= 0:
            limit = 50
        
        # Filter by search term if provided
        if q:
            filtered = [i for i in nutrition_dataset if q in str(i.get('food', '')).lower()]
        else:
            filtered = nutrition_dataset
        
        # Prepare formatted items
        items = []
        for item in filtered[:limit]:
            food_name = item.get('food', '')
            food_id = str(item.get('food_id') or (food_name.lower().replace(' ', '_')))
            
            # Get CO₂ emission data from dataset
            co2_emissions = item.get('CO2_emissions_kg_per_kg', 0)
            co2_data = {
                'emission_level': 'high' if co2_emissions > 10 else 'medium' if co2_emissions > 2 else 'low',
                'emission_value': float(co2_emissions) if pd.notna(co2_emissions) else 0.0,
                'color': '#dc2626' if co2_emissions > 10 else '#f59e0b' if co2_emissions > 2 else '#10b981',
                'description': 'High CO₂ emissions' if co2_emissions > 10 else 'Medium CO₂ emissions' if co2_emissions > 2 else 'Low CO₂ emissions'
            }
            
            items.append({
                'food_id': food_id,
                'food': food_name,
                'price': float(item.get('price', 0) or 0),
                'caloric_value': item.get('caloric_value', 0) or 0,
                'protein': item.get('protein', 0) or 0,
                'fat': item.get('fat', 0) or 0,
                'nutrition_density': item.get('nutrition_density', 0) or 0,
                'carbohydrates': item.get('carbohydrates', 0) or 0,
                'dietary_fiber': item.get('dietary_fiber', 0) or 0,
                'sugars': item.get('sugars', 0) or 0,
                'co2_emissions': co2_data
            })
        
        return jsonify({'success': True, 'items': items, 'total': len(filtered)}), 200
    except Exception as e:
        print(f"Items endpoint error: {str(e)}")
        return jsonify({'success': False, 'items': [], 'total': 0, 'message': 'Failed to load items'}), 500

@app.route('/api/items/csv-data', methods=['GET'])
def get_csv_data():
    """Get all CSV data for greener alternatives"""
    try:
        if not nutrition_dataset:
            return jsonify({'success': False, 'message': 'No dataset loaded'}), 500
        
        # Return all items with their categories
        return jsonify({'success': True, 'items': nutrition_dataset}), 200
        
    except Exception as e:
        print(f"Error getting CSV data: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to load CSV data'}), 500

# Apriori Algorithm Implementation
def get_user_transactions(user_id, limit=50):
    """Fetch user transactions from database"""
    try:
        cursor = mysql.connection.cursor()
        
        # Get the most recent transactions for the user
        query = """
        SELECT ci.food_name, ci.food_id, ci.price, ci.quantity, ci.caloric_value,
               ci.protein, ci.fat, ci.nutrition_density, uc.created_at
        FROM user_carts uc
        JOIN cart_items ci ON uc.id = ci.cart_id
        WHERE uc.user_id = %s
        ORDER BY uc.created_at DESC
        LIMIT %s
        """
        
        cursor.execute(query, (user_id, limit))
        transactions = cursor.fetchall()
        cursor.close()
        
        return transactions
    except Exception as e:
        print(f"Error fetching user transactions: {str(e)}")
        return []

def generate_transaction_itemsets(transactions):
    """Convert transactions to itemsets for Apriori algorithm"""
    # Group items by cart/transaction
    transaction_groups = {}
    
    for transaction in transactions:
        cart_id = transaction.get('created_at')  # Using timestamp as transaction ID
        if cart_id not in transaction_groups:
            transaction_groups[cart_id] = []
        
        transaction_groups[cart_id].append(transaction['food_name'])
    
    # Convert to list of itemsets
    itemsets = list(transaction_groups.values())
    return itemsets

def apriori_algorithm(transactions, min_support=0.1, min_confidence=0.6):
    """Implement Apriori algorithm for association rule mining"""
    try:
        # Step 1: Count item frequencies
        item_counts = {}
        total_transactions = len(transactions)
        
        for transaction in transactions:
            for item in transaction:
                item_counts[item] = item_counts.get(item, 0) + 1
        
        # Step 2: Find frequent 1-itemsets
        frequent_1_itemsets = []
        for item, count in item_counts.items():
            support = count / total_transactions
            if support >= min_support:
                frequent_1_itemsets.append((item, support))
        
        # Step 3: Generate frequent 2-itemsets
        frequent_2_itemsets = []
        for i in range(len(frequent_1_itemsets)):
            for j in range(i + 1, len(frequent_1_itemsets)):
                item1, support1 = frequent_1_itemsets[i]
                item2, support2 = frequent_1_itemsets[j]
                
                # Count co-occurrence
                co_occurrence = 0
                for transaction in transactions:
                    if item1 in transaction and item2 in transaction:
                        co_occurrence += 1
                
                support = co_occurrence / total_transactions
                if support >= min_support:
                    frequent_2_itemsets.append(((item1, item2), support))
        
        # Step 4: Generate association rules
        association_rules = []
        
        for (item1, item2), support in frequent_2_itemsets:
            # Count individual item frequencies
            count1 = sum(1 for transaction in transactions if item1 in transaction)
            count2 = sum(1 for transaction in transactions if item2 in transaction)
            
            # Count co-occurrence for this specific pair
            co_occurrence = sum(1 for transaction in transactions if item1 in transaction and item2 in transaction)
            
            # Calculate confidence for both directions
            confidence_1_to_2 = co_occurrence / count1 if count1 > 0 else 0
            confidence_2_to_1 = co_occurrence / count2 if count2 > 0 else 0
            
            # Calculate lift
            lift_1_to_2 = confidence_1_to_2 / (count2 / total_transactions) if count2 > 0 else 0
            lift_2_to_1 = confidence_2_to_1 / (count1 / total_transactions) if count1 > 0 else 0
            
            # Add rules if they meet confidence threshold
            if confidence_1_to_2 >= min_confidence:
                association_rules.append({
                    'antecedent': [item1],
                    'consequent': [item2],
                    'support': support,
                    'confidence': confidence_1_to_2,
                    'lift': lift_1_to_2
                })
            
            if confidence_2_to_1 >= min_confidence:
                association_rules.append({
                    'antecedent': [item2],
                    'consequent': [item1],
                    'support': support,
                    'confidence': confidence_2_to_1,
                    'lift': lift_2_to_1
                })
        
        # Sort rules by lift (descending)
        association_rules.sort(key=lambda x: x['lift'], reverse=True)
        
        return {
            'rules': association_rules,
            'frequent_items': [item for item, _ in frequent_1_itemsets],
            'frequent_pairs': [pair for pair, _ in frequent_2_itemsets],
            'total_transactions': total_transactions,
            'unique_items': len(item_counts)
        }
        
    except Exception as e:
        print(f"Error in Apriori algorithm: {str(e)}")
        return {
            'rules': [],
            'frequent_items': [],
            'frequent_pairs': [],
            'total_transactions': 0,
            'unique_items': 0
        }

def generate_recommendations(apriori_results, user_id):
    """Generate personalized recommendations based on Apriori results"""
    try:
        recommendations = []
        
        # Get user's recent purchases
        recent_transactions = get_user_transactions(user_id, 10)
        recent_items = set()
        for transaction in recent_transactions:
            recent_items.add(transaction['food_name'])
        
        # Generate recommendations based on association rules
        for rule in apriori_results['rules'][:10]:  # Top 10 rules
            antecedent = rule['antecedent'][0]
            consequent = rule['consequent'][0]
            
            # If user recently bought antecedent, recommend consequent
            if antecedent in recent_items and consequent not in recent_items:
                recommendations.append({
                    'item': consequent,
                    'reason': f"Frequently bought with {antecedent}",
                    'confidence': rule['confidence'],
                    'lift': rule['lift'],
                    'support': rule['support']
                })
        
        # Remove duplicates and sort by confidence
        unique_recommendations = []
        seen_items = set()
        
        for rec in recommendations:
            if rec['item'] not in seen_items:
                unique_recommendations.append(rec)
                seen_items.add(rec['item'])
        
        return unique_recommendations[:5]  # Top 5 recommendations
        
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        return []

@app.route('/api/apriori/analyze/<int:user_id>', methods=['GET'])
def analyze_user_apriori(user_id):
    """Analyze user transactions using Apriori algorithm"""
    try:
        # Get parameters from query string
        min_support = float(request.args.get('min_support', 0.1))  # 10% default
        min_confidence = float(request.args.get('min_confidence', 0.6))  # 60% default
        limit = int(request.args.get('limit', 50))  # 50 transactions default
        
        # Fetch user transactions
        transactions_data = get_user_transactions(user_id, limit)
        
        if not transactions_data:
            return jsonify({
                'success': False,
                'message': 'No transactions found for this user'
            }), 404
        
        # Convert to itemsets
        itemsets = generate_transaction_itemsets(transactions_data)
        
        if len(itemsets) < 2:
            return jsonify({
                'success': False,
                'message': 'Insufficient transactions for analysis (need at least 2)'
            }), 400
        
        # Run Apriori algorithm
        apriori_results = apriori_algorithm(itemsets, min_support, min_confidence)
        
        # Generate recommendations
        recommendations = generate_recommendations(apriori_results, user_id)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'analysis_results': {
                'total_transactions': apriori_results['total_transactions'],
                'unique_items': apriori_results['unique_items'],
                'frequent_items': apriori_results['frequent_items'],
                'association_rules': apriori_results['rules'],
                'recommendations': recommendations
            },
            'parameters': {
                'min_support': min_support,
                'min_confidence': min_confidence,
                'transaction_limit': limit
            }
        }), 200
        
    except Exception as e:
        print(f"Error in Apriori analysis: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Analysis failed: {str(e)}'
        }), 500

@app.route('/api/apriori/recommendations/<int:user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    """Get personalized recommendations for a user"""
    try:
        # Get user's recent transactions
        recent_transactions = get_user_transactions(user_id, 20)
        
        if not recent_transactions:
            return jsonify({
                'success': False,
                'message': 'No recent transactions found'
            }), 404
        
        # Convert to itemsets
        itemsets = generate_transaction_itemsets(recent_transactions)
        
        # Run Apriori with default parameters
        apriori_results = apriori_algorithm(itemsets, 0.1, 0.6)
        
        # Generate recommendations
        recommendations = generate_recommendations(apriori_results, user_id)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'recommendations': recommendations,
            'total_rules': len(apriori_results['rules']),
            'frequent_items': apriori_results['frequent_items'][:10]  # Top 10 frequent items
        }), 200
        
    except Exception as e:
        print(f"Error getting recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Failed to get recommendations: {str(e)}'
        }), 500

@app.route('/api/apriori/debug/<int:user_id>', methods=['GET'])
def debug_user_transactions(user_id):
    """Debug endpoint to show raw transaction data for a user"""
    try:
        # Get user's transactions
        transactions = get_user_transactions(user_id, 50)
        
        if not transactions:
            return jsonify({
                'success': False,
                'message': 'No transactions found for this user'
            }), 404
        
        # Convert to itemsets for analysis
        itemsets = generate_transaction_itemsets(transactions)
        
        # Get item frequencies
        item_counts = {}
        for transaction in itemsets:
            for item in transaction:
                item_counts[item] = item_counts.get(item, 0) + 1
        
        # Sort by frequency
        sorted_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'raw_transactions': transactions,
            'itemsets': itemsets,
            'item_frequencies': sorted_items,
            'total_transactions': len(itemsets),
            'unique_items': len(item_counts)
        }), 200
        
    except Exception as e:
        print(f"Error debugging transactions: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Debug failed: {str(e)}'
        }), 500

@app.route('/api/apriori/cart-recommendations/<int:user_id>', methods=['POST'])
def get_cart_recommendations(user_id):
    """Get recommendations based on current cart items"""
    try:
        # Get cart items from request
        cart_items = request.json.get('cart_items', [])
        
        if not cart_items:
            return jsonify({
                'success': False,
                'message': 'No cart items provided'
            }), 400
        
        # Get user's transaction history
        user_transactions = get_user_transactions(user_id, 50)
        
        if not user_transactions:
            return jsonify({
                'success': False,
                'message': 'No transaction history found for recommendations'
            }), 404
        
        # Convert to itemsets for analysis
        itemsets = generate_transaction_itemsets(user_transactions)
        
        # Run Apriori analysis
        apriori_results = apriori_algorithm(itemsets, 0.05, 0.3)  # Lower thresholds for more recommendations
        
        # Get cart item names
        cart_item_names = [item.get('food', item.get('name', '')) for item in cart_items]
        
        # Find recommendations based on association rules
        recommendations = []
        seen_items = set()
        
        for rule in apriori_results['rules']:
            antecedent = rule['antecedent'][0]
            consequent = rule['consequent'][0]
            
            # If cart contains antecedent but not consequent, recommend consequent
            if antecedent in cart_item_names and consequent not in cart_item_names and consequent not in seen_items:
                recommendations.append({
                    'item': consequent,
                    'reason': f"Frequently bought with {antecedent}",
                    'confidence': rule['confidence'],
                    'lift': rule['lift'],
                    'support': rule['support'],
                    'trigger_item': antecedent
                })
                seen_items.add(consequent)
        
        # Sort by confidence and lift
        recommendations.sort(key=lambda x: (x['confidence'], x['lift']), reverse=True)
        
        # Limit to top 3 recommendations
        recommendations = recommendations[:3]
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'recommendations': recommendations,
            'cart_items': cart_item_names,
            'total_rules': len(apriori_results['rules'])
        }), 200
        
    except Exception as e:
        print(f"Error getting cart recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Failed to get recommendations: {str(e)}'
        }), 500

@app.route('/api/healthier-swaps', methods=['POST'])
def get_healthier_swaps():
    """
    API endpoint for finding healthier alternatives using trained KNN model
    Accepts food name and returns 5 healthier alternatives
    """
    try:
        data = request.get_json()
        food_name = data.get('food_name', '').strip()
        
        if not food_name:
            return jsonify({
                'success': False, 
                'message': 'Food name is required'
            }), 400
        
        # Check if KNN model is trained
        if knn_model is None:
            return jsonify({
                'success': False, 
                'message': 'KNN model not ready. Please try again in a moment.'
            }), 503
        
        print(f"Finding healthier alternatives for: {food_name}")
        
        # Find healthier alternatives using KNN
        alternatives = find_healthier_alternatives(food_name, top_k=5)
        
        if not alternatives:
            return jsonify({
                'success': False,
                'message': f'No alternatives found for "{food_name}". Try a different food item.'
            }), 404
        
        # Format response for frontend
        formatted_alternatives = []
        for alt in alternatives:
            # Ensure all values are JSON serializable
            formatted_alt = {
                'food_id': str(alt['food_id']),
                'food': str(alt['food']),
                'price': float(alt['price']),
                'caloric_value': int(alt['caloric_value']) if alt['caloric_value'] is not None else 0,
                'protein': float(alt['protein']) if alt['protein'] is not None else 0.0,
                'fat': float(alt['fat']) if alt['fat'] is not None else 0.0,
                'carbohydrates': float(alt['carbohydrates']) if alt['carbohydrates'] is not None else 0.0,
                'dietary_fiber': float(alt['dietary_fiber']) if alt['dietary_fiber'] is not None else 0.0,
                'sugars': float(alt['sugars']) if alt['sugars'] is not None else 0.0,
                'nutrition_density': float(alt['nutrition_density']) if alt['nutrition_density'] is not None else 0.0,
                'health_improvement': float(alt['health_improvement']) if alt['health_improvement'] is not None else 0.0,
                'similarity_score': float(alt['similarity_score']) if alt['similarity_score'] is not None else 0.0,
                'co2_emissions': alt.get('co2_emissions', {})
            }
            formatted_alternatives.append(formatted_alt)
        
        return jsonify({
            'success': True,
            'message': f'Found {len(formatted_alternatives)} healthier alternatives for "{food_name}"',
            'original_food': food_name,
            'alternatives': formatted_alternatives,
            'total_alternatives': len(formatted_alternatives)
        }), 200
        
    except Exception as e:
        print(f"Healthier swaps API error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to find healthier alternatives'
        }), 500

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'Backend is working!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
