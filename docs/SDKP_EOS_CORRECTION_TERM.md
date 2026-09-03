# SDKP EOS Correction Term

## 1. Purpose

This document defines a candidate Scale-Density-Kinetic Principle (SDKP)
correction based on Earth's orbital velocity:

    v_EOS = 29,780 m/s

The purpose is to distinguish a mathematical normalization from a physical
correction law.

The exploratory quantity is:

    K / v_EOS^2

where K is an energy-like kinetic quantity.

This document does not assume that the term is physically valid. Its purpose
is to establish the requirements necessary for deriving, testing, and
potentially falsifying an EOS-normalized SDKP correction.

---

## 2. Baseline Normalization

The conventional mass-equivalent normalization of an energy K is:

    Δm_c = K / c^2

where:

    c = 299,792,458 m/s

The proposed exploratory normalization is:

    Δm_EOS = K / v_EOS^2

with:

    v_EOS = 29,780 m/s

The ratio is:

    Δm_EOS / Δm_c
        = c^2 / v_EOS^2

Therefore:

    A_EOS = (c / v_EOS)^2

and numerically:

    A_EOS ≈ 1.013 × 10^8

Thus the EOS-normalized quantity is approximately 101 million times larger
than the conventional c^2-normalized quantity for the same K.

---

## 3. Candidate SDKP Correction

A general phenomenological correction can be written as:

    X_SDKP = X_0 + α_EOS (K / v_EOS^2)

where:

    X_0      = baseline prediction
    K        = defined kinetic/energy quantity
    v_EOS    = Earth's orbital reference velocity
    α_EOS    = coupling coefficient
    X_SDKP   = corrected observable

The coefficient α_EOS must be defined such that the equation is dimensionally
consistent.

No numerical value for α_EOS should be assumed without a physical derivation
or independent calibration.

---

## 4. Dimensional Requirement

Because:

    [K] = J = kg·m^2/s^2

and:

    [v_EOS^2] = m^2/s^2

then:

    [K/v_EOS^2] = kg

Therefore:

    K/v_EOS^2

has dimensions of mass.

Consequently, α_EOS must have units appropriate to convert this mass into
the observable X.

For example, if X is an acceleration:

    [α_EOS] = m/s^2/kg

If X is a force:

    [α_EOS] = m/s^2

If X is a dimensionless fractional correction:

    α_EOS

must carry inverse-mass units.

This dimensional requirement prevents the EOS term from being inserted into
an equation where its units are incompatible with the quantity being
corrected.

---

## 5. Example

Let:

    K = 10^12 J

Then:

    K/v_EOS^2
        = 10^12 / (29,780)^2

approximately:

    K/v_EOS^2 ≈ 1.1278 × 10^3 kg

or approximately:

    1,127.8 kg

For comparison:

    K/c^2 ≈ 1.11265 × 10^-5 kg

The ratio is approximately:

    1.013 × 10^8

---

## 6. Physical Meaning Must Be Derived

The existence of the numerical factor does not demonstrate that Earth's
orbital velocity is a fundamental physical scale.

A physical theory must explain why:

    v_EOS = 29,780 m/s

appears in the governing equation.

Possible hypotheses must be treated separately and tested independently.

Examples include:

1. v_EOS represents an environmental kinetic reference scale.

2. v_EOS represents a characteristic velocity of Earth's gravitational
   system.

3. v_EOS represents an emergent scale arising from the geometry of the
   solar system.

4. v_EOS is only a convenient normalization and has no fundamental status.

The model must determine which interpretation is correct.

---

## 7. Reference-Velocity Test

A critical falsification test is to replace Earth's orbital velocity with
another characteristic orbital velocity:

    v_ref

and evaluate:

    K/v_ref^2

If the physical correction is claimed to be universal, the theory must
define how v_ref is selected.

For two systems:

    ΔX_1 = α K_1/v_1^2

    ΔX_2 = α K_2/v_2^2

the model predicts a systematic dependence on the characteristic velocity.

This dependence can be compared against observations.

---

## 8. Experimental Test Structure

A useful experiment should compare three quantities:

    X_observed

    X_baseline

    X_SDKP

The residual of the baseline model is:

    R_0 = X_observed - X_baseline

The residual after the EOS correction is:

    R_SDKP = X_observed - X_SDKP

The hypothesis gains support only if the EOS correction produces a
statistically significant improvement while remaining predictive on
independent data.

A model that is fitted directly to the same observations it is evaluated
against does not provide a strong falsification test.

---

## 9. Required Prediction

Before testing data, the model should specify:

    K
    v_EOS
    α_EOS
    X_0
    X_SDKP

and calculate:

    X_SDKP(predicted)

The measured result must then be compared against this prediction.

The prediction should be generated without adjusting α_EOS after seeing
the experimental result.

---

## 10. Falsification Conditions

The EOS correction should be considered falsified if independent experiments
show that:

1. The predicted correction is absent when it should be measurable.

2. The correction has the wrong magnitude.

3. The correction has the wrong sign.

4. The correction does not scale with K as predicted.

5. The predicted dependence on v_ref is absent or inconsistent with the
   model.

6. A standard baseline model explains the observations significantly better
   without the EOS correction.

---

## 11. Important Distinction

The statement:

    K/v_EOS^2 > K/c^2

is mathematically true for positive K because:

    v_EOS << c

However:

    mathematical amplification ≠ physical validation

The physical question is not whether the EOS normalization produces a larger
number.

The physical question is whether that larger term corresponds to a measurable
effect in nature.

---

## 12. Minimal Testable Form

The minimal phenomenological model is:

    X_SDKP = X_0 + α_EOS K/v_EOS^2

with:

    v_EOS = 29,780 m/s


Status:

    EXPLORATORY / TESTABLE HYPOTHESIS

The EOS normalization is mathematically defined.


