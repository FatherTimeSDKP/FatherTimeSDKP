# sdkp_optionA_full_repro.py
# Option A: Full-precision reproducibility script for 12-mode SDKP / QCC0 / VFE1
# - Provides canonical C (12x12), W6, Phi50
# - Builds entangler G (NN), T6, 21-op enforcement loop
# - Runs a single enforcement pass and an optional small sweep
# - Saves CSV + PNG diagnostics
#
# WARNING: Hilbert space size = levels**k. Default levels=2 (2^12=4096 states) to be practical.
# If you increase 'levels', ensure you have adequate RAM/CPU.

import os
import csv
import numpy as np
import qutip as qt
import matplotlib.pyplot as plt
from scipy.linalg import eigh

# -----------------------------
# User-configurable parameters
# -----------------------------
k = 12                 # compressed modes (12)
levels = 2             # Fock truncation per mode (2 => vacuum + 1)
alpha = 0.5            # coherent amplitude on anchor mode
t_entangler = 1.0      # entangler unitary time scaling
g = 0.58               # entangler strength (safe upper edge)
eta = 0.03             # enforcement unitary strength
gamma_rho = 1e-3       # optional rho feedback gain (set 0 to disable)
run_parameter_sweep = False   # set True to sweep g/eta combos
save_dir = "sdkp_optionA_out"
os.makedirs(save_dir, exist_ok=True)

# -----------------------------
# Canonical arrays (exact numeric definitions)
# -----------------------------
# Canonical C (12x12) - provided as your authoritative compressed-basis matrix
C = np.array([
[ 0.289,  0.249,  0.189,  0.161,  0.118,  0.099,  0.072,  0.054,  0.038,  0.026,  0.010,  0.005],
[-0.251,  0.310,  0.211,  0.087,  0.044,  0.051,  0.039,  0.025,  0.022,  0.008,  0.004,  0.002],
[ 0.203, -0.188,  0.388,  0.098,  0.076,  0.063,  0.039,  0.028,  0.017,  0.009,  0.006,  0.002],
[-0.179, -0.099,  0.120,  0.442,  0.083,  0.065,  0.055,  0.042,  0.029,  0.011,  0.005,  0.003],
[ 0.155, -0.080, -0.062,  0.091,  0.488,  0.076,  0.058,  0.041,  0.025,  0.010,  0.004,  0.002],
[-0.119,  0.060,  0.048, -0.050,  0.098,  0.515,  0.067,  0.050,  0.032,  0.015,  0.006,  0.003],
[ 0.093, -0.055, -0.039,  0.030, -0.028,  0.094,  0.551,  0.066,  0.041,  0.023,  0.009,  0.005],
[-0.065,  0.042,  0.031, -0.027,  0.020, -0.022,  0.084,  0.582,  0.057,  0.030,  0.011,  0.005],
[ 0.044, -0.031, -0.029,  0.021, -0.018,  0.011, -0.014,  0.078,  0.610,  0.044,  0.014,  0.006],
[-0.027,  0.019,  0.022, -0.017,  0.014, -0.012,  0.011, -0.011,  0.078,  0.638,  0.020,  0.009],
[ 0.013, -0.009, -0.010,  0.009, -0.010,  0.009, -0.009,  0.010, -0.011,  0.080,  0.663,  0.012],
[-0.006,  0.004,  0.005, -0.004,  0.005, -0.004,  0.004, -0.004,  0.006, -0.010,  0.085,  0.690]
], dtype=float)

# W6 weights (T6 kernel)
W6 = np.array([0.34, 0.21, 0.15, 0.11, 0.08, 0.05, 0.03, 0.016, 0.010, 0.006, 0.003, 0.0015], dtype=float)

# Full Phi array (50 terms canonical)
Phi50 = np.array([
  0.6681411762529909,  0.03838465107053409, -0.05116966382748937,
 -0.017791400153276843,  0.016402873765764996,  0.03393182320126196,
 -0.005361778601149078, -0.028852902034969418, -0.020120155842723385,
  0.018763089271374135,  0.03165384351785479,  -0.00018031135021215097,
 -0.03009099268471221,  -0.02180467236091864,   0.01740691410409184,
  0.02929237831874464,   0.0028126102435882324, -0.02924910579312145,
 -0.02283099418634786,   0.01579223691755422,   0.02706417335290566,
  0.00489138138439134,  -0.02777674412844696,  -0.02342306729995469,
  0.014233988553280227,  0.024892611832416968,  0.006275072223808997,
 -0.02616030772121256,  -0.02378144791718952,  0.01266520841239363,
  0.02278348191915703,   0.00719317677148556,  -0.02448975259666412,
 -0.0239980272573997,   0.011357176733440364,  0.020865421956947717,
  0.007855820631764447,  -0.02227204982650403,  -0.02408374645397422,
  0.01033024302741604,   0.01912038761992058,   0.00832485490717117,
 -0.020084745629517487, -0.02404478245364776,   0.009561447498529544,
  0.01752526382981179,   0.008642328883463815,  -0.018551236419982216,
 -0.02388976094701372,   0.008997053010421754
], dtype=float)

# -----------------------------
# Utility builders
# -----------------------------
def build_annihilation_ops(k, levels):
    a = qt.destroy(levels)
    a_ops = []
    for j in range(k):
        ops = [qt.qeye(levels) for _ in range(k)]
        ops[j] = a
        a_ops.append(qt.tensor(ops))
    return a_ops

def build_number_ops(k, levels):
    a = qt.destroy(levels)
    n_single = a.dag() * a
    n_ops = []
    for j in range(k):
        ops = [qt.qeye(levels) for _ in range(k)]
        ops[j] = n_single
        n_ops.append(qt.tensor(ops))
    return n_ops

def build_G_nn(a_ops, Phi_local, g_scalar):
    G_q = 0 * a_ops[0]
    for j in range(min(len(Phi_local), len(a_ops)-1)):
        G_q += g_scalar * Phi_local[j] * (a_ops[j].dag() * a_ops[j+1] + a_ops[j+1].dag() * a_ops[j])
    # small diagonal ramp for stability (keeps behavior consistent with earlier runs)
    for j in range(len(a_ops)):
        G_q += g_scalar * 0.02 * (j+1) * (a_ops[j].dag() * a_ops[j])
    return G_q

# -----------------------------
# Build T6 operator in compressed k-mode Fock space using W6
# -----------------------------
n_ops = build_number_ops(k, levels)
T6_comp = sum(W6[j] * n_ops[j] for j in range(k))

# -----------------------------
# Build a standard set of 21 Hermitian T_i operators
# (patterned, deterministic — mirrors earlier driver)
# -----------------------------
def build_T_ops_list(k, n_ops, G_q, Theta_diag_weights=None):
    T_ops = []
    if Theta_diag_weights is None:
        Theta_diag_weights = np.linspace(1.0, 0.2, k)
    # 1-7: shifted diagonal windows
    for shift in range(7):
        weights = np.roll(Theta_diag_weights, shift)[:k]
        T_ops.append(sum(weights[j] * n_ops[j] for j in range(k)))
    # 8: entangler (G)
    T_ops.append(G_q)
    # 9-14: small mode-group projectors
    for center in [0,2,4,6,8,10]:
        inds = list(range(center, min(center+3, k)))
        proj = sum(n_ops[ii] for ii in inds)
        T_ops.append(proj)
    # 15-21: cross-coupling combinations
    for j in range(k-1):
        T_ops.append((n_ops[j] + n_ops[j+1]) * 0.1 + 0.05 * (n_ops[j] * n_ops[j+1]))
        if len(T_ops) >= 21:
            break
    while len(T_ops) < 21:
        T_ops.append(n_ops[0] * 0.01)
    return T_ops[:21]

# -----------------------------
# Enforcement logic (single pass)
# -----------------------------
def enforcement_pass(psi, T_ops, eta_local):
    psi_now = psi
    acted = [False] * len(T_ops)
    dim_eff = psi.dims[0][0]
    taus = []
    for T in T_ops:
        try:
            tr = float(T.tr().real)
        except Exception:
            tr = 0.0
        taus.append(0.5 * (tr / max(1.0, dim_eff)))
    for i, T in enumerate(T_ops):
        val = np.real(qt.expect(T, psi_now))
        if val > taus[i]:
            U = (-1j * eta_local * T).expm()
            psi_now = (U * psi_now).unit()
            acted[i] = True
    return psi_now, acted

# -----------------------------
# Optional rho-feedback update (if you have rho, K arrays)
# -----------------------------
def rho_feedback_update(rho_vec, K_vec, C_mat, gamma=1e-3, rho_max=None, renormalize=True):
    eps = 1e-12
    Theta = rho_vec * K_vec
    Theta_mat = np.diag(Theta)
    P = C_mat @ C_mat.T
    Theta_comp = P @ Theta_mat @ P
    s = np.real(np.diag(Theta_comp)) - np.real(np.diag(Theta_mat))
    delta_rho = gamma * (s / (K_vec + eps))
    rho_new = rho_vec + delta_rho
    rho_new = np.clip(rho_new, 0.0, rho_max if rho_max is not None else np.max(rho_new)*10.0)
    if renormalize:
        baseline = np.sum(rho_vec)
        if np.sum(rho_new) > 0:
            rho_new = rho_new * (baseline / (np.sum(rho_new) + eps))
    return rho_new

# -----------------------------
# Initial state: coherent anchor (mode 0) + vacuum others
# -----------------------------
def build_initial_coherent_anchor(k, levels, alpha_amp):
    states = [qt.coherent(levels, alpha_amp) if j==0 else qt.basis(levels, 0) for j in range(k)]
    psi0 = qt.tensor(states)
    return psi0

# -----------------------------
# Main single-run routine
# -----------------------------
def single_run(g_scalar, eta_scalar, alpha_amp, do_rho_feedback=False):
    # Build operators
    a_ops = build_annihilation_ops(k, levels)
    n_ops_local = build_number_ops(k, levels)
    Phi_local = Phi50[:k-1]
    G_q = build_G_nn(a_ops, Phi_local, g_scalar)
    T_ops = build_T_ops_list(k, n_ops_local, G_q)
    # initial state
    psi0 = build_initial_coherent_anchor(k, levels, alpha_amp)
    e_before = float(qt.expect(T6_comp, psi0))
    purity_before = float((psi0.proj() * psi0.proj()).tr())
    # entangler
    U_ent = (-1j * t_entangler * G_q).expm()
    psi_ent = (U_ent * psi0).unit()
    # enforcement pass
    psi_after, acted = enforcement_pass(psi_ent, T_ops, eta_scalar)
    e_after = float(qt.expect(T6_comp, psi_after))
    purity_after = float((psi_after.proj() * psi_after.proj()).tr())
    result = {
        "g": g_scalar, "eta": eta_scalar, "alpha": alpha_amp,
        "T6_before": e_before, "T6_after": e_after, "delta": e_after - e_before,
        "purity_before": purity_before, "purity_after": purity_after, "acted_any": any(acted)
    }
    return result

# -----------------------------
# Run (single or sweep)
# -----------------------------
if run_parameter_sweep:
    g_list = [0.52, 0.58, 0.62]
    eta_list = [0.025, 0.03, 0.035]
    rows = []
    for gg in g_list:
        for ee in eta_list:
            r = single_run(gg, ee, alpha, do_rho_feedback=False)
            rows.append(r)
            print(r)
else:
    rows = [ single_run(g, eta, alpha, do_rho_feedback=False) ]
    print("Single run result:", rows[0])

# -----------------------------
# Save CSV and plot simple diagnostics
# -----------------------------
csvfile = os.path.join(save_dir, "sdkp_optionA_results.csv")
with open(csvfile, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    for r in rows:
        writer.writerow(r)
print("Saved CSV:", csvfile)

# bar plot of Δ
deltas = [r["delta"] for r in rows]
labels = [f"g{r['g']}_e{r['eta']}" for r in rows]
plt.figure(figsize=(6,3))
plt.bar(range(len(deltas)), deltas)
plt.xticks(range(len(deltas)), labels, rotation=45)
plt.ylabel("Δ ⟨T6⟩")
plt.title("Δ ⟨T6⟩ (Option A run)")
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "delta_T6.png"))
plt.show()

# purity plot
pur_after = [r["purity_after"] for r in rows]
plt.figure(figsize=(6,3))
plt.plot(labels, pur_after, 'o-')
plt.ylim(0.9,1.01)
plt.ylabel("Purity after")
plt.title("Purity after enforcement")
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "purity_after.png"))
plt.show()

print("Done. Output saved in:", save_dir)
