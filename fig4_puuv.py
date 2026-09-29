from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

beta_HZ_0 = 1.0
w_L, kappa, alpha = 0.7, 5.0, 2.0

M = np.array([0.20, 0.90, 0.10])
L = np.array([0.10, 0.80, 0.20])
Q = np.array([0.70, 0.90, 0.20])
AH = np.array([0.10, 0.50, 0.90])

beta = (beta_HZ_0 * M * (1 + w_L * L)
        * (1 - np.exp(-kappa * Q))
        * AH * np.exp(-alpha * AH))

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 9.5,
    "axes.labelsize": 9.5,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.linewidth": 0.6,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.bbox": None,
    "figure.autolayout": False,
    "figure.constrained_layout.use": False,
})

fig = plt.figure(figsize=(170 / 25.4, 60 / 25.4), facecolor="white")
ax = fig.add_axes([24 / 170, 15 / 60, 141 / 170, 35 / 60])

ax.bar(range(3), beta, width=0.5,
       color=["#8FA9BC", "#C1502E", "#A8A8A8"],
       edgecolor="black", linewidth=0.6)

ax.set_xticks(range(3))
ax.set_xticklabels([
    "Patch 1\nForest interior",
    "Patch 2\nForest–farmland edge",
    "Patch 3\nResidential core",
])
ax.set_ylabel(r"$\beta_{\mathrm{HZ},r}$", labelpad=6)
ax.set_ylim(0, beta.max() * 1.15)
ax.yaxis.set_major_locator(MultipleLocator(0.05))
ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(width=0.6, length=3, pad=3.5)

fig.text(5 / 170, 55 / 60,
         r"$(e)$ Patch-specific environment-to-human transmission coefficient",
         fontsize=9.5, ha="left", va="center")

output = Path("Figure 4")
output.mkdir(exist_ok=True)

fig.savefig(output / "fig4.png", dpi=600,
            bbox_inches=None, facecolor="white")

plt.show()
