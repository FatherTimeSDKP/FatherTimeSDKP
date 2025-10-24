# Stage 1 — Build Frontend
FROM node:20 AS build
WORKDIR /app

# Copy root dependencies (frontend)
COPY package*.json ./
RUN npm install

# Copy frontend source
COPY .# Build Docker image
docker build -t timing-sdk-management .

# Run container
docker run -p 3000:3000 timing-sdk-management .

# Build frontend (Vite)
RUN npm run build

# Stage 2 — Setup Backend + Serve App
FROM node:20-alpine
WORKDIR /app

# Copy backend
COPY backend ./backend
WORKDIR /app/backend

# Install backend dependencies
COPY backend/package*.json ./
RUN npm install --production

# Copy built frontend into backend's public folder
WORKDIR /app
COPY --from=build /app/dist ./backend/public

# Set environment
ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

# Run backend server
CMD ["node", "import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Serve built frontend
app.use(express.static(path.join(__dirname, 'public')));

// API routes
import dataRoutes from './routes/data.js';
import sdkpRoutes from './routes/sdkp.js';
import statusRoutes from './routes/status.js';

app.use('/api/data', dataRoutes);
app.use('/api/sdkp', sdkpRoutes);
app.use('/api/status', statusRoutes);

// Catch-all to serve frontend
app.get('*', (_, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Unified SDKP-TimeSeal app running on port ${PORT}`));"]
