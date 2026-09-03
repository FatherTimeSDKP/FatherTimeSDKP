# SDKP EOS Derivation Specification

## 1. Objective

This specification defines the mathematical structure required to derive an
Earth-Orbital-Speed (EOS) kinetic correction within the SDKP framework.

The exploratory normalization is:

    K / v_EOS^2

with:

    v_EOS = 29,780 m/s

The purpose of this specification is not to assume that the correction is
physically valid, but to establish a precise route from the proposed
normalization to a falsifiable physical prediction.

---

## 2. Fundamental Quantities

Define:

    K = kinetic/energy-like quantity [J]

    v_EOS = Earth orbital reference velocity [m/s]

    c = speed of light [m/s]

    X_0 = baseline physical prediction

    X_SDKP = SDKP-corrected prediction

    α_EOS = EOS coupling coefficient

The normalized EOS quantity is:

    M_EOS = K / v_EOS^2

with dimensions:

    [M_EOS] = kg

---

## 3. Conventional Comparison

The conventional relativistic normalization is:

    M_c = K / c^2

The ratio is:

    A_EOS = M_EOS / M_c

Therefore:

    A_EOS = c^2 / v_EOS^2

or:

    A_EOS = (c/v_EOS)^2

Using:

    c = 299,792,458 m/s

    v_EOS = 29,780 m/s

gives:

    A_EOS ≈ 1.013 × 10^8

Thus:

    M_EOS ≈ 1.013 × 10^8 M_c

for the same K.

---

## 4. General Correction Equation

The most general first-order phenomenological implementation is:

    X_SDKP = X_0 + α_EOS M_EOS

Substituting M_EOS:

    X_SDKP = X_0 + α_EOS K/v_EOS^2

This equation is intentionally written with an explicit coupling coefficient.

The term:

    K/v_EOS^2

by itself is not an observable.

It is an energy-to-mass normalization.

The coupling α_EOS determines whether and how that quantity affects the
observable X.

---

## 5. Dimensionless Form

For comparisons across systems, a dimensionless correction may be preferable.

Define:

    δ_X = (X_SDKP - X_0) / X_0

Then a general first-order model can be written:

    δ_X = β_EOS (K / (M_ref v_EOS^2))

where:

    M_ref = reference mass [kg]

    β_EOS = dimensionless coupling coefficient

This form makes the correction explicitly dimensionless.

---

## 6. Alternative Energy-Density Form

If the SDKP framework requires a local rather than global correction, define
a characteristic volume:

    V

and energy density:

    u_K = K/V

Then:

    u_K/v_EOS^2

has dimensions:

    kg/m^3

and therefore behaves as an effective kinetic density:

    ρ_K = K/(V v_EOS^2)

This form can be compared directly with a density-based SDKP formulation.

---

## 7. Density-Coupled Form

If the correction is intended to interact with a background density ρ, define:

    ρ_eff = ρ + λ_EOS ρ_K

where:

    ρ_K = K/(V v_EOS^2)

and:

    λ_EOS

is a dimensionless coupling.

The resulting density gradient becomes:

    ∇ρ_eff
        = ∇ρ + λ_EOS ∇ρ_K

This provides a possible bridge between the EOS kinetic hypothesis and an
SDKP density-gradient formulation.

This equation is a candidate structure only and must be derived or justified
from the underlying SDKP theory before being treated as a physical law.

---

## 8. Spatially Varying K

If K varies through space:

    K = K(x,y,z)

then:

    ρ_K(x,y,z)
        = K(x,y,z)/(V(x,y,z) v_EOS^2)

and:

    ∇ρ_K

can contribute to the total SDKP density gradient.

A computational implementation must therefore distinguish between:

    constant K

and:

    spatially varying K.

---

## 9. Time-Dependent Form

If K varies with time:

    K = K(t)

then:

    M_EOS(t) = K(t)/v_EOS^2

and:

    dM_EOS/dt = (1/v_EOS^2) dK/dt

If the observable depends on the correction dynamically:

    X_SDKP(t)
        = X_0(t) + α_EOS K(t)/v_EOS^2

The model can therefore be tested against time-dependent measurements.

---

## 10. Reference Velocity Generalization

To test whether v_EOS is physically privileged, define:

    v_ref

and:

    M_ref = K/v_ref^2

The EOS model becomes:

    X(v_ref)
        = X_0 + α K/v_ref^2

The predicted scaling is:

    M_ref ∝ 1/v_ref^2

Therefore, if two otherwise equivalent systems have characteristic
velocities v_1 and v_2:

    M_1/M_2 = (v_2/v_1)^2

This provides a direct scaling test.

---

## 11. Earth-Orbit Specific Model

For an Earth-specific implementation:

    v_ref = v_EOS

with:

    v_EOS = 29,780 m/s

Therefore:

    X_Earth
        = X_0 + α_EOS K/(29,780)^2

The numerical denominator is:

    v_EOS^2 = 886,848,400 m^2/s^2

Therefore:

    X_Earth
        = X_0 + α_EOS K/886,848,400

with α_EOS carrying the units required by X.

---

## 12. Example

For:

    K = 10^12 J

the normalized EOS quantity is:

    M_EOS
        = 10^12/(29,780)^2

approximately:

    M_EOS ≈ 1.1278 × 10^3 kg

Therefore:

    X_SDKP
        = X_0 + α_EOS(1.1278 × 10^3 kg)

The physical magnitude of the correction cannot be determined until
α_EOS and X are explicitly defined.

---

## 13. Parameter Identification

The following parameters must not be conflated:

    v_EOS
    K
    α_EOS
    X_0

v_EOS is the proposed characteristic velocity.

K is the energy-like input.

α_EOS is the physical coupling.

X_0 is the baseline prediction.

Changing K is not equivalent to changing α_EOS.

Changing v_EOS is not equivalent to changing α_EOS.

This separation is necessary for parameter identifiability.

---

## 14. Calibration and Validation

If α_EOS cannot be derived analytically, it may be estimated using a
calibration dataset.

The procedure must be:

    Dataset A → estimate α_EOS

followed by:

    Dataset B → test prediction

Dataset B must remain independent of the calibration process.

A model that uses the same data for parameter fitting and validation cannot
provide a strong out-of-sample test.

---

## 15. Sensitivity

For:

    M_EOS = K/v_EOS^2

the sensitivity to K is:

    ∂M_EOS/∂K = 1/v_EOS^2

The sensitivity to v_EOS is:

    ∂M_EOS/∂v_EOS
        = -2K/v_EOS^3

Therefore small changes in the reference velocity produce a fractional
change:

    δM_EOS/M_EOS ≈ δK/K - 2δv_EOS/v_EOS

This relation should be included in uncertainty propagation.

---

## 16. Uncertainty Propagation

For independent uncertainties in K and v_EOS:

    (σ_M/M)^2
        ≈ (σ_K/K)^2
        + (2σ_v/v_EOS)^2

where:

    σ_M = uncertainty in M_EOS

    σ_K = uncertainty in K

    σ_v = uncertainty in v_EOS

Additional covariance terms must be included if K and v_EOS are correlated.

---

## 17. Falsification Boundary

The EOS correction becomes experimentally meaningful only when its predicted
effect exceeds the uncertainty of the measurement:

    |X_SDKP - X_0| > σ_X

A stronger test requires:

    |X_SDKP - X_0| >> σ_X

while accounting for systematic uncertainty.

If the predicted correction is not detectable, the experiment may still
provide an upper bound on α_EOS.

---

## 18. Required Derivation

The next theoretical step is to derive α_EOS rather than arbitrarily
selecting it.

A successful derivation must establish:

    α_EOS = f(S, ρ, K, geometry, reference frame, ...)
    
where the exact functional dependence follows from the underlying SDKP
principles.

The derivation must preserve dimensional consistency.

---

## 19. Required Computational Test

An implementation should calculate:

    1. Baseline prediction X_0
    2. Kinetic quantity K
    3. EOS-normalized quantity K/v_EOS^2
    4. Coupled correction α_EOS K/v_EOS^2
    5. SDKP prediction X_SDKP
    6. Observed value X_obs
    7. Baseline residual
    8. SDKP residual
    9. Uncertainty
    10. Statistical comparison

The implementation must report all intermediate quantities.

---

## 20. Scientific Status

The equations in this document define a candidate phenomenological framework.

They do not establish a new physical law.

The following statement is therefore required:

    K/v_EOS^2 is an exploratory EOS normalization. A physical SDKP effect
    exists only if a theoretically justified coupling converts this
    normalization into an independently measurable observable and the
    resulting prediction survives controlled experimental testing.

---

## 21. Development Gate

The EOS correction should advance to physical testing only after the following
conditions are satisfied:

    [ ] K is uniquely defined.
    [ ] v_EOS reference frame is explicitly defined.
    [ ] α_EOS is derived or independently calibrated.
    [ ] All equations pass dimensional analysis.
    [ ] A baseline model is specified.
    [ ] A measurable observable X is specified.
    [ ] A quantitative prediction is generated before validation.
    [ ] Independent validation data are available.
    [ ] Statistical criteria are defined.
    [ ] Falsification criteria are defined.

Until these conditions are met, the EOS correction remains an exploratory
SDKP hypothesis rather than an experimentally established effect.
