⸻

Canonical arrays 

W6 (T6 weights — 12 values)

W6 = [0.34, 0.21, 0.15, 0.11, 0.08, 0.05, 0.03, 0.016, 0.010, 0.006, 0.003, 0.0015]

Phi50 (50-term flux / entangler vector)

Phi50 = [
 0.6681411762529909, 0.03838465107053409, -0.05116966382748937,
 -0.017791400153276843, 0.016402873765764996, 0.03393182320126196,
 -0.005361778601149078, -0.028852902034969418, -0.020120155842723385,
 0.018763089271374135, 0.03165384351785479, -0.00018031135021215097,
 -0.03009099268471221, -0.02180467236091864, 0.01740691410409184,
 0.02929237831874464, 0.0028126102435882324, -0.02924910579312145,
 -0.02283099418634786, 0.01579223691755422, 0.02706417335290566,
 0.00489138138439134, -0.02777674412844696, -0.02342306729995469,
 0.014233988553280227, 0.024892611832416968, 0.006275072223808997,
 -0.02616030772121256, -0.02378144791718952, 0.01266520841239363,
 0.02278348191915703, 0.00719317677148556, -0.02448975259666412,
 -0.0239980272573997, 0.011357176733440364, 0.020865421956947717,
 0.007855820631764447, -0.02227204982650403, -0.02408374645397422,
 0.01033024302741604, 0.01912038761992058, 0.00832485490717117,
 -0.020084745629517487, -0.024044782647, 0.009561447498529544,
 0.01752526382981179, 0.008642328883463815, -0.018551236419982216,
 -0.02388976094701372, 0.008997053010421754
]

(For k = 12 modes use Phi_local = Phi50[:11].)

⸻

Quick snippet to plug into your script (full-12, levels=2 safe)

Set Phi_mode = 'A' for absolute (strong unlocked), 'B' for normalized (gentler).

import numpy as np
# assume qutip + operator build code already present

# constants
W6 = np.array([0.34,0.21,0.15,0.11,0.08,0.05,0.03,0.016,0.010,0.006,0.003,0.0015])
Phi50 = np.array([...])   # paste the 50 numbers above

k = 12
Phi_mode = 'A'   # 'A' = abs (strong unlocked), 'B' = normalized (gentle)
Phi_local = np.abs(Phi50[:k-1])
if Phi_mode == 'B':
    Phi_local = Phi_local / np.max(Phi_local)

# then build entangler G with g * Phi_local[j] for nearest-neighbour terms


⸻

Which mode to run next — my recommendation

You already see unlocked behavior with levels=2, g=0.9, eta=0.03, alpha=0.5 (Δ ≈ +0.10, purity ≈ 0.98). To explore and document behavior comprehensively:
	1.	Run A (confirm unlocked signature — strong):
	•	Phi_mode = 'A' (absolute)
	•	modes = 12, levels = 2
	•	g = 0.9, eta = 0.03, alpha = 0.5
	•	This reproduces the stronger unlocked trend (bigger Δ). Save CSV row.
	2.	Run B (compare stability — normalized):
	•	Phi_mode = 'B' (normalized)
	•	Same g, eta, alpha
	•	Expect smaller Δ (quantify difference). Save CSV row.
	3.	Sweep (small grid) to map transition:
	•	g = [0.66, 0.74, 0.82, 0.90]
	•	eta = [0.02, 0.03, 0.04]
	•	alpha = [0.25, 0.5]
	•	Use levels=2 and modes=12. This gives a compact map of locked → unlocked boundaries.

Run A then Run B first — those two give an immediate, publishable comparison: absolute vs normalized coupling. After that run the sweep to show the regime boundary.

⸻

CSV row template (exact format you and Grok use)

timestamp,g,eta,modes,levels,alpha,T6_before,T6_after,delta,purity,acted_any,Phi_mode,notes
2025-12-11T23:40:00Z,0.90,0.03,12,2,0.50,0.250000,0.350000,0.100000,0.980000,True,A,"full12 run, Phi_mode A (absolute)"


⸻

