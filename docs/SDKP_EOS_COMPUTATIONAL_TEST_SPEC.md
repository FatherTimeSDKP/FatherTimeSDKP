# SDKP EOS Computational Test Specification

**Framework:** Scale-Density-Kinetic Principle (SDKP)  
**Module:** Earth-Orbital-Speed (EOS) Kinetic Correction  
**Status:** Exploratory computational specification  
**Version:** 1.0  
**Author:** Donald Paul Smith  

---

## 1. Purpose

This specification defines a computational testing protocol for the exploratory SDKP Earth-Orbital-Speed (EOS) kinetic correction.

The purpose is to determine whether an EOS-normalized kinetic term produces a measurable improvement over a conventional baseline model.

The computational test must distinguish between:

1. mathematical consequences of changing the normalization velocity,
2. fitted phenomenological corrections, and
3. genuinely predictive physical effects.

A numerical fit alone must **not** be interpreted as validation of SDKP.

---

## 2. Reference Velocities

The test compares two velocity scales.

### 2.1 Speed of light

\[
c = 299\,792\,458\ \mathrm{m/s}
\]

### 2.2 Earth orbital speed

\[
v_{\mathrm{EOS}} = 29\,780\ \mathrm{m/s}
\]

The corresponding squared velocities are

\[
c^2 = 8.987551787\times10^{16}\ \mathrm{m^2/s^2}
\]

and

\[
v_{\mathrm{EOS}}^2
=
8.868484\times10^8\ \mathrm{m^2/s^2}.
\]

---

## 3. Competing Models

Let

\[
X_0
\]

represent the baseline prediction for an observable \(X\).

The conventional kinetic normalization is

\[
M_c = \frac{K}{c^2}.
\]

The exploratory EOS normalization is

\[
M_{\mathrm{EOS}}
=
\frac{K}{v_{\mathrm{EOS}}^2}.
\]

An EOS-corrected observable may therefore be written phenomenologically as

\[
X_{\mathrm{EOS}}
=
X_0
+
\alpha_{\mathrm{EOS}}
\frac{K}{v_{\mathrm{EOS}}^2}.
\]

Here:

- \(X_0\) = baseline prediction,
- \(K\) = kinetic-energy-like quantity,
- \(v_{\mathrm{EOS}}\) = reference velocity,
- \(\alpha_{\mathrm{EOS}}\) = coupling coefficient,
- \(X_{\mathrm{EOS}}\) = corrected prediction.

The coefficient \(\alpha_{\mathrm{EOS}}\) must have units appropriate to the observable.

---

# 4. Dimensionless Alternative

For observables where an additive dimensional correction is inappropriate, define

\[
\delta_X
=
\beta_{\mathrm{EOS}}
\frac{K}{M_{\mathrm{ref}}v_{\mathrm{EOS}}^2}.
\]

The prediction becomes

\[
X_{\mathrm{EOS}}
=
X_0(1+\delta_X).
\]

Here:

- \(M_{\mathrm{ref}}\) = independently defined reference mass,
- \(\beta_{\mathrm{EOS}}\) = dimensionless coupling,
- \(\delta_X\) = fractional correction.

This form is preferred when \(X\) is dimensionless or represents a relative deviation.

---

# 5. Required Computational Comparisons

Every test must evaluate at least four cases.

### Test A — Baseline

\[
X_A = X_0
\]

### Test B — Conventional \(c\)-normalization

\[
X_B
=
X_0
+
\alpha_c\frac{K}{c^2}
\]

### Test C — EOS normalization

\[
X_C
=
X_0
+
\alpha_{\mathrm{EOS}}
\frac{K}{v_{\mathrm{EOS}}^2}
\]

### Test D — Reference-velocity sweep

Generalize the model to

\[
X(v_{\mathrm{ref}})
=
X_0
+
\alpha
\frac{K}{v_{\mathrm{ref}}^2}.
\]

Evaluate the prediction over a range of physically motivated reference velocities.

---

# 6. Synthetic Test Dataset

Before using real experimental observations, the implementation must be tested against synthetic data.

Generate a synthetic observable:

\[
X_i^{\mathrm{synthetic}}
=
X_{\mathrm{true}}(K_i)
+
\epsilon_i
\]

where

\[
\epsilon_i
\sim
\mathcal{N}(0,\sigma_i^2).
\]

The synthetic dataset must be generated independently of the model-fitting routine.

This prevents implementation errors from being mistaken for physical agreement.

---

# 7. Residual Definition

For each observation \(i\), define

\[
r_i
=
X_i^{\mathrm{obs}}
-
X_i^{\mathrm{model}}.
\]

The normalized residual is

\[
z_i
=
\frac{r_i}{\sigma_i}.
\]

A good implementation must report both raw and normalized residuals.

---

# 8. Chi-Squared Statistic

For observations with known uncertainties,

\[
\chi^2
=
\sum_{i=1}^{N}
\left(
\frac{X_i^{\mathrm{obs}}-X_i^{\mathrm{model}}}
{\sigma_i}
\right)^2.
\]

The reduced chi-squared statistic is

\[
\chi_\nu^2
=
\frac{\chi^2}{N-p},
\]

where

- \(N\) = number of observations,
- \(p\) = number of independently fitted parameters.

A lower \(\chi_\nu^2\) does not automatically establish that a model is physically correct.

---

# 9. Mean Absolute Error

Calculate

\[
\mathrm{MAE}
=
\frac{1}{N}
\sum_{i=1}^{N}
|r_i|.
\]

---

# 10. Root Mean Square Error

Calculate

\[
\mathrm{RMSE}
=
\sqrt{
\frac{1}{N}
\sum_{i=1}^{N}
r_i^2
}.
\]

Both MAE and RMSE must be reported.

---

# 11. Relative Improvement

For a baseline error metric \(E_0\) and corrected metric \(E_1\),

\[
I
=
1-
\frac{E_1}{E_0}.
\]

The percentage improvement is

\[
I_{\%}
=
100
\left(
1-
\frac{E_1}{E_0}
\right).
\]

An improvement must be evaluated on data that were **not used to fit the coupling coefficient**.

---

# 12. Train/Test Separation

If a coupling coefficient is fitted,

\[
\alpha_{\mathrm{EOS}}
=
\operatorname{fit}(D_{\mathrm{train}}),
\]

then the final performance must be evaluated independently:

\[
E_{\mathrm{test}}
=
E
\left(
D_{\mathrm{test}},
\alpha_{\mathrm{EOS}}
\right).
\]

The same observations must not be used both to determine the parameter and to claim predictive accuracy.

---

# 13. Reference-Velocity Sweep

The EOS assumption must be explicitly tested.

Define

\[
v_{\mathrm{ref}}
\in
[v_{\min},v_{\max}].
\]

For each reference velocity calculate

\[
X(v_{\mathrm{ref}})
=
X_0
+
\alpha
\frac{K}{v_{\mathrm{ref}}^2}.
\]

The computational experiment must determine whether

\[
v_{\mathrm{EOS}}
=
29\,780\ \mathrm{m/s}
\]

provides a uniquely superior prediction.

If a broad range of velocities produces equivalent performance after refitting \(\alpha\), then the EOS velocity is not uniquely identified by the data.

---

# 14. Fixed-Coupling Test

The strongest version of the reference-velocity experiment keeps the coupling coefficient fixed.

For each velocity,

\[
X(v)
=
X_0
+
\alpha_{\mathrm{fixed}}
\frac{K}{v^2}.
\]

Do **not** refit \(\alpha\) for every \(v\).

This test determines whether the velocity scale itself carries predictive information.

---

# 15. Free-Coupling Test

A secondary experiment may allow

\[
\alpha=\alpha(v).
\]

This tests model flexibility but is weaker evidence.

If every reference velocity can obtain a similar fit by changing \(\alpha\), then the model has demonstrated parameter degeneracy rather than identification of \(v_{\mathrm{EOS}}\).

---

# 16. Amplification Factor

The ratio between EOS and relativistic normalization is

\[
A_{\mathrm{EOS}}
=
\frac{K/v_{\mathrm{EOS}}^2}
{K/c^2}.
\]

Therefore,

\[
A_{\mathrm{EOS}}
=
\left(
\frac{c}{v_{\mathrm{EOS}}}
\right)^2.
\]

Using the defined constants,

\[
A_{\mathrm{EOS}}
\approx
1.013\times10^8.
\]

Thus,

\[
\frac{K}{v_{\mathrm{EOS}}^2}
\]

is approximately \(10^8\) times larger than

\[
\frac{K}{c^2}.
\]

This is a mathematical consequence of the selected normalization and is **not evidence of a physical effect by itself**.

---

# 17. Example Computational Case

Let

\[
K=10^{12}\ \mathrm{J}.
\]

Then

\[
\frac{K}{c^2}
\approx
1.11265\times10^{-5}\ \mathrm{kg}.
\]

The EOS normalization gives

\[
\frac{K}{v_{\mathrm{EOS}}^2}
\approx
1.1278\times10^3\ \mathrm{kg}.
\]

Therefore,

\[
A_{\mathrm{EOS}}
\approx
1.013\times10^8.
\]

The model must not interpret the resulting \(1127.8\ \mathrm{kg}\) quantity as an experimentally established mass.

It is an EOS-normalized kinetic quantity unless an independent physical derivation establishes otherwise.

---

# 18. Sensitivity Analysis

The EOS term is

\[
M_{\mathrm{EOS}}
=
\frac{K}{v_{\mathrm{EOS}}^2}.
\]

Its differential sensitivity is

\[
\frac{\partial M_{\mathrm{EOS}}}{\partial K}
=
\frac{1}{v_{\mathrm{EOS}}^2}
\]

and

\[
\frac{\partial M_{\mathrm{EOS}}}
{\partial v_{\mathrm{EOS}}}
=
-\frac{2K}{v_{\mathrm{EOS}}^3}.
\]

The logarithmic sensitivity to velocity is

\[
\frac{\partial\ln M_{\mathrm{EOS}}}
{\partial\ln v_{\mathrm{EOS}}}
=
-2.
\]

Therefore a fractional change in reference velocity produces approximately twice that fractional change, with opposite sign, in the normalized quantity.

---

# 19. Uncertainty Propagation

For independent uncertainties in \(K\) and \(v_{\mathrm{EOS}}\),

\[
\sigma_M^2
=
\left(
\frac{\partial M}{\partial K}
\sigma_K
\right)^2
+
\left(
\frac{\partial M}{\partial v}
\sigma_v
\right)^2.
\]

Therefore,

\[
\sigma_M^2
=
\left(
\frac{\sigma_K}{v_{\mathrm{EOS}}^2}
\right)^2
+
\left(
\frac{2K\sigma_v}{v_{\mathrm{EOS}}^3}
\right)^2.
\]

The implementation must propagate uncertainty rather than reporting excessive numerical precision.

---

# 20. Monte Carlo Validation

A Monte Carlo implementation should independently sample uncertain parameters.

For each trial \(j\),

\[
K_j
\sim
P(K)
\]

and

\[
v_j
\sim
P(v).
\]

Then calculate

\[
M_j
=
\frac{K_j}{v_j^2}.
\]

After \(N_{\mathrm{MC}}\) trials, report:

- median,
- standard deviation,
- 16th percentile,
- 84th percentile,
- 2.5th percentile,
- 97.5th percentile.

The Monte Carlo result must not be confused with experimental validation.

---

# 21. Null Model

A proper test requires a null hypothesis.

### Null hypothesis

\[
H_0:
\alpha_{\mathrm{EOS}}=0.
\]

Under \(H_0\),

\[
X=X_0.
\]

### Alternative hypothesis

\[
H_1:
\alpha_{\mathrm{EOS}}\neq0.
\]

The statistical test must determine whether the observed improvement is sufficiently large to reject \(H_0\).

---

# 22. Parameter Identifiability

The EOS correction cannot be considered independently validated if

\[
\alpha_{\mathrm{EOS}}
\]

is completely degenerate with another model parameter.

For example,

\[
X
=
X_0
+
\alpha_{\mathrm{EOS}}
\frac{K}{v_{\mathrm{EOS}}^2}
\]

may be mathematically equivalent to

\[
X
=
X_0+\gamma K
\]

where

\[
\gamma
=
\frac{\alpha_{\mathrm{EOS}}}
{v_{\mathrm{EOS}}^2}.
\]

If only \(K\) varies while \(v_{\mathrm{EOS}}\) remains fixed, the data may be unable to distinguish these formulations.

Therefore the test must include observations spanning multiple relevant physical scales.

---

# 23. Out-of-Sample Prediction

A successful model must predict observations not used during calibration.

Required workflow:

```text
Raw observations
       |
       v
Independent train/test split
       |
       +----------------+
       |                |
       v                v
Baseline fit       SDKP-EOS fit
       |                |
       +-------+--------+
               |
               v
        Independent test
               |
               v
        Error comparison
               |
               v
       Statistical analysis
