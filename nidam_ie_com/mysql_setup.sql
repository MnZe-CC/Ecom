-- MySQL database setup script for nidam-ie-com

-- Create database
CREATE DATABASE IF NOT EXISTS nidam_ie_com CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use database
USE nidam_ie_com;

-- Create products table
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_ar VARCHAR(200) NOT NULL,
    name_en VARCHAR(200) NOT NULL,
    description_ar TEXT,
    description_en TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_status VARCHAR(50) DEFAULT 'in_stock',
    category_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
);

-- Create categories table
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    description_ar TEXT,
    description_en TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create admin_users table
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create product_attributes table
CREATE TABLE product_attributes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    value_ar VARCHAR(200) NOT NULL,
    value_en VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Create ecommerce_index_parameters table
CREATE TABLE ecommerce_index_parameters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_ar VARCHAR(100) NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    formula TEXT NOT NULL,
    weight FLOAT DEFAULT 1.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create ecommerce_index_results table
CREATE TABLE ecommerce_index_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    parameter_id INT NOT NULL,
    value FLOAT NOT NULL,
    calculated_score FLOAT NOT NULL,
    date DATE DEFAULT (CURRENT_DATE),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (parameter_id) REFERENCES ecommerce_index_parameters(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_created ON products(created_at);
CREATE INDEX idx_categories_name_en ON categories(name_en);
CREATE INDEX idx_categories_name_ar ON categories(name_ar);
CREATE INDEX idx_attributes_product ON product_attributes(product_id);
CREATE INDEX idx_index_results_product ON ecommerce_index_results(product_id);
CREATE INDEX idx_index_results_parameter ON ecommerce_index_results(parameter_id);
CREATE INDEX idx_index_results_date ON ecommerce_index_results(date);

-- Insert sample admin user (password should be hashed)
-- INSERT INTO admin_users (username, email, password_hash) VALUES ('admin', 'admin@example.com', 'hashed_password_here');

-- Insert sample categories
INSERT INTO categories (name_en, name_ar, description_en, description_ar) VALUES
('Electronics', 'إلكترونيات', 'Electronic devices and gadgets', 'الأجهزة والإلكترونيات'),
('Clothing', 'ملابس', 'Apparel and fashion items', 'الملابس وإكسسوارات الموضة');

-- Insert sample product
INSERT INTO products (name_en, name_ar, description_en, description_ar, price, stock_status, category_id) VALUES
('Smartphone', 'هاتف ذكي', 'Latest smartphone with advanced features', 'أحدث هاتف ذكي بميزات متقدمة', 699.99, 'in_stock', 1);

-- Insert sample attribute
INSERT INTO product_attributes (product_id, name_en, name_ar, value_en, value_ar) VALUES
(1, 'Color', 'اللون', 'Black', 'أسود');

-- Insert sample index parameters
INSERT INTO ecommerce_index_parameters (name_en, name_ar, formula, weight) VALUES
('Sales Performance', 'أداء المبيعات', 'sales * 0.1', 0.4),
('Traffic Metrics', 'مقاييس الزوار', 'views / 100', 0.3),
('Conversion Rate', 'معدل التحويل', 'conversion_rate * 100', 0.3);