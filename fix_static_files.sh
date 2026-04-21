#!/bin/bash
# Script to fix static file serving for the ecommerce application

echo "=== Fixing static file serving ==="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "This script needs to be run as root (sudo) to modify system directories"
    echo "Please run: sudo /home/nidami/ecom/fix_static_files.sh"
    exit 1
fi

# Create a directory for static files that nginx can access
echo "1. Creating static files directory..."
mkdir -p /var/www/nidami-static

# Copy static files to the new location
echo "2. Copying static files..."
cp -r /home/nidami/ecom/static/* /var/www/nidami-static/

# Set proper permissions
echo "3. Setting permissions..."
chown -R www-data:www-data /var/www/nidami-static
chmod -R 755 /var/www/nidami-static

# Update nginx configuration to use the new static files location
echo "4. Updating nginx configuration..."
sed -i 's|alias /home/nidami/ecom/static/;|alias /var/www/nidami-static/;|' /etc/nginx/sites-available/nidami.online

# Test nginx configuration
echo "5. Testing nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo "Nginx configuration test passed"
else
    echo "Nginx configuration test failed!"
    exit 1
fi

# Restart nginx
echo "6. Restarting nginx..."
systemctl restart nginx

echo "=== Static file serving fix completed ==="
echo "Static files are now being served from /var/www/nidami-static/"
echo "Please refresh your browser to see the changes"