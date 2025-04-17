#!/bin/sh

# Create necessary directories
mkdir -p /var/log/nginx
mkdir -p /var/log/fastapi
mkdir -p /var/www/frontend/.next/cache

# Set proper permissions
chown -R nobody:nobody /var/www
chown -R nobody:nobody /var/log

# Start supervisor
exec /usr/bin/supervisord -n -c /etc/supervisor/conf.d/supervisord.conf 