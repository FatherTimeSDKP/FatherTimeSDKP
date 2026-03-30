import numpy as np
import qutip as qt
from scipy.linalg import eigh
import csv, os

# ---------------- USER SETTINGS ----------------
N_symbolic = 12        # we model compressed-space only (12 modes); scale to full N if you need
k_vals = [12]          # mode counts to test (you can add 8,10,12)
g_vals = [0.25, 0.4, 0.5]   # entangler scalars to sweep
eta_vals = [1e-3, 1e-2, 2.5e-2]  # enforcement strengths
t_evolve = 10.0
levels = 3             # Fock truncation per mode (2=vacuum+1, 3=allow 2 excitations)
save_csv = True
outcsv = "12mode_sweep_results.csv"
os.makedirs("out", exist_ok=True)

# ---------------- canonical C (12x12) and W6 from earlier messages ----------------
C = np.array([
[ 0.28892,  0.57211,  0.54709,  0.37059,  0.13878, -0.13878, -0.37059, -0.54709, -0.57211, -0.28892,  0.09468,  0.28892],
[ 0.57211,  0.28892, -0.13878, -0.54709, -0.57211, -0.28892,  0.13878,  0.54709,  0.57211,  0.28892, -0.09468, -0.28892],
[ 0.54709, -0.13878, -0.37059, -0.57211, -0.28892,  0.28892,  0.57211,  0.37059, -0.13878, -0.54709, -0.09468,  0.28892],
[ 0.37059, -0.54709, -0.57211, -0.13878,  0.28892,  0.57211,  0.28892, -0.13878, -0.57211, -0.54709, -0.09468,  0.28892],
[ 0.13878, -0.57211, -0.28892,  0.28892,  0.57211,  0.13878, -0.37059, -0.54709, -0.09468,  0.28892,  0.54709,  0.37059],
[-0.13878, -0.28892,  0.28892,  0.57211,  0.13878, -0.37059, -0.54709, -0.09468,  0.28892,  0.54709,  0.57211,  0.13878],
[-0.37059,  0.13878,  0.57211,  0.28892, -0.28892, -0.57211, -0.13878,  0.54709,  0.37059, -0.09468, -0.54709, -0.57211],
[-0.54709,  0.54709,  0.37059, -0.13878, -0.57211, -0.28892,  0.28892,  0.57211,  0.13878, -0.09468, -0.37059, -0.54709],
[-0.57211,  0.57211, -0.13878, -0.57211, -0.28892,  0.28892,  0.54709,  0.13878, -0.09468, -0.54709, -0.28892,  0.28892],
[-0.28892,  0.28892, -0.54709, -0.54709,  0.28892,  0.54709,  0.13878, -0.09468, -0.54709, -0.28892,  0.28892,  0.54709],
[ 0.09468, -0.09468, -0.09468, -0.09468,  0.54709,  0.57211,  0.54709,  0.37059, -0.09468, -0.28892, -0.54709, -0.57211],
[ 0.28892, -0.28892,  0.28892,  0.28892,  0.37059,  0.54709,  0.57211,  0.54709,  0.37059, -0.09468, -0.28892, -0.54709]
], dtype=float)

W6 = np.array([-0.05187, -0.10767, 0.01847, 0.00752, 0.11231, 0.02777, -0.02754,
               0.09310, -0.00170, -0.00083, 0.02045, 0.01377], dtype=float)

# ---------------- helper builders ----------------
def build_nn_G_from_C(C, Phi_local, g):
    N, k = C.shape
    G = np.zeros((N,N), dtype=complex)
    for j in range(min(len(Phi_local), k-1)):
        cj = C[:, j].reshape(N,1)
        cj1 = C[:, j+1].reshape(N,1)
        G += g * Phi_local[j] * (cj @ cj1.T + cj1 @ cj.T)
    # small diag ramp for stability
    for j in range(k):
        v = C[:, j].reshape(N,1)
        G += g * 0.02*(j+1) * (v @ v.T)
    return G

def build_T6_comp(k, levels, W6_arr):
    # build number ops on k-mode truncated Fock space
    a = qt.destroy(levels)
    n_single = a.dag() * a
    n_ops = []
    for j in range(k):
        ops = [qt.qeye(levels) for _ in range(k)]
        ops[j] = n_single
        n_ops.append(qt.tensor(ops))
    T6 = sum(W6_arr[j] * n_ops[j] for j in range(k))
    return T6, n_ops

# ---------------- initial states ----------------
def build_anchor_comp_state(k):
    v = np.zeros(k, dtype=complex)
    v[0] = 1.0
    return qt.Qobj(v, dims=[[k],[1]])

def build_coherent_comp(alpha, k, levels):
    # small coherent-like state approximated on truncated basis using displaced vacuum on each mode
    # here we create product coherent up to truncation by applying displacement on each mode
    states = [qt.coherent(levels, alpha) for _ in range(k)]
    return qt.tensor(states)

# ---------------- sweep driver ----------------
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
])

# limit Phi to first k-1 entries (NN)
def run_single_case(k, g, eta, alpha_coh=0.5):
    Phi_local = Phi50[:k-1]
    Gmat = build_nn_G_from_C(C[:, :k], Phi_local, g)
    # build G in compressed basis as QuTiP operator if needed:
    # but we will treat enforcement T_ops independently; T6 is the metric
    T6_comp, n_ops = build_T6_comp(k, levels, W6[:k])
    # initial state: coherent product approximation in compressed basis
    psi0 = build_coherent_comp(alpha_coh, k, levels)
    # expectation before
    e_before = float(qt.expect(T6_comp, psi0))
    # Create a simple enforcement loop: for demo, apply entangler unitary and a small T_op unitary
    G_q_k = qt.Qobj(Gmat, dims=[[k],[k]])
    U_ent = (-1j * (G_q_k)).expm()      # entangler (dimension mismatch: only if you embed operators into same Hilbert space)
    # For consistent dims, map Gmat to k-mode Fock space via single-mode mapping (approx): use diagonal projection onto first k basis states
    # Simplify: perform small unitary on the compressed-state vector via exponentiating a diagonally embedded version
    # Build a diagonal operator from Gmat's diag as qobj on product space:
    diag_vals = np.real(np.diag(Gmat))
    # Create product-space operator H_diag = sum_j diag_vals[j]*n_j
    H_diag = sum(diag_vals[j] * n_ops[j] for j in range(k))
    U_enf = (-1j * eta * H_diag).expm()
    psi_after = U_enf * psi0
    psi_after = psi_after.unit()
    e_after = float(qt.expect(T6_comp, psi_after))
    purity_before = float((psi0.proj() * psi0.proj()).tr())
    purity_after = float((psi_after.proj() * psi_after.proj()).tr())
    acted_any = True if abs(e_after - e_before) > 1e-12 else False
    return dict(k=k, g=g, eta=eta, e_before=e_before, e_after=e_after,
                delta=e_after - e_before, purity_before=purity_before, purity_after=purity_after,
                acted_any=acted_any)

# ---------------- perform sweep ----------------
rows = []
for k in k_vals:
    for g in g_vals:
        for eta in eta_vals:
            row = run_single_case(k, g, eta, alpha_coh=0.5)
            rows.append(row)
            print(f"k={row['k']}, g={row['g']}, eta={row['eta']}: <T6> {row['e_before']:.6f} -> {row['e_after']:.6f}, Δ={row['delta']:.6f}, purity_after={row['purity_after']:.6f}")

# ---------------- save csv ----------------
if save_csv:
    keys = list(rows[0].keys())
    with open(os.path.join("out", outcsv), "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print("Saved sweep CSV to out/", outcsv)

# End of cell
