#!/usr/bin/env python3
"""
Database Update Script for Multi-Basket Support
This script updates the existing database to support multiple baskets per user
"""

import mysql.connector
from mysql.connector import Error

def update_database_schema():
    """Update the database schema to support multiple baskets"""
    
    print("🔄 Updating Database Schema for Multi-Basket Support...")
    print("=" * 60)
    
    # Database configuration
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Mysql#@22',  # Update with your MySQL password
        'database': 'shopsmart_ai'
    }
    
    try:
        # Connect to MySQL
        print("📡 Connecting to MySQL database...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("✅ Connected to MySQL successfully!")
        
        # Check if the new columns already exist
        print("🔍 Checking current table structure...")
        cursor.execute("DESCRIBE user_carts")
        columns = [row[0] for row in cursor.fetchall()]
        
        # Add new columns if they don't exist
        new_columns = [
            ("cart_type", "ENUM('active', 'saved', 'completed') DEFAULT 'active'"),
            ("total_amount", "DECIMAL(10,2) DEFAULT 0.00"),
            ("item_count", "INT DEFAULT 0")
        ]
        
        for column_name, column_definition in new_columns:
            if column_name not in columns:
                print(f"➕ Adding column: {column_name}")
                cursor.execute(f"ALTER TABLE user_carts ADD COLUMN {column_name} {column_definition}")
            else:
                print(f"✅ Column {column_name} already exists")
        
        # Add indexes for better performance
        print("🔍 Adding indexes for better performance...")
        indexes = [
            ("idx_user_carts_user_id", "user_id"),
            ("idx_user_carts_type", "cart_type")
        ]
        
        for index_name, column in indexes:
            try:
                cursor.execute(f"CREATE INDEX {index_name} ON user_carts ({column})")
                print(f"✅ Index {index_name} created")
            except Error as e:
                if "Duplicate key name" in str(e):
                    print(f"✅ Index {index_name} already exists")
                else:
                    print(f"⚠️  Warning: Could not create index {index_name}: {e}")
        
        # Update existing carts to have 'active' type
        print("🔄 Updating existing carts...")
        cursor.execute("UPDATE user_carts SET cart_type = 'active' WHERE cart_type IS NULL")
        updated_rows = cursor.rowcount
        print(f"✅ Updated {updated_rows} existing carts to 'active' type")
        
        # Commit changes
        connection.commit()
        print("✅ Database schema updated successfully!")
        
        # Show updated table structure
        print("\n📋 Updated user_carts table structure:")
        cursor.execute("DESCRIBE user_carts")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]} {row[2]} {row[3]} {row[4]}")
        
        # Show sample data
        print("\n📊 Sample data from user_carts:")
        cursor.execute("SELECT id, user_id, cart_name, cart_type, total_amount, item_count FROM user_carts LIMIT 5")
        for row in cursor.fetchall():
            print(f"   ID: {row[0]}, User: {row[1]}, Name: {row[2]}, Type: {row[3]}, Total: {row[4]}, Items: {row[5]}")
        
        print("\n🎉 Database update completed successfully!")
        print("   Your database now supports multiple baskets per user.")
        print("   Each basket save will create a new row with a unique cart_id.")
        
    except Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("📡 Database connection closed.")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Database Schema Update")
    print("   This will add multi-basket support to your existing database.")
    print()
    
    # Ask for confirmation
    confirm = input("Do you want to proceed? (y/N): ").lower().strip()
    if confirm != 'y':
        print("❌ Update cancelled.")
        exit()
    
    success = update_database_schema()
    
    if success:
        print("\n✅ Database update completed successfully!")
        print("   You can now run the Flask app and test multi-basket functionality.")
    else:
        print("\n❌ Database update failed. Please check the error messages above.")
