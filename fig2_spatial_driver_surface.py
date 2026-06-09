#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

np.random.seed(42)

grid_size = 100
x = np.linspace(0, 10, grid_size)
y = np.linspace(0, 10, grid_size)
X, Y = np.meshgrid(x, y)

dx = float(x[1] - x[0])
dy = float(y[1] - y[0])


def normalize(arr, eps=1e-12):
    arr = np.asarray(arr, dtype=float)
    arr_min, arr_max = arr.min(), arr.max()
    return (arr - arr_min) / (arr_max - arr_min + eps)

A_H_raw = (
    1.0 * np.exp(-((X - 2) ** 2 + (Y - 2) ** 2) / 15)
    + 0.6 * np.exp(-((X - 8) ** 2 + (Y - 8) ** 2) / 12)
)
A_H = normalize(A_H_raw)

L_noise = np.random.rand(grid_size, grid_size)
L = gaussian_filter(L_noise, sigma=8)
L = normalize(L)

urban_mask = (
    np.exp(-((X - 2) ** 2 + (Y - 2) ** 2) / 8)
    + 0.7 * np.exp(-((X - 8) ** 2 + (Y - 8) ** 2) / 6)
)
urban_mask = np.clip(urban_mask, 0, 1)

L = L * (1 - urban_mask)
L = normalize(L)

dLy, dLx = np.gradient(L, dy, dx)
M = np.sqrt(dLx ** 2 + dLy ** 2)
M = gaussian_filter(M, sigma=1.5)
M = normalize(M)

Q_raw = np.zeros((grid_size, grid_size))

Q_raw[20:35, 20:35] = 1.0
Q_raw[70:85, 8:23] = 1.0
Q_raw[42:58, 52:68] = 1.0

Q = gaussian_filter(Q_raw, sigma=4)
Q = normalize(Q)



beta_0 = 1.0
omega_L = 0.7
kappa = 5.0
alpha = 2.0


spatial_driver_term = M * (1.0 + omega_L * L)
Q_term = 1.0 - np.exp(-kappa * Q)
A_H_filter_raw = A_H * np.exp(-alpha * A_H)
A_H_filter = normalize(A_H_filter_raw)
beta_HA = beta_0 * spatial_driver_term * Q_term * A_H_filter_raw
beta_HA_rel = normalize(beta_HA)


max_idx = np.unravel_index(np.argmax(beta_HA_rel), beta_HA_rel.shape)

print("Model form: interface driven")
print("Maximum beta_HA location:")
print("x =", X[max_idx], "y =", Y[max_idx])
print("Values at maximum:")
print("A_H =", A_H[max_idx])
print("L =", L[max_idx])
print("M =", M[max_idx])
print("Q =", Q[max_idx])
print("A_H filter raw =", A_H_filter_raw[max_idx])
print("beta_HA relative =", beta_HA_rel[max_idx])

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 12,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})


fig, axes = plt.subplots(2, 3, figsize=(8, 5), constrained_layout=True)

panels = [
    (
        A_H,
        r"($\mathit{a}$) Human activity $A_{\mathrm{H}}(\mathbf{x})$",
        "viridis",
    ),
    (
        L,
        r"($\mathit{b}$) Land use context $L(\mathbf{x})$",
        "viridis",
    ),
    (
        M,
        r"($\mathit{c}$) Local interface intensity $M(\mathbf{x})$",
        "viridis",
    ),
    (
        Q,
        r"($\mathit{d}$) Resource attractant $Q(\mathbf{x})$",
        "viridis",
    ),
    (
        A_H_filter,
        r"($\mathit{e}$) Exposure filter $A_{\mathrm{H}}(\mathbf{x})e^{-\alpha A_{\mathrm{H}}(\mathbf{x})}$",
        "viridis",
    ),
    (
        beta_HA_rel,
        r"($\mathit{f}$) Relative transmission surface $\beta_{\mathrm{HA}}(\mathbf{x})$",
        "magma",
    ),
]

for ax, (field, title, cmap) in zip(axes.ravel(), panels):
    im = ax.imshow(field, cmap=cmap, origin="lower", vmin=0, vmax=1)
    ax.set_title(title, loc="left")
    ax.set_xticks([])
    ax.set_yticks([])

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cbar.ax.tick_params(labelsize=10)
    cbar.set_ticks([0, 0.25, 0.5, 0.75, 1.0])



ax_f = axes.ravel()[5]
ax_f.contour(
    beta_HA_rel,
    levels=[0.5, 0.75],
    colors="black",
    linewidths=0.8,
    alpha=0.95,
)


save_dir = Path("outputs") / "figures"
save_dir.mkdir(parents=True, exist_ok=True)

png_path = save_dir / "fig2_spatial_driver_surface.png"
tif_path = save_dir / "fig2_spatial_driver_surface.tif"
pdf_path = save_dir / "fig2_spatial_driver_surface.pdf"
eps_path = save_dir / "fig2_spatial_driver_surface.eps"

fig.savefig(png_path, dpi=600, bbox_inches="tight")
fig.savefig(tif_path, dpi=600, bbox_inches="tight")
fig.savefig(pdf_path, bbox_inches="tight")
fig.savefig(eps_path, bbox_inches="tight")

plt.show()

print("Saved PNG to:", png_path)
print("Saved TIFF to:", tif_path)
print("Saved PDF to:", pdf_path)
print("Saved EPS to:", eps_path)

