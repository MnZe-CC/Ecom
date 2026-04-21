#!/bin/bash

# Install dependencies if not already installed
if [ ! -f "venv/bin/activate" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run the Flask app
echo "Starting the server..."
echo "Visit http://localhost:8000 to view the e-commerce site"
python app.py