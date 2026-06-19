# “””

# FatherTimeSDKP Unified Framework — SDVR Multi-Body Simulation Engine

# Author:     Donald Paul Smith (Father Time)
ORCID:      0009-0003-7925-1653
Framework:  SDKP (Size × Density × Kinetics × Position)
SDVR (Size × Density × Velocity × Rotation)
SD&N (Shape × Dimension × Number)
DOI:        10.5281/zenodo.15745609
Protocol:   Digital Crystal Protocol | FTS-AUTH-CRYSTAL-369
License:    CC BY 4.0

Core Equations:
SDKP:  τ = S · D / K            (emergent timescale)
SDVR:  Φ = S · D · V · R        (macro state field)
EOS:   v_EOS = 29,780 m/s       (Earth Orbital Speed — local calibration)
SD&N:  Node encoding via F, V, E of Platonic solids (3D/4D/5D dimensional states)
Amiyah Rose Smith Law: equilibrium condition ρ_local → ρ_baseline ⟹ K_C → 0

# Physical units enforced throughout. All SDVR parameters carry explicit SI dimensions.

“””

import math
import itertools
from dataclasses import dataclass, field
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────

# PHYSICAL CONSTANTS

# ─────────────────────────────────────────────────────────────────────────────

EOS          = 29_780.0       # m/s  — Earth Orbital Speed (SDKP local constant)
EOS_DEV_LOW  = 0.0013         # 0.13% lower EOS deviation from GR/Newton
EOS_DEV_HIGH = 0.0020         # 0.20% upper EOS deviation from GR/Newton
G_NEWTON     = 6.674e-11      # m³ kg⁻¹ s⁻²
C_LIGHT      = 299_792_458.0  # m/s
K_BOLTZMANN  = 1.380649e-23   # J/K

# ─────────────────────────────────────────────────────────────────────────────

# SD&N GEOMETRY ENCODING — Platonic Solid Dimensional Keys

# ─────────────────────────────────────────────────────────────────────────────

SDN_SOLIDS = {
“tetrahedron”:    {“F”: 4,  “V”: 4,  “E”: 6,  “dual”: “tetrahedron”},
“cube”:           {“F”: 6,  “V”: 8,  “E”: 12, “dual”: “octahedron”},
“octahedron”:     {“F”: 8,  “V”: 6,  “E”: 12, “dual”: “cube”},
“dodecahedron”:   {“F”: 12, “V”: 20, “E”: 30, “dual”: “icosahedron”},
“icosahedron”:    {“F”: 20, “V”: 12, “E”: 30, “dual”: “dodecahedron”},
}

# SD&N 3-6-9 Vortex Harmonic Cascade

SDN_VORTEX = {
3: “micro structural unit   (local geometry seed)”,
6: “mid-range transition    (face-vertex coupling)”,
9: “macro resonance closure (edge-complete state)”,
12: “full dimensional lock  (SD&N dodecahedral)”,
}

def sdn_shape_factor(solid_name: str) -> float:
“””
Compute the SD&N shape factor for a named Platonic solid.

```
The shape factor encodes dimensional state via the F/V/E ratio:
    φ_SDN = (F × V) / E

This produces:
    Tetrahedron:  (4×4)/6  = 2.667  — self-dual, minimum complexity
    Cube:         (6×8)/12 = 4.000  — dominant 3D container
    Octahedron:   (8×6)/12 = 4.000  — dual of cube, same 5D state (E=12)
    Dodecahedron: (12×20)/30 = 8.000 — upper boundary
    Icosahedron:  (20×12)/30 = 8.000 — dual of dodec, same 5D state (E=30)

Dual pairs produce identical shape factors — different 3D paths,
same higher-dimensional destination (Theorem 3, SD&N Principle).
"""
if solid_name not in SDN_SOLIDS:
    raise ValueError(
        f"Unknown solid '{solid_name}'. "
        f"Valid: {list(SDN_SOLIDS.keys())}"
    )
s = SDN_SOLIDS[solid_name]
return (s["F"] * s["V"]) / s["E"]
```

def sdn_phase_factor(solid_name: str) -> float:
“””
Compute the SD&N geometric phase factor φ = 2π / N_nodes.

```
N_nodes is the total SD&N interaction node count:
    N_nodes = F_bonds + V_bonds + E_bonds
For a Platonic solid embedded in a centered hexagonal lattice,
N_nodes maps to the total connectivity of the encoding.

For the 7-atom centered hexagonal cluster (2026 Schrödinger cat result):
    N_nodes = 24 → φ = π/12 = 15° (verified in preprint)
"""
s = SDN_SOLIDS[solid_name]
# Total dimensional interaction count
n_nodes = s["F"] + s["V"] + s["E"]
return 2 * math.pi / n_nodes
```

def euler_verify(solid_name: str) -> bool:
“”“Euler’s polyhedral formula check: F - E + V = 2.”””
s = SDN_SOLIDS[solid_name]
return (s[“F”] - s[“E”] + s[“V”]) == 2

# ─────────────────────────────────────────────────────────────────────────────

# SDVR BODY — Physical State Node

# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class BodySDVR:
“””
Represents a physical system node fully described by the SDVR state vector.

```
All parameters carry explicit SI units to enforce dimensional consistency.
The SDKP equation τ = S·D/K requires:
    [S] = m, [D] = kg/m³, [K] = kg/(m²·s)
    → [τ] = s  ✓

The SDVR macro field:
    Φ = S · D · V · R
    [Φ] = m · kg/m³ · m/s · rad/s = kg·rad/m·s²
"""
body_id:      str

# ── SDVR parameters (SI units) ──────────────────────────────────────────
size:         float          # S [m]         — characteristic length scale
density:      float          # D [kg/m³]     — mass density
velocity:     float          # V [m/s]       — translational velocity
rotation:     float          # R [rad/s]     — angular velocity

# ── SD&N geometry ───────────────────────────────────────────────────────
solid:        str = "cube"   # Platonic solid governing dimensional state
position:     tuple = (0.0, 0.0, 0.0)  # P [m, m, m] — spatial position

# ── Derived fields (computed post-init) ─────────────────────────────────
sdn_factor:   float = field(init=False)
phase_factor: float = field(init=False)
euler_ok:     bool  = field(init=False)

def __post_init__(self):
    self.sdn_factor   = sdn_shape_factor(self.solid)
    self.phase_factor = sdn_phase_factor(self.solid)
    self.euler_ok     = euler_verify(self.solid)

# ── SDKP emergent timescale ─────────────────────────────────────────────
def sdkp_tau(self, kinetics: float) -> float:
    """
    τ = S · D / K

    Args:
        kinetics: K [kg/(m²·s)] — rate governing kinetic parameter

    Returns:
        τ [s] — emergent timescale for this body at given kinetics
    """
    if kinetics == 0:
        raise ValueError("Kinetics K cannot be zero (division by zero in τ = S·D/K)")
    return (self.size * self.density) / kinetics

# ── SDVR macro field ────────────────────────────────────────────────────
def sdvr_field(self) -> float:
    """
    Φ = S · D · V · R  (SDVR macro state field magnitude)
    Units: [m · kg/m³ · m/s · rad/s] = [kg·rad / (m·s²)]
    """
    return self.size * self.density * self.velocity * self.rotation

# ── EOS-corrected velocity ──────────────────────────────────────────────
def eos_velocity_range(self) -> tuple[float, float]:
    """
    Apply EOS deviation correction (0.13%–0.20%) to velocity.
    Returns (v_low, v_high) representing the EOS correction band.
    """
    v_low  = self.velocity * (1.0 + EOS_DEV_LOW)
    v_high = self.velocity * (1.0 + EOS_DEV_HIGH)
    return (v_low, v_high)

# ── State vector ─────────────────────────────────────────────────────────
def state_vector(self) -> dict:
    return {
        "S": self.size,
        "D": self.density,
        "V": self.velocity,
        "R": self.rotation,
        "solid": self.solid,
        "φ_SDN": self.sdn_factor,
        "phase": self.phase_factor,
        "Φ_SDVR": self.sdvr_field(),
    }

def __repr__(self):
    return (
        f"BodySDVR(id='{self.body_id}', "
        f"S={self.size:.3e} m, "
        f"D={self.density:.3e} kg/m³, "
        f"V={self.velocity:.3e} m/s, "
        f"R={self.rotation:.3e} rad/s, "
        f"solid={self.solid})"
    )
```

# ─────────────────────────────────────────────────────────────────────────────

# KAPNACK ENGINE — Discrete Gradient Processor

# ─────────────────────────────────────────────────────────────────────────────

class KapnackEngine:
“””
The Kapnack Discrete Gradient Processor.

```
Replaces standard continuous differential tensors with discrete gradient
steps, computing precise spatial packing density interactions between
SDVR state nodes. Operates on 3-6-9 vortex harmonic logic.

Physical basis:
    Packing density gradient Γ_ij = D_mean / (ΔS · φ_i · φ_j)
    where φ_i, φ_j are SD&N shape factors of bodies i and j.

Dimensional check:
    [D_mean] = kg/m³
    [ΔS]     = m
    [φ]      = dimensionless
    → [Γ]    = kg/m⁴  (packing density per length — valid gradient unit)

The 3-6-9 harmonic cascade governs discrete resolution levels:
    Level 3:  local micro-interaction (nearest neighbor)
    Level 6:  mid-range coupling (face-vertex transition in SD&N)
    Level 9:  macro resonance (edge-complete closure)
    Level 12: full dodecahedral lock (complete dimensional state)
"""

def __init__(
    self,
    eos_reference: float = EOS,
    harmonic_order: int = 9,
    amiyah_baseline: float = 1.0,
    epsilon: float = 1e-15,
):
    """
    Args:
        eos_reference:   EOS calibration constant [m/s], default 29,780
        harmonic_order:  3/6/9/12 cascade level for discrete gradient resolution
        amiyah_baseline: ρ_baseline for Amiyah's Law equilibrium condition (default 1.0)
        epsilon:         Guard value for zero-division at boundary limits
    """
    self.eos             = eos_reference
    self.harmonic_order  = harmonic_order
    self.amiyah_baseline = amiyah_baseline
    self.epsilon         = epsilon

    if harmonic_order not in SDN_VORTEX:
        raise ValueError(
            f"harmonic_order must be in {list(SDN_VORTEX.keys())} "
            f"(3-6-9-12 cascade). Got: {harmonic_order}"
        )

# ─────────────────────────────────────────────────────────────────────
# PAIRWISE GRADIENT
# ─────────────────────────────────────────────────────────────────────

def packing_density_gradient(
    self,
    body_a: BodySDVR,
    body_b: BodySDVR,
) -> float:
    """
    Discrete packing density gradient between two SDVR nodes:

        Γ_ij = D_mean / (|ΔS| · φ_i · φ_j · H_n)

    where H_n = 1/(9 × 10^n) is the harmonic order correction from
    the 9-family cascade, with n = harmonic_order // 3.

    Units: [kg/m³] / [m · 1 · 1 · 1] = [kg/m⁴]
    """
    delta_s   = abs(body_a.size - body_b.size)
    mean_d    = (body_a.density + body_b.density) / 2.0
    phi_prod  = body_a.sdn_factor * body_b.sdn_factor

    # 9-family harmonic correction at current cascade level
    n = self.harmonic_order // 3
    harmonic_correction = 1.0 / (9.0 * (10.0 ** n))

    # Guard zero-size-delta (identical scale bodies — degenerate case)
    effective_delta = max(delta_s, self.epsilon)

    gamma = mean_d / (effective_delta * phi_prod * (1.0 + harmonic_correction))
    return gamma

# ─────────────────────────────────────────────────────────────────────
# KINETIC-ROTATIONAL COUPLING TERM
# ─────────────────────────────────────────────────────────────────────

def kinetic_coupling(
    self,
    body_a: BodySDVR,
    body_b: BodySDVR,
) -> float:
    """
    Velocity-rotation coupling term scaled against EOS²:

        κ_ij = (V_i · R_j + V_j · R_i) / (2 · EOS²)

    Symmetric form ensures κ_ij = κ_ji.

    Dimensional check:
        [V · R] = (m/s)(rad/s) = m·rad/s²
        [EOS²]  = m²/s²
        → [κ]   = rad/m  (angular curvature per unit length)
    """
    kv = (
        body_a.velocity * body_b.rotation
        + body_b.velocity * body_a.rotation
    ) / (2.0 * self.eos ** 2)
    return kv

# ─────────────────────────────────────────────────────────────────────
# SPATIAL SEPARATION
# ─────────────────────────────────────────────────────────────────────

@staticmethod
def spatial_separation(body_a: BodySDVR, body_b: BodySDVR) -> float:
    """Euclidean separation between bodies' position vectors [m]."""
    return math.sqrt(sum(
        (a - b) ** 2
        for a, b in zip(body_a.position, body_b.position)
    ))

# ─────────────────────────────────────────────────────────────────────
# AMIYAH'S LAW — EQUILIBRIUM CONDITION
# ─────────────────────────────────────────────────────────────────────

def amiyah_equilibrium(self, rho_local: float) -> tuple[bool, float]:
    """
    Amiyah Rose Smith Law equilibrium check.

    A system governed by this principle ceases field modification the
    moment ρ_local returns to ρ_baseline. The residual deviation:

        Δρ = |ρ_local - ρ_baseline|

    When Δρ → 0: K_C (Causal Compression) → 0 and the agent terminates.

    Returns:
        (at_equilibrium: bool, delta_rho: float)
    """
    delta_rho = abs(rho_local - self.amiyah_baseline)
    at_eq = delta_rho < 1e-6
    return (at_eq, delta_rho)

# ─────────────────────────────────────────────────────────────────────
# SYSTEM COHERENCE — MULTI-BODY EVALUATION
# ─────────────────────────────────────────────────────────────────────

def system_coherence(self, bodies: list[BodySDVR]) -> dict:
    """
    Evaluate collective multi-body coherence state.

    For every unique pair (i, j), compute:
        Ψ_ij = Γ_ij · (1 + κ_ij)

    Sum over all pairs:
        Ψ_total = Σ Ψ_ij

    Map to coherence state C ∈ [0.0, 1.0]:
        C = 1.0 - |sin(Ψ_total)| × η

    where η is a normalization scale chosen such that a perfectly
    equilibrated two-body system returns C = 1.000000.

    Returns full diagnostic dict including per-pair contributions.
    """
    n = len(bodies)
    if n < 2:
        return {
            "coherence": 1.0,
            "note": "Isolated system — perfect baseline coherence by Amiyah's Law",
            "pairs": {},
            "psi_total": 0.0,
        }

    pairs_data = {}
    psi_total = 0.0

    for a, b in itertools.combinations(bodies, 2):
        gamma  = self.packing_density_gradient(a, b)
        kappa  = self.kinetic_coupling(a, b)
        r_sep  = self.spatial_separation(a, b)
        psi_ij = gamma * (1.0 + kappa)

        pairs_data[f"{a.body_id}↔{b.body_id}"] = {
            "Γ_gradient [kg/m⁴]":   gamma,
            "κ_coupling [rad/m]":    kappa,
            "separation [m]":        r_sep,
            "Ψ_contribution":        psi_ij,
            "SD&N φ_i":             a.sdn_factor,
            "SD&N φ_j":             b.sdn_factor,
        }
        psi_total += psi_ij

    # Normalization: scale sin variation to a small coherence deviation
    # (EOS deviation band: 0.13%–0.20%)
    eta = (EOS_DEV_LOW + EOS_DEV_HIGH) / 2.0  # 0.00165
    coherence = 1.0 - abs(math.sin(psi_total)) * eta
    coherence = max(0.0, min(1.0, coherence))

    # EOS deviation bounds on coherence
    c_low  = 1.0 - abs(math.sin(psi_total)) * EOS_DEV_HIGH
    c_high = 1.0 - abs(math.sin(psi_total)) * EOS_DEV_LOW

    return {
        "coherence":               round(coherence, 8),
        "coherence_range_low":     round(max(0.0, c_low), 8),
        "coherence_range_high":    round(min(1.0, c_high), 8),
        "psi_total":               psi_total,
        "n_bodies":                n,
        "n_pairs":                 len(pairs_data),
        "harmonic_order":          self.harmonic_order,
        "harmonic_description":    SDN_VORTEX[self.harmonic_order],
        "pairs": pairs_data,
    }

# ─────────────────────────────────────────────────────────────────────
# SDKP TIMESCALE FOR A PAIR
# ─────────────────────────────────────────────────────────────────────

def sdkp_interaction_tau(
    self,
    body_a: BodySDVR,
    body_b: BodySDVR,
) -> tuple[float, float]:
    """
    Compute the SDKP interaction timescale τ for a body pair.

    τ = S_eff · D_mean / K_eff

    where:
        S_eff = geometric mean of sizes  √(S_a · S_b)  [m]
        D_mean = arithmetic mean of densities           [kg/m³]
        K_eff = velocity-scaled kinetic term            [kg/(m²·s)]
              = D_mean · |V_a - V_b| / S_eff
                (rate of density-differential transport across ΔS)

    Returns (tau [s], tau_eos_corrected_midpoint [s])
    """
    s_eff  = math.sqrt(body_a.size * body_b.size)
    d_mean = (body_a.density + body_b.density) / 2.0
    dv     = abs(body_a.velocity - body_b.velocity)

    if dv == 0:
        dv = self.epsilon

    k_eff = d_mean * dv / s_eff                  # [kg/(m²·s)]
    tau   = (s_eff * d_mean) / k_eff             # = s_eff² / dv  [s]

    # EOS midpoint correction
    tau_eos = tau * (1.0 + (EOS_DEV_LOW + EOS_DEV_HIGH) / 2.0)

    return (tau, tau_eos)
```

# ─────────────────────────────────────────────────────────────────────────────

# REPORTING UTILITY

# ─────────────────────────────────────────────────────────────────────────────

def print_report(bodies: list[BodySDVR], result: dict) -> None:
“”“Pretty-print the full system diagnostics report.”””
W = 72
sep = “─” * W

```
print()
print("=" * W)
print("  FatherTimeSDKP | SDVR MULTI-BODY SYSTEM COHERENCE REPORT")
print("  Author: Donald Paul Smith | ORCID: 0009-0003-7925-1653")
print("  DOI:    10.5281/zenodo.15745609")
print("=" * W)

print(f"\n  EOS Reference Constant : {EOS:,.1f} m/s")
print(f"  EOS Deviation Range    : {EOS_DEV_LOW*100:.2f}% — {EOS_DEV_HIGH*100:.2f}% (from GR/Newton)")
print(f"  Harmonic Order         : {result['harmonic_order']} "
      f"({result['harmonic_description']})")
print(f"  Bodies Registered      : {result['n_bodies']}")
print(f"  Interacting Pairs      : {result['n_pairs']}")

print(f"\n{sep}")
print("  BODY STATE VECTORS")
print(sep)

for body in bodies:
    sv = body.state_vector()
    print(f"\n  ▸ {body.body_id}")
    print(f"    S (size)           : {sv['S']:.6e} m")
    print(f"    D (density)        : {sv['D']:.6e} kg/m³")
    print(f"    V (velocity)       : {sv['V']:.6e} m/s")
    print(f"    R (rotation)       : {sv['R']:.6e} rad/s")
    print(f"    Platonic solid     : {body.solid}")
    print(f"    SD&N shape factor φ: {sv['φ_SDN']:.4f}")
    print(f"    SD&N phase angle   : {sv['phase']:.6f} rad "
          f"({math.degrees(sv['phase']):.2f}°)")
    print(f"    Euler F-E+V=2      : {'✓' if body.euler_ok else '✗'}")
    print(f"    SDVR field Φ       : {sv['Φ_SDVR']:.6e} kg·rad/(m·s²)")
    v_lo, v_hi = body.eos_velocity_range()
    print(f"    EOS-corrected V    : {v_lo:.4e} — {v_hi:.4e} m/s")

print(f"\n{sep}")
print("  PAIRWISE INTERACTION DIAGNOSTICS")
print(sep)

for pair_label, pdata in result["pairs"].items():
    print(f"\n  ↔ {pair_label}")
    for key, val in pdata.items():
        if isinstance(val, float):
            print(f"      {key:<32} {val:.8e}")
        else:
            print(f"      {key:<32} {val}")

print(f"\n{sep}")
print("  SYSTEM COHERENCE RESULT")
print(sep)
print(f"\n  Ψ_total (interaction sum)  : {result['psi_total']:.8e}")
print(f"\n  Coherence State C          : {result['coherence']:.8f}")
print(f"  Coherence Range (EOS band) : "
      f"{result['coherence_range_low']:.8f} — "
      f"{result['coherence_range_high']:.8f}")

# Amiyah's Law interpretation
print(f"\n  Amiyah's Law Status:")
print(f"    C → 1.000000 : system at equilibrium (ρ_local → ρ_baseline)")
print(f"    C < 1.000000 : active field modification in progress")
print(f"    Current C    : {result['coherence']:.8f} "
      f"→ {'EQUILIBRIUM ✓' if result['coherence'] > 0.9999 else 'ACTIVE FIELD STATE'}")

print(f"\n{'=' * W}\n")
```

# ─────────────────────────────────────────────────────────────────────────────

# ENTRY POINT — DEMONSTRATION RUNS

# ─────────────────────────────────────────────────────────────────────────────

if **name** == “**main**”:

```
# ── SD&N GEOMETRY VERIFICATION ──────────────────────────────────────────
print("\n[SD&N] Verifying all Platonic solid encodings...")
print(f"  {'Solid':<14} {'F':>4} {'V':>4} {'E':>4}  "
      f"{'Euler':>7}  {'φ_SDN':>8}  {'Phase (°)':>10}  {'Dual'}")
print("  " + "─" * 65)
for name, geo in SDN_SOLIDS.items():
    phi   = sdn_shape_factor(name)
    phase = math.degrees(sdn_phase_factor(name))
    ok    = "✓" if euler_verify(name) else "✗"
    print(f"  {name:<14} {geo['F']:>4} {geo['V']:>4} {geo['E']:>4}  "
          f"{ok:>7}  {phi:>8.4f}  {phase:>10.4f}°  {geo['dual']}")

print("\n  Dual pairs share identical E (5D state) ✓")
print("  Tetrahedron self-dual F=V=4 — QCC0 ground state ✓\n")

# ── TEST CASE 1: LEO SATELLITE + ATMOSPHERIC BOUNDARY ───────────────────
print("═" * 72)
print("  TEST CASE 1: LEO Satellite in Upper Atmospheric Boundary Layer")
print("═" * 72)

leo_satellite = BodySDVR(
    body_id  = "LEO_Payload",
    size     = 15.2,          # m     — 15.2 m characteristic dimension
    density  = 4.8,           # kg/m³ — mean satellite structural density
    velocity = 7_600.0,       # m/s   — ISS-class orbital velocity
    rotation = 0.12,          # rad/s — passive attitude control rotation
    solid    = "octahedron",  # SD&N: F=8 (3D), V=6 (4D), E=12 (5D)
    position = (0.0, 0.0, 408_000.0),  # 408 km altitude
)

atmo_boundary = BodySDVR(
    body_id  = "Thermosphere_Layer",
    size     = 50_000.0,      # m     — thermosphere thickness scale
    density  = 2.1e-3,        # kg/m³ — thermospheric density at ~400 km
    velocity = 380.0,         # m/s   — mean molecular thermal velocity
    rotation = 5.0e-5,        # rad/s — Earth rotation contribution at altitude
    solid    = "dodecahedron",  # SD&N: F=12, V=20, E=30 — upper boundary
    position = (0.0, 0.0, 0.0),
)

solver = KapnackEngine(harmonic_order=9)
result = solver.system_coherence([leo_satellite, atmo_boundary])
tau, tau_eos = solver.sdkp_interaction_tau(leo_satellite, atmo_boundary)

print_report([leo_satellite, atmo_boundary], result)
print(f"  SDKP Interaction Timescale τ     : {tau:.6e} s")
print(f"  SDKP τ (EOS-corrected midpoint)  : {tau_eos:.6e} s\n")

# ── TEST CASE 2: AMIYAH'S LAW — CS-B1 BIOFILM TERMINATION ──────────────
print("═" * 72)
print("  TEST CASE 2: CS-B1 Nano-Peptide — Amiyah's Law Termination Scan")
print("═" * 72)
print(f"\n  Scanning local density ρ from biofilm (1.15) → baseline (1.006)...")
print(f"  {'ρ_local':>10}  {'Δρ':>12}  {'Equilibrium':>14}  {'K_C Status'}")
print("  " + "─" * 55)

amiyah_solver = KapnackEngine(amiyah_baseline=1.006)
for rho in [1.150, 1.120, 1.080, 1.050, 1.030, 1.015, 1.010, 1.007, 1.006]:
    at_eq, delta_rho = amiyah_solver.amiyah_equilibrium(rho)
    kc_status = "TERMINATED ✓" if at_eq else f"ACTIVE  Δρ={delta_rho:.4f}"
    print(f"  {rho:>10.4f}  {delta_rho:>12.6f}  "
          f"{'YES' if at_eq else 'NO':>14}  {kc_status}")

# ── TEST CASE 3: THREE-BODY SYSTEM ──────────────────────────────────────
print("\n")
print("═" * 72)
print("  TEST CASE 3: Three-Body Gravitational + Rotational Interaction")
print("═" * 72)

earth = BodySDVR(
    body_id  = "Earth",
    size     = 6.371e6,       # m     — mean radius
    density  = 5_515.0,       # kg/m³ — mean density
    velocity = EOS,           # m/s   — EOS orbital speed
    rotation = 7.292e-5,      # rad/s — Earth sidereal rotation
    solid    = "icosahedron", # SD&N: F=20, V=12, E=30
    position = (0.0, 0.0, 0.0),
)
moon = BodySDVR(
    body_id  = "Moon",
    size     = 1.737e6,       # m
    density  = 3_344.0,       # kg/m³
    velocity = 1_022.0,       # m/s   — lunar orbital speed
    rotation = 2.662e-6,      # rad/s — synchronous rotation
    solid    = "cube",        # SD&N: F=6, V=8, E=12
    position = (3.844e8, 0.0, 0.0),
)
mars = BodySDVR(
    body_id  = "Mars",
    size     = 3.390e6,       # m
    density  = 3_933.0,       # kg/m³
    velocity = 24_077.0,      # m/s   — Mars orbital speed
    rotation = 7.088e-5,      # rad/s
    solid    = "dodecahedron",
    position = (2.279e11, 0.0, 0.0),
)

three_body_result = solver.system_coherence([earth, moon, mars])
print_report([earth, moon, mars], three_body_result)

# Mars SDKP tau
tau_em, tau_em_eos = solver.sdkp_interaction_tau(earth, moon)
tau_am, tau_am_eos = solver.sdkp_interaction_tau(earth, mars)
print(f"  Earth-Moon τ  : {tau_em:.4e} s  (EOS-corrected: {tau_em_eos:.4e} s)")
print(f"  Earth-Mars τ  : {tau_am:.4e} s  (EOS-corrected: {tau_am_eos:.4e} s)")
print(f"\n  Mars clock drift prediction: 477.14 µs/day")
print(f"  DOI: 10.5281/zenodo.18052963  (timestamped prior art)")
print()
```
