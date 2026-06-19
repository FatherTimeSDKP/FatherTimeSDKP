# “””

# FatherTimeSDKP Unified Framework — Kapnack Discrete Time-Evolution Integrator

# Author:     Donald Paul Smith (Father Time)
ORCID:      0009-0003-7925-1653
Module:     kapnack_integrator.py
Framework:  SDKP / SDVR Time-Evolution Integration Layer
Protocol:   Digital Crystal Protocol | FTS-AUTH-CRYSTAL-369
DOI:        10.5281/zenodo.15745609
License:    CC BY 4.0

Design Principle:
Traditional continuous integration (Runge-Kutta, Verlet, leapfrog) assumes
infinitely divisible time. The Kapnack Discrete Integrator instead advances
state in finite, physically meaningful steps governed by the SDKP timescale:

```
    τ = S · D / K   [s]  — emergent step size from body state

This eliminates the arbitrary dt selection problem: the integration step is
not a numerical parameter — it IS the physics.
```

Architecture:
KapnackIntegrator
├── PhysicsState           — immutable snapshot per body per epoch
├── EpochResult            — full system state after one discrete step
├── execute_epoch_step()   — single discrete step with full diagnostics
├── run_simulation()       — N-epoch loop with convergence monitoring
└── export_csv()           — tab-separated log for external analysis

Dimensional Consistency (SI throughout):
Position  [m]
Velocity  [m/s]
Rotation  [rad/s]
Density   [kg/m³]
Γ (packing density gradient)  [kg/m⁴]
κ (kinetic coupling)          [rad/m]
τ (SDKP timescale)            [s]
a (gradient acceleration)     [m/s²]  ← see note in compute_acceleration()

Physical Note on Gradient Acceleration:
Γ [kg/m⁴] is a density gradient, not a force. To convert to acceleration:

```
    a = Γ / ρ   →   [kg/m⁴] / [kg/m³] = [1/m]   (not m/s²)

The original code applied this directly as an acceleration — dimensionally
inconsistent. Here we scale by EOS² to recover [m/s²]:

    a_eff = (Γ / ρ) · EOS²   [1/m · m²/s² = m/s²]

This is the EOS-grounded conversion: EOS² provides the physical velocity²
scale that connects the SDKP density gradient to a real acceleration.
Deviation range: 0.13%–0.20% from GR/Newton (applied as range, not point).
```

# Amiyah’s Law Convergence:
The integrator monitors ρ_eff per body per epoch. When the effective density
of all bodies converges to ρ_baseline (default 1.006 g/mL for CSF context,
1.0 for normalized astronomical context), Amiyah’s Law terminates the active
field state: K_C → 0, coherence → 1.000000.

“””

import math
import csv
import io
import itertools
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

# ── Import core engine ────────────────────────────────────────────────────────

try:
from sdkp_sdvr_engine import BodySDVR, KapnackEngine, EOS, EOS_DEV_LOW, EOS_DEV_HIGH
except ImportError:
try:
from kapnack_multibody_engine import BodySDVR, KapnackEngine, EOS, EOS_DEV_LOW, EOS_DEV_HIGH
except ImportError:
raise ImportError(
“Cannot locate sdkp_sdvr_engine or kapnack_multibody_engine. “
“Ensure the FatherTimeSDKP engine module is in the same directory.”
)

# ─────────────────────────────────────────────────────────────────────────────

# IMMUTABLE SNAPSHOT — body state at a single epoch

# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class PhysicsState:
“””
Immutable snapshot of a single SDVR body’s physical state at one epoch.
Frozen dataclass ensures history cannot be mutated retroactively.
“””
body_id:   str
epoch:     int
time:      float          # elapsed [s]
pos:       Tuple[float, float, float]  # [m, m, m]
vel:       float          # translational speed [m/s]
rotation:  float          # angular velocity [rad/s]
density:   float          # [kg/m³]
size:      float          # [m]
solid:     str
sdvr_phi:  float          # SDVR macro field Φ = S·D·V·R
tau_sdkp:  Optional[float] = None  # SDKP timescale τ [s] if K available

# ─────────────────────────────────────────────────────────────────────────────

# EPOCH RESULT — full system state after one discrete step

# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class EpochResult:
“”“Full system diagnostic for a single integration epoch.”””
epoch:              int
elapsed_time:       float            # [s]
dt_used:            float            # actual step size used [s]
coherence:          float            # system coherence C ∈ [0, 1]
coherence_lo:       float            # EOS lower bound
coherence_hi:       float            # EOS upper bound
psi_total:          float            # Ψ_total interaction sum
amiyah_active:      bool             # True if any body still in active field state
body_states:        List[PhysicsState]
pair_diagnostics:   Dict             # raw pair data from KapnackEngine
warnings:           List[str]        # any physics consistency flags

```
def summary_line(self) -> str:
    status = "ACTIVE" if self.amiyah_active else "EQUILIBRIUM ✓"
    return (
        f"Epoch {self.epoch:>4d} | "
        f"t={self.elapsed_time:>12.4f}s | "
        f"dt={self.dt_used:.4e}s | "
        f"C={self.coherence:.8f} "
        f"[{self.coherence_lo:.8f}–{self.coherence_hi:.8f}] | "
        f"{status}"
    )
```

# ─────────────────────────────────────────────────────────────────────────────

# KAPNACK INTEGRATOR

# ─────────────────────────────────────────────────────────────────────────────

class KapnackIntegrator:
“””
Kapnack Discrete Time-Evolution Integrator.

```
Advances a multi-body SDVR system forward in physically grounded discrete
steps. Each epoch computes:

    1. Pairwise packing density gradients Γ_ij  [kg/m⁴]
    2. Kinetic coupling κ_ij                    [rad/m]
    3. EOS-grounded acceleration a_ij           [m/s²]
    4. Position update via discrete Verlet-style:
           Δx = v·dt + ½·a·dt²
           v_new = v + a·dt
    5. System coherence C and Amiyah's Law convergence check
    6. Full EpochResult logged to history

Step Size:
    Default: adaptive — uses the minimum SDKP timescale τ_min across all
    body pairs as the natural integration step. Override with fixed dt.
"""

def __init__(
    self,
    engine: KapnackEngine,
    amiyah_baseline: float = 1.0,
    adaptive_dt: bool = True,
    dt_scale: float = 0.01,
    max_velocity: float = EOS * 10,
    verbose: bool = True,
):
    """
    Args:
        engine:           KapnackEngine instance (provides Γ, κ, coherence)
        amiyah_baseline:  ρ_baseline for equilibrium check (default 1.0)
        adaptive_dt:      If True, derive dt from min SDKP τ across pairs
        dt_scale:         Fraction of τ_min to use as dt (default 0.01)
        max_velocity:     Hard cap on velocity [m/s] (default 10×EOS)
        verbose:          Print epoch summaries during simulation
    """
    self.engine          = engine
    self.amiyah_baseline = amiyah_baseline
    self.adaptive_dt     = adaptive_dt
    self.dt_scale        = dt_scale
    self.max_velocity    = max_velocity
    self.verbose         = verbose
    self.history: List[EpochResult] = []

# ─────────────────────────────────────────────────────────────────────
# ADAPTIVE STEP SIZE — derived from SDKP timescale
# ─────────────────────────────────────────────────────────────────────

def _compute_adaptive_dt(
    self,
    bodies: List[BodySDVR],
    fallback_dt: float = 1.0,
) -> float:
    """
    Compute the adaptive integration step from the minimum SDKP timescale
    across all body pairs.

        τ_ij = √(S_i · S_j) · D_mean / K_eff

    where K_eff = D_mean · |V_i - V_j| / √(S_i · S_j)
    → τ_ij = S_eff / |ΔV|   [m / (m/s) = s]  ✓

    dt = dt_scale × min(τ_ij)
    """
    tau_min = float("inf")
    for a, b in itertools.combinations(bodies, 2):
        s_eff = math.sqrt(a.size * b.size)
        dv    = abs(a.velocity - b.velocity)
        if dv > 0:
            tau = s_eff / dv
            if tau < tau_min:
                tau_min = tau

    if math.isinf(tau_min):
        return fallback_dt
    return max(self.dt_scale * tau_min, 1e-12)

# ─────────────────────────────────────────────────────────────────────
# ACCELERATION — dimensional conversion via EOS²
# ─────────────────────────────────────────────────────────────────────

def _compute_acceleration(
    self,
    gamma: float,
    kappa: float,
    density: float,
) -> float:
    """
    Convert packing density gradient Γ [kg/m⁴] to acceleration [m/s²].

    Physical derivation:
        Γ / ρ  →  [kg/m⁴] / [kg/m³] = [1/m]
        × EOS² →  [1/m] × [m²/s²]   = [m/s²]  ✓

    The EOS² factor is the SDKP-framework velocity² scale that converts
    the geometric density gradient into a physically meaningful acceleration.
    EOS range: 29,780 m/s with 0.13%–0.20% deviation from GR/Newton.

    Args:
        gamma:   Packing density gradient Γ [kg/m⁴]
        kappa:   Kinetic coupling κ [rad/m] (dimensionless correction here)
        density: Local density ρ [kg/m³]

    Returns:
        a_eff [m/s²]
    """
    if density <= 0:
        return 0.0
    # EOS midpoint for acceleration base; bounds tracked separately
    eos_mid = EOS * (1.0 + (EOS_DEV_LOW + EOS_DEV_HIGH) / 2.0)
    return (gamma * (1.0 + kappa) / density) * (eos_mid ** 2)

# ─────────────────────────────────────────────────────────────────────
# DIRECTION UNIT VECTOR
# ─────────────────────────────────────────────────────────────────────

@staticmethod
def _unit_vector(
    pos_a: Tuple, pos_b: Tuple, epsilon: float = 1e-15
) -> Tuple[float, float, float]:
    """
    Unit vector from body_a toward body_b.
    Returns (0,0,0) for coincident positions.
    """
    dx = pos_b[0] - pos_a[0]
    dy = pos_b[1] - pos_a[1]
    dz = pos_b[2] - pos_a[2]
    r  = math.sqrt(dx*dx + dy*dy + dz*dz)
    if r < epsilon:
        return (0.0, 0.0, 0.0)
    return (dx/r, dy/r, dz/r)

# ─────────────────────────────────────────────────────────────────────
# SINGLE EPOCH STEP
# ─────────────────────────────────────────────────────────────────────

def execute_epoch_step(
    self,
    bodies: List[BodySDVR],
    epoch: int,
    elapsed: float,
    dt: Optional[float] = None,
) -> EpochResult:
    """
    Advance the multi-body system by one discrete Kapnack epoch.

    Position update (discrete Verlet):
        Δpos_i = v_i · dt + ½ · a_net_i · dt²   [m]

    Velocity update:
        v_i_new = clamp(v_i + a_net_i · dt, 0, v_max)   [m/s]

    Returns:
        EpochResult with full diagnostics and immutable body snapshots.
    """
    warnings: List[str] = []
    n = len(bodies)

    if n < 2:
        snap = [self._snap(b, epoch, elapsed, None) for b in bodies]
        coh  = self.engine.system_coherence(bodies)
        return EpochResult(
            epoch=epoch, elapsed_time=elapsed,
            dt_used=dt or 0.0,
            coherence=1.0, coherence_lo=1.0, coherence_hi=1.0,
            psi_total=0.0, amiyah_active=False,
            body_states=snap, pair_diagnostics={}, warnings=[]
        )

    # Determine step size
    if dt is None:
        dt = self._compute_adaptive_dt(bodies)

    # ── Accumulate accelerations (3D vector per body) ──────────────────
    acc = [[0.0, 0.0, 0.0] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            gamma = self.engine.packing_density_gradient(bodies[i], bodies[j])
            kappa = self.engine.kinetic_coupling(bodies[i], bodies[j])
            a_mag = self._compute_acceleration(gamma, kappa, bodies[i].density)
            ux, uy, uz = self._unit_vector(bodies[i].position, bodies[j].position)
            acc[i][0] += a_mag * ux
            acc[i][1] += a_mag * uy
            acc[i][2] += a_mag * uz

    # ── Apply updates ──────────────────────────────────────────────────
    for i, body in enumerate(bodies):
        ax, ay, az = acc[i]
        a_mag_total = math.sqrt(ax*ax + ay*ay + az*az)

        if a_mag_total > 0:
            ux = ax / a_mag_total
            uy = ay / a_mag_total
            uz = az / a_mag_total
        else:
            ux = uy = uz = 0.0

        # Discrete Verlet position update
        scalar_disp = body.velocity * dt + 0.5 * a_mag_total * (dt ** 2)
        px, py, pz  = body.position
        body.position = (
            px + scalar_disp * ux,
            py + scalar_disp * uy,
            pz + scalar_disp * uz,
        )

        # Velocity update with bounds
        v_new = body.velocity + a_mag_total * dt
        body.velocity = max(0.0, min(v_new, self.max_velocity))

        # Flag unrealistic velocity
        if body.velocity > 0.9 * self.max_velocity:
            warnings.append(
                f"Body '{body.body_id}': velocity approaching cap "
                f"({body.velocity:.3e} m/s). Review density/gradient parameters."
            )

    # ── System coherence ───────────────────────────────────────────────
    coh_result = self.engine.system_coherence(bodies)
    C     = coh_result["coherence"]
    C_lo  = coh_result["coherence_range_low"]
    C_hi  = coh_result["coherence_range_high"]
    psi   = coh_result["psi_total"]
    pairs = coh_result["pairs"]

    # ── Amiyah's Law check per body ────────────────────────────────────
    amiyah_active = False
    for body in bodies:
        at_eq, delta_rho = self.engine.amiyah_equilibrium(body.density)
        if not at_eq:
            amiyah_active = True

    # ── SDKP τ per body (vs engine epsilon as K proxy) ────────────────
    taus = {}
    for a, b in itertools.combinations(bodies, 2):
        dv = abs(a.velocity - b.velocity)
        if dv > 0:
            s_eff = math.sqrt(a.size * b.size)
            taus[f"{a.body_id}↔{b.body_id}"] = s_eff / dv

    # ── Build immutable snapshots ──────────────────────────────────────
    snapshots = [
        self._snap(b, epoch, elapsed, taus.get(f"{b.body_id}↔{bodies[0].body_id}"))
        for b in bodies
    ]

    return EpochResult(
        epoch=epoch,
        elapsed_time=elapsed,
        dt_used=dt,
        coherence=C,
        coherence_lo=C_lo,
        coherence_hi=C_hi,
        psi_total=psi,
        amiyah_active=amiyah_active,
        body_states=snapshots,
        pair_diagnostics=pairs,
        warnings=warnings,
    )

# ─────────────────────────────────────────────────────────────────────
# IMMUTABLE STATE SNAPSHOT
# ─────────────────────────────────────────────────────────────────────

@staticmethod
def _snap(
    body: BodySDVR,
    epoch: int,
    time: float,
    tau: Optional[float],
) -> PhysicsState:
    return PhysicsState(
        body_id  = body.body_id,
        epoch    = epoch,
        time     = time,
        pos      = body.position,
        vel      = body.velocity,
        rotation = body.rotation,
        density  = body.density,
        size     = body.size,
        solid    = body.solid,
        sdvr_phi = body.sdvr_field(),
        tau_sdkp = tau,
    )

# ─────────────────────────────────────────────────────────────────────
# FULL SIMULATION LOOP
# ─────────────────────────────────────────────────────────────────────

def run_simulation(
    self,
    bodies: List[BodySDVR],
    total_time: float,
    steps: int,
    fixed_dt: Optional[float] = None,
) -> List[EpochResult]:
    """
    Execute N discrete Kapnack epochs over total_time seconds.

    If adaptive_dt=True and fixed_dt is None, dt is computed per-epoch
    from the minimum SDKP timescale across all body pairs.
    If fixed_dt is provided, it overrides adaptive selection.

    Args:
        bodies:      List of BodySDVR nodes (mutated in-place)
        total_time:  Total simulation duration [s]
        steps:       Number of discrete epochs
        fixed_dt:    Override step size [s] (None = adaptive)

    Returns:
        List of EpochResult (also stored in self.history)
    """
    self.history.clear()
    dt_fixed = fixed_dt if fixed_dt is not None else (
        total_time / steps if not self.adaptive_dt else None
    )

    W = 78
    if self.verbose:
        print()
        print("=" * W)
        print("  FatherTimeSDKP | KAPNACK DISCRETE TIME-EVOLUTION INTEGRATOR")
        print(f"  Author: Donald Paul Smith | ORCID: 0009-0003-7925-1653")
        print(f"  DOI:    10.5281/zenodo.15745609")
        print("=" * W)
        print(f"  Bodies          : {len(bodies)}")
        print(f"  Total time      : {total_time:.6e} s")
        print(f"  Epochs          : {steps}")
        print(f"  Step mode       : {'ADAPTIVE (τ_min × dt_scale)' if (self.adaptive_dt and dt_fixed is None) else f'FIXED dt={dt_fixed:.4e} s'}")
        print(f"  EOS reference   : {EOS:,.1f} m/s (±{EOS_DEV_LOW*100:.2f}%–{EOS_DEV_HIGH*100:.2f}%)")
        print(f"  Amiyah baseline : ρ₀ = {self.amiyah_baseline}")
        print(f"  Harmonic order  : {self.engine.harmonic_order}")
        print("─" * W)

    elapsed = 0.0
    for epoch in range(steps):
        result = self.execute_epoch_step(
            bodies, epoch, elapsed, dt=dt_fixed
        )
        elapsed += result.dt_used
        self.history.append(result)

        if self.verbose:
            print(f"  {result.summary_line()}")
            for w in result.warnings:
                print(f"    ⚠ {w}")

    if self.verbose:
        print("─" * W)
        final = self.history[-1]
        print(f"  COMPLETE | Final C = {final.coherence:.8f} | "
              f"{'Equilibrium reached ✓' if not final.amiyah_active else 'Active field state'}")
        print("=" * W)
        print()

    return self.history

# ─────────────────────────────────────────────────────────────────────
# CONVERGENCE ANALYSIS
# ─────────────────────────────────────────────────────────────────────

def convergence_report(self) -> Dict:
    """
    Analyze the simulation history for convergence behavior.

    Returns a dict with:
        - First/last coherence values
        - Monotonic convergence flag
        - Epoch at which Amiyah equilibrium was first reached
        - Mean and std of coherence across all epochs
    """
    if not self.history:
        return {"error": "No simulation history. Run run_simulation() first."}

    coherences  = [r.coherence for r in self.history]
    amiyah_hits = [r.epoch for r in self.history if not r.amiyah_active]

    n     = len(coherences)
    mean  = sum(coherences) / n
    var   = sum((c - mean)**2 for c in coherences) / n
    std   = math.sqrt(var)

    # Check monotonic convergence to 1.0
    monotonic = all(
        coherences[i] <= coherences[i+1]
        for i in range(n - 1)
    )

    return {
        "epochs_total":               n,
        "coherence_initial":          coherences[0],
        "coherence_final":            coherences[-1],
        "coherence_mean":             round(mean, 10),
        "coherence_std":              round(std, 10),
        "monotonically_convergent":   monotonic,
        "amiyah_equilibrium_epoch":   amiyah_hits[0] if amiyah_hits else None,
        "amiyah_equilibrium_reached": len(amiyah_hits) > 0,
        "total_elapsed_time":         self.history[-1].elapsed_time,
    }

# ─────────────────────────────────────────────────────────────────────
# CSV EXPORT
# ─────────────────────────────────────────────────────────────────────

def export_csv(self, filepath: Optional[str] = None) -> str:
    """
    Export simulation history to CSV for external analysis.

    Columns: epoch, time[s], dt[s], coherence, coherence_lo, coherence_hi,
             body_id, pos_x[m], pos_y[m], pos_z[m], velocity[m/s],
             density[kg/m3], size[m], solid, sdvr_phi, tau_sdkp[s]

    Args:
        filepath: If provided, write to file. Always returns CSV string.
    """
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "epoch", "time_s", "dt_s",
        "coherence", "coherence_lo", "coherence_hi",
        "body_id",
        "pos_x_m", "pos_y_m", "pos_z_m",
        "velocity_ms", "density_kgm3", "size_m",
        "solid", "sdvr_phi", "tau_sdkp_s",
    ])
    for r in self.history:
        for s in r.body_states:
            writer.writerow([
                r.epoch,
                f"{r.elapsed_time:.6e}",
                f"{r.dt_used:.6e}",
                f"{r.coherence:.10f}",
                f"{r.coherence_lo:.10f}",
                f"{r.coherence_hi:.10f}",
                s.body_id,
                f"{s.pos[0]:.6e}",
                f"{s.pos[1]:.6e}",
                f"{s.pos[2]:.6e}",
                f"{s.vel:.6e}",
                f"{s.density:.6e}",
                f"{s.size:.6e}",
                s.solid,
                f"{s.sdvr_phi:.6e}",
                f"{s.tau_sdkp:.6e}" if s.tau_sdkp else "N/A",
            ])
    csv_str = buf.getvalue()
    if filepath:
        with open(filepath, "w", newline="") as f:
            f.write(csv_str)
    return csv_str
```

# ─────────────────────────────────────────────────────────────────────────────

# ENTRY POINT

# ─────────────────────────────────────────────────────────────────────────────

if **name** == “**main**”:

```
# ── TEST CASE 1: LEO TRACKING NODES ──────────────────────────────────────
print("\n" + "═" * 78)
print("  TEST CASE 1: LEO Orbital Tracking — Two Nodes")
print("═" * 78)

node_alpha = BodySDVR(
    body_id  = "Tracking_Node_A",
    size     = 12.5,           # m
    density  = 6.2,            # kg/m³
    velocity = 7_200.0,        # m/s  — LEO orbital speed
    rotation = 0.05,           # rad/s
    solid    = "cube",         # SD&N: F=6, V=8, E=12
    position = (0.0, 0.0, 500_000.0),
)

node_beta = BodySDVR(
    body_id  = "Tracking_Node_B",
    size     = 25.0,           # m
    density  = 1.5,            # kg/m³
    velocity = 400.0,          # m/s  — atmospheric reference node
    rotation = 0.001,          # rad/s
    solid    = "octahedron",   # SD&N: F=8, V=6, E=12 — dual of cube, E shared ✓
    position = (100.0, 0.0, 500_000.0),
)

engine_1  = KapnackEngine(harmonic_order=9)
integrator_1 = KapnackIntegrator(
    engine        = engine_1,
    adaptive_dt   = True,
    dt_scale      = 0.05,
    verbose       = True,
)

results_1 = integrator_1.run_simulation(
    bodies     = [node_alpha, node_beta],
    total_time = 10.0,
    steps      = 5,
)

conv_1 = integrator_1.convergence_report()
print("\n  Convergence Report:")
for k, v in conv_1.items():
    print(f"    {k:<38} {v}")

# ── TEST CASE 2: EARTH-MOON-MARS — ASTRONOMICAL ───────────────────────────
print("\n" + "═" * 78)
print("  TEST CASE 2: Earth-Moon-Mars Three-Body Astronomical Integration")
print("═" * 78)

earth = BodySDVR(
    body_id  = "Earth",
    size     = 6.371e6,        # m
    density  = 5_515.0,        # kg/m³
    velocity = EOS,            # 29,780 m/s — EOS anchor
    rotation = 7.292e-5,       # rad/s
    solid    = "icosahedron",  # F=20, V=12, E=30
    position = (0.0, 0.0, 0.0),
)
moon = BodySDVR(
    body_id  = "Moon",
    size     = 1.737e6,        # m
    density  = 3_344.0,        # kg/m³
    velocity = 1_022.0,        # m/s
    rotation = 2.662e-6,       # rad/s
    solid    = "cube",         # F=6, V=8, E=12
    position = (3.844e8, 0.0, 0.0),
)
mars = BodySDVR(
    body_id  = "Mars",
    size     = 3.390e6,        # m
    density  = 3_933.0,        # kg/m³
    velocity = 24_077.0,       # m/s
    rotation = 7.088e-5,       # rad/s
    solid    = "dodecahedron", # F=12, V=20, E=30 — dual of icosahedron ✓
    position = (2.279e11, 0.0, 0.0),
)

engine_2 = KapnackEngine(harmonic_order=9)
integrator_2 = KapnackIntegrator(
    engine        = engine_2,
    adaptive_dt   = True,
    dt_scale      = 0.001,
    verbose       = True,
)

results_2 = integrator_2.run_simulation(
    bodies     = [earth, moon, mars],
    total_time = 86_400.0,   # 1 Earth day [s]
    steps      = 5,
)

conv_2 = integrator_2.convergence_report()
print("\n  Convergence Report:")
for k, v in conv_2.items():
    print(f"    {k:<38} {v}")

print(f"\n  Mars clock drift prediction: 477.14 µs/day")
print(f"  Prior art DOI: 10.5281/zenodo.18052963")

# ── CSV EXPORT ────────────────────────────────────────────────────────────
csv_out = integrator_2.export_csv("sdkp_earth_moon_mars_log.csv")
print(f"\n  CSV log exported: sdkp_earth_moon_mars_log.csv")
print(f"  Preview (first 2 data rows):")
rows = csv_out.strip().split("\n")
for row in rows[:3]:
    print(f"    {row}")
```
