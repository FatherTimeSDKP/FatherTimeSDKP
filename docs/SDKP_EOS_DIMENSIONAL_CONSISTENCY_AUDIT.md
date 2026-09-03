
# SDKP EOS Dimensional Consistency Audit
**Framework:** Scale-Density-Kinetic Principle (SDKP)  
**Module:** Earth-Orbital-Speed (EOS) Correction  
**Status:** Formal audit specification  
**Version:** 1.0  
**Author:** Donald Paul Smith  
---
## 1. Purpose
This document defines a dimensional-analysis audit for the SDKP Earth-Orbital-Speed (EOS) correction.
The objective is to ensure that every proposed SDKP EOS equation:
1. has consistent physical dimensions,
2. uses explicitly defined quantities,
3. does not silently combine incompatible units,
4. distinguishes dimensional quantities from dimensionless parameters,
5. remains valid when SI units are changed.
Dimensional consistency is a necessary condition for a physical equation, but it is not sufficient evidence that the equation is physically correct.
---
# 2. Fundamental SI Dimensions
Use the base dimensions
\[
[M],\quad[L],\quad[T].
\]
where:
- \(M\) = mass,
- \(L\) = length,
- \(T\) = time.
---
# 3. Kinetic-Energy Dimension
Let
\[
K
\]
represent kinetic energy.
The SI unit is joule:
\[
[K]=\mathrm{J}.
\]
Since
\[
1\ \mathrm{J}
=
1\ \mathrm{kg\,m^2\,s^{-2}},
\]
the dimensional form is
\[
[K]
=
ML^2T^{-2}.
\]
---
# 4. Velocity Dimension
For any velocity \(v\),
\[
[v]
=
LT^{-1}.
\]
Therefore,
\[
[v^2]
=
L^2T^{-2}.
\]
---
# 5. EOS Normalization
The proposed normalization is
\[
M_{\mathrm{EOS}}
=
\frac{K}{v_{\mathrm{EOS}}^2}.
\]
Dimensional analysis gives
\[
[M_{\mathrm{EOS}}]
=
\frac{ML^2T^{-2}}
{L^2T^{-2}}.
\]
Therefore,
\[
\boxed{
[M_{\mathrm{EOS}}]=M
}
\]
and the SI unit is kilograms.
Thus
\[
\boxed{
\frac{K}{v_{\mathrm{EOS}}^2}
\text{ has units of mass.}
}
\]
---
# 6. Conventional Relativistic Normalization
The conventional comparison is
\[
M_c
=
\frac{K}{c^2}.
\]
Because
\[
[c]=LT^{-1},
\]
we obtain
\[
[M_c]
=
\frac{ML^2T^{-2}}
{L^2T^{-2}}
=
M.
\]
Therefore,
\[
\boxed{
\frac{K}{c^2}
\text{ also has units of mass.}
}
\]
---
# 7. Dimensional Equivalence
Both expressions
\[
\frac{K}{c^2}
\]
and
\[
\frac{K}{v_{\mathrm{EOS}}^2}
\]
have the same physical dimension:
\[
[M].
\]
This establishes dimensional compatibility between the two normalizations.
It does **not** establish that the two quantities represent the same physical phenomenon.
---
# 8. Amplification Factor
Define
\[
A_{\mathrm{EOS}}
=
\frac{K/v_{\mathrm{EOS}}^2}
{K/c^2}.
\]
Canceling \(K\),
\[
A_{\mathrm{EOS}}
=
\frac{c^2}{v_{\mathrm{EOS}}^2}.
\]
Therefore,
\[
A_{\mathrm{EOS}}
=
\left(
\frac{c}{v_{\mathrm{EOS}}}
\right)^2.
\]
Because both velocities have identical dimensions,
\[
[A_{\mathrm{EOS}}]=1.
\]
Thus
\[
\boxed{
A_{\mathrm{EOS}}
\text{ is dimensionless.}
}
\]
---
# 9. EOS Numerical Value
Using
\[
c=299\,792\,458\ \mathrm{m/s}
\]
and
\[
v_{\mathrm{EOS}}
=
29\,780\ \mathrm{m/s},
\]
the amplification factor is approximately
\[
A_{\mathrm{EOS}}
\approx
1.013\times10^8.
\]
This large value arises from the ratio of the two velocity scales.
It is not itself evidence of a new physical interaction.
---
# 10. Generic EOS Correction
Consider
\[
X_{\mathrm{EOS}}
=
X_0+
\alpha_{\mathrm{EOS}}
\frac{K}{v_{\mathrm{EOS}}^2}.
\]
For addition to be valid,
\[
[X_{\mathrm{EOS}}]
=
[X_0].
\]
Therefore,
\[
[\alpha_{\mathrm{EOS}}]
\frac{K}{v_{\mathrm{EOS}}^2}
=
[X_0].
\]
Since
\[
\left[
\frac{K}{v_{\mathrm{EOS}}^2}
\right]
=
M,
\]
we require
\[
\boxed{
[\alpha_{\mathrm{EOS}}]
=
\frac{[X_0]}{M}.
}
\]
---
# 11. Examples of Coupling Dimensions
If
\[
X_0
\]
is itself a mass,
\[
[\alpha_{\mathrm{EOS}}]=1.
\]
Therefore,
\[
\alpha_{\mathrm{EOS}}
\]
is dimensionless.
If \(X_0\) is an energy,
\[
[X_0]=ML^2T^{-2},
\]
so
\[
[\alpha_{\mathrm{EOS}}]
=
L^2T^{-2}.
\]
If \(X_0\) is an acceleration,
\[
[X_0]=LT^{-2},
\]
then
\[
[\alpha_{\mathrm{EOS}}]
=
L T^{-2}M^{-1}.
\]
The coupling cannot be declared dimensionless without first specifying the observable.
---
# 12. Dimensionless Fractional Correction
A preferred formulation for many applications is
\[
\delta_X
=
\beta_{\mathrm{EOS}}
\frac{K}
{M_{\mathrm{ref}}v_{\mathrm{EOS}}^2}.
\]
We have
\[
[K]=ML^2T^{-2},
\]
and
\[
[M_{\mathrm{ref}}v_{\mathrm{EOS}}^2]
=
M L^2T^{-2}.
\]
Therefore,
\[
\left[
\frac{K}
{M_{\mathrm{ref}}v_{\mathrm{EOS}}^2}
\right]
=1.
\]
Consequently,
\[
[\beta_{\mathrm{EOS}}]=1.
\]
Thus,
\[
\boxed{
\delta_X
\text{ is dimensionless.}
}
\]
---
# 13. Corrected Dimensionless Observable
If \(X\) is dimensionless,
\[
X_{\mathrm{EOS}}
=
X_0(1+\delta_X).
\]
Because
\[
[\delta_X]=1,
\]
the term
\[
1+\delta_X
\]
is dimensionless.
Therefore,
\[
[X_{\mathrm{EOS}}]
=
[X_0].
\]
---
# 14. Density Formulation
Suppose the kinetic quantity is distributed over volume:
\[
\rho_K
=
\frac{K}
{Vv_{\mathrm{EOS}}^2}.
\]
The dimensions are
\[
[K]
=
ML^2T^{-2},
\]
\[
[V]=L^3,
\]
and
\[
[v_{\mathrm{EOS}}^2]
=
L^2T^{-2}.
\]
Therefore,
\[
[\rho_K]
=
\frac{ML^2T^{-2}}
{L^3L^2T^{-2}}.
\]
Hence,
\[
\boxed{
[\rho_K]=ML^{-3}.
}
\]
Thus the EOS kinetic-density quantity has the dimensions of mass density.
---
# 15. Effective Density
Define
\[
\rho_{\mathrm{eff}}
=
\rho+
\lambda_{\mathrm{EOS}}\rho_K.
\]
If both \(\rho_{\mathrm{eff}}\) and \(\rho\) represent mass density,
\[
[\rho_{\mathrm{eff}}]
=
[\rho]
=
ML^{-3}.
\]
Therefore,
\[
[\lambda_{\mathrm{EOS}}]=1.
\]
So the coupling may be dimensionless in this formulation.
---
# 16. Density Gradient
The spatial density gradient is
\[
\nabla\rho.
\]
Since
\[
[\rho]=ML^{-3},
\]
and
\[
[\nabla]=L^{-1},
\]
we obtain
\[
\boxed{
[\nabla\rho]
=
ML^{-4}.
}
\]
The EOS correction must therefore satisfy
\[
[\lambda_{\mathrm{EOS}}\nabla\rho_K]
=
ML^{-4}.
\]
---
# 17. SDKP Effective Gradient
If
\[
\rho_{\mathrm{eff}}
=
\rho+
\lambda_{\mathrm{EOS}}\rho_K,
\]
then
\[
\nabla\rho_{\mathrm{eff}}
=
\nabla\rho+
\lambda_{\mathrm{EOS}}\nabla\rho_K
\]
provided that \(\lambda_{\mathrm{EOS}}\) is constant in space.
If
\[
\lambda_{\mathrm{EOS}}
=
\lambda_{\mathrm{EOS}}(\mathbf{x}),
\]
then the product rule gives
\[
\nabla\rho_{\mathrm{eff}}
=
\nabla\rho
+
\lambda_{\mathrm{EOS}}\nabla\rho_K
+
\rho_K\nabla\lambda_{\mathrm{EOS}}.
\]
The final term must not be omitted when the coupling varies spatially.
---
# 18. Variable EOS Velocity
If
\[
v_{\mathrm{EOS}}
=
v_{\mathrm{EOS}}(\mathbf{x}),
\]
then
\[
\rho_K
=
\frac{K}
{Vv_{\mathrm{EOS}}^2}
\]
has a spatial derivative containing
\[
\nabla(v_{\mathrm{EOS}}^{-2}).
\]
Using
\[
\nabla(v^{-2})
=
-2v^{-3}\nabla v,
\]
we obtain
\[
\nabla\rho_K
=
\frac{1}{Vv^2}\nabla K
-
\frac{K}{V^2v^2}\nabla V
-
\frac{2K}{Vv^3}\nabla v.
\]
This expanded form should be used whenever \(K\), \(V\), or \(v\) varies spatially.
---
# 19. Time Dependence
If the quantities depend on time,
\[
K=K(t),
\]
\[
V=V(t),
\]
\[
v=v(t),
\]
then
\[
\rho_K(t)
=
\frac{K(t)}
{V(t)v(t)^2}.
\]
Its logarithmic derivative is
\[
\frac{\dot{\rho}_K}{\rho_K}
=
\frac{\dot K}{K}
-
\frac{\dot V}{V}
-
2\frac{\dot v}{v}.
\]
This relation provides a useful numerical consistency check.
---
# 20. Unit-Invariance Test
A valid physical equation must produce equivalent physical predictions under a change of units.
For example, convert
\[
v_{\mathrm{EOS}}
=
29\,780\ \mathrm{m/s}
\]
to kilometers per second:
\[
v_{\mathrm{EOS}}
=
29.780\ \mathrm{km/s}.
\]
Similarly,
\[
K
\]
must be converted consistently.
The numerical value of the intermediate quantities will change, but the physical result must remain invariant.
---
# 21. Automated Dimensional Audit
The implementation should verify the fundamental relation
\[
\frac{\mathrm{J}}
{(\mathrm{m/s})^2}
=
\mathrm{kg}.
\]
Python reference test:
```python
from dataclasses import dataclass
@dataclass(frozen=True)
class Dimensions:
    M: int = 0
    L: int = 0
    T: int = 0
    def __mul__(self, other):
        return Dimensions(
            self.M + other.M,
            self.L + other.L,
            self.T + other.T
        )
    def __truediv__(self, other):
        return Dimensions(
            self.M - other.M,
            self.L - other.L,
            self.T - other.T
        )
    def __pow__(self, exponent):
        return Dimensions(
            self.M * exponent,
            self.L * exponent,
            self.T * exponent
        )
MASS = Dimensions(M=1)
LENGTH = Dimensions(L=1)
TIME = Dimensions(T=1)
VELOCITY = LENGTH / TIME
ENERGY = MASS * (VELOCITY ** 2)
EOS_MASS = ENERGY / (VELOCITY ** 2)
assert EOS_MASS == MASS
print("Dimensional audit passed:")
print("Energy / velocity^2 = mass")

⸻

22. Unit Conversion Test

C = 299_792_458.0
V_EOS_MS = 29_780.0
K_J = 1.0e12
# SI calculation
mass_si = K_J / V_EOS_MS**2
# Convert quantities to km-based units.
# 1 J = 1e-6 kg km^2 / s^2
# 1 m/s = 1e-3 km/s
K_km_units = K_J * 1e-6
V_EOS_KMS = V_EOS_MS * 1e-3
mass_km_units = (
    K_km_units /
    V_EOS_KMS**2
)
assert abs(mass_si - mass_km_units) < 1e-10
print("Unit-invariance test passed.")
print(f"Mass = {mass_si:.12e} kg")

⸻

23. Symbol Definition Requirement

Every equation entering the SDKP repository must define every symbol.

For the EOS correction,

[
X_{\mathrm{EOS}}

X_0+
\alpha_{\mathrm{EOS}}
\frac{K}{v_{\mathrm{EOS}}^2},
]

the definitions are:

Symbol	Definition	SI Unit
(X_{\mathrm{EOS}})	corrected observable	depends on (X)
(X_0)	baseline observable	depends on (X)
(\alpha_{\mathrm{EOS}})	EOS coupling	depends on (X)
(K)	kinetic-energy-like quantity	J
(v_{\mathrm{EOS}})	EOS reference velocity	m/s

⸻

24. Dimensional Audit Checklist

Every new equation must pass:

* Every symbol is defined.
* Every quantity has declared units.
* Both sides have identical dimensions.
* Additive terms have identical dimensions.
* Multiplicative coupling coefficients have appropriate dimensions.
* Dimensionless quantities are explicitly identified.
* Powers of velocity are correct.
* Spatial derivatives include their (L^{-1}) dimension.
* Temporal derivatives include their (T^{-1}) dimension.
* Unit conversion preserves physical predictions.
* Numerical constants are not silently assigned units.
* Fitted parameters are not incorrectly declared universal constants.

⸻

25. Common Failure Modes

25.1 Adding Different Dimensions

Invalid:

[
X

1+\frac{K}{v^2}.
]

The right-hand side is invalid unless

[
\frac{K}{v^2}
]

has first been nondimensionalized.

Correct:

[
X

1+
\beta
\frac{K}{M_{\mathrm{ref}}v^2}.
]

⸻

25.2 Missing Reference Mass

Invalid for a dimensionless correction:

[
\delta

\beta\frac{K}{v^2}.
]

Because

[
K/v^2
]

has units of mass.

Correct:

[
\delta

\beta
\frac{K}{M_{\mathrm{ref}}v^2}.
]

⸻

25.3 Undefined Coupling Units

An equation such as

[
a

a_0+
\alpha\frac{K}{v^2}
]

cannot declare (\alpha) dimensionless unless

[
[a_0]=M.
]

The units of (\alpha) must follow from the observable.

⸻

26. Dimensional Consistency Does Not Establish Causality

The fact that

[
\frac{K}{v_{\mathrm{EOS}}^2}
]

has units of mass demonstrates dimensional consistency.

It does not demonstrate:

[
\text{kinetic energy}
\rightarrow
\text{additional gravitational mass}.
]

A physical derivation is still required to establish that relationship.

⸻

27. Dimensional Consistency Does Not Establish EOS Uniqueness

Both

[
\frac{K}{c^2}
]

and

[
\frac{K}{v_{\mathrm{EOS}}^2}
]

are dimensionally valid mass quantities.

Dimensional analysis cannot determine which velocity is physically appropriate.

That question requires:

1. theoretical derivation,
2. independent prediction,
3. experimental discrimination.

⸻

28. Required Audit Result

The EOS module receives a dimensional-consistency pass only if:

[
\boxed{
[\text{LHS}]

[\text{RHS}]
}
]

for every equation.

A dimensional pass means:

[
\text{Equation is dimensionally admissible}.
]

It does not mean:

[
\text{Equation is physically confirmed}.
]

⸻

29. Formal Status

The current EOS formulation satisfies the basic dimensional requirement:

[
\boxed{
\frac{K}{v_{\mathrm{EOS}}^2}
\rightarrow
\mathrm{kg}
}
]

provided (K) is an energy quantity and (v_{\mathrm{EOS}}) is a velocity.

The remaining scientific question is therefore not whether the normalization is dimensionally possible, but whether the resulting quantity has a justified physical role in SDKP.

⸻

30. Development Gate

Before an EOS correction is incorporated into a fundamental SDKP field equation, the following must be completed:

[
\boxed{
\text{Dimensional Audit}
\rightarrow
\text{Derivation}
\rightarrow
\text{Parameter Identification}
\rightarrow
\text{Independent Prediction}
\rightarrow
\text{Experimental Test}
\rightarrow
\text{Falsification Attempt}
}
]

No stage should be treated as evidence that automatically establishes the next stage.

⸻

Final Principle

[
\boxed{
\text{Dimensional consistency is necessary, but not sufficient, for physical validity.}
}
]

The EOS correction must therefore remain explicitly classified as an exploratory hypothesis until independent empirical evidence supports its physical interpretation.
