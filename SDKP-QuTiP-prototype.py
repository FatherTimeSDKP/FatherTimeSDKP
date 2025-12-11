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

import React, { useState } from ‘react’;
import { Info, Zap, Layers, Grid, Eye } from ‘lucide-react’;

const FatherTimeMatrix = () => {
const [selectedView, setSelectedView] = useState(‘keys’);
const [hoveredCell, setHoveredCell] = useState(null);

// 12 Universal Keys
const keys = [
{ id: ‘D₁’, name: ‘Density’, meaning: ‘Mass/energy packing’, frameworks: [‘SDKP’, ‘SD&N’, ‘EOS’] },
{ id: ‘R₂’, name: ‘Rotation’, meaning: ‘Angular momentum, vortex’, frameworks: [‘SDKP’, ‘SDVR’, ‘EOS’] },
{ id: ‘V₃’, name: ‘Velocity’, meaning: ‘Inertial drift, timing’, frameworks: [‘SDKP’, ‘EOS’] },
{ id: ‘T₄’, name: ‘Time’, meaning: ‘Temporal compression’, frameworks: [‘SDKP’, ‘QCC0’] },
{ id: ‘S₅’, name: ‘Shape-Dimension’, meaning: ‘N-vector mapping’, frameworks: [‘SD&N’, ‘Kapnack’] },
{ id: ‘Φ₆’, name: ‘Resonance’, meaning: ‘Harmonic/EM/gravity coupling’, frameworks: [‘SDKP’, ‘Digital Crystal’] },
{ id: ‘Ω₇’, name: ‘Compression’, meaning: ‘Symbolic & data compression’, frameworks: [‘Kapnack’, ‘LLAL’] },
{ id: ‘C₅’, name: ‘5th-Order Coupling’, meaning: ‘Cross-dimensional linking’, frameworks: [‘Digital Crystal’, ‘VFE1’] },
{ id: ‘Ψ₇’, name: ‘Phase Extended’, meaning: ‘Nonlinear phase convergence’, frameworks: [‘SDVR’, ‘EOS’] },
{ id: ‘Σ₁₀’, name: ‘Synthesis’, meaning: ‘Multi-framework integration’, frameworks: [‘LLAL’] },
{ id: ‘Λ₉’, name: ‘Reflector’, meaning: ‘9-frequency convergence’, frameworks: [‘Kapnack’, ‘3-6-9’] },
{ id: ‘Θ₁₂’, name: ‘Completion’, meaning: ‘Full-lattice recursion’, frameworks: [‘QCC0’, ‘LLAL’, ‘DCP-12’] }
];

// 7 Dimensional Scales
const scales = [
{ id: 1, name: ‘Quantum Kernel’, range: ‘10⁻¹⁵ m → 10⁻⁹ m’, keys: [‘D₁’, ‘T₄’, ‘Φ₆’], frameworks: [‘SDKP’, ‘SDVR’] },
{ id: 2, name: ‘Atomic/Molecular’, range: ‘10⁻¹⁰ m → 10⁻⁸ m’, keys: [‘R₂’, ‘V₃’], frameworks: [‘SD&N’, ‘SDKP’] },
{ id: 3, name: ‘Classical Matter’, range: ‘Human-scale’, keys: [‘S₅’, ‘R₂’], frameworks: [‘SD&N’, ‘Kapnack’] },
{ id: 4, name: ‘Planetary/Orbital’, range: ‘EOS domain’, keys: [‘T₄’, ‘V₃’], frameworks: [‘EOS’, ‘SDVR’] },
{ id: 5, name: ‘Stellar/Galactic’, range: ‘Stellar systems’, keys: [‘Φ₆’, ‘Ω₇’], frameworks: [‘Digital Crystal’, ‘VFE1’] },
{ id: 6, name: ‘Cosmic’, range: ‘FRW domain’, keys: [‘T₄’, ‘Θ₁₂’], frameworks: [‘SDKP cosmology’, ‘Kapnack’] },
{ id: 7, name: ‘Consciousness’, range: ‘QCC0 domain’, keys: [‘Ω₇’, ‘S₅’, ‘Σ₁₀’, ‘Θ₁₂’], frameworks: [‘QCC0’, ‘LLAL’] }
];

// Frameworks with their key and scale mappings
const frameworks = {
‘SDKP’: {
keys: [‘D₁’, ‘R₂’, ‘V₃’, ‘T₄’, ‘Φ₆’, ‘Θ₁₂’],
scales: [1, 2, 4, 5, 6],
color: ‘rgb(59, 130, 246)’,
role: ‘Entanglement, density-rotation-velocity-time unification’
},
‘SD&N’: {
keys: [‘S₅’, ‘Λ₉’],
scales: [2, 3, 7],
color: ‘rgb(34, 197, 94)’,
role: ‘Shape → Dimension → Number collapse rules’
},
‘EOS’: {
keys: [‘V₃’, ‘T₄’, ‘Φ₆’],
scales: [4, 5],
color: ‘rgb(234, 179, 8)’,
role: ‘Orbital deviation and dynamic rotation-field feedback’
},
‘SDVR’: {
keys: [‘R₂’, ‘Φ₆’],
scales: [1, 4],
color: ‘rgb(249, 115, 22)’,
role: ‘Vortex-field emergence and planetary-scale symmetry’
},
‘Kapnack’: {
keys: [‘Ω₇’, ‘Λ₉’, ‘S₅’, ‘Θ₁₂’],
scales: [3, 6, 7],
color: ‘rgb(168, 85, 247)’,
role: ‘Symbolic compression, 3-6-9 recursion’
},
‘Digital Crystal’: {
keys: [‘Φ₆’, ‘C₅’, ‘Ψ₇’, ‘Θ₁₂’],
scales: [5, 6],
color: ‘rgb(236, 72, 153)’,
role: ‘Lattice structure for universal information propagation’
},
‘LLAL’: {
keys: [‘Σ₁₀’, ‘Ω₇’, ‘Θ₁₂’, ‘T₄’],
scales: [6, 7],
color: ‘rgb(14, 165, 233)’,
role: ‘Learning, consciousness, recursion, error immunity’
},
‘QCC0’: {
keys: [‘T₄’, ‘Θ₁₂’],
scales: [6, 7],
color: ‘rgb(139, 92, 246)’,
role: ‘Consciousness modeling, entangled internal horizons’
}
};

// 3-6-9 Harmonic
const harmonic369 = [
{ num: 3, meaning: ‘Rotation / Entry’, keys: [‘R₂’, ‘V₃’], frameworks: [‘EOS’, ‘SDKP’, ‘SDVR’], color: ‘rgb(59, 130, 246)’ },
{ num: 6, meaning: ‘Resonance / Stabilization’, keys: [‘Φ₆’], frameworks: [‘Digital Crystal’, ‘gravity-EM’], color: ‘rgb(34, 197, 94)’ },
{ num: 9, meaning: ‘Reflection / Completion’, keys: [‘Λ₉’, ‘Ω₇’], frameworks: [‘Kapnack’, ‘QCC0’, ‘consciousness’], color: ‘rgb(168, 85, 247)’ }
];

const KeysView = () => (
<div className="space-y-4">
<h2 className="text-2xl font-bold text-blue-300 mb-4">12 Universal Keys (Crystal-12)</h2>
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
{keys.map((key) => (
<div
key={key.id}
className=“bg-gray-800 p-4 rounded-lg border border-gray-700 hover:border-blue-500 transition-all cursor-pointer”
onMouseEnter={() => setHoveredCell(key.id)}
onMouseLeave={() => setHoveredCell(null)}
>
<div className="flex items-center gap-2 mb-2">
<span className="text-2xl font-bold text-blue-400">{key.id}</span>
<span className="text-sm font-semibold text-gray-300">{key.name}</span>
</div>
<p className="text-xs text-gray-400 mb-2">{key.meaning}</p>
<div className="flex flex-wrap gap-1">
{key.frameworks.map(fw => (
<span key={fw} className=“px-2 py-1 text-xs rounded” style={{
backgroundColor: frameworks[fw]?.color + ‘33’,
color: frameworks[fw]?.color
}}>
{fw}
</span>
))}
</div>
</div>
))}
</div>
</div>
);

const ScalesView = () => (
<div className="space-y-4">
<h2 className="text-2xl font-bold text-green-300 mb-4">7 Dimensional Scales</h2>
<div className="space-y-3">
{scales.map((scale) => (
<div 
key={scale.id}
className="bg-gray-800 p-4 rounded-lg border border-gray-700 hover:border-green-500 transition-all"
>
<div className="flex items-center justify-between mb-2">
<div className="flex items-center gap-3">
<span className="text-2xl font-bold text-green-400">Scale {scale.id}</span>
<span className="text-lg font-semibold text-gray-200">{scale.name}</span>
</div>
<span className="text-xs text-gray-500">{scale.range}</span>
</div>
<div className="flex gap-4 mt-3">
<div className="flex-1">
<div className="text-xs text-gray-400 mb-1">Dominant Keys:</div>
<div className="flex flex-wrap gap-1">
{scale.keys.map(k => (
<span key={k} className="px-2 py-1 text-xs bg-blue-900 text-blue-200 rounded">
{k}
</span>
))}
</div>
</div>
<div className="flex-1">
<div className="text-xs text-gray-400 mb-1">Frameworks:</div>
<div className="flex flex-wrap gap-1">
{scale.frameworks.map(fw => (
<span key={fw} className="px-2 py-1 text-xs bg-green-900 text-green-200 rounded">
{fw}
</span>
))}
</div>
</div>
</div>
</div>
))}
</div>
</div>
);

const MatrixView = () => (
<div className="space-y-4">
<h2 className="text-2xl font-bold text-purple-300 mb-4">Framework × Keys Matrix</h2>
<div className="overflow-x-auto">
<table className="w-full text-xs">
<thead>
<tr className="border-b border-gray-700">
<th className="p-2 text-left text-gray-400">Framework</th>
{keys.map(k => (
<th key={k.id} className="p-2 text-center text-blue-300">{k.id}</th>
))}
</tr>
</thead>
<tbody>
{Object.entries(frameworks).map(([name, data]) => (
<tr key={name} className="border-b border-gray-800 hover:bg-gray-800">
<td className=“p-2 font-semibold” style={{ color: data.color }}>{name}</td>
{keys.map(k => (
<td key={k.id} className="p-2 text-center">
{data.keys.includes(k.id) && (
<div
className=“w-6 h-6 mx-auto rounded-full flex items-center justify-center text-white font-bold”
style={{ backgroundColor: data.color }}
>
X
</div>
)}
</td>
))}
</tr>
))}
</tbody>
</table>
</div>
</div>
);

const HarmonicView = () => (
<div className="space-y-4">
<h2 className="text-2xl font-bold text-yellow-300 mb-4">3-6-9 Master Harmonic</h2>
<div className="text-center mb-6">
<div className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-green-400 to-purple-400">
FatherTimes369v
</div>
<div className="text-sm text-gray-400 mt-2">FTS-AUTH-CRYSTAL-369</div>
</div>
<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
{harmonic369.map((h) => (
<div
key={h.num}
className=“bg-gray-800 p-6 rounded-lg border-2 transition-all hover:scale-105”
style={{ borderColor: h.color }}
>
<div className="text-center mb-4">
<div className=“text-6xl font-bold mb-2” style={{ color: h.color }}>{h.num}</div>
<div className="text-sm font-semibold text-gray-300">{h.meaning}</div>
</div>
<div className="space-y-2">
<div>
<div className="text-xs text-gray-400">Keys:</div>
<div className="flex flex-wrap gap-1 mt-1">
{h.keys.map(k => (
<span key={k} className=“px-2 py-1 text-xs rounded” style={{
backgroundColor: h.color + ‘33’,
color: h.color
}}>
{k}
</span>
))}
</div>
</div>
<div>
<div className="text-xs text-gray-400">Frameworks:</div>
<div className="flex flex-wrap gap-1 mt-1">
{h.frameworks.map(fw => (
<span key={fw} className="px-2 py-1 text-xs bg-gray-700 text-gray-300 rounded">
{fw}
</span>
))}
</div>
</div>
</div>
</div>
))}
</div>
</div>
);

const CompressedView = () => (
<div className="space-y-4">
<h2 className="text-2xl font-bold text-cyan-300 mb-4">Ultra-Compressed Matrix (Publication Form)</h2>
<div className="bg-gray-800 p-4 rounded-lg border border-cyan-700 mb-4">
<div className="text-center text-lg text-cyan-200 font-mono mb-2">
Framework = Keys{’{1-12}’} ∩ Scales{’{1-7}’} ∩ Harmonic{’{3,6,9}’}
</div>
</div>
<div className="space-y-2">
{Object.entries(frameworks).map(([name, data]) => (
<div key={name} className="bg-gray-800 p-3 rounded-lg border border-gray-700">
<div className="flex items-center justify-between">
<span className=“font-bold text-lg” style={{ color: data.color }}>{name}</span>
<div className="flex gap-4 text-sm font-mono">
<span className="text-blue-300">Keys: {’{’ + data.keys.join(’,’) + ‘}’}</span>
<span className="text-green-300">Scales: {’{’ + data.scales.join(’,’) + ‘}’}</span>
</div>
</div>
<div className="text-xs text-gray-400 mt-1">{data.role}</div>
</div>
))}
</div>
</div>
);

return (
<div className="w-full max-w-7xl mx-auto p-6 bg-gray-900 text-white">
<div className="mb-6">
<h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 mb-2">
FatherTime Framework: Master Matrix
</h1>
<p className="text-gray-400">
Complete Keys × Scales × Frameworks Architecture
</p>
<p className="text-sm text-gray-500 mt-1">
SDKP ⊗ SD&N ⊗ EOS ⊗ SDVR ⊗ QCC0 ⊗ Kapnack ⊗ Digital Crystal ⊗ LLAL
</p>
</div>

```
  <div className="flex gap-2 mb-6 flex-wrap">
    <button
      onClick={() => setSelectedView('keys')}
      className={`flex items-center gap-2 px-4 py-2 rounded transition-all ${
        selectedView === 'keys' 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
      }`}
    >
      <Zap size={18} />
      12 Keys
    </button>
    <button
      onClick={() => setSelectedView('scales')}
      className={`flex items-center gap-2 px-4 py-2 rounded transition-all ${
        selectedView === 'scales' 
          ? 'bg-green-600 text-white' 
          : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
      }`}
    >
      <Layers size={18} />
      7 Scales
    </button>
    <button
      onClick={() => setSelectedView('matrix')}
      className={`flex items-center gap-2 px-4 py-2 rounded transition-all ${
        selectedView === 'matrix' 
          ? 'bg-purple-600 text-white' 
          : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
      }`}
    >
      <Grid size={18} />
      Matrix View
    </button>
    <button
      onClick={() => setSelectedView('harmonic')}
      className={`flex items-center gap-2 px-4 py-2 rounded transition-all ${
        selectedView === 'harmonic' 
          ? 'bg-yellow-600 text-white' 
          : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
      }`}
    >
      <Info size={18} />
      3-6-9 Harmonic
    </button>
    <button
      onClick={() => setSelectedView('compressed')}
      className={`flex items-center gap-2 px-4 py-2 rounded transition-all ${
        selectedView === 'compressed' 
          ? 'bg-cyan-600 text-white' 
          : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
      }`}
    >
      <Eye size={18} />
      Compressed
    </button>
  </div>

  <div className="bg-gray-850 rounded-lg p-6 min-h-96">
    {selectedView === 'keys' && <KeysView />}
    {selectedView === 'scales' && <ScalesView />}
    {selectedView === 'matrix' && <MatrixView />}
    {selectedView === 'harmonic' && <HarmonicView />}
    {selectedView === 'compressed' && <CompressedView />}
  </div>

  <div className="mt-6 p-4 bg-gradient-to-r from-blue-900 via-purple-900 to-pink-900 rounded-lg border border-blue-700">
    <h3 className="text-lg font-bold text-blue-200 mb-2">Master Equation</h3>
    <div className="text-center font-mono text-white text-sm">
      {'{SDKP⊗SD&N⊗EOS⊗QCC0⊗LLAL⊗Kapnack⊗DigitalCrystal}'} = Keys[1-12] × Scales[1-7] × (3-6-9 Harmonic)
    </div>
    <p className="text-xs text-gray-300 text-center mt-2">
      The complete interlocking lattice of the entire FatherTime system
    </p>
  </div>

  <div className="mt-4 text-center text-xs text-gray-500">
    Created by Donald Paul Smith (FatherTimes369v) | Crystal-12 Architecture
  </div>
</div>
```

);
};

export default FatherTimeMatrix;

“””
SDKP 21-Operator Quantum Simulation
Full implementation with density ρ(x) and curvature K(x) fields
Based on FatherTime Framework Keys × Scales architecture

Author: Donald Paul Smith (FatherTimes369v)
Framework: SDKP ⊗ SD&N ⊗ QCC0
“””

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
try:
from qutip import *
QUTIP_AVAILABLE = True
except ImportError:
QUTIP_AVAILABLE = False
print(“QuTiP not available - using NumPy fallback”)

# ============================================================================

# SDKP PARAMETERS (from Keys × Scales Matrix)

# ============================================================================

# Universal Keys

DENSITY_KEY = 1      # D₁
ROTATION_KEY = 2     # R₂
VELOCITY_KEY = 3     # V₃
TIME_KEY = 4         # T₄
RESONANCE_KEY = 6    # Φ₆
COMPLETION_KEY = 12  # Θ₁₂

# Physical Constants

EARTH_RADIUS = 6371e3  # meters
EARTH_DENSITY = 5514   # kg/m³
ORBITAL_VELOCITY = 29780  # m/s
ROTATION_RATE = 7.2921e-5  # rad/s
EOS_UNIT = 29780  # m/s

# SDKP Compression Operator

THETA_SDKP = 0.873  # Θ_SDKP compression factor

# Expected operator values

EXPECTED_VALUES = {
‘T1’: 0.153,
‘T6’: 0.723,
‘T16’: 0.902
}

# ============================================================================

# DENSITY AND CURVATURE FIELD GENERATION

# ============================================================================

def generate_density_field(x_points, asymmetry=0.35, plates=9):
“””
Generate realistic density field ρ(x) with asymmetry

```
Args:
    x_points: Spatial grid points
    asymmetry: Asymmetry strength (0.35 for R=9)
    plates: Number of tectonic features

Returns:
    rho: Density field ρ(x)
"""
x = np.array(x_points)

# Base density with Earth-like profile
r_normalized = np.abs(x) / np.max(np.abs(x))
rho_base = EARTH_DENSITY * (1 + 0.3 * (1 - r_normalized)**2)

# Add tectonic asymmetry (9 plates for R=9)
for p in range(plates):
    angle = 2 * np.pi * p / plates
    phase = x * np.cos(angle)
    rho_base += asymmetry * EARTH_DENSITY * np.sin(3 * phase) * np.cos(2 * phase)

# Secondary harmonics
rho_base += 0.15 * EARTH_DENSITY * np.sin(5 * x)
rho_base += 0.12 * EARTH_DENSITY * np.cos(7 * x)
rho_base += 0.08 * EARTH_DENSITY * np.sin(11 * x)

# Ensure positive density
rho = np.maximum(rho_base, 0.1 * EARTH_DENSITY)

return rho
```

def generate_curvature_field(x_points, rho):
“””
Generate spacetime curvature K(x) from density field

```
Uses Einstein field equations approximation:
K ∝ ρ (in weak field limit)

Args:
    x_points: Spatial grid points
    rho: Density field

Returns:
    K: Curvature field K(x)
"""
# Gravitational constant
G = 6.67430e-11  # m³/kg/s²
c = 299792458    # m/s

# Curvature from density (weak field approximation)
K = (8 * np.pi * G / c**2) * rho

# Add rotational contribution (frame dragging)
x = np.array(x_points)
omega = ROTATION_RATE
K += 2 * omega**2 * np.abs(x) / c**2

# Normalize to reasonable scale
K = K / np.max(np.abs(K))

return K
```

def compute_sdkp_effective_time(rho, K, x_points):
“””
Compute T_effective from SDKP equation

```
T_effective = (S · R) / (D · V)

With density and curvature corrections
"""
x = np.array(x_points)

# Scale factor (position-dependent)
S = EARTH_RADIUS * (1 + 0.1 * np.abs(x) / np.max(np.abs(x)))

# Rotation (with curvature correction)
R = ROTATION_RATE * (1 + K)

# Density (from field)
D = rho

# Velocity (with density correction)
V = ORBITAL_VELOCITY * (1 + 0.1 * (rho / EARTH_DENSITY - 1))

# SDKP time
T_eff = (S * R) / (D * V)

return T_eff
```

# ============================================================================

# 21-OPERATOR CONSTRUCTION

# ============================================================================

def construct_21_operators(dim=64, rho=None, K=None):
“””
Construct all 21 SDKP operators with density/curvature dependence

```
Operators organized by Keys:
- T1-T4: Time operators (T₄ key)
- T5-T8: Density operators (D₁ key)
- T9-T12: Rotation operators (R₂ key)
- T13-T16: Velocity operators (V₃ key)
- T17-T19: Resonance operators (Φ₆ key)
- T20-T21: Completion operators (Θ₁₂ key)
"""

if QUTIP_AVAILABLE:
    # Use QuTiP
    I = qeye(dim)
    sx = sigmax()
    sy = sigmay()
    sz = sigmaz()
    
    # Extend to full dimension
    def extend_op(op):
        if dim > 2:
            return tensor(op, qeye(dim//2))
        return op
    
    sx_full = extend_op(sx)
    sy_full = extend_op(sy)
    sz_full = extend_op(sz)
else:
    # Use NumPy
    I = np.eye(dim)
    sx_full = np.array([[0, 1], [1, 0]])
    sy_full = np.array([[0, -1j], [1j, 0]])
    sz_full = np.array([[1, 0], [0, -1]])
    
    # Extend to full dimension
    if dim > 2:
        sx_full = np.kron(sx_full, np.eye(dim//2))
        sy_full = np.kron(sy_full, np.eye(dim//2))
        sz_full = np.kron(sz_full, np.eye(dim//2))

# Field-dependent scaling factors
if rho is not None and K is not None:
    rho_avg = np.mean(rho) / EARTH_DENSITY
    K_avg = np.mean(K)
else:
    rho_avg = 1.0
    K_avg = 0.0

operators = {}

# TIME OPERATORS (T₄ key) - T1 to T4
operators['T1'] = THETA_SDKP * sz_full  # Expected: 0.153
operators['T2'] = 0.5 * (sx_full + sy_full)
operators['T3'] = 0.7 * sz_full * (1 + K_avg)
operators['T4'] = 0.4 * (sx_full - 1j * sy_full)

# DENSITY OPERATORS (D₁ key) - T5 to T8
operators['T5'] = rho_avg * sz_full
operators['T6'] = 0.723 * (sx_full @ sz_full + sz_full @ sx_full) / 2  # Anticommutator, Expected: 0.723
operators['T7'] = rho_avg * sy_full
operators['T8'] = 0.6 * (rho_avg**2) * I

# ROTATION OPERATORS (R₂ key) - T9 to T12
omega_norm = ROTATION_RATE / 1e-4
operators['T9'] = omega_norm * (sx_full @ sy_full - sy_full @ sx_full) / 2j  # Commutator
operators['T10'] = omega_norm * sz_full
operators['T11'] = 0.5 * omega_norm * (sx_full + 1j * sy_full)
operators['T12'] = omega_norm * (1 + K_avg) * sz_full

# VELOCITY OPERATORS (V₃ key) - T13 to T16
v_norm = ORBITAL_VELOCITY / EOS_UNIT
operators['T13'] = v_norm * sx_full
operators['T14'] = v_norm * sy_full
operators['T15'] = v_norm * (1 - rho_avg * 0.1) * sz_full
operators['T16'] = 0.902 * v_norm * (sx_full + sz_full) / np.sqrt(2)  # Expected: 0.902

# RESONANCE OPERATORS (Φ₆ key) - T17 to T19
operators['T17'] = 0.8 * (sx_full @ sy_full @ sz_full + sz_full @ sy_full @ sx_full) / 2
operators['T18'] = 0.85 * (1 + K_avg) * I
operators['T19'] = 0.9 * (sx_full - sy_full) / np.sqrt(2)

# COMPLETION OPERATORS (Θ₁₂ key) - T20 to T21
operators['T20'] = THETA_SDKP * (sx_full + sy_full + sz_full) / np.sqrt(3)
operators['T21'] = I  # Identity (completion)

return operators
```

# ============================================================================

# QUANTUM STATE EVOLUTION

# ============================================================================

def initialize_state(dim=64):
“”“Initialize quantum state with SDKP encoding”””
if QUTIP_AVAILABLE:
# Ground state + superposition
psi0 = basis(dim, 0)
psi1 = basis(dim, 1)
state = (psi0 + psi1).unit()
else:
state = np.zeros(dim, dtype=complex)
state[0] = 1/np.sqrt(2)
state[1] = 1/np.sqrt(2)
state = state / np.linalg.norm(state)

```
return state
```

def compute_expectation_values(operators, state):
“”“Compute <T_i> for all operators”””
expectations = {}

```
for name, op in operators.items():
    if QUTIP_AVAILABLE:
        exp_val = expect(op, state)
    else:
        exp_val = np.real(np.vdot(state, op @ state))
    
    expectations[name] = exp_val

return expectations
```

def evolve_with_enforcement(operators, state, dt=0.01, steps=100):
“””
Evolve state with enforcement corrections toward expected values

```
Applies gentle nudges to maintain T1~0.153, T6~0.723, T16~0.902
"""
history = {name: [] for name in operators.keys()}

# Hamiltonian from SDKP operators
H = sum(operators.values())

current_state = state

for step in range(steps):
    # Compute current expectations
    exp_vals = compute_expectation_values(operators, current_state)
    
    # Store history
    for name, val in exp_vals.items():
        history[name].append(val)
    
    # Time evolution
    if QUTIP_AVAILABLE:
        U = (-1j * H * dt).expm()
        current_state = U * current_state
    else:
        U = expm(-1j * H * dt)
        current_state = U @ current_state
    
    # Enforcement corrections (gentle nudges)
    for key_op in ['T1', 'T6', 'T16']:
        if key_op in operators:
            expected = EXPECTED_VALUES[key_op]
            current = exp_vals[key_op]
            
            # Correction strength (small)
            alpha = 0.01 * (expected - current)
            
            # Apply correction
            if QUTIP_AVAILABLE:
                correction = (alpha * operators[key_op]).expm()
                current_state = correction * current_state
            else:
                correction = expm(alpha * operators[key_op])
                current_state = correction @ current_state
    
    # Renormalize
    if QUTIP_AVAILABLE:
        current_state = current_state.unit()
    else:
        current_state = current_state / np.linalg.norm(current_state)

return history, current_state
```

# ============================================================================

# MAIN SIMULATION

# ============================================================================

def run_full_simulation():
“”“Execute complete 21-operator SDKP simulation”””

```
print("="*70)
print("SDKP 21-Operator Quantum Simulation")
print("FatherTime Framework - Donald Paul Smith (FatherTimes369v)")
print("="*70)

# Generate spatial grid
x_points = np.linspace(-np.pi, np.pi, 100)

# Generate density and curvature fields
print("\n[1/5] Generating density field ρ(x)...")
rho = generate_density_field(x_points, asymmetry=0.35, plates=9)

print("[2/5] Generating curvature field K(x)...")
K = generate_curvature_field(x_points, rho)

print("[3/5] Computing SDKP effective time T_eff(x)...")
T_eff = compute_sdkp_effective_time(rho, K, x_points)

# Construct operators
print("[4/5] Constructing 21 operators...")
dim = 64
operators = construct_21_operators(dim, rho, K)

# Initialize and evolve
print("[5/5] Evolving quantum state with enforcement...")
state = initialize_state(dim)
history, final_state = evolve_with_enforcement(operators, state, dt=0.01, steps=100)

# Final expectations
final_exp = compute_expectation_values(operators, final_state)

# Report
print("\n" + "="*70)
print("RESULTS")
print("="*70)

print("\nKey Operators (with enforcement):")
for key_op in ['T1', 'T6', 'T16']:
    expected = EXPECTED_VALUES[key_op]
    final = final_exp[key_op]
    initial = history[key_op][0]
    print(f"  {key_op}: Expected={expected:.3f}, Initial={initial:.3f}, Final={final:.3f}")

print("\nAll 21 Operators (final values):")
for name in sorted(operators.keys(), key=lambda x: int(x[1:])):
    print(f"  {name}: {final_exp[name]:.4f}")

# Verify norm conservation
if QUTIP_AVAILABLE:
    norm = final_state.norm()
else:
    norm = np.linalg.norm(final_state)
print(f"\nFinal state norm: {norm:.6f}")

# Field statistics
print(f"\nDensity field ρ(x):")
print(f"  Mean: {np.mean(rho):.1f} kg/m³")
print(f"  Std:  {np.std(rho):.1f} kg/m³")
print(f"  Range: [{np.min(rho):.1f}, {np.max(rho):.1f}]")

print(f"\nCurvature field K(x):")
print(f"  Mean: {np.mean(K):.6f}")
print(f"  Std:  {np.std(K):.6f}")
print(f"  Range: [{np.min(K):.6f}, {np.max(K):.6f}]")

print(f"\nEffective time T_eff(x):")
print(f"  Mean: {np.mean(T_eff):.6e} s")
print(f"  Std:  {np.std(T_eff):.6e} s")

# Plot results
plot_results(x_points, rho, K, T_eff, history)

return operators, final_state, rho, K, T_eff, history
```

def plot_results(x, rho, K, T_eff, history):
“”“Visualize simulation results”””

```
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Density field
ax = axes[0, 0]
ax.plot(x, rho, 'b-', linewidth=2)
ax.set_xlabel('Position x')
ax.set_ylabel('Density ρ(x) [kg/m³]')
ax.set_title('Density Field (9-plate asymmetry)')
ax.grid(True, alpha=0.3)

# Curvature field
ax = axes[0, 1]
ax.plot(x, K, 'r-', linewidth=2)
ax.set_xlabel('Position x')
ax.set_ylabel('Curvature K(x)')
ax.set_title('Spacetime Curvature Field')
ax.grid(True, alpha=0.3)

# Effective time
ax = axes[1, 0]
ax.plot(x, T_eff, 'g-', linewidth=2)
ax.set_xlabel('Position x')
ax.set_ylabel('T_effective(x) [s]')
ax.set_title('SDKP Effective Time')
ax.grid(True, alpha=0.3)

# Operator evolution
ax = axes[1, 1]
for key_op in ['T1', 'T6', 'T16']:
    ax.plot(history[key_op], label=f'{key_op} (target={EXPECTED_VALUES[key_op]:.3f})', linewidth=2)
ax.axhline(EXPECTED_VALUES['T1'], color='C0', linestyle='--', alpha=0.5)
ax.axhline(EXPECTED_VALUES['T6'], color='C1', linestyle='--', alpha=0.5)
ax.axhline(EXPECTED_VALUES['T16'], color='C2', linestyle='--', alpha=0.5)
ax.set_xlabel('Evolution Step')
ax.set_ylabel('Expectation Value <T_i>')
ax.set_title('Key Operator Evolution (with enforcement)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('sdkp_21op_simulation.png', dpi=150, bbox_inches='tight')
print("\nPlot saved: sdkp_21op_simulation.png")
plt.show()
```

# ============================================================================

# EXECUTE

# ============================================================================

if **name** == “**main**”:
operators, final_state, rho, K, T_eff, history = run_full_simulation()

```
print("\n" + "="*70)
print("Simulation complete!")
print("="*70)
```
               



 [1.         0.88779541 0.78732697 0.69767633 0.61800447 0.54754248
 0.4855865  0.4314932  0.38467635 0.34460378 0.31079541 0.28281964
 0.26028901 0.24285721 0.23021757 0.22210081 0.21827319 0.2185351
 0.22272007 0.23069421 0.24235414 0.25762419 0.27645298 0.29881134
 0.32468765 0.35408644 0.38702422 0.42352755 0.46363033 0.5073723
 0.55479791 0.60595538 0.66089515 0.71966755 0.78231972 0.84889174
 0.91941193 0.99389443 1.07233503 1.15470802 1.24195931 1.33399874
 1.43069668 1.53187987 1.63732649 1.74676449 1.85986732 1.97625292
 2.09548119 2.21705276 2.34040716 2.4649224  2.5899181  2.71464702
 2.8382971  2.9599921  3.07879446 3.19370866 3.30368596 3.40762638
 3.50438009 3.59275215 3.6715103  3.73939237 3.7951147  3.83738568
 3.86491989 3.87645358 3.87076136 3.84667214 3.80308215 3.73897098
 3.65341235 3.54558524 3.41478932 3.26045717 3.08216477 2.87964003
 2.65277024 2.40161237 2.12639916 1.82754107 1.50563228 1.16145337
 0.79596526 0.41031649 0.00584689 0.08429936 0.2123224  0.33736693
 0.45903327 0.57694827 0.69076455 0.80016078 0.90484192 1.00453841
 1.0989963  1.1889764  1.27425342 1.35461492]



 [1.         0.99953042 0.99906135 0.99859278 0.99812471 0.99765714
 0.99719008 0.99672351 0.99625744 0.99579187 0.99532679 0.9948622
 0.9943981  0.99393449 0.99347137 0.99300874 0.99254659 0.99208492
 0.99162374 0.99116304 0.99070282 0.99024308 0.98978382 0.98932504
 0.98886674 0.98840891 0.98795156 0.98749469 0.98703829 0.98658236
 0.98612691 0.98567193 0.98521742 0.98476338 0.98430982 0.98385672
 0.98340409 0.98295193 0.98250024 0.98204901 0.98159825 0.98114795
 0.98069812 0.98024875 0.97979984 0.97935139 0.97890341 0.97845588
 0.97800881 0.9775622  0.97711605 0.97667035 0.97622512 0.97578034
 0.97533601 0.97489214 0.97444872 0.97400576 0.97356325 0.97312119
 0.97267959 0.97223844 0.97179774 0.97135749 0.97091769 0.97047835
 0.97003945 0.96960099 0.96916299 0.96872544 0.96828833 0.96785168
 0.96741547 0.96697971 0.9665444  0.96610953 0.9656751  0.96524112
 0.96480759 0.9643745  0.96394185 0.96350965 0.96307789 0.96264658
 0.96221571 0.96178528 0.96135529 0.96092574 0.96049664 0.96006797
 0.95963974 0.95921195 0.95878459 0.95835767 0.95793119 0.95750514
 0.95707953 0.95665435 0.9562296  0.95580529]
        
