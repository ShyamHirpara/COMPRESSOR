# Gunicorn configuration file
import multiprocessing

# Bind to the port defined by the environment (Render sets this automatically)
bind = "0.0.0.0:10000"

# Workers
# On the free tier (512MB RAM), too many workers = OOM Crash.
# 2 workers is a safe balance.
workers = 2

# Threads
# Use threads to handle concurrent requests without consuming as much RAM as workers.
threads = 4
worker_class = 'gthread'

# Timeout
# Vital for large image processing. Default is 30s.
# Increase to 120s (2 minutes) to allow 50MB images to process.
timeout = 120

# Keepalive protection
keepalive = 5

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
