#!/usr/bin/env python3
"""
Test script for KNN Healthier Swaps Algorithm
This script tests the KNN model training and prediction functionality
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

def test_knn_model():
    """Test the KNN model training and prediction"""
    
    print("🧪 Testing KNN Healthier Swaps Algorithm...")
    print("=" * 50)
    
    try:
        # Load dataset
        csv_path = 'nutrition_with_co2_with_refined_categories.csv'
        df = pd.read_csv(csv_path)
        print(f"✅ Dataset loaded: {len(df)} food items")
        
        # Select nutritional features
        feature_columns = [
            'caloric_value', 'protein', 'fat', 'carbohydrates', 
            'dietary_fiber', 'sugars', 'saturated_fats', 'cholesterol', 
            'sodium', 'calcium', 'iron'
        ]
        
        # Fill missing values
        df[feature_columns] = df[feature_columns].fillna(0)
        
        # Extract features
        nutrition_features = df[feature_columns].values
        food_names = df['food'].values
        
        print(f"✅ Features extracted: {len(feature_columns)} nutritional metrics")
        print(f"✅ Feature shape: {nutrition_features.shape}")
        
        # Standardize features
        scaler = StandardScaler()
        nutrition_features_scaled = scaler.fit_transform(nutrition_features)
        print("✅ Features standardized")
        
        # Train KNN model
        knn_model = NearestNeighbors(
            n_neighbors=6, 
            algorithm='auto', 
            metric='cosine'
        )
        knn_model.fit(nutrition_features_scaled)
        print("✅ KNN model trained successfully")
        
        # Test prediction
        test_food = "white bread"
        print(f"\n🔍 Testing with food: '{test_food}'")
        
        # Find test food index
        test_food_idx = None
        for i, name in enumerate(food_names):
            if test_food.lower() in name.lower():
                test_food_idx = i
                break
        
        if test_food_idx is not None:
            print(f"✅ Found test food at index: {test_food_idx}")
            
            # Get test features
            test_features = nutrition_features[test_food_idx:test_food_idx+1]
            test_features_scaled = scaler.transform(test_features)
            
            # Find neighbors
            distances, indices = knn_model.kneighbors(test_features_scaled)
            
            print(f"\n📊 Results for '{test_food}':")
            print(f"Original food: {food_names[test_food_idx]}")
            print(f"Nutrition density: {df.iloc[test_food_idx].get('nutrition_density', 0):.2f}")
            
            print(f"\n🔄 Top 5 alternatives:")
            for i, idx in enumerate(indices[0][1:], 1):
                if idx < len(df):
                    food_item = df.iloc[idx]
                    similarity = 1 - distances[0][list(indices[0]).index(idx)]
                    health_improvement = food_item.get('nutrition_density', 0) - df.iloc[test_food_idx].get('nutrition_density', 0)
                    
                    print(f"{i}. {food_item['food']}")
                    print(f"   Similarity: {similarity:.3f}")
                    print(f"   Nutrition Density: {food_item.get('nutrition_density', 0):.2f}")
                    print(f"   Health Improvement: {health_improvement:+.2f}")
                    print(f"   Price: ₹{food_item.get('price', 0):.2f}")
                    print()
            
            print("✅ KNN model test completed successfully!")
            return True
            
        else:
            print(f"❌ Test food '{test_food}' not found in dataset")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_knn_model()
    if success:
        print("\n🎉 All tests passed! KNN model is working correctly.")
    else:
        print("\n💥 Some tests failed. Please check the implementation.")

