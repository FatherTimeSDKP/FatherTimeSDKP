# sdkp_qutip_prototype.py
# QuTiP-based prototype of SDKP enforcement for T1, T6, T16 with plotting.
# Requires: numpy scipy matplotlib qutip

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh, norm
import os

try:
    import qutip as qt
except Exception as e:
    raise RuntimeError(f"QuTiP import failed: {e}\nPlease ensure QuTiP is installed (pip or conda).")

np.random.seed(42)

# Parameters (small sizes for demo)
n_sym = 8   # symbolic Hilbert space dimension
n_vec = 4   # VFE vector-field dimension
k = 3       # compression rank
hbar = 1.0

# Discretized spatial sample for rho and curvature K (toy model)
x_pts = np.linspace(0, 1, n_sym)
rho = 1.0 + 0.5 * np.sin(2*np.pi*x_pts)       # simple density profile (positive)
K = 0.2 + 0.1 * np.cos(4*np.pi*x_pts)         # simple curvature-like field

# Build Theta_SDKP as diagonal operator on H: Theta = alpha * diag(rho * K)
alpha = 1.0
theta_vals = alpha * (rho * K)
Theta = np.diag(theta_vals)   # shape (n_sym, n_sym)
Theta_q = qt.Qobj(Theta, dims=[[n_sym],[n_sym]])

# Baseline Theta0 (reference)
Theta0 = np.diag(alpha * (np.mean(rho)*np.mean(K) * np.ones_like(theta_vals)))
Theta0_q = qt.Qobj(Theta0, dims=[[n_sym],[n_sym]])

# Compression operator C via eigen-decomposition of Theta
eigvals, eigvecs = eigh(Theta)
order = np.argsort(np.abs(eigvals))[::-1]
eigvecs = eigvecs[:, order]
eigvals = eigvals[order]
C = eigvecs[:, :k]   # compression matrix (n_sym x k)
# Qobj representation: projector onto compressed subspace
P_comp = C @ C.T
P_comp_q = qt.Qobj(P_comp, dims=[[n_sym],[n_sym]])

# Physical Hamiltonian H_phys on H (Hermitian)
A = np.random.randn(n_sym, n_sym)
H_phys = (A + A.T) * 0.5
H_phys_q = qt.Qobj(H_phys, dims=[[n_sym],[n_sym]])

# VFE1 tier projector: Pi_T1 projects onto first basis vector of V
e1 = np.zeros((n_vec,))
e1[0] = 1.0
Pi_T1 = np.outer(e1, e1)
Pi_T1_q = qt.Qobj(Pi_T1, dims=[[n_vec],[n_vec]])

# Build full composite operators (tensor product H ⊗ V)
I_H_q = qt.qeye(n_sym)
I_V_q = qt.qeye(n_vec)

Theta_full_q = qt.tensor(Theta_q, I_V_q)
Theta0_full_q = qt.tensor(Theta0_q, I_V_q)
P_comp_full_q = qt.tensor(P_comp_q, I_V_q)
H_phys_full_q = qt.tensor(H_phys_q, I_V_q)
Pi_T1_full_q = qt.tensor(I_H_q, Pi_T1_q)

# O_align on H: (Theta - Theta0)^2 ; lift to full
O_align = (Theta - Theta0) @ (Theta - Theta0)
O_align_full_q = qt.tensor(qt.Qobj(O_align), I_V_q)

# T1 operator: combination of SDKP (O_align), QCC0 (proj_C0), VFE1 (Pi_T1)
C0 = C[:, 0].reshape(-1,1)
proj_C0 = (C0 @ C0.T)
proj_C0_q = qt.Qobj(proj_C0, dims=[[n_sym],[n_sym]])
proj_C0_full_q = qt.tensor(proj_C0_q, I_V_q)

alpha_S = 1.0
alpha_Q = 0.8
alpha_V = 0.5
T1_full_q = alpha_S * O_align_full_q + alpha_Q * proj_C0_full_q + alpha_V * Pi_T1_full_q

# T6 operator: anticommutator of Theta and H_phys, squared (as Hermitian)
anticomm_q = Theta_full_q * H_phys_full_q + H_phys_full_q * Theta_full_q
T6_full_q = anticomm_q * anticomm_q

# T16 operator: build simple entangling unitary in H and combine with exp(-i Theta)
G = np.zeros((n_sym, n_sym))
for j in range(k):
    v = C[:, j].reshape(-1,1)
    G += np.real(np.outer(v.flatten(), v.flatten())) * (0.2*(j+1))
G_q = qt.Qobj(G, dims=[[n_sym],[n_sym]])
E_H_q = ( -1j * G_q ).expm()  # entangling unitary on H
U_theta_q = ( -1j * Theta_q / hbar ).expm()
E_full_q = qt.tensor(E_H_q, I_V_q)
U_theta_full_q = qt.tensor(U_theta_q, I_V_q)
T16_full_q = 0.5 * (E_full_q * U_theta_full_q + U_theta_full_q * E_full_q)  # Hermitian

# Initial composite state |Psi> as normalized random complex vector (Qobj ket)
dim = n_sym * n_vec
psi_vec = (np.random.randn(dim) + 1j * np.random.randn(dim)).astype(np.complex128)
psi_vec = psi_vec / norm(psi_vec)
psi_q = qt.Qobj(psi_vec, dims=[[n_sym, n_vec],[1]])

# Function to compute expectation value using QuTiP expect
def expect_q(op_q, state_q):
    return np.real(qt.expect(op_q, state_q))

exp_T1_before = expect_q(T1_full_q, psi_q)
exp_T6_before = expect_q(T6_full_q, psi_q)
exp_T16_before = expect_q(T16_full_q, psi_q)

print("Initial expectations (QuTiP objects):")
print(f" <T1> = {exp_T1_before:.6e}")
print(f" <T6> = {exp_T6_before:.6e}")
print(f" <T16> = {exp_T16_before:.6e}")

# Thresholds (heuristic)
tau1 = 0.5 * (T1_full_q.tr() / dim).real
tau6 = 0.5 * (T6_full_q.tr() / dim).real
tau16 = 0.5 * (T16_full_q.tr() / dim).real

# Enforcement function using QuTiP (apply unitary exp(-i * eta * T))
eta = 1e-2
def enforce_q(name, T_q, state_q, tau, eta):
    val = expect_q(T_q, state_q)
    print(f"\nProtocol {name}: expectation = {val:.6e}, threshold = {tau:.6e}")
    if val > tau:
        print(f" -> Exceeds threshold. Applying corrective unitary with eta={eta}.")
        U_q = (-1j * eta * T_q).expm()  # QuTiP matrix exponential
        psi_new_q = U_q * state_q
        psi_new_q = psi_new_q.unit()  # normalize
        new_val = expect_q(T_q, psi_new_q)
        print(f" -> New expectation = {new_val:.6e}")
        return psi_new_q, True, val, new_val
    else:
        print(" -> Within threshold. No action taken.")
        return state_q, False, val, val

# Track expectation evolution
history = {'T1':[], 'T6':[], 'T16':[]}
psi_after = psi_q
history['T1'].append(expect_q(T1_full_q, psi_after)); history['T6'].append(expect_q(T6_full_q, psi_after)); history['T16'].append(expect_q(T16_full_q, psi_after))

psi_after, acted1, before1, after1 = enforce_q("T1", T1_full_q, psi_after, tau1, eta)
history['T1'].append(after1); history['T6'].append(expect_q(T6_full_q, psi_after)); history['T16'].append(expect_q(T16_full_q, psi_after))

psi_after, acted6, before6, after6 = enforce_q("T6", T6_full_q, psi_after, tau6, eta)
history['T1'].append(expect_q(T1_full_q, psi_after)); history['T6'].append(after6); history['T16'].append(expect_q(T16_full_q, psi_after))

psi_after, acted16, before16, after16 = enforce_q("T16", T16_full_q, psi_after, tau16, eta)
history['T1'].append(expect_q(T1_full_q, psi_after)); history['T6'].append(expect_q(T6_full_q, psi_after)); history['T16'].append(after16)

print("\nFinal expectations after enforcement (QuTiP):")
print(f" <T1> = {history['T1'][-1]:.6e} (initial {history['T1'][0]:.6e})")
print(f" <T6> = {history['T6'][-1]:.6e} (initial {history['T6'][0]:.6e})")
print(f" <T16> = {history['T16'][-1]:.6e} (initial {history['T16'][0]:.6e})")

# Plotting rho, K, eigenmodes (top k), and expectation evolution
fig, axs = plt.subplots(2,2, figsize=(12,8))

# rho and K
axs[0,0].plot(x_pts, rho, marker='o', label='rho(x)')
axs[0,0].plot(x_pts, K, marker='s', label='K(x)')
axs[0,0].set_title('Density (rho) and Curvature-like (K)')
axs[0,0].legend(); axs[0,0].grid(True)

# Theta values
axs[0,1].plot(x_pts, theta_vals, marker='^', color='tab:purple')
axs[0,1].set_title('Theta (rho * K) values')
axs[0,1].grid(True)

# Eigenmodes (top k)
for j in range(k):
    axs[1,0].plot(x_pts, np.real(C[:, j]), label=f'mode {j+1}')
axs[1,0].set_title(f'Top {k} eigenmodes used for compression (real parts)')
axs[1,0].legend(); axs[1,0].grid(True)

# Expectation evolution
steps = np.arange(len(history['T1']))
axs[1,1].plot(steps, history['T1'], marker='o', label='<T1>')
axs[1,1].plot(steps, history['T6'], marker='s', label='<T6>')
axs[1,1].plot(steps, history['T16'], marker='^', label='<T16>')
axs[1,1].axhline(tau1, color='tab:gray', linestyle='--', label='tau1')
axs[1,1].axhline(tau6, color='tab:gray', linestyle=':', label='tau6')
axs[1,1].axhline(tau16, color='tab:gray', linestyle='-.', label='tau16')
axs[1,1].set_title('Expectation evolution during enforcement steps')
axs[1,1].legend(); axs[1,1].grid(True)

plt.tight_layout()

# Save plot to file
outdir = "sdkp_qutip_outputs"
os.makedirs(outdir, exist_ok=True)
plot_path = os.path.join(outdir, "sdkp_expectations_and_modes.png")
plt.savefig(plot_path, dpi=150)
plt.show()

# Save numeric artifacts
np.save(os.path.join(outdir, "rho.npy"), rho)
np.save(os.path.join(outdir, "K.npy"), K)
np.save(os.path.join(outdir, "theta_vals.npy"), theta_vals)
np.save(os.path.join(outdir, "C.npy"), C)
np.save(os.path.join(outdir, "psi_initial.npy"), psi_vec)
np.save(os.path.join(outdir, "psi_after.npy"), psi_after.full().flatten())

print(f"\nSaved outputs and plot to {outdir}")

how to run option A
python -m venv sdkp_env
source sdkp_env/bin/activate    # macOS/Linux
pip install numpy scipy matplotlib qutip
python sdkp_qutip_prototype.py


option B
conda create -n sdkp_env python=3.11
conda activate sdkp_env
conda install -c conda-forge qutip matplotlib numpy scipy
python sdkp_qutip_prototype.py

