import express from 'express';
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
app.listen(PORT, () => console.log(`✅ Backend running on port ${PORT}`));
