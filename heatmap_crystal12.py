# heatmap_crystal12.py
import numpy as np
import matplotlib.pyplot as plt

def plot_crystal12_heatmap(sigma, outpath="crystal12_heatmap.png", cmap="viridis", annotate=True):
    """
    sigma: 12-vector (iterable)
    outpath: path to save PNG
    """
    sigma = np.asarray(sigma, dtype=float)
    if sigma.size != 12:
        raise ValueError("sigma must be length 12")
    # reshape to 3x4 (3 rows, 4 cols) or 4x3 depending visual preference
    mat = sigma.reshape((3,4))
    plt.figure(figsize=(6,4))
    im = plt.imshow(mat, aspect='auto', cmap=cmap)
    plt.colorbar(im, fraction=0.046, pad=0.04)
    if annotate:
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                plt.text(j, i, f"{mat[i,j]:.3f}", ha='center', va='center', color='white' if mat[i,j]>0 else 'black', fontsize=9)
    plt.title("Crystal-12 Heatmap (3×4 view)")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()
    return outpath

# quick demo
if __name__ == "__main__":
    s = np.linspace(0.1, 1.2, 12)
    p = plot_crystal12_heatmap(s, outpath="crystal12_demo.png")
    print("Saved heatmap:", p)
