docs/SDKP_EOS_REFERENCE_VELOCITY_IDENTIFICATION.md

# SDKP EOS Reference-Velocity Identification Protocol
**Framework:** Scale-Density-Kinetic Principle (SDKP)  
**Module:** Earth-Orbital-Speed (EOS) Reference-Velocity Identification  
**Status:** Exploratory / falsifiable test specification  
**Version:** 1.0  
**Author:** Donald Paul Smith  
---
## 1. Purpose
This protocol tests whether the Earth orbital speed
\[
v_{\mathrm{EOS}} = 29\,780\ \mathrm{m/s}
\]
has predictive significance within the SDKP EOS correction.
The central question is:
> Does the data independently select \(29\,780\ \mathrm{m/s}\), or can an equivalent fit be obtained using arbitrary reference velocities?
This distinction is essential.
A model that can obtain the same performance for any reference velocity has not demonstrated that EOS is physically special.
---
## 2. Core Hypothesis
The exploratory EOS correction is
\[
\Delta X(v)
=
\alpha
\frac{K}{v^2}.
\]
The SDKP EOS hypothesis proposes that
\[
v=v_{\mathrm{EOS}}
\]
with
\[
v_{\mathrm{EOS}}=29\,780\ \mathrm{m/s}.
\]
Therefore,
\[
\boxed{
\Delta X_{\mathrm{EOS}}
=
\alpha
\frac{K}{(29\,780)^2}
}
\]
must be compared against the same functional form evaluated at alternative velocities.
---
## 3. Null Hypothesis
The null hypothesis is:
\[
H_0:
\text{The data do not uniquely prefer }v_{\mathrm{EOS}}.
\]
The alternative hypothesis is:
\[
H_1:
\text{The data preferentially select }v_{\mathrm{EOS}}
\]
under a preregistered model and evaluation procedure.
---
## 4. Why This Test Is Necessary
Because
\[
\Delta X
=
\alpha\frac{K}{v^2},
\]
the coupling coefficient and reference velocity can become degenerate.
Define
\[
\gamma=\frac{\alpha}{v^2}.
\]
Then
\[
\Delta X=\gamma K.
\]
If \(v\) is fixed throughout an experiment, the data may only determine \(\gamma\), rather than separately determining \(\alpha\) and \(v\).
Therefore, simply fitting
\[
\alpha_{\mathrm{EOS}}
\]
at \(29\,780\ \mathrm{m/s}\) is insufficient to establish that \(29\,780\ \mathrm{m/s}\) is physically fundamental.
---
# 5. Identification Strategy
The protocol uses two complementary tests.
### Test 1 — Fixed Coupling
Hold
\[
\alpha=\alpha_0
\]
constant while varying \(v\).
Evaluate
\[
X(v)
=
X_0+
\alpha_0\frac{K}{v^2}.
\]
This directly tests the effect of the reference velocity.
### Test 2 — Free Coupling
For every candidate velocity \(v\), independently fit
\[
\alpha(v).
\]
Evaluate
\[
X(v)
=
X_0+
\alpha(v)\frac{K}{v^2}.
\]
This determines whether the velocity is identifiable after accounting for parameter flexibility.
---
# 6. Candidate Velocity Grid
A minimum candidate grid should include:
\[
v\in
\{
10\,000,\,
15\,000,\,
20\,000,\,
25\,000,\,
29\,780,\,
35\,000,\,
40\,000,\,
50\,000
\}
\ \mathrm{m/s}.
\]
A finer sweep should also be performed:
\[
v_i=v_{\min}+i\Delta v.
\]
For example,
\[
v_{\min}=10\,000\ \mathrm{m/s},
\]
\[
v_{\max}=50\,000\ \mathrm{m/s},
\]
and
\[
\Delta v=100\ \mathrm{m/s}.
\]
The EOS value must be included exactly rather than rounded to the nearest grid point.
---
# 7. Generalized Model
Define
\[
X_i(v,\alpha)
=
X_{0,i}
+
\alpha
\frac{K_i}{v^2}.
\]
For each candidate \(v\), calculate
\[
\chi^2(v,\alpha)
=
\sum_i
\frac{
[X_i^{\mathrm{obs}}
-
X_i(v,\alpha)]^2
}{
\sigma_i^2
}.
\]
The minimum at each velocity is
\[
\chi^2_{\min}(v)
=
\min_{\alpha}\chi^2(v,\alpha).
\]
The preferred velocity is
\[
v_{\mathrm{best}}
=
\operatorname*{arg\,min}_v
\chi^2_{\min}(v).
\]
---
# 8. EOS Preference Ratio
Define
\[
R_{\mathrm{EOS}}
=
\frac{
\chi^2_{\min}(v_{\mathrm{EOS}})
}{
\chi^2_{\min}(v_{\mathrm{best}})
}.
\]
Interpretation:
- \(R_{\mathrm{EOS}}\approx1\): EOS performs approximately as well as the best velocity.
- \(R_{\mathrm{EOS}}>1\): another velocity performs better.
- \(R_{\mathrm{EOS}}<1\): impossible if \(v_{\mathrm{best}}\) is correctly defined.
However, a small ratio difference alone does not establish statistical significance.
---
# 9. Velocity Profile
The computational experiment should produce the function
\[
\chi^2_{\min}(v).
\]
The resulting profile provides a direct visualization of whether the likelihood/error surface has a localized minimum.
A physically meaningful identification would require a minimum that is:
1. reproducible,
2. statistically distinguishable,
3. stable across datasets,
4. stable under reasonable model variations.
---
# 10. Confidence Interval
If a likelihood function is used,
\[
\mathcal{L}(v)
\propto
e^{-\chi^2_{\min}(v)/2}.
\]
The relative likelihood is
\[
\Lambda(v)
=
\exp
\left[
-\frac{
\chi^2_{\min}(v)-\chi^2_{\min}(v_{\mathrm{best}})
}{2}
\right].
\]
A confidence or credible interval may then be calculated using a preregistered statistical method.
The interval must be reported rather than only reporting
\[
v_{\mathrm{best}}.
\]
---
# 11. Distance From EOS
Define
\[
\Delta v
=
v_{\mathrm{best}}
-
v_{\mathrm{EOS}}.
\]
The fractional difference is
\[
\delta_v
=
\frac{
v_{\mathrm{best}}-v_{\mathrm{EOS}}
}{
v_{\mathrm{EOS}}
}.
\]
The percentage difference is
\[
\delta_{v,\%}
=
100\delta_v.
\]
If the best-fit velocity is substantially displaced from \(29\,780\ \mathrm{m/s}\), the EOS hypothesis must explain the discrepancy.
---
# 12. Independent Dataset Requirement
The velocity identification must be repeated on independent datasets:
\[
D_1,D_2,\ldots,D_n.
\]
For each dataset calculate
\[
v_{\mathrm{best},j}.
\]
Then examine
\[
\{v_{\mathrm{best},1},
v_{\mathrm{best},2},
\ldots,
v_{\mathrm{best},n}\}.
\]
A genuine reference scale should demonstrate stability rather than appearing in only one dataset.
---
# 13. Cross-Dataset Stability
Define
\[
\bar v
=
\frac{1}{N}
\sum_jv_{\mathrm{best},j}.
\]
Calculate the dispersion
\[
s_v
=
\sqrt{
\frac{1}{N-1}
\sum_j
(v_{\mathrm{best},j}-\bar v)^2
}.
\]
The stability of the inferred velocity should be compared with
\[
v_{\mathrm{EOS}}=29\,780\ \mathrm{m/s}.
\]
---
# 14. Leave-One-Dataset-Out Test
For \(N\) datasets, fit the model using all datasets except dataset \(j\).
This produces
\[
v_{\mathrm{best}}^{(-j)}.
\]
Repeat for every \(j\).
The inferred velocity must not depend critically on a single dataset.
---
# 15. Parameter Degeneracy Test
Consider
\[
\Delta X
=
\alpha
\frac{K}{v^2}.
\]
A transformation
\[
v\rightarrow\lambda v
\]
can be offset by
\[
\alpha\rightarrow\lambda^2\alpha.
\]
Therefore,
\[
\frac{\alpha'}{v'^2}
=
\frac{\lambda^2\alpha}
{\lambda^2v^2}
=
\frac{\alpha}{v^2}.
\]
This demonstrates an exact degeneracy in the simplest model.
Therefore:
\[
\boxed{
\text{EOS cannot be identified from }K
\text{ variation alone if }\alpha\text{ is completely free.}
}
\]
Additional independent physical structure is required.
---
# 16. Breaking the Degeneracy
Potential mechanisms for breaking the degeneracy include:
1. independently predicted \(\alpha\),
2. independently measured velocity dependence,
3. multiple physical observables,
4. datasets covering different orbital environments,
5. predictions where \(v_{\mathrm{EOS}}\) changes but the coupling does not,
6. a first-principles derivation connecting \(v_{\mathrm{EOS}}\) to SDKP geometry.
The strongest test is a prediction in which the reference velocity changes independently of the fitted parameters.
---
# 17. Reference-Velocity Generalization
The model should be generalized to
\[
v_{\mathrm{ref}}
=
f(S,\rho,K,\ldots)
\]
if SDKP theory predicts that the relevant velocity depends on system properties.
The corresponding correction becomes
\[
\Delta X
=
\alpha
\frac{K}
{v_{\mathrm{ref}}^2}.
\]
The Earth-orbital case is then
\[
v_{\mathrm{ref}}
=
v_{\mathrm{EOS}}
\]
only for systems where the theoretical conditions require it.
This prevents Earth-specific calibration from being mistaken for a universal constant.
---
# 18. Local Reference Velocity Test
If the hypothesis predicts a local orbital reference speed, define
\[
v_{\mathrm{orb}}
=
\sqrt{\frac{GM}{r}}
\]
for a Newtonian circular-orbit approximation.
Then compare
\[
\Delta X_{\mathrm{EOS}}
=
\alpha\frac{K}{v_{\mathrm{EOS}}^2}
\]
against
\[
\Delta X_{\mathrm{orb}}
=
\alpha\frac{K}{v_{\mathrm{orb}}^2}.
\]
This provides a direct test of whether SDKP requires the Earth's particular orbital velocity or a more general orbital-kinematic quantity.
---
# 19. Stronger Falsification Experiment
The preferred experiment is one in which systems have substantially different characteristic velocities.
For systems \(A\) and \(B\),
\[
v_A\neq v_B.
\]
The model predicts
\[
\frac{\Delta X_A}{\Delta X_B}
=
\frac{K_A}{K_B}
\left(
\frac{v_B}{v_A}
\right)^2
\]
if the coupling \(\alpha\) is universal.
This creates a directly testable scaling law.
---
# 20. Scaling Test
Hold the coupling fixed and test
\[
\Delta X
\propto
K v^{-2}.
\]
Taking logarithms,
\[
\ln|\Delta X|
=
\ln|\alpha|
+
\ln K
-
2\ln v.
\]
Therefore the predicted logarithmic slope with respect to velocity is
\[
\boxed{
\frac{\partial\ln|\Delta X|}
{\partial\ln v}
=
-2
}
\]
when \(K\) and \(\alpha\) are otherwise controlled.
This is a stronger prediction than merely inserting \(29\,780\ \mathrm{m/s}\) into an equation.
---
# 21. Computational Implementation
```python
import numpy as np
C = 299_792_458.0
V_EOS = 29_780.0
def prediction(K, alpha, velocity, baseline=0.0):
    K = np.asarray(K, dtype=float)
    return baseline + alpha * K / velocity**2
def chi_squared(observed, predicted, sigma):
    observed = np.asarray(observed, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    sigma = np.asarray(sigma, dtype=float)
    return np.sum(((observed - predicted) / sigma) ** 2)
def velocity_sweep(
    K,
    observed,
    sigma,
    alpha,
    velocities,
    baseline=0.0
):
    results = []
    for velocity in velocities:
        predicted = prediction(
            K,
            alpha,
            velocity,
            baseline
        )
        chi2 = chi_squared(
            observed,
            predicted,
            sigma
        )
        results.append({
            "velocity": float(velocity),
            "chi_squared": float(chi2)
        })
    return results
if __name__ == "__main__":
    K = np.array([
        1.0e9,
        2.0e9,
        3.0e9,
        5.0e9,
        1.0e10
    ])
    alpha = 1.0
    # Synthetic demonstration data.
    observed = prediction(
        K,
        alpha,
        V_EOS
    )
    sigma = np.full_like(
        observed,
        1.0e-3
    )
    velocities = np.linspace(
        10_000.0,
        50_000.0,
        401
    )
    results = velocity_sweep(
        K,
        observed,
        sigma,
        alpha,
        velocities
    )
    best = min(
        results,
        key=lambda x: x["chi_squared"]
    )
    print("Best reference velocity:")
    print(
        f"{best['velocity']:.2f} m/s"
    )
    print()
    print("EOS reference velocity:")
    print(
        f"{V_EOS:.2f} m/s"
    )

⸻

22. Important Synthetic-Data Warning

The demonstration above intentionally generates the synthetic observations using

[
v_{\mathrm{EOS}}=29,780\ \mathrm{m/s}.
]

Therefore recovery of approximately (29,780\ \mathrm{m/s}) in that demonstration is expected.

It is a software verification test.

It is not evidence that the EOS hypothesis is true.

For physical testing, the observations must be independently measured.

⸻

23. Required Real-Data Experiment

For an actual validation experiment:

Step 1

Define the observable before examining the validation data.

Step 2

Specify

[
K,\quad
X_0,\quad
\sigma_X,\quad
\alpha
]

and all relevant constants.

Step 3

Predefine the candidate velocity range.

Step 4

Calculate predictions.

Step 5

Lock the analysis procedure.

Step 6

Evaluate independent observations.

Step 7

Calculate

[
\chi^2(v).
]

Step 8

Determine

[
v_{\mathrm{best}}.
]

Step 9

Compare (v_{\mathrm{best}}) with

[
29,780\ \mathrm{m/s}.
]

Step 10

Attempt to falsify the hypothesis.

⸻

24. Required Result Table

The final experiment must report:

Quantity	Result
(v_{\mathrm{EOS}})	29,780 m/s
(v_{\mathrm{best}})	measured
(\Delta v)	measured
Fractional difference	measured
(\chi^2_{\mathrm{EOS}})	measured
(\chi^2_{\mathrm{best}})	measured
(R_{\mathrm{EOS}})	measured
Confidence interval	measured
Number of datasets	measured
Independent validation	yes/no

⸻

25. Decision Criteria

Strong EOS support

All of the following should occur:

[
v_{\mathrm{best}}
\approx
29,780\ \mathrm{m/s},
]

the EOS preference is statistically significant,

the result survives independent datasets,

the result survives parameter perturbations,

and alternative reference velocities perform materially worse.

Weak support

The EOS velocity performs well but is statistically indistinguishable from a broad range of alternatives.

No support

Another reference velocity performs significantly better.

Falsification

A preregistered prediction based on

[
v_{\mathrm{EOS}}=29,780\ \mathrm{m/s}
]

fails independently measured observations beyond the predefined uncertainty threshold.

⸻

26. Critical Interpretation Rule

The following statement is not sufficient:

“The EOS equation produces a good numerical fit.”

The required statement is substantially stronger:

[
\boxed{
\text{The EOS reference velocity produces a uniquely predictive,
out-of-sample, reproducible improvement over independently defined alternatives.}
}
]

Only that stronger result would justify treating (v_{\mathrm{EOS}}) as an empirically supported SDKP scale.

⸻

27. Development Gate

The EOS reference-velocity hypothesis advances to the next stage only if:

[
\boxed{
\begin{aligned}
&\text{Dimensional consistency}\
&\land\ \text{parameter identifiability}\
&\land\ \text{independent prediction}\
&\land\ \text{out-of-sample improvement}\
&\land\ \text{velocity-scale discrimination}\
&\land\ \text{cross-dataset stability}\
&\land\ \text{falsifiability}
\end{aligned}
}
]

are all satisfied.

Otherwise the EOS term remains an exploratory phenomenological normalization.

⸻

28. Final Statement

This protocol is designed to answer one specific scientific question:

[
\boxed{
\text{Does nature select }29,780\ \mathrm{m/s},
\text{ or did the model select it?}
}
]

The distinction must be resolved experimentally rather than assumed mathematically.
