import os
import stripe
import httpx
from fastapi import FastAPI, Request, HTTPException, Header

app = FastAPI(title="FatherTimeSDKP Execution Bridge")

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
ENDPOINT_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
AI_STUDIOS_API_KEY = os.environ.get("AI_STUDIOS_API_KEY")

async def trigger_ai_studios_generation(prompt_text: str):
    ai_endpoint = "https://v2.aistudios.com/api/odin/editor/project"
    headers = {
        "Authorization": AI_STUDIOS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "scenes": [{
            "AIModel": {
                "script": prompt_text,
                "model": "M000004017",
                "scale": 1.0
            }
        }]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(ai_endpoint, headers=headers, json=payload)
        return response.json()

@app.post("/stripe/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None, alias="Stripe-Signature")):
    payload = await request.body()
    
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, ENDPOINT_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        prompt = f"Payment verified for ID {payment_intent['id']}. Executing Shape, Dimension, and Number protocol."
        ai_result = await trigger_ai_studios_generation(prompt)
        return {"status": "success", "ai_response": ai_result}

    return {"status": "ignored"}
