#!/usr/bin/env python3
"""
Script to generate placeholder images for e-commerce products
"""

import os
import requests
from urllib.parse import urlencode

def create_placeholder_image(text, category, filename):
    """
    Create a placeholder image using placehold.co API

    Args:
        text (str): Text to display on the image
        category (str): Product category (clothing, electronics, books)
        filename (str): Name of the file to save
    """
    # Define colors based on category
    colors = {
        'clothing': 'FF6B6B/FFFFFF',      # Red/White
        'electronics': '4ECDC4/000000',   # Teal/Black
        'books': '45B7D1/FFFFFF'          # Blue/White
    }

    # Get color scheme for category
    color_scheme = colors.get(category, 'CCCCCC/000000')  # Default gray/black

    # Create URL for placehold.co
    params = {
        'text': text.replace(' ', '+'),
        'width': '300',
        'height': '300'
    }

    url = f"https://placehold.co/300x300/{color_scheme}/png?{urlencode(params)}"

    # Download and save image
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Created {filename}")
        else:
            print(f"Failed to download image for {text}")
    except Exception as e:
        print(f"Error creating image for {text}: {e}")

def generate_product_images():
    """Generate placeholder images for all product categories"""

    # Create directory if it doesn't exist
    os.makedirs('static/images/products', exist_ok=True)

    # Product data organized by category
    products = {
        'clothing': [
            {'name': 'Classic T-Shirt', 'image': 'tshirt.png'},
            {'name': 'Designer Jeans', 'image': 'jeans.png'},
            {'name': 'Winter Sweater', 'image': 'sweater.png'},
            {'name': 'Summer Dress', 'image': 'dress.png'},
            {'name': 'Formal Shirt', 'image': 'shirt.png'}
        ],
        'electronics': [
            {'name': 'Gaming Laptop', 'image': 'laptop.png'},
            {'name': 'Smartphone Pro', 'image': 'smartphone.png'},
            {'name': 'Wireless Headphones', 'image': 'headphones.png'},
            {'name': 'Smart Watch', 'image': 'watch.png'},
            {'name': 'Bluetooth Speaker', 'image': 'speaker.png'}
        ],
        'books': [
            {'name': 'Mystery Novel', 'image': 'mystery_book.png'},
            {'name': 'Science Fiction', 'image': 'sci_fi_book.png'},
            {'name': 'Biography Collection', 'image': 'biography_book.png'},
            {'name': 'Cookbook Deluxe', 'image': 'cookbook.png'},
            {'name': 'Self-Help Guide', 'image': 'self_help_book.png'}
        ]
    }

    # Generate images for each product
    for category, items in products.items():
        print(f"Generating images for {category}...")
        for item in items:
            filepath = f"static/images/products/{item['image']}"
            create_placeholder_image(item['name'], category, filepath)

    print("Finished generating product images!")

if __name__ == "__main__":
    generate_product_images()