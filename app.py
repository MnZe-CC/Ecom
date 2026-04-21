from flask import Flask, render_template, send_from_directory, jsonify
import os
import json

app = Flask(__name__)

# Load product data
def load_product_data():
    with open('products.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/products')
def get_products():
    data = load_product_data()
    return jsonify(data['products'])

@app.route('/api/categories')
def get_categories():
    data = load_product_data()
    return jsonify(data['categories'])

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)