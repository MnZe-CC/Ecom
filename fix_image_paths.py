#!/usr/bin/env python3
# Script to fix image paths in products.json to use absolute paths

import json
import os

def fix_image_paths():
    """Fix image paths in products.json to use absolute paths"""

    # Path to the products.json file
    products_file = '/home/nidami/ecom/products.json'

    # Read the current products.json
    with open(products_file, 'r') as f:
        data = json.load(f)

    # Fix product image paths
    for product in data['products']:
        if 'image' in product and product['image'].startswith('static/'):
            product['image'] = '/' + product['image']

    # Fix category image paths
    for category in data['categories']:
        if 'image' in category and category['image'].startswith('static/'):
            category['image'] = '/' + category['image']

    # Write the updated data back to the file
    with open(products_file, 'w') as f:
        json.dump(data, f, indent=2)

    print("Image paths fixed in products.json")

if __name__ == '__main__':
    fix_image_paths()