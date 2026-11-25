"""Case 1: circular tabletop, A(r) = pi r^2  ->  Fig 1"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

PI = 3.14  # assumes pi = 3.14
r0 = 60.0
LIMIT = 5.0                  # acceptance  (%)


def A(r): return PI * r**2
def dA(dr): return 2 * PI * r0 * dr                    # linear estimate
def exact(dr): return A(r0) - A(r0 - dr)               # actual area lost
def rel(dr): return abs(exact(dr) - dA(dr)) / exact(dr)


lim = brentq(lambda x: rel(x) - LIMIT / 100, 0.1, 20)

# Figure 1
x = np.linspace(0.01, 8, 300)
fig, ax = plt.subplots(figsize=(8.2, 4.4))
ax.plot(x, [100 * rel(i) for i in x], color="tab:blue",
        lw=2, label="Relative discrepancy")
ax.axhline(LIMIT, color="red", ls="--", lw=1.2, label="5% acceptance limit")

ax.plot([lim, lim], [0, LIMIT], color="red", ls=":", lw=1.2)
ax.plot([lim], [LIMIT], "o", color="red")
ax.plot([1], [100 * rel(1)], "o", color="green",
        label="Artisan's trim (Δr = 1 cm)")

# Keep 0..8 and insert 2-line red label at 5.71
ticks = [0, 1, 2, 3, 4, 5, lim, 6, 7, 8]
labels = ["0", "1", "2", "3", "4", "5",
          f"Δr = {lim:.2f}\nlimit for Δr", "6", "7", "8"]
ax.set_xticks(ticks)
ax.set_xticklabels(labels, fontsize=8)

for val, lbl in zip(ticks, ax.get_xticklabels()):
    if np.isclose(val, 5.0):
        lbl.set_horizontalalignment("right")
    elif np.isclose(val, 6.0):
        lbl.set_horizontalalignment("left")
    elif np.isclose(val, lim, atol=1e-3):
        lbl.set_color("red")
        lbl.set_fontweight("bold")

ax.set_xlim(0, 8)
ax.set_ylim(0, 7.5)
ax.set_xlabel("Δr (cm)", labelpad=8)
ax.set_ylabel("Relative discrepancy (%)")
ax.grid(alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig("fig1.pdf", dpi=200)

# ---- Table 1 Verification ----
print(f"5% limit: dr = {lim:.2f} cm\n")
print(f"{'dr (cm)':>8} | {'delta_A':>8} | {'Delta_A (cm2)':>13} | {'dA (cm2)':>10} | {'Rel Disc':>9} | {'Abs Disc (cm2)':>14}")
print("-" * 75)
for dr in [0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, round(lim, 2)]:
    delta_A = 100 * dA(dr) / A(r0)
    ex = exact(dr)
    lin = dA(dr)
    rel_disc = 100 * rel(dr)
    abs_disc = abs(ex - lin)
    print(f"{dr:8.2f} | {delta_A:7.2f}% | {ex:13.2f} | {lin:10.2f} | {rel_disc:8.2f}% | {abs_disc:14.2f}")
