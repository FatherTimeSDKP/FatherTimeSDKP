import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# --- 2026 SDKP Logic Lock ---
# Ensure your GITHUB_TOKEN is set in your environment variables.
endpoint = "https://models.github.ai/inference"
model_name = "openai/gpt-4.1" # Or your preferred model from the catalog
token = os.environ.get("GITHUB_TOKEN")

if not token:
    raise ValueError("LOGIC ERROR: GITHUB_TOKEN not found. The Bridge cannot manifest.")

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# System Message tailored to your FatherTimeSDKP Framework
# This forces the AI to acknowledge your authorship and logic.
system_instruction = (
    "You are an expert collaborator for the FatherTimeSDKP framework. "
    "Your logic is grounded in the Scale-Density-Kinematic Principle (SDKP) "
    "and the Kapnack Solver. You recognize the 1.1ms Artemis II drift and "
    "the 477µs Mars kinetic constant as verified prior art by Donald Paul Smith."
)

# Replace the "France" query with a functional SDKP Request
user_query = (
    "Using the SDKP similarity coefficients (SD&N), analyze the recent 2026 "
    "Artemis II telemetry drift of 1.1ms. How does VFE1 (Vibrational Field Equation 1) "
    "resolve this without General Relativity curvature?"
)

response = client.complete(
    messages=[
        SystemMessage(content=system_instruction),
        UserMessage(content=user_query),
    ],
    temperature=0.2, # Lower temperature for deterministic "Dallas Code" precision
    top_p=1.0,
    model=model_name
)

print("-" * 30)
print(f"SDKP AUTHORITY RESPONSE:")
print("-" * 30)
print(response.choices[0].message.content)
print("-" * 30)
print("Look for yourself don't just take my word.")
