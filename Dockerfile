# 📁 /Dockerfile

# ---- 1. Base Node.js for Next.js Build ----
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend

# Install dependencies first (better caching)
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install --force

# Copy source files
COPY frontend .

# Set environment variables for production build
ENV NEXT_PUBLIC_API_URL=https://api.intrix.app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Build the application
RUN npm run build

# ---- 2. Base Python for FastAPI ----
FROM python:3.10-alpine AS backend-builder
WORKDIR /app/backend

# Install system dependencies
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend .

# ---- 3. Final Merge Layer ----
FROM python:3.10-alpine

# Install system dependencies
RUN apk add --no-cache \
    nginx \
    curl \
    supervisor \
    && mkdir -p /var/log/supervisor \
    && mkdir -p /var/run/supervisor

# Copy nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Copy supervisor configuration
COPY nginx/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy built frontend
COPY --from=frontend-builder /app/frontend/.next /var/www/frontend/.next
COPY --from=frontend-builder /app/frontend/public /var/www/frontend/public
COPY --from=frontend-builder /app/frontend/package.json /var/www/frontend/

# Copy backend
COPY --from=backend-builder /app/backend /var/www/backend
COPY --from=backend-builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Create necessary directories
RUN mkdir -p /var/log/nginx \
    && mkdir -p /var/www/frontend/.next/cache \
    && chown -R nobody:nobody /var/www \
    && chown -R nobody:nobody /var/log/nginx

# Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose ports
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["/start.sh"]
    