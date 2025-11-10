-- Simple ShopSmart AI Database Setup
-- Run this script in your MySQL server to create the basic database and users table

-- Create database
CREATE DATABASE IF NOT EXISTS shopsmart_ai;
USE shopsmart_ai;

-- Create users table (basic authentication only)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create user_preferences table for budget optimization
CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    budget_limit DECIMAL(10,2) DEFAULT 100.00,
    family_size INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create user_carts table for shopping carts (supports multiple baskets per user)
CREATE TABLE IF NOT EXISTS user_carts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    cart_name VARCHAR(100) NOT NULL,
    cart_type ENUM('active', 'saved', 'completed') DEFAULT 'active',
    total_amount DECIMAL(10,2) DEFAULT 0.00,
    item_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_carts_user_id (user_id),
    INDEX idx_user_carts_type (cart_type)
);

-- Create cart_items table for cart items
CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    food_name VARCHAR(100) NOT NULL,
    food_id VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    quantity INT DEFAULT 1,
    caloric_value INT,
    protein DECIMAL(5,2),
    fat DECIMAL(5,2),
    nutrition_density DECIMAL(5,2),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cart_id) REFERENCES user_carts(id) ON DELETE CASCADE
);

-- Insert a test user (password: test123)
INSERT INTO users (name, email, password_hash) VALUES 
('Test User', 'test@example.com', '$2b$10$rQZ8K9L2M1N0O7P6Q5R4S3T2U1V0W9X8Y7Z6A5B4C3D2E1F0G9H8I7J6K5L4M3N2O1P0Q9R8S7T6U5V4W3X2Y1Z0');

-- Create default preferences for test user
INSERT INTO user_preferences (user_id, budget_limit, family_size) VALUES 
(1, 100.00, 2);

-- Create default active cart for test user
INSERT INTO user_carts (user_id, cart_name, cart_type) VALUES 
(1, 'My Shopping Cart', 'active');

-- Show created tables
SHOW TABLES;
DESCRIBE users;
DESCRIBE user_preferences;
DESCRIBE user_carts;
DESCRIBE cart_items;
