#!/usr/bin/env python3
"""
Passenger WSGI configuration for cPanel deployment.
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

# Create the Flask application
application = create_app()

if __name__ == "__main__":
    # For debugging purposes
    application.run(debug=True)