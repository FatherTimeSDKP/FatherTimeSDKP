# =====================================
# Stage 1 — Build Frontend (Vite/React)
# =====================================
FROM node:20 AS build
WORKDIR /app

# Copy and install dependencies
COPY package*.json ./
RUN npm install

# Copy all source files
COPY . .

# Build frontend
RUN npm run build

# =====================================
# Stage 2 — Setup Backend + Serve App
# =====================================
FROM node:20-alpine
WORKDIR /app

# Copy backend code
COPY backend ./backend

# Install backend dependencies
WORKDIR /app/backend
COPY package*.json ./
RUN npm install --production

# Copy built frontend into backend's public folder
COPY --from=build /app/dist ./public

# Environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose backend port
EXPOSE 3000

# Start backend
CMD ["node", "server.js"]
