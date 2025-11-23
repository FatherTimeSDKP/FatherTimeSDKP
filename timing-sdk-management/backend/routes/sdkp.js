import express from 'express';
import { getSDKPState } from '../controllers/sdkpController.js';

const router = express.Router();

router.get('/', getSDKPState);

export default router;
