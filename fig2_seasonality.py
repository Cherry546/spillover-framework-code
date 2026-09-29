from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

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

MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.",
          "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]

beta_0 = 1.0        

T = 12.0            
tau_A = 1.0        
tau_H = 1.0        
delta_A = 0.538     
delta_H = 0.939    

def f_A(t):
    return 1.0 + delta_A * np.cos(2 * np.pi * (t - tau_A) / T)


def f_H(t):
    return 1.0 + delta_H * np.cos(2 * np.pi * (t - tau_H) / T)


def beta_HZ(t):
    return beta_0 * f_A(t) * f_H(t)


t = np.linspace(1, 13, 600)

fig, ax = plt.subplots(figsize=(6.8, 3.6))

ax.fill_between(t, beta_HZ(t), color="#C1502E", alpha=0.16, lw=0)
ax.plot(t, beta_HZ(t), color="#C1502E", lw=2.3,
        label=r"$\beta_{\mathrm{HZ}}(t)$")
ax.plot(t, f_A(t), "--", color="#3B6E8F", lw=1.7,
        label=r"$f_{\mathrm{A}}(t)$  bat visitation")
ax.plot(t, f_H(t), ":", color="#5B8C5A", lw=2.1,
        label=r"$f_{\mathrm{H}}(t)$  human exposure")

ax.set_xticks(np.arange(1, 13))
ax.set_xticklabels(MONTHS, fontsize=7.5)
ax.set_xlim(1, 13)
ax.set_ylim(0, beta_HZ(t).max() * 1.28)
ax.set_xlabel("Month")
ax.set_ylabel(r"$\beta_{\mathrm{HZ}}(t)$")
ax.legend(frameon=False, loc="upper center", fontsize=8)
ax.spines[["top", "right"]].set_visible(False)

plt.tight_layout()

save_dir = Path.home() / "Desktop"
if not save_dir.exists():
    save_dir = Path.cwd()

png_path = save_dir / "fig2.png"

fig.savefig(png_path, dpi=600, bbox_inches="tight")

plt.show()

print(f"Saved PNG to: {png_path}")

months = np.arange(1, 13)
fa, fh = f_A(months), f_H(months)
bt = beta_HZ(months)

print("\n" + " " * 12 + "".join(f"{m:>8}" for m in MONTHS))
for label, values in [("f_A         ", fa),
                      ("f_H         ", fh),
                      ("beta_HZ(t)  ", bt)]:
    print(label + "".join(f"{v:>8.3f}" for v in values))

print(f"\nSeasonal contrast (max/min):"
      f"   f_A {fa.max()/fa.min():.1f}x"
      f"   f_H {fh.max()/fh.min():.1f}x"
      f"   beta_HZ {bt.max()/bt.min():.0f}x")
print(f"Ratio min/max:"
      f"   f_A {fa.min()/fa.max():.3f} (reported 0.300)"
      f"   f_H {fh.min()/fh.max():.3f} (reported 0.031)")
