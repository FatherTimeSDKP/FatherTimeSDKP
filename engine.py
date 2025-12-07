import json
import numpy as np

# ---------------------------------------------------------
# Load Configuration
# ---------------------------------------------------------
with open("config.json", "r") as f:
    cfg = json.load(f)

size = np.array(cfg["size"])
density = np.array(cfg["density"])
rotation = cfg["rotation"]
velocity = np.array(cfg["velocity"])
crystal_weights = np.array(cfg["crystal12_weights"])

# ---------------------------------------------------------
# SDKP Tensor
# ---------------------------------------------------------
def sdkp_tensor(S, D, ω, v):
    return S * D * ω * v

SDKP = sdkp_tensor(size, density, rotation, velocity)

# ---------------------------------------------------------
# Crystal-12 → 3x3 Projection
# ---------------------------------------------------------
def crystal12_matrix(weights):
    C12 = np.diag(weights)
    # project to 3x3 by simple block extraction
    return C12[:3, :3]

Σ = crystal12_matrix(crystal_weights)

# ---------------------------------------------------------
# Kapnack Recursion Function
# ---------------------------------------------------------
def update(A_n, Σ, ρ, ω):
    return Σ @ A_n + ω * ρ

# ---------------------------------------------------------
# Main Simulation Loop
# ---------------------------------------------------------
print("\n--- FatherTimeSDKP Engine ---")

A = np.array(cfg["A0"])
print("Initial A0:", A)

history = [A]

for step in range(10):
    A = update(A, Σ, density, rotation)
    history.append(A)
    print(f"A{step+1}:", A)

# ---------------------------------------------------------
# Entropy & Time Drift
# ---------------------------------------------------------
ΔS = float(np.sum(np.abs(history[-1] - history[0])))
Δτ = float(ΔS / (1 + np.linalg.norm(SDKP)))

print("\nEntropy ΔS:", ΔS)
print("Time Drift Δτ:", Δτ)
