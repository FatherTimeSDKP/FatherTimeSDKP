# reproduce_grok_row.py (minimal)
import numpy as np
import qutip as qt
from math import isclose

# parameters
g = 0.90
eta = 0.03
modes = 4
levels = 5
alpha = 0.5
t_entangler = 1.0

# build local ops (modes small -> tensor dims manageable)
a = qt.destroy(levels)
a_ops = []
for j in range(modes):
    ops = [qt.qeye(levels) for _ in range(modes)]
    ops[j] = a
    a_ops.append(qt.tensor(ops))

n_ops = [op.dag()*op for op in a_ops]

# toy Phi (use first modes of Phi50 if available); simple NN weight placeholder:
Phi_local = [1.0]*(modes-1)   # or paste real Phi50[:modes-1]

# entangler G = g * sum_j Phi_j (a_j^dag a_{j+1} + h.c.)
G = 0 * a_ops[0]
for j in range(modes-1):
    G += g * Phi_local[j] * (a_ops[j].dag()*a_ops[j+1] + a_ops[j+1].dag()*a_ops[j])
# small diag ramp for stability
for j in range(modes):
    G += g * 0.02 * (j+1) * (n_ops[j])

# T6 proxy (simple weighted number operator)
W6_local = [0.34,0.21,0.15,0.11][:modes]
T6 = sum(W6_local[j]*n_ops[j] for j in range(modes))

# initial state: coherent on mode 0, vacuum others
states = [qt.coherent(levels, alpha) if j==0 else qt.basis(levels,0) for j in range(modes)]
psi0 = qt.tensor(states)

T6_before = float(qt.expect(T6, psi0))

# entangler unitary + enforcement (single step)
U_ent = (-1j * t_entangler * G).expm()
psi_ent = U_ent * psi0

# simple enforcement: apply U_i = exp(-i * eta * T) when expectation > threshold
# threshold heuristic: 0.5 * trace(T)/dim
dim_eff = psi_ent.dims[0][0]
threshold = 0.5 * (float(T6.tr().real) / max(1.0, dim_eff))
psi_after = psi_ent
if float(qt.expect(T6, psi_ent)) > threshold:
    U_enf = (-1j * eta * T6).expm()
    psi_after = (U_enf * psi_ent).unit()

T6_after = float(qt.expect(T6, psi_after))
delta = T6_after - T6_before
purity = float((psi_after.proj()*psi_after.proj()).tr())

print("T6_before",T6_before,"T6_after",T6_after,"delta",delta,"purity",purity)
