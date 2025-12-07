# app_streamlit.py
import streamlit as st
import numpy as np
from kapnack import crystal12_signature, kapnack_compress, kapnack_serialize
from heatmap_crystal12 import plot_crystal12_heatmap
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="FatherTimeSDKP — Kapnack Demo", layout="wide")

st.title("FatherTimeSDKP — Kapnack & Crystal-12 Demo")

st.sidebar.header("Data input")
mode = st.sidebar.radio("Mode", ["Random demo","Upload CSV (runs)"])

if mode == "Random demo":
    R = st.sidebar.slider("Runs (R)", 2, 12, 5)
    T = st.sidebar.slider("Points per run (T)", 12, 240, 60)
    runs = np.random.rand(R, T)
else:
    uploaded = st.sidebar.file_uploader("Upload CSV (rows=runs, cols=timepoints)", type=["csv"])
    if uploaded:
        import pandas as pd
        df = pd.read_csv(uploaded, header=None)
        runs = df.values
    else:
        st.info("Upload a CSV or switch to Random demo.")
        st.stop()

st.sidebar.header("Kapnack params")
tau = st.sidebar.slider("tau (threshold)", 0.0, 0.2, 0.03, 0.005)
beta = st.sidebar.slider("beta (boost)", 1.0, 2.0, 1.12, 0.01)
steps = st.sidebar.slider("recursion steps", 1, 200, 30)

# Compute Sigma
Sigma = crystal12_signature(runs)
st.subheader("Crystal-12 signature")
st.write(Sigma.round(6))

# Heatmap
heatpath = "streamlit_crystal12.png"
plot_crystal12_heatmap(Sigma, outpath=heatpath)
st.image(heatpath, use_column_width=True)

st.subheader("Kapnack compression")
comp = kapnack_compress(Sigma, tau=tau, beta=beta)
st.write("Compressed vector:", comp.round(6))
st.write("Signature ID:", kapnack_serialize(comp))

st.subheader("Recursion demo (simple A_{n+1} = Σ A_n + ω ρ + sinusoid)")
A0 = np.array([1.0, 0.9, 0.8])  # minimal anchor
omega = st.sidebar.slider("omega (scalar)", 0.1, 12.57, 6.283, 0.1)
rho_vec = np.mean(runs, axis=1)[:3] if runs.shape[0]>=3 else np.mean(runs, axis=1)

A = A0.copy()
path = [A.copy()]
for n in range(steps):
    # project Sigma to 3x3 diag for recursion
    Sigma3 = np.diag(Sigma[:3])
    t = n
    A = Sigma3.dot(A) + omega * rho_vec[:3] + 0.05 * np.sin(omega * t)
    # Kapnack style compress (on 3-vector)
    A = kapnack_compress(A, tau=tau, beta=beta)
    # normalize
    if np.linalg.norm(A)>0:
        A = A / np.linalg.norm(A)
    path.append(A.copy())

path = np.array(path)
st.line_chart(path)

st.success("Done — you can download heatmap or copy signature ID.")
