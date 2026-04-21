#!/usr/bin/env python3
"""
Database initialization script for nidam-ie-com.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models.product import Product, db
from models.category import Category
from models.admin_user import AdminUser
from models.attribute import ProductAttribute
from models.index_parameter import IndexParameter
from models.index_result import IndexResult

def init_db():
    """Initialize the database with tables and sample data."""
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if we already have data
        if AdminUser.query.first() is None:
            print("Creating sample data...")

            # Create admin user
            admin = AdminUser(
                username='admin',
                email='admin@example.com'
            )
            admin.set_password('admin123')  # Default password
            db.session.add(admin)

            # Create sample categories
            electronics = Category(
                name_en='Electronics',
                name_ar='إلكترونيات',
                description_en='Electronic devices and gadgets',
                description_ar='الأجهزة والإلكترونيات'
            )
            db.session.add(electronics)

            clothing = Category(
                name_en='Clothing',
                name_ar='ملابس',
                description_en='Apparel and fashion items',
                description_ar='الملابس وإكسسوارات الموضة'
            )
            db.session.add(clothing)

            # Create sample product
            product = Product(
                name_en='Smartphone',
                name_ar='هاتف ذكي',
                description_en='Latest smartphone with advanced features',
                description_ar='أحدث هاتف ذكي بميزات متقدمة',
                price=699.99,
                stock_status='in_stock',
                category_id=1
            )
            db.session.add(product)

            # Create sample attribute
            attribute = ProductAttribute(
                product_id=1,
                name_en='Color',
                name_ar='اللون',
                value_en='Black',
                value_ar='أسود'
            )
            db.session.add(attribute)

            # Create sample index parameters
            sales_param = IndexParameter(
                name_en='Sales Performance',
                name_ar='أداء المبيعات',
                formula='sales * 0.1',
                weight=0.4
            )
            db.session.add(sales_param)

            views_param = IndexParameter(
                name_en='Traffic Metrics',
                name_ar='مقاييس الزوار',
                formula='views / 100',
                weight=0.3
            )
            db.session.add(views_param)

            conversion_param = IndexParameter(
                name_en='Conversion Rate',
                name_ar='معدل التحويل',
                formula='conversion_rate * 100',
                weight=0.3
            )
            db.session.add(conversion_param)

            db.session.commit()
            print("Sample data created successfully!")

        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()