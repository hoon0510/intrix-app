# 📁 /Dockerfile

# ---- 1. Base Node.js for Next.js Build ----
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY frontend .
RUN pnpm build

# ---- 2. Base Python for FastAPI ----
FROM python:3.10-alpine AS backend-builder
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend .

# ---- 3. Final Merge Layer ----
FROM python:3.10-alpine

# Install required packages
RUN apk add --no-cache nginx curl

# Copy built frontend
COPY --from=frontend-builder /app/frontend/.next /var/www/frontend/.next
COPY --from=frontend-builder /app/frontend/public /var/www/frontend/public
COPY --from=frontend-builder /app/frontend/package.json /var/www/frontend/

# Copy backend
COPY --from=backend-builder /app/backend /var/www/backend

# Copy nginx config
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

CMD ["/start.sh"]
    