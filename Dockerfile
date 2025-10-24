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
COPY backend/package*.json ./
RUN npm install --production

# Copy built frontend into backend's public folder
WORKDIR /app
COPY --from=build /app/dist ./backend/public

# Environment variables
ENV NODE_ENV=production
ENV PORT=3000

# Expose backend port
EXPOSE 3000

# Start backend
WORKDIR /app/backend
CMD ["node", "{
  "import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';

import dataRoutes from './routes/data.js';
import sdkpRoutes from './routes/sdkp.js';
import statusRoutes from './routes/status.js';

dotenv.config();

const app = express();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(cors());
app.use(express.json());

// API routes
app.use('/api/data', dataRoutes);
app.use('/api/sdkp', sdkpRoutes);
app.use('/api/status', statusRoutes);

// Serve built frontend
app.use(express.static(path.join(__dirname, 'public')));
app.get('*', (_, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ Backend running on port ${PORT}`));"]
