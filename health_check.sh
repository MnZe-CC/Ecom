#!/bin/bash
# Health check script for the ecommerce application

echo "=== Ecommerce Application Health Check ==="

# Check if the Flask app is running
echo "1. Checking if Flask app process is running..."
FLASK_PID=$(pgrep -f "python3 app.py")
if [ ! -z "$FLASK_PID" ]; then
    echo "✓ Flask app is running (PID: $FLASK_PID)"
else
    echo "✗ Flask app is not running"
fi

# Check if we can access the app locally
echo "2. Checking local connectivity..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "✓ Local connectivity successful (HTTP $HTTP_STATUS)"
else
    echo "✗ Local connectivity failed (HTTP $HTTP_STATUS)"
fi

# Check disk space
echo "3. Checking disk space..."
DISK_USAGE=$(df -h /home | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 90 ]; then
    echo "✓ Disk usage is healthy (${DISK_USAGE}%)"
else
    echo "⚠ Disk usage is high (${DISK_USAGE}%)"
fi

# Check memory usage
echo "4. Checking memory usage..."
MEM_USAGE=$(free | grep Mem | awk '{printf("%.0f"), $3/$2 * 100.0}')
if [ "$MEM_USAGE" -lt 80 ]; then
    echo "✓ Memory usage is healthy (${MEM_USAGE}%)"
else
    echo "⚠ Memory usage is high (${MEM_USAGE}%)"
fi

echo "=== Health Check Complete ==="