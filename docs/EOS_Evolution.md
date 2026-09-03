# SDKP Exploratory EOS Kinetic Correction

## Purpose

This document defines an exploratory comparison between the conventional
relativistic kinetic normalization K/c^2 and an alternative normalization
using Earth's orbital velocity:

    K/v_EOS^2

where:

    c = 299,792,458 m/s
    v_EOS = 29,780 m/s

This comparison does not establish K/v_EOS^2 as a physical law. It defines
a testable hypothesis that requires an independent physical coupling and
experimental validation.

## Equations

Conventional normalization:

    Δ_c = K/c^2

Exploratory EOS normalization:

    Δ_EOS = K/v_EOS^2

Amplification factor:

    A = Δ_EOS / Δ_c

    A = (c/v_EOS)^2

Using:

    c = 299,792,458 m/s
    v_EOS = 29,780 m/s

gives approximately:

    A ≈ 1.013 × 10^8

Therefore, for the same K, the EOS-normalized correction is approximately
101 million times larger than the c^2-normalized correction.

## Example

Let:

    K = 10^12 J

Conventional:

    K/c^2 ≈ 1.11265 × 10^-5 kg

Exploratory EOS:

    K/v_EOS^2 ≈ 1.1278 × 10^3 kg

Therefore:

    K/c^2      ≈ 0.0000111265 kg
    K/v_EOS^2  ≈ 1127.8 kg

## Physical Interpretation

The numerical amplification is a mathematical consequence of using a much
smaller velocity scale in the denominator.

It should NOT by itself be interpreted as evidence that the EOS correction
is physically valid.

The physical model must establish why v_EOS is an appropriate characteristic
velocity and what observable quantity is modified.

## Requirements for Falsifiability

For the hypothesis to become physically testable, SDKP must specify:

1. The exact definition of K.
2. The physical observable affected by the correction.
3. The coupling coefficient connecting K/v_EOS^2 to that observable.
4. The units and dimensions of every term.
5. A quantitative prediction made before examining the experimental result.
6. An independent experimental or observational dataset.
7. A standard-physics baseline for comparison.
8. A criterion under which the EOS model would be rejected.

A generic test structure is:

    X_SDKP = X_baseline + α(K/v_EOS^2)

where X is an observable and α is a theoretically defined coupling.

The model becomes falsifiable when α and all other parameters are fixed
independently and the resulting prediction can be compared against data.

## Critical Reference-Frame Test

Because v_EOS represents Earth's heliocentric orbital velocity, a major
test is whether the predicted correction depends on the chosen reference
velocity.

A successful theory must explain:

    Why Earth's orbital velocity?

and determine whether equivalent systems with different orbital velocities
should produce different corrections.

This distinction separates a physical mechanism from a simple numerical
rescaling.

## Status

This is an exploratory SDKP hypothesis.

The numerical comparison is valid as a mathematical normalization:

    K/v_EOS^2 ≈ 1.013 × 10^8 (K/c^2)

but the physical interpretation remains to be demonstrated experimentally.
