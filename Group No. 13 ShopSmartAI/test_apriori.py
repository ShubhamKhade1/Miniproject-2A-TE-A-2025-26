#!/usr/bin/env python3
"""
Test script for Apriori Algorithm Implementation
This script demonstrates how to use the Apriori analysis with sample data
"""

import requests
import json

def test_apriori_analysis():
    """Test the Apriori analysis endpoint"""
    base_url = "http://localhost:5000"
    
    # Test user ID (you can change this to any existing user ID)
    user_id = 5
    
    print("🧪 Testing Apriori Analysis Implementation")
    print("=" * 50)
    
    # Test 1: Run Apriori Analysis
    print(f"\n1. Running Apriori Analysis for User ID: {user_id}")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/apriori/analyze/{user_id}?min_support=0.1&min_confidence=0.6&limit=50")
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                analysis = result['analysis_results']
                print(f"✅ Analysis completed successfully!")
                print(f"   📊 Total Transactions: {analysis['total_transactions']}")
                print(f"   🛒 Unique Items: {analysis['unique_items']}")
                print(f"   🔗 Association Rules: {len(analysis['association_rules'])}")
                print(f"   🎯 Recommendations: {len(analysis['recommendations'])}")
                
                # Show top 3 association rules
                if analysis['association_rules']:
                    print(f"\n   📈 Top Association Rules:")
                    for i, rule in enumerate(analysis['association_rules'][:3], 1):
                        antecedent = rule['antecedent'][0]
                        consequent = rule['consequent'][0]
                        confidence = rule['confidence'] * 100
                        lift = rule['lift']
                        print(f"      {i}. {antecedent} → {consequent} (Confidence: {confidence:.1f}%, Lift: {lift:.2f})")
                
                # Show recommendations
                if analysis['recommendations']:
                    print(f"\n   🎯 Personalized Recommendations:")
                    for i, rec in enumerate(analysis['recommendations'][:3], 1):
                        print(f"      {i}. {rec['item']} - {rec['reason']} (Confidence: {rec['confidence']*100:.1f}%)")
            else:
                print(f"❌ Analysis failed: {result['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask server is running on localhost:5000")
        return
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Test 2: Get Recommendations
    print(f"\n2. Getting Personalized Recommendations for User ID: {user_id}")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/apriori/recommendations/{user_id}")
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"✅ Recommendations retrieved successfully!")
                print(f"   🎯 Total Recommendations: {len(result['recommendations'])}")
                print(f"   📊 Total Rules: {result['total_rules']}")
                print(f"   🛒 Frequent Items: {len(result['frequent_items'])}")
                
                # Show recommendations
                if result['recommendations']:
                    print(f"\n   🎯 Recommendations:")
                    for i, rec in enumerate(result['recommendations'], 1):
                        print(f"      {i}. {rec['item']} - {rec['reason']} (Confidence: {rec['confidence']*100:.1f}%)")
                else:
                    print("   ℹ️  No recommendations available")
            else:
                print(f"❌ Recommendations failed: {result['message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print(f"\n{'='*50}")
    print("🎉 Apriori Analysis Test Complete!")
    print("\n📝 Usage Instructions:")
    print("1. Make sure you have transactions in your database for the user")
    print("2. Start the Flask server: python simple_app.py")
    print("3. Open the dashboard and go to 'Apriori Analysis' tab")
    print("4. Click 'Run Analysis' to analyze user transactions")
    print("5. Click 'Get Recommendations' for personalized suggestions")

if __name__ == "__main__":
    test_apriori_analysis()
