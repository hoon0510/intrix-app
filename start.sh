#!/bin/bash

# 1. Start FastAPI on 8001
cd /var/www/backend
PYTHONPATH=. uvicorn main:app --host 0.0.0.0 --port 8001 &

# 2. Start Next.js on 3000
cd /var/www/frontend
pnpm install
pnpm start &

# 3. Start nginx on 8000
nginx -g 'daemon off;' 