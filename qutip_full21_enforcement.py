# quip_full21_enforcement.py
# Requires: numpy, qutip, matplotlib
import numpy as np
import qutip as qt
from scipy.linalg import eigh
import os

# --------- Load or build theta, rho, K ----------
# If you have arrays saved, load them; otherwise rebuild quickly:
# theta = np.load("sdkp_arrays/theta_100.npy")
# rho   = np.load("sdkp_arrays/rho_100.npy")
# K     = np.load("sdkp_arrays/K_100.npy")

# Quick reconstruct if needed:
def make_arrays(N=100):
    G = 6.67430e-11; M = 5.97219e24; R = 6_371_000.0
    h = np.linspace(0, 100e3, N)
    rho0 = 1.225; H_scale = 8500.0
    rho = rho0 * np.exp(-h / H_scale)
    rho = np.clip(rho, 0.0, None)  # ensure non-negative
    r = R + h
    K_raw = (G * M) / (r**3)
    K = K_raw / np.max(K_raw)
    theta_raw = rho * K
    theta = theta_raw / np.max(theta_raw)
    return h, rho, K, theta

N = 100
h, rho, K, theta = make_arrays(N=N)

# --------- Normalize / sanitize ----------
rho = np.clip(rho, 0.0, None)
rho = rho / np.max(rho)
K  = K  / np.max(K)
theta = theta / np.max(theta)

# --------- Hilbert sizes ----------
M = 4   # number of VFE tiers (tuneable)
dim = N * M

# --------- SDKP operators on H_S ----------
Theta_mat = np.diag(theta)                # (N,N)
Theta_q = qt.Qobj(Theta_mat, dims=[[N],[N]])
mean_theta = np.mean(theta)
O_align_mat = (Theta_mat - mean_theta*np.eye(N)) @ (Theta_mat - mean_theta*np.eye(N))
O_align_q = qt.Qobj(O_align_mat, dims=[[N],[N]])
O_density_q = qt.Qobj(np.diag(rho), dims=[[N],[N]])
O_curv_q = qt.Qobj(np.diag(K), dims=[[N],[N]])

# --------- QCC0: compression (top-k eigenmodes) ----------
eigvals, eigvecs = eigh(Theta_mat)
order = np.argsort(np.abs(eigvals))[::-1]
k = min(6, N//10)   # choose k (e.g., 5-6)
C = eigvecs[:, order[:k]]   # (N,k)
# build compression projector (Qobj)
P_comp_q = qt.Qobj(np.real(C @ C.T), dims=[[N],[N]])
proj_C0_q = qt.Qobj(np.real(np.outer(C[:,0], C[:,0])), dims=[[N],[N]])

# entangler generator G (Hermitian) on H_S
Gmat = np.zeros((N,N))
for j in range(k):
    v = C[:, j].reshape(-1,1)
    Gmat += (v @ v.T) * (0.1*(j+1))   # tunable coeffs
G_q = qt.Qobj(Gmat, dims=[[N],[N]])
E_H_q = (-1j * G_q).expm()   # unitary entangler on H_S

# --------- VFE1 operators on H_V ----------
I_S = qt.qeye(N)
I_V = qt.qeye(M)
Pi_tiers = [qt.ket2dm(qt.basis(M,i)) for i in range(M)]
Phi_mat = np.random.randn(M,M)
Phi_mat = 0.5*(Phi_mat + Phi_mat.T)
Phi_q = qt.Qobj(Phi_mat, dims=[[M],[M]])

# lift to full Hilbert space
Theta_full = qt.tensor(Theta_q, I_V)
O_align_full = qt.tensor(O_align_q, I_V)
O_density_full = qt.tensor(O_density_q, I_V)
O_curv_full = qt.tensor(O_curv_q, I_V)
P_comp_full = qt.tensor(P_comp_q, I_V)
proj_C0_full = qt.tensor(proj_C0_q, I_V)
E_full = qt.tensor(E_H_q, I_V)
Phi_full = qt.tensor(qt.qeye(N), Phi_q)
Pi_tier_full = [qt.tensor(qt.qeye(N), Pi) for Pi in Pi_tiers]

# --------- Canonical seed mapping for T1..T21 ----------
# Choose SDKP, QCC0, VFE1 seeds per TTP index (example, tunable)
sdkp_seeds = [
    O_align_full, O_density_full, O_drift_full if 'O_drift_full' in globals() else O_align_full,
    O_align_full, O_drift_full if 'O_drift_full' in globals() else O_align_full,
    Theta_full, O_curv_full, O_drift_full if 'O_drift_full' in globals() else O_align_full,
    Theta_full, O_align_full, (Theta_full*qt.tensor(qt.Qobj(np.eye(N)), qt.qeye(M)))  # placeholder for anticomm_sq
] 
# We'll actually use a safe systematic generator below instead of listing by hand.

# --------- Build T_ops systematically (preferred)
T_ops = []
alpha_defaults = {'S':1.0, 'Q':0.7, 'V':0.4}
for i in range(1,22):   # 1..21
    # pick SDKP op
    if i in (1,4,10,12,17,19):
        O_S = O_align_full
    elif i in (2,13):
        O_S = O_density_full
    elif i in (6,9,15,16,21):
        O_S = Theta_full
    elif i in (5,8,14):
        O_S = O_curv_full
    elif i==11:
        anticomm = (Theta_full * qt.tensor(qt.Qobj(H_q if 'H_q' in globals() else np.eye(N)), I_V) 
                    + qt.tensor(qt.Qobj(H_q if 'H_q' in globals() else np.eye(N)), I_V) * Theta_full)
        O_S = anticomm * anticomm if isinstance(anticomm, qt.Qobj) else Theta_full
    else:
        O_S = O_align_full
    # pick QCC0 op
    if i in (18,17):
        O_Q = P_comp_full
    else:
        O_Q = proj_C0_full
    # pick VFE op
    if i <= 4:
        O_V = Pi_tier_full[0]
    elif i <= 8:
        O_V = Pi_tier_full[1]
    elif i <= 14:
        O_V = Pi_tier_full[2]
    else:
        O_V = Pi_tier_full[3] if M>3 else Pi_tier_full[-1]
    # weights
    aS = alpha_defaults['S']
    aQ = alpha_defaults['Q']
    aV = alpha_defaults['V']
    T_i = aS * O_S + aQ * O_Q + aV * O_V
    T_ops.append(T_i)

# --------- If H_phys needed for anticomm, build one (toy)
A = np.random.randn(N,N)
H_phys_mat = 0.5*(A + A.T)
H_phys_q = qt.Qobj(H_phys_mat, dims=[[N],[N]])
H_phys_full = qt.tensor(H_phys_q, I_V)

# Replace any placeholder anticomm entries with actual anticomm_sq
anticomm = Theta_full * H_phys_full + H_phys_full * Theta_full
anticomm_sq = anticomm * anticomm
# put anticomm_sq into T11 (index 10)
T_ops[10] = anticomm_sq

# --------- Prepare initial state ----------
psi_vec = (np.random.randn(N*M) + 1j*np.random.randn(N*M)).astype(complex)
psi = qt.Qobj(psi_vec).unit()

# --------- Expectation before enforcement ----------
exps_before = [np.real(qt.expect(T_ops[i], psi)) for i in range(21)]

# --------- Enforcement loop ----------
eta = 1e-2
taus = [0.5 * (T_ops[i].tr().real / (N*M)) for i in range(21)]
history = [exps_before.copy()]
psi_now = psi
acted = [False]*21

for i in range(21):
    val = np.real(qt.expect(T_ops[i], psi_now))
    if val > taus[i]:
        U = (-1j * eta * T_ops[i]).expm()
        psi_now = (U * psi_now).unit()
        acted[i] = True
    history.append([np.real(qt.expect(T_ops[j], psi_now)) for j in range(21)])

# --------- Results ----------
exps_after = history[-1]
print("Initial <T6>:", exps_before[5])
print("Final   <T6>:", exps_after[5])
print("Delta   <T6>:", exps_after[5] - exps_before[5])
print("Any acted?:", any(acted))

# Save (np.save) or plot as needed
outdir = "sdkp_qutip_full21"
os.makedirs(outdir, exist_ok=True)
np.save(os.path.join(outdir, "exps_before.npy"), np.array(exps_before))
np.save(os.path.join(outdir, "exps_after.npy"), np.array(exps_after))
np.save(os.path.join(outdir, "acted_flags.npy"), np.array(acted))
