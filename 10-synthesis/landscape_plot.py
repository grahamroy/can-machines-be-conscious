"""landscape_plot.py

Plot the eight theories of consciousness surveyed in the series on a 2D map.

    X-axis: support for machine consciousness
        -1 = consciousness requires biological substrate
        +1 = consciousness is substrate-independent and/or ubiquitous

    Y-axis: empirical tractability
        -1 = purely philosophical, no experimental programme
        +1 = generates concrete falsifiable predictions

Positions reflect the stance Graham defends across the series; they are
deliberately defensible rather than definitive.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Series house palette — light theme matching earlier article headers
BG        = "#FFFFFF"
FG        = "#1F2937"
MUTED     = "#6B7280"
GRID      = "#E2E8F0"
ACCENT_A  = "#3b82f6"   # blue — functionalist / permissive theories
ACCENT_B  = "#ef4444"   # red — anti-functionalist / conservative theories
ACCENT_C  = "#8b5cf6"   # violet — panpsychism / radical

THEORIES = [
    # label,                                       x,     y,    colour,    anchor
    ("Integrated Information Theory",             +0.75, +0.85, ACCENT_A, "lower_right"),
    ("Recurrent Processing Theory",               +0.45, +0.90, ACCENT_A, "upper_right"),
    ("Global Workspace / Access",                 +0.60, +0.65, ACCENT_A, "lower_right"),
    ("Attention Schema Theory",                   +0.80, +0.45, ACCENT_A, "lower_right"),
    ("Free Energy / Predictive Processing",       +0.35, +0.50, ACCENT_A, "upper_left"),
    ("Higher-Order Theories",                     +0.20, +0.25, ACCENT_A, "lower_right"),
    ("Chinese Room",                              -0.50, -0.80, ACCENT_B, "upper_left"),
    ("Embodiment / Enactivism",                   -0.70, -0.30, ACCENT_B, "upper_right"),
    ("Zombie Argument",                            0.00, -0.90, ACCENT_B, "upper_right"),
    ("Panpsychism / Russellian Monism",           +0.90, -0.70, ACCENT_C, "upper_left"),
]

def offset_for(anchor):
    dx, dy = 0.04, 0.04
    return {
        "upper_right": ( dx,  dy, "left",   "bottom"),
        "upper_left":  (-dx,  dy, "right",  "bottom"),
        "lower_right": ( dx, -dy, "left",   "top"),
        "lower_left":  (-dx, -dy, "right",  "top"),
    }[anchor]

fig, ax = plt.subplots(figsize=(16/1.5, 10/1.5), dpi=150)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# Quadrant tints
ax.add_patch(Rectangle((0, 0),  1.1,  1.1, facecolor=ACCENT_A, alpha=0.06, zorder=0))
ax.add_patch(Rectangle((-1.1, 0), 1.1, 1.1, facecolor=ACCENT_B, alpha=0.04, zorder=0))
ax.add_patch(Rectangle((0, -1.1),  1.1, 1.1, facecolor=ACCENT_C, alpha=0.06, zorder=0))
ax.add_patch(Rectangle((-1.1, -1.1), 1.1, 1.1, facecolor=ACCENT_B, alpha=0.08, zorder=0))

# Quadrant labels
ax.text( 1.05,  1.05, "testable & permissive",   color=MUTED, fontsize=10,
        ha="right", va="top", style="italic")
ax.text(-1.05,  1.05, "testable & conservative", color=MUTED, fontsize=10,
        ha="left",  va="top", style="italic")
ax.text( 1.05, -1.05, "untestable & permissive", color=MUTED, fontsize=10,
        ha="right", va="bottom", style="italic")
ax.text(-1.05, -1.05, "untestable & conservative", color=MUTED, fontsize=10,
        ha="left",  va="bottom", style="italic")

# Crosshair at origin
ax.axhline(0, color=MUTED, linewidth=0.8, alpha=0.6, zorder=1)
ax.axvline(0, color=MUTED, linewidth=0.8, alpha=0.6, zorder=1)

# Plot theories
for label, x, y, colour, anchor in THEORIES:
    ax.scatter(x, y, s=160, c=colour, edgecolors=FG, linewidths=1.2, zorder=3)
    dx, dy, ha, va = offset_for(anchor)
    ax.annotate(label, xy=(x, y), xytext=(x + dx, y + dy),
                color=FG, fontsize=10, ha=ha, va=va, zorder=4)

# Axis cosmetics
ax.set_xlim(-1.15, 1.15)
ax.set_ylim(-1.15, 1.15)
ax.set_xlabel("support for machine consciousness", color=FG, fontsize=12, labelpad=10)
ax.set_ylabel("empirical tractability",           color=FG, fontsize=12, labelpad=10)
for spine in ax.spines.values():
    spine.set_color(MUTED)
ax.tick_params(colors=MUTED)
ax.set_xticks([-1, -0.5, 0, 0.5, 1])
ax.set_yticks([-1, -0.5, 0, 0.5, 1])

ax.set_title("The landscape of consciousness theories",
             color=FG, fontsize=14, pad=16, loc="left")

plt.tight_layout()
plt.savefig("landscape.png", dpi=150, facecolor=BG,
            bbox_inches="tight", pad_inches=0.3)
plt.close(fig)

# Summary for stdout
quads = {"TR": 0, "TL": 0, "BR": 0, "BL": 0}
for _, x, y, *_ in THEORIES:
    if x >= 0 and y >= 0: quads["TR"] += 1
    elif x < 0 and y >= 0: quads["TL"] += 1
    elif x >= 0 and y < 0: quads["BR"] += 1
    else: quads["BL"] += 1

print(f"Plotted {len(THEORIES)} theories. "
      f"Quadrants: testable&permissive={quads['TR']}, "
      f"testable&conservative={quads['TL']}, "
      f"untestable&permissive={quads['BR']}, "
      f"untestable&conservative={quads['BL']}.")
