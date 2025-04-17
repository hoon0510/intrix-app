# 📁 /Dockerfile

# ---- 1. Base Node.js for Next.js Build ----
    FROM node:18 AS frontend-builder
    WORKDIR /app/frontend
    COPY frontend/package.json frontend/pnpm-lock.yaml ./
    RUN npm install -g pnpm && pnpm install
    COPY frontend .
    RUN pnpm build
    
    # ---- 2. Base Python for FastAPI ----
    FROM python:3.10-slim
    WORKDIR /app
    COPY . .
    RUN pip install -r requirements.txt
    
    # ---- 3. Final Merge Layer ----
    FROM ubuntu:22.04
    
    # 필수 패키지 설치 (nginx, node, python, etc)
    RUN apt update && apt install -y nginx curl python3 python3-pip
    
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
    