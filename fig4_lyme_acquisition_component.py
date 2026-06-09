#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Figure 4: Lyme disease dilution and amplification landscape
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

FIG_WIDTH_IN = 7.2
FIG_HEIGHT_IN = 5.4
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

kappa_mouse = 0.921
kappa_squirrel = 0.147
kappa_opossum = 0.026
a_feed = 1.0
n_grid = 250
f_mouse = np.linspace(0, 1, n_grid)
f_opossum = np.linspace(0, 1, n_grid)
F_MOUSE, F_OPOSSUM = np.meshgrid(f_mouse, f_opossum)
F_SQUIRREL = 1.0 - F_MOUSE - F_OPOSSUM
valid_mask = F_SQUIRREL >= 0

p_eff = (F_MOUSE * kappa_mouse+ F_SQUIRREL * kappa_squirrel+ F_OPOSSUM * kappa_opossum)
beta_eff = a_feed * p_eff
beta_eff_masked = np.ma.masked_where(~valid_mask, beta_eff)
fig, ax = plt.subplots(
    figsize=(FIG_WIDTH_IN, FIG_HEIGHT_IN),
    constrained_layout=True
)
ax.set_facecolor("0.92")
levels = np.linspace(float(beta_eff_masked.min()),float(beta_eff_masked.max()), 21)

contour = ax.contourf(F_MOUSE, F_OPOSSUM, beta_eff_masked,levels=levels, cmap="RdYlBu_r",alpha=0.95)

contour_lines = ax.contour(F_MOUSE, F_OPOSSUM, beta_eff_masked, levels=np.linspace(0.10, 0.90, 9), colors="0.25", linewidths=0.45, alpha=0.75)

ax.clabel(contour_lines, inline=True, fontsize=9, fmt="%.2f")


ax.plot( [0, 1],[1, 0],color="black", linewidth=1.0
)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal", adjustable="box")
ax.set_xlabel(r"Proportion of larval meals on white-footed mice, $f_{\mathrm{mouse}}$")
ax.set_ylabel(r"Proportion of larval meals on Virginia opossums, $f_{\mathrm{opossum}}$")
ax.tick_params(direction="out", length=3, width=0.8)


cbar = fig.colorbar(contour, ax=ax, shrink=0.88, pad=0.03)

cbar.set_label( r"Community-weighted acquisition component, $p_{\mathrm{eff}}$", fontsize=10)

cbar.ax.tick_params(labelsize=9, direction="out", length=3, width=0.8)

ax.text(0.13, 0.82, "Dilution\nlower acquisition", color="navy", fontweight="bold", ha="center", va="center", fontsize=9, bbox=dict(facecolor="white", edgecolor="none", alpha=0.70, pad=2.0))

ax.text(0.82, 0.12, "Amplification\nhigher acquisition", color="darkred", fontweight="bold", ha="center", va="center", fontsize=9, bbox=dict(facecolor="white", edgecolor="none", alpha=0.70, pad=2.0))

ax.text(0.69, 0.91, "Infeasible region", transform=ax.transAxes, fontsize=9, color="0.35", ha="center", va="center")

ax.grid(True, linestyle=":", linewidth=0.45, alpha=0.25)
for spine in ax.spines.values():
    spine.set_linewidth(0.8)

save_dir = Path("outputs") / "figures"
save_dir.mkdir(parents=True, exist_ok=True)

png_path = save_dir / "fig3_lyme_acquisition_component.png"
tif_path = save_dir / "fig3_lyme_acquisition_component.tif"
pdf_path = save_dir / "fig3_lyme_acquisition_component.pdf"
eps_path = save_dir / "fig3_lyme_acquisition_component.eps"

