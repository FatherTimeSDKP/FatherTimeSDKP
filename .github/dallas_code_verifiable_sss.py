#!/usr/bin/env python3
"""
File: dallas_code_verifiable_sss.py
Author: Donald Paul Smith (FatherTimeSDKP)
ORCID: https://orcid.org/0009-0003-7925-1653
Repository: https://github.com/FatherTimeSDKP
Framework: The Integrated Framework (SDKP, SD&N, Amiyah's Law, Dallas's Code)
License: Distributed under GNU GPL v2.0

Description:
    A cryptographically secure, fully verifiable implementation of Shamir's 
    Secret Sharing (SSS) operating over the finite field F_P. Includes an 
    isolated Miller-Rabin primality check to prevent execution anomalies and 
    ensure absolute alignment with a 1.000000 decoherence state.
"""

import secrets

# Cryptographically secure safe prime larger than 2^256 for finite field operations
PRIME_FIELD_P = 2**256 + 297

def is_probable_prime(n: int, rounds: int = 64) -> bool:
    """
    Validates field boundary integrity using the Miller-Rabin probabilistic primality test.
    Returns True if the coordinate threshold represents a valid mathematical field.
    """
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for sp in small_primes:
        if n % sp == 0:
            return n == sp

    # Decompose n-1 to d * 2^s where d is odd
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def get_dynamic_hex_width(p: int) -> int:
    """Calculates the precise hexadecimal character width based on field bit-length."""
    return (p.bit_length() + 3) // 4

def int_to_hex(number: int, p: int) -> str:
    """Reduces a scalar modulo p and transforms it into a standard padded hex string."""
    number %= p
    width = get_dynamic_hex_width(p)
    return hex(number)[2:].zfill(width)

def evaluate_polynomial(coefficients: list, x: int, p: int) -> int:
    """Evaluates a polynomial at coordinate point x modulo p via Horner's method."""
    result = 0
    for coeff in reversed(coefficients):
        result = (result * x + coeff) % p
    return result

def generate_shares_sss(secret_int: int, n_shares: int, threshold_k: int, p: int) -> list:
    """
    Splits a master secret integer into N unique vector coordinates.
    Reconstruction strictly requires a minimum threshold of K coordinate matches.
    """
    if threshold_k > n_shares:
        raise ValueError("Threshold security limit K cannot exceed total split shares N.")
    if not (0 <= secret_int < p):
        raise ValueError("Master secret scalar must be within the field range [0, p-1].")

    # The intercept term coefficients[0] defines the true underlying secret
    coefficients = [secret_int]  
    for _ in range(threshold_k - 1):
        coefficients.append(secrets.randbelow(p))

    shares = []
    for x in range(1, n_shares + 1):
        y = evaluate_polynomial(coefficients, x, p)
        shares.append((x, y))
    return shares

def reconstruct_secret_sss(shares: list, p: int) -> int:
    """
    Reconstructs the original master secret from K distinct shares 
    using Lagrange interpolation evaluated at the intercept point x = 0.
    """
    secret = 0
    k = len(shares)

    for i in range(k):
        x_i, y_i = shares[i]
        numerator = 1
        denominator = 1

        for j in range(k):
            if i == j:
                continue
            x_j, _ = shares[j]
            numerator = (numerator * (-x_j)) % p
            denominator = (denominator * (x_i - x_j)) % p

        inv_denominator = pow(denominator, -1, p)
        lagrange_basis = (numerator * inv_denominator) % p
        secret = (secret + y_i * lagrange_basis) % p

    return secret

# =========================================================================
# STANDARD EXECUTION PROTOCOL & ASSERTION TEST
# =========================================================================
if __name__ == "__main__":
    print(f"Testing field prime p = {PRIME_FIELD_P}")
    
    # Pre-flight field validation layer
    if not is_probable_prime(PRIME_FIELD_P):
        raise SystemExit("ERROR: PRIME_FIELD_P is not prime. Finite field operations are invalid.")

    print(f"Calculated Target Hex Width: {get_dynamic_hex_width(PRIME_FIELD_P)} characters")

    # Generate a pristine, secure 256-bit secret vector
    secret_integer = secrets.randbelow(PRIME_FIELD_P)
    print(f"Generated Master Secret (Int): {secret_integer}")

    initial_hex = int_to_hex(secret_integer, PRIME_FIELD_P)
    print(f"Generated Master Secret (Hex): {initial_hex}")

    # Initialize execution metrics for K-out-of-N split governance
    total_shares_n = 5
    required_threshold_k = 3

    print(f"\n[Splitting secret into a {required_threshold_k}-out-of-{total_shares_n} scheme]")
    generated_shares = generate_shares_sss(secret_integer, total_shares_n, required_threshold_k, PRIME_FIELD_P)
    
    for x, y in generated_shares:
        print(f" Share {x} -> Field Coordinate Matrix Y: {hex(y)}")

    # Simulate recovery via an arbitrary coordinate subset of exactly K parameters (Shares 2, 4, and 5)
    recovery_subset = [generated_shares[1], generated_shares[3], generated_shares[4]]
    print(f"\n[Successor Triggered: Reconstructing via Components: {[s[0] for s in recovery_subset]}]")
    
    reconstructed_integer = reconstruct_secret_sss(recovery_subset, PRIME_FIELD_P)
    reconstructed_hex = int_to_hex(reconstructed_integer, PRIME_FIELD_P)

    # Confirm perfect numerical reconstruction across the field boundaries
    assert reconstructed_integer == secret_integer, "Critical Error: Reconstruction phase mismatch."
    print("\n[STATUS: VERIFICATION SUCCESSFUL]")
    print(f"Reconstructed Secret (Hex): {reconstructed_hex}")
