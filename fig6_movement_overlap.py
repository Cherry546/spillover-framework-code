from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 9,
    "axes.titlesize": 9,
    "axes.labelsize": 8.5,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
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


T = 12.0                     
tau_A = 1.0                   
tau_H = 1.0                    
delta_A = 0.538                
delta_H = 0.939                

p_HZ = 1.0
c_field = np.ones_like(X)


times = np.arange(0, 60.01, 0.2)          
snapshot_times = [1, 13, 25, 37, 49]      


def f_A(t):
    """Seasonal modifier of reservoir activity (Section 3)."""
    return 1.0 + delta_A * np.cos(2 * np.pi * (t - tau_A) / T)


def f_H(t):
    """Seasonal modifier of human exposure activity (Section 3)."""
    return 1.0 + delta_H * np.cos(2 * np.pi * (t - tau_H) / T)


def W_A(t):
    """
    Normalised spatial distribution of bat activity, unit maximum.
    Centre shifts towards human-used areas over time.
    """
    x_A = x_A0 + v_x * t
    y_A = y_A0 + v_y * t
    return np.exp(-((X - x_A) ** 2 + (Y - y_A) ** 2) / (2 * sigma_A ** 2))


def W_H(t):
    """
    Normalised spatial distribution of human activity, unit maximum.
    Centre fixed; spatial extent expands over time.
    """
    sigma_H = sigma_H0 + sigma_H_growth * t
    return np.exp(-((X - x_h) ** 2 + (Y - y_h) ** 2) / (2 * sigma_H ** 2))


def exposure_filter(t):
    """
    Unimodal exposure filter W_H exp(-alpha W_H), applied to the spatial
    pattern rather than the full activity surface, since it represents the
    exclusion of reservoir hosts from densely settled areas.
    """
    w = W_H(t)
    return w * np.exp(-alpha * w)


overlap_integral = np.array([
    np.sum(c_field * W_A(t) * exposure_filter(t)) * dA
    for t in times
])

beta_series = p_HZ * f_A(times) * f_H(times) * overlap_integral


beta_rel = beta_series

seasonal_max = (1 + delta_A) * (1 + delta_H)
envelope_rel = overlap_integral * seasonal_max


UA_snapshots, FH_snapshots, overlap_snapshots = [], [], []

for t in snapshot_times:
    wa = W_A(t)
    filt = exposure_filter(t)
    UA_snapshots.append(f_A(t) * wa)
    FH_snapshots.append(f_H(t) * filt)
    overlap_snapshots.append(f_A(t) * f_H(t) * wa * filt)

UA_max = max(field.max() for field in UA_snapshots)
FH_max = max(field.max() for field in FH_snapshots)
overlap_max = max(field.max() for field in overlap_snapshots)


fig = plt.figure(figsize=(7.2, 4.8))

gs = fig.add_gridspec(
    2, 5,
    height_ratios=[0.85, 1.05],
    hspace=0.58, wspace=0.22,
    top=0.86, bottom=0.12, left=0.08, right=0.98,
)

snapshot_axes = [fig.add_subplot(gs[0, i]) for i in range(5)]
ax_beta = fig.add_subplot(gs[1, :])

snapshot_axes[0].set_title(
    r"($\mathit{a}$) Simulation snapshots at the January peak of each year",
    loc="left", pad=6, fontsize=9,
)

legend_elements = [
    Patch(facecolor="#6F8FEA", edgecolor="none", label="Human exposure kernel"),
    Patch(facecolor="#E34A33", edgecolor="none", label="Bat activity surface"),
    Line2D([0], [0], color="#5c1a72", lw=1.2, label="High overlap contours"),
]

fig.legend(
    handles=legend_elements,
    loc="upper right", ncol=3, frameon=False,
    bbox_to_anchor=(0.98, 0.99),
    columnspacing=1.1, handlelength=1.4, fontsize=8,
)

for ax, t, UA, FH, overlap in zip(
    snapshot_axes, snapshot_times,
    UA_snapshots, FH_snapshots, overlap_snapshots,
):
    UA_vis = UA / (UA_max + 1e-12)
    FH_vis = FH / (FH_max + 1e-12)
    overlap_vis = overlap / (overlap_max + 1e-12)

    rgb = np.ones((grid_size, grid_size, 3))
    rgb[..., 0] -= 0.45 * FH_vis
    rgb[..., 1] -= 0.30 * FH_vis
    rgb[..., 1] -= 0.55 * UA_vis
    rgb[..., 2] -= 0.65 * UA_vis
    rgb = np.clip(rgb, 0, 1)

    ax.imshow(rgb, origin="lower", extent=[0, 10, 0, 10])
    ax.contour(
        X, Y, overlap_vis,
        levels=[0.25, 0.50, 0.75],
        colors=["#5c1a72"], linewidths=0.55, alpha=0.78,
    )

    ax.set_xlabel(f"$t$ = {t}", labelpad=3)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")

    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("0.45")

ax_beta.fill_between(times, beta_rel, color="#C1502E", alpha=0.16, lw=0)
ax_beta.plot(times, beta_rel, lw=1.5, color="#C1502E",
             label=r"$\beta_{\mathrm{HZ}}(t)$")
ax_beta.plot(times, envelope_rel, "--", lw=1.9, color="#3B6E8F",
             label="Seasonal maximum envelope")

snapshot_idx = [np.argmin(np.abs(times - t)) for t in snapshot_times]
ax_beta.scatter(snapshot_times, beta_rel[snapshot_idx],
                s=22, color="#C1502E", zorder=4)

for t in snapshot_times:
    ax_beta.axvline(t, color="0.78", linestyle=":", linewidth=0.8)

ax_beta.set_xlabel("Simulation time (months)")
ax_beta.set_ylabel(r"$\beta_{\mathrm{HZ}}(t)$")
ax_beta.set_title(
    r"($\mathit{b}$) Temporal change in the resulting $\beta_{\mathrm{HZ}}(t)$",
    loc="left", pad=5,
)
ax_beta.legend(frameon=False, loc="upper left")
ax_beta.set_xlim(0, 60)
ax_beta.set_ylim(0, beta_rel.max() * 1.12)
ax_beta.grid(True, alpha=0.25, linewidth=0.6)

for spine in ax_beta.spines.values():
    spine.set_linewidth(0.8)
    spine.set_color("0.35")


save_dir = Path.home() / "Desktop"
if not save_dir.exists():
    save_dir = Path.cwd()

png_path = save_dir / "fig6.png"


fig.savefig(png_path, dpi=600, bbox_inches="tight")

plt.show()

print(f"Saved PNG to: {png_path}")


print("\nJanuary of each year:   beta      envelope")
for t, i in zip(snapshot_times, snapshot_idx):
    print(f"  t = {t:2d} months        {beta_rel[i]:.4f}    {envelope_rel[i]:.4f}")

print(f"\nSpatial overlap peaks at t = {times[np.argmax(overlap_integral)]:.0f} months")
print(f"beta_HZ(t) peaks at       t = {times[np.argmax(beta_series)]:.0f} months")
