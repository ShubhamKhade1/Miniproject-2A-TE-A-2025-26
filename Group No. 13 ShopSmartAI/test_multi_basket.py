#!/usr/bin/env python3
"""
Test script for Multi-Basket functionality
This script tests the new multi-basket save functionality
"""

import requests
import json
import time

def test_multi_basket_functionality():
    """Test the multi-basket save functionality"""
    
    print("🧪 Testing Multi-Basket Functionality...")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    user_id = 1  # Test user ID
    
    # Test data for multiple baskets
    test_baskets = [
        {
            "cart_name": "Weekly Groceries",
            "items": [
                {"food": "Apples", "food_id": "apples_1", "price": 50.0, "quantity": 2, "caloric_value": 52, "protein": 0.3, "fat": 0.2, "nutrition_density": 8.5},
                {"food": "Bananas", "food_id": "bananas_1", "price": 30.0, "quantity": 3, "caloric_value": 89, "protein": 1.1, "fat": 0.3, "nutrition_density": 7.2}
            ]
        },
        {
            "cart_name": "Healthy Meals",
            "items": [
                {"food": "Chicken Breast", "food_id": "chicken_1", "price": 200.0, "quantity": 1, "caloric_value": 165, "protein": 31.0, "fat": 3.6, "nutrition_density": 12.8},
                {"food": "Brown Rice", "food_id": "rice_1", "price": 80.0, "quantity": 2, "caloric_value": 111, "protein": 2.6, "fat": 0.9, "nutrition_density": 9.1}
            ]
        },
        {
            "cart_name": "Snacks & Drinks",
            "items": [
                {"food": "Almonds", "food_id": "almonds_1", "price": 150.0, "quantity": 1, "caloric_value": 579, "protein": 21.2, "fat": 49.9, "nutrition_density": 15.3},
                {"food": "Green Tea", "food_id": "tea_1", "price": 25.0, "quantity": 5, "caloric_value": 2, "protein": 0.0, "fat": 0.0, "nutrition_density": 6.8}
            ]
        }
    ]
    
    try:
        # Test 1: Save multiple baskets
        print("📦 Test 1: Saving multiple baskets...")
        saved_cart_ids = []
        
        for i, basket in enumerate(test_baskets):
            print(f"   Saving basket {i+1}: '{basket['cart_name']}'")
            
            response = requests.post(f"{base_url}/api/cart/save", json={
                "user_id": user_id,
                "cart_name": basket["cart_name"],
                "items": basket["items"]
            })
            
            if response.status_code == 200:
                result = response.json()
                if result["success"]:
                    saved_cart_ids.append(result["cart_id"])
                    print(f"   ✅ Basket saved with ID: {result['cart_id']}")
                    print(f"   📊 Items: {result['items_saved']}, Total: ₹{result['total_amount']}")
                else:
                    print(f"   ❌ Failed to save basket: {result['message']}")
                    return False
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                return False
        
        print(f"✅ All {len(test_baskets)} baskets saved successfully!")
        
        # Test 2: Retrieve saved baskets
        print("\n📋 Test 2: Retrieving saved baskets...")
        
        response = requests.get(f"{base_url}/api/cart/saved-baskets?user_id={user_id}")
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                baskets = result["baskets"]
                print(f"   ✅ Retrieved {len(baskets)} saved baskets")
                
                for basket in baskets:
                    print(f"   📦 {basket['cart_name']} (ID: {basket['id']})")
                    print(f"      Items: {basket['item_count']}, Total: ₹{basket['total_amount']}")
                    print(f"      Created: {basket['created_at']}")
                    print(f"      Items: {[item['food_name'] for item in basket['items']]}")
                    print()
            else:
                print(f"   ❌ Failed to retrieve baskets: {result['message']}")
                return False
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            return False
        
        # Test 3: Verify each basket has unique cart_id
        print("🔍 Test 3: Verifying unique cart IDs...")
        unique_ids = set(saved_cart_ids)
        if len(unique_ids) == len(saved_cart_ids):
            print("   ✅ All baskets have unique cart IDs")
        else:
            print("   ❌ Some baskets have duplicate cart IDs")
            return False
        
        # Test 4: Verify basket data integrity
        print("🔍 Test 4: Verifying basket data integrity...")
        for i, basket in enumerate(baskets):
            original_basket = test_baskets[i]
            if basket['cart_name'] == original_basket['cart_name']:
                print(f"   ✅ Basket {i+1} name matches")
            else:
                print(f"   ❌ Basket {i+1} name mismatch")
                return False
            
            if len(basket['items']) == len(original_basket['items']):
                print(f"   ✅ Basket {i+1} item count matches")
            else:
                print(f"   ❌ Basket {i+1} item count mismatch")
                return False
        
        print("\n🎉 All tests passed! Multi-basket functionality is working correctly.")
        print(f"📊 Summary:")
        print(f"   - {len(test_baskets)} baskets saved")
        print(f"   - {len(unique_ids)} unique cart IDs")
        print(f"   - All baskets retrievable")
        print(f"   - Data integrity verified")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("   Make sure the Flask app is running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Multi-Basket Functionality Test")
    print("   Make sure the Flask app is running first!")
    print()
    
    success = test_multi_basket_functionality()
    
    if success:
        print("\n✅ Multi-basket functionality is working perfectly!")
        print("   You can now save multiple baskets per user for Apriori algorithm.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
