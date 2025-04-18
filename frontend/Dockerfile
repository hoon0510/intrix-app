FROM node:18-alpine

WORKDIR /app

COPY frontend/package.json ./frontend/
RUN cd frontend && npm install -g pnpm && pnpm install

COPY frontend/ ./frontend/

RUN cd frontend && pnpm build

WORKDIR /app/frontend
CMD ["pnpm", "start"] 