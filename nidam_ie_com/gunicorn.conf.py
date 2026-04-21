# Gunicorn configuration for VPS deployment

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Debugging
debug = False
reload = False

# Process naming
proc_name = "nidam_ie_com"

# Logging
accesslog = "/var/log/nidam_ie_com/access.log"
errorlog = "/var/log/nidam_ie_com/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Server mechanics
preload_app = True
max_requests = 1000
max_requests_jitter = 100

# Environment variables
raw_env = [
    "FLASK_ENV=production",
]

# Where to store temporary files
tmp_upload_dir = None

# SSL
# keyfile = "/path/to/server.key"
# certfile = "/path/to/server.crt"