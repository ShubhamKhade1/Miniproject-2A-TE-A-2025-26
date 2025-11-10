#!/usr/bin/env python3
"""
Test script for Cart Recommendations
"""

import requests
import json

def test_cart_recommendations():
    """Test the cart recommendations endpoint"""
    base_url = "http://localhost:5000"
    user_id = 5
    
    print("🧪 Testing Cart Recommendations")
    print("=" * 50)
    
    # Test cart with wheat bread and soymilk
    cart_items = [
        {"food": "wheat bread"},
        {"food": "soymilk"}
    ]
    
    try:
        response = requests.post(
            f"{base_url}/api/apriori/cart-recommendations/{user_id}",
            json={"cart_items": cart_items},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"✅ Cart recommendations retrieved successfully!")
                print(f"   🛒 Cart Items: {result['cart_items']}")
                print(f"   🎯 Recommendations: {len(result['recommendations'])}")
                print(f"   📊 Total Rules: {result['total_rules']}")
                
                if result['recommendations']:
                    print(f"\n   🎯 Recommendations:")
                    for i, rec in enumerate(result['recommendations'], 1):
                        print(f"      {i}. {rec['item']} - {rec['reason']}")
                        print(f"         Confidence: {rec['confidence']*100:.1f}% | Lift: {rec['lift']:.2f}")
                        print(f"         Trigger: {rec['trigger_item']}")
                else:
                    print("   ℹ️  No recommendations available")
            else:
                print(f"❌ Recommendations failed: {result['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask server is running on localhost:5000")
        return
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    print(f"\n{'='*50}")
    print("🎉 Cart Recommendations Test Complete!")

if __name__ == "__main__":
    test_cart_recommendations()
