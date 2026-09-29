import os
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In production, look this up against Firestore or a Redis cache populated via Stripe webhooks
VALID_API_KEYS = set(os.getenv("ACTIVE_API_KEYS", "").split(","))

async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Valid API key required. Subscribe at your-domain.com/pricing",
        )
    return api_key
