# kapnack.py
import numpy as np

def harmonic_mean_safe(runs):
    return np.mean(1.0 / (runs + 1e-12)) ** -1

def rotational_variance(runs):
    return np.var(np.gradient(runs, axis=1))

def density_compression(runs):
    return np.mean(np.log1p(runs))

def resonance_peak(runs):
    return np.max(np.abs(np.fft.rfft(runs)))

def median_stability(runs):
    return np.median(runs, axis=1).mean()

def torsion_bias(runs):
    return np.mean(runs - runs.mean(axis=1, keepdims=True))

def triple_entanglement(runs):
    return np.prod(runs[:3] + 1e-12)

def loop_correlation(runs):
    return np.corrcoef(runs)[0,1] if runs.shape[0] > 1 else 0.0

def crystal12_signature(runs):
    """
    runs: ndarray shape (R, T) or (Nnodes, T)
    returns: normalized 12-vector (np.array length 12)
    """
    runs = np.asarray(runs)
    S1 = harmonic_mean_safe(runs)
    S2 = rotational_variance(runs)
    S3 = density_compression(runs)
    S4 = resonance_peak(runs)
    S5 = median_stability(runs)
    S6 = torsion_bias(runs)
    S7 = np.min(runs)
    S8 = np.max(runs)
    S9 = np.sum(runs**2)
    S10 = triple_entanglement(runs)
    S11 = np.linalg.norm(runs[0])
    S12 = loop_correlation(runs)
    vec = np.array([S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12], dtype=float)
    # normalize to unit scale (preserve sign)
    denom = np.max(np.abs(vec)) + 1e-12
    return vec / denom

# Kapnack compression operator
def kapnack_compress(vec, tau=0.03, beta=1.12, hard=True):
    """
    vec: input vector (real-valued)
    tau: threshold
    beta: boost for retained components
    hard: if False apply smooth soft-threshold instead
    returns: compressed vector (same shape)
    """
    v = np.array(vec, dtype=float)
    if hard:
        mask = np.abs(v) >= tau
        out = np.zeros_like(v)
        out[mask] = v[mask] * beta
        return out
    else:
        # soft threshold (smooth compression)
        out = np.sign(v) * np.maximum(0.0, np.abs(v) - tau)
        # re-scale retained
        out = out * (1.0 + (beta - 1.0) * (np.abs(out) > 0).astype(float))
        return out

def kapnack_serialize(vec, digits=6):
    """Return a short hash-like string from vector (useful as signature)"""
    v = np.round(vec / (np.max(np.abs(vec)) + 1e-12), digits)
    return "-".join([str(x).replace(".","p").replace("-","m") for x in v.tolist()])

# Example quick test
if __name__ == "__main__":
    runs = np.random.rand(5,12)
    sig = crystal12_signature(runs)
    comp = kapnack_compress(sig, tau=0.02, beta=1.15)
    print("Sigma:", sig)
    print("Compressed:", comp)
    print("Signature ID:", kapnack_serialize(comp))
