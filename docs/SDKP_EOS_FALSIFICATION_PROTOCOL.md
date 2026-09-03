# SDKP EOS Falsification Protocol

## 1. Purpose

This protocol defines a reproducible procedure for testing the exploratory
SDKP Earth-Orbital-Speed (EOS) kinetic correction.

The hypothesis under investigation is that an observable may contain a
correction proportional to:

    K / v_EOS^2

where:

    K     = explicitly defined kinetic/energy quantity
    v_EOS = 29,780 m/s

The protocol is designed to determine whether this term produces predictive
power beyond an established baseline model.

---

## 2. Competing Models

### Model A — Baseline

The baseline model is:

    X_A = X_0

where X_0 represents the prediction of the accepted physical model.

The baseline must be specified before testing.

---

### Model B — EOS Correction

The exploratory SDKP model is:

    X_B = X_0 + α_EOS (K / v_EOS^2)

where:

    α_EOS = independently specified coupling coefficient

The coefficient must not be freely adjusted to each individual observation.

---

## 3. Null Hypothesis

The null hypothesis is:

    H0: α_EOS = 0

Under H0:

    X_B = X_0

The alternative hypothesis is:

    H1: α_EOS ≠ 0

A statistically significant result requires rejection of H0 according to a
predefined statistical criterion.

---

## 4. Required Independent Variables

Every test must record:

    K
    v_EOS
    X_observed
    X_baseline
    uncertainty_X

If applicable, the dataset should additionally contain:

    distance
    mass
    velocity
    orbital radius
    orbital period
    density
    temperature
    measurement time
    reference frame

The exact variables depend on the physical experiment.

---

## 5. Prediction Procedure

Before examining the experimental outcome:

1. Define K.
2. Define v_EOS.
3. Define α_EOS.
4. Calculate X_B.
5. Record the prediction.
6. Only then compare with X_observed.

The prediction must not be changed after examining the result.

---

## 6. Residual Analysis

For the baseline:

    R_A = X_observed - X_A

For the EOS model:

    R_B = X_observed - X_B

Compare:

    |R_A|

against:

    |R_B|

and, when uncertainties are available, compare normalized residuals:

    z_A = R_A / σ_X

    z_B = R_B / σ_X

A successful correction should systematically reduce unexplained residuals
without introducing new systematic errors.

---

## 7. Statistical Comparison

For a dataset containing N independent observations, calculate:

    χ²_A = Σ [(X_i,observed - X_i,A)^2 / σ_i^2]

and:

    χ²_B = Σ [(X_i,observed - X_i,B)^2 / σ_i^2]

The difference is:

    Δχ² = χ²_A - χ²_B

A positive Δχ² indicates that the EOS model has a smaller chi-squared value,
but statistical significance must account for the number of fitted
parameters and the complexity of each model.

Appropriate information criteria may include:

    AIC
    BIC

where appropriate.

---

## 8. Prediction vs. Fitting

A critical requirement is separation between:

    calibration data

and:

    validation data

If α_EOS is estimated from calibration data, the resulting model must be
tested against independent validation data.

The validation dataset must not be used to determine α_EOS.

This prevents overfitting.

---

## 9. Scaling Test

The EOS hypothesis predicts a specific dependence on K.

If:

    ΔX = α_EOS K/v_EOS^2

then, for fixed v_EOS:

    ΔX ∝ K

Therefore, experiments should test whether the measured correction scales
linearly with K.

For two measurements:

    ΔX_1 / ΔX_2 = K_1 / K_2

provided all other relevant variables remain controlled.

Deviation from this predicted scaling is evidence against the simple linear
EOS correction.

---

## 10. Velocity-Scale Test

The hypothesis must also determine whether v_EOS is genuinely physical.

Replace the reference velocity with a general velocity:

    v_ref

and define:

    ΔX(v_ref) = α K/v_ref^2

Then:

    ΔX(v_1) / ΔX(v_2) = (v_2/v_1)^2

if all other quantities remain constant.

A failure of this predicted inverse-square velocity dependence would falsify
this particular formulation.

---

## 11. Reference-Frame Requirement

Earth's orbital velocity is approximately:

    v_EOS = 29,780 m/s

This is a heliocentric orbital speed rather than a universal invariant such
as c.

Therefore, the theory must explicitly define the reference frame in which
v_EOS is evaluated.

The model must answer:

    Why is Earth's heliocentric orbital velocity the relevant velocity scale?

If another reference frame produces a different value, the theory must
specify which value is physically relevant and why.

---

## 12. Dimensional Check

Because:

    [K] = kg m^2/s^2

and:

    [v_EOS^2] = m^2/s^2

then:

    [K/v_EOS^2] = kg

Therefore:

    α_EOS

must provide whatever additional units are required by X.

Every proposed implementation must pass dimensional analysis before
numerical testing.

---

## 13. Sign Test

The theory must specify the sign of α_EOS.

If:

    α_EOS > 0

the correction increases X relative to X_0.

If:

    α_EOS < 0

the correction decreases X relative to X_0.

The sign must be predicted independently of the observed result.

A model whose sign is selected after seeing the data does not constitute a
strong predictive test.

---

## 14. Magnitude Test

For:

    K = 10^12 J

the normalization gives:

    K/v_EOS^2 ≈ 1.1278 × 10^3 kg

while:

    K/c^2 ≈ 1.11265 × 10^-5 kg

with:

    (K/v_EOS^2)/(K/c^2)
        ≈ 1.013 × 10^8

This large numerical difference makes the hypothesis potentially easy to
distinguish experimentally if the normalized quantity is coupled to an
observable at measurable strength.

However, the magnitude of K/v_EOS^2 alone does not establish that the
corresponding physical effect exists.

---

## 15. Strong Test

The strongest test is one in which:

1. The baseline model makes a known prediction.
2. The SDKP EOS model makes a different prediction.
3. The difference exceeds experimental uncertainty.
4. All SDKP parameters are specified before measurement.
5. The measurement is independent.
6. The result can potentially falsify the EOS model.

The ideal experiment therefore satisfies:

    |X_SDKP - X_baseline| >> σ_X

while maintaining adequate control of systematic uncertainties.

---

## 16. Negative Result

A null result is scientifically useful.

If:

    X_observed ≈ X_baseline

and the predicted EOS correction is sufficiently large that it should have
been detected, then the proposed EOS coupling is constrained or falsified.

The model should report the experimental upper bound on α_EOS rather than
simply declaring the experiment unsuccessful.

---

## 17. Reproducibility

Every published test should include:

    - exact equations
    - constants
    - units
    - parameter values
    - raw or appropriately archived data
    - preprocessing procedure
    - uncertainty model
    - statistical method
    - predicted values
    - observed values
    - residuals
    - baseline comparison
    - code used for analysis

A second researcher should be able to reproduce the result from the archived
materials.

---

## 18. Minimum Acceptance Criterion

The EOS correction should not be considered experimentally supported merely
because it fits an existing dataset.

A stronger minimum criterion is:

    independent prediction
    +
    independent measurement
    +
    statistically significant improvement
    +
    reproducibility

The model must also survive tests designed specifically to distinguish it
from the baseline model.

---

## 19. Falsification Statement

The following statement defines the intended scientific status:

    The SDKP EOS correction is a falsifiable exploratory hypothesis.
    Its validity depends on whether an independently specified correction
    proportional to K/v_EOS^2 produces reproducible predictions that are
    distinguishable from established baseline physics.

The numerical amplification factor:

    A_EOS ≈ 1.013 × 10^8

is a mathematical consequence of the chosen velocity normalization and is
not itself evidence of physical validity.

---

## 20. Status

STATUS:

    EXPLORATORY
    FALSIFIABLE IN PRINCIPLE
    NOT YET EMPIRICALLY VALIDATED

Next required development:

    Derive α_EOS from the underlying SDKP framework and identify a specific
    observable for which the EOS correction produces a quantitative,
    independently testable prediction.
