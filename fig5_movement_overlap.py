#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

FIG_WIDTH_IN = 7.2
FIG_HEIGHT_IN = 4.8
EXPORT_DPI = 600

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 10.5,
    "axes.titlesize": 10.5,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


grid_size = 300

x = np.linspace(0, 10, grid_size)
y = np.linspace(0, 10, grid_size)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]
dA = dx * dy



x_h, y_h = 8.0, 8.0
alpha = 2.0
sigma_H0 = 1.0
sigma_H_growth = 0.035
x_A0, y_A0 = 1.0, 1.0
v_x, v_y = 0.12, 0.12
sigma_A = 0.75
a_A = 1.0
a_H = 1.0
p_HA = 1.0
c_field = np.ones_like(X)
times = np.arange(0, 61, 1)
snapshot_times = [0, 15, 30, 45, 60]

def human_activity_surface(t):
    sigma_H = sigma_H0 + sigma_H_growth * t
    U_H = a_H * np.exp(
        -((X - x_h) ** 2 + (Y - y_h) ** 2) / (2 * sigma_H ** 2)
    )
    return U_H


def bat_activity_surface(t):
    x_A = x_A0 + v_x * t
    y_A = y_A0 + v_y * t

    U_A = a_A * np.exp(
        -((X - x_A) ** 2 + (Y - y_A) ** 2) / (2 * sigma_A ** 2)
    )
    return U_A


def human_exposure_kernel(U_H):
    return U_H * np.exp(-alpha * U_H)


beta_series = []

for t in times:
    U_H = human_activity_surface(t)
    F_H = human_exposure_kernel(U_H)
    U_A = bat_activity_surface(t)

    beta_t = p_HA * np.sum(c_field * U_A * F_H) * dA
    beta_series.append(beta_t)

beta_series = np.array(beta_series)
beta_series_rel = beta_series / (beta_series.max() + 1e-12)

F_H_snapshots = []
U_A_snapshots = []
overlap_snapshots = []

for t in snapshot_times:
    U_H = human_activity_surface(t)
    F_H = human_exposure_kernel(U_H)
    U_A = bat_activity_surface(t)
    overlap = U_A * F_H

    F_H_snapshots.append(F_H)
    U_A_snapshots.append(U_A)
    overlap_snapshots.append(overlap)

F_H_max = max(field.max() for field in F_H_snapshots)
U_A_max = max(field.max() for field in U_A_snapshots)
overlap_max = max(field.max() for field in overlap_snapshots)

fig = plt.figure(figsize=(FIG_WIDTH_IN, FIG_HEIGHT_IN))

gs = fig.add_gridspec(
    2,
    5,
    height_ratios=[0.85, 1.05],
    hspace=0.62,
    wspace=0.22,
    top=0.80,
    bottom=0.13,
    left=0.08,
    right=0.98,
)

snapshot_axes = [fig.add_subplot(gs[0, i]) for i in range(5)]
ax_beta = fig.add_subplot(gs[1, :])


fig.text(
    0.08,
    0.875,
    r"($\mathit{a}$) Simulation snapshots at five time points",
    ha="left",
    va="bottom",
    fontsize=10.5,
)


legend_elements = [
    Patch(facecolor="#6F8FEA", edgecolor="none", label="Human exposure kernel"),
    Patch(facecolor="#E34A33", edgecolor="none", label="Bat activity surface"),
    Line2D([0], [0], color="#5c1a72", lw=1.2, label="High overlap contours"),
]

fig.legend(
    handles=legend_elements,
    loc="upper right",
    ncol=3,
    frameon=False,
    bbox_to_anchor=(0.98, 0.965),
    columnspacing=1.1,
    handlelength=1.4,
    fontsize=9,
)


for ax, t, F_H, U_A, overlap in zip(
    snapshot_axes,
    snapshot_times,
    F_H_snapshots,
    U_A_snapshots,
    overlap_snapshots,
):
    F_H_vis = F_H / (F_H_max + 1e-12)
    U_A_vis = U_A / (U_A_max + 1e-12)
    overlap_vis = overlap / (overlap_max + 1e-12)

    rgb = np.ones((grid_size, grid_size, 3))


    rgb[..., 0] -= 0.45 * F_H_vis
    rgb[..., 1] -= 0.30 * F_H_vis


    rgb[..., 1] -= 0.55 * U_A_vis
    rgb[..., 2] -= 0.65 * U_A_vis

    rgb = np.clip(rgb, 0, 1)

    ax.imshow(rgb, origin="lower", extent=[0, 10, 0, 10])

    ax.contour(
        X,
        Y,
        overlap_vis,
        levels=[0.25, 0.50, 0.75],
        colors=["#5c1a72"],
        linewidths=0.55,
        alpha=0.78,
    )

    ax.set_title(f"t = {t}", pad=3)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")

    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("0.45")


ax_beta.plot(times, beta_series_rel, linewidth=1.6, color="black")
ax_beta.scatter(
    snapshot_times,
    beta_series_rel[snapshot_times],
    s=24,
    color="black",
    zorder=3,
)

for t in snapshot_times:
    ax_beta.axvline(t, color="0.75", linestyle=":", linewidth=0.8)

ax_beta.set_xlabel("Simulation time")
ax_beta.set_ylabel(r"Relative $\beta_{\mathrm{HA}}(t)$")
ax_beta.set_title(
    r"($\mathit{b}$) Temporal change in the resulting relative $\beta_{\mathrm{HA}}(t)$",
    loc="left",
    pad=5,
)
ax_beta.grid(True, alpha=0.25, linewidth=0.6)

for spine in ax_beta.spines.values():
    spine.set_linewidth(0.8)
    spine.set_color("0.35")


save_dir = Path("outputs") / "figures"
save_dir.mkdir(parents=True, exist_ok=True)

png_path = save_dir / "fig5_movement_overlap_beta_HA.png"
tif_path = save_dir / "fig5_movement_overlap_beta_HA.tif"
eps_path = save_dir / "fig5_movement_overlap_beta_HA.eps"
pdf_path = save_dir / "fig5_movement_overlap_beta_HA.pdf"

