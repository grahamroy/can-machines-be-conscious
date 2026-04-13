"""
Generate header image for Article 2: Measuring Consciousness with a Number (IIT & Phi)

Visual concept: Three network topologies side by side — disconnected, chain, fully connected —
with Phi values below each, showing how integration increases with connectivity.
Nodes as circles, connections as lines, warm orange accent for the "most conscious" network.

White theme matching the algorithms-in-python header series.
Output: 1600x900 PNG
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe

# Palette — matches header series
BG       = "#ffffff"
PANEL    = "#f5f7fa"
CELL_ED  = "#cbd5e0"
GRIDLINE = "#e2e8f0"
ACCENT   = "#ff7a45"
ACCENT2  = "#f6ad3b"
TEXT     = "#0f1724"
MUTED    = "#64748b"
LIGHT    = "#94a3b8"

WIDTH  = 1600
HEIGHT = 900
DPI    = 100
FIGSIZE = (WIDTH / DPI, HEIGHT / DPI)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "header_iit_phi.png")


def draw_network(ax, cx, cy, nodes, edges, node_color, edge_color, label, phi_text, phi_color, radius=28):
    """Draw a small network diagram centered at (cx, cy)."""
    # Draw edges first (behind nodes)
    for (i, j) in edges:
        x0, y0 = nodes[i]
        x1, y1 = nodes[j]
        ax.annotate("",
            xy=(cx + x1, cy + y1),
            xytext=(cx + x0, cy + y0),
            arrowprops=dict(
                arrowstyle="-",
                color=edge_color,
                linewidth=2.5,
                connectionstyle="arc3,rad=0.0"
            ))

    # Draw nodes
    for idx, (nx, ny) in enumerate(nodes):
        circle = Circle((cx + nx, cy + ny), radius,
                        facecolor=node_color, edgecolor=edge_color,
                        linewidth=2, zorder=5)
        ax.add_patch(circle)
        # Node label
        ax.text(cx + nx, cy + ny, chr(65 + idx),
                ha="center", va="center", fontsize=13, fontweight="bold",
                color="#ffffff" if node_color == ACCENT else TEXT,
                zorder=6, fontfamily="sans-serif")

    # Network label below
    ax.text(cx, cy - 130, label, ha="center", va="center",
            fontsize=14, color=TEXT, fontweight="bold", fontfamily="sans-serif")

    # Phi value
    ax.text(cx, cy - 165, phi_text, ha="center", va="center",
            fontsize=18, color=phi_color, fontweight="bold", fontfamily="monospace")


fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(BG)
ax.set_xlim(0, WIDTH)
ax.set_ylim(0, HEIGHT)
ax.axis("off")

# Title area
ax.text(WIDTH / 2, HEIGHT - 80, "Integrated Information Theory",
        ha="center", va="center", fontsize=32, fontweight="bold",
        color=TEXT, fontfamily="sans-serif")
ax.text(WIDTH / 2, HEIGHT - 125, "How network topology determines \u03A6",
        ha="center", va="center", fontsize=16, color=MUTED, fontfamily="sans-serif")

# --- Four networks ---
# Positions for each network (evenly spaced)
centers = [220, 580, 940, 1300]
net_cy = 420

# Node positions (relative to center) — triangle layout
tri_nodes = [
    (0, 65),     # A (top)
    (-60, -40),  # B (bottom-left)
    (60, -40),   # C (bottom-right)
]

# 1. Disconnected — no edges
draw_network(ax, centers[0], net_cy, tri_nodes, [],
             GRIDLINE, CELL_ED,
             "Disconnected", "\u03A6 = 0.000", LIGHT)

# 2. Chain — A→B→C (feedforward)
chain_edges = [(0, 1), (1, 2)]
draw_network(ax, centers[1], net_cy, tri_nodes, chain_edges,
             PANEL, CELL_ED,
             "Chain (A\u2192B\u2192C)", "\u03A6 = 1.268", MUTED)

# 3. Cycle — A→B→C→A
cycle_edges = [(0, 1), (1, 2), (2, 0)]
draw_network(ax, centers[2], net_cy, tri_nodes, cycle_edges,
             "#fff0e6", ACCENT2,
             "Cycle (A\u2192B\u2192C\u2192A)", "\u03A6 = 2.536", ACCENT2)

# 4. Fully connected — all pairs
full_edges = [(0, 1), (1, 2), (2, 0)]
draw_network(ax, centers[3], net_cy, tri_nodes, full_edges,
             ACCENT, ACCENT,
             "Fully Connected", "\u03A6 = 3.170", ACCENT)

# Gradient arrow at bottom showing increasing Phi
arrow_y = 180
arrow_x0 = 180
arrow_x1 = 1350

# Draw gradient bar
n_steps = 200
for i in range(n_steps):
    t = i / n_steps
    # Interpolate from light grey to orange
    r = int(203 + t * (255 - 203))
    g = int(213 + t * (122 - 213))
    b = int(224 + t * (69 - 224))
    x = arrow_x0 + t * (arrow_x1 - arrow_x0)
    w = (arrow_x1 - arrow_x0) / n_steps + 1
    ax.add_patch(plt.Rectangle((x, arrow_y - 8), w, 16,
                               facecolor=f"#{r:02x}{g:02x}{b:02x}", edgecolor="none"))

# Arrow head
ax.annotate("", xy=(arrow_x1 + 30, arrow_y), xytext=(arrow_x1, arrow_y),
            arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=2.5))

# Labels on the gradient
ax.text(arrow_x0 - 10, arrow_y, "Less integrated", ha="right", va="center",
        fontsize=11, color=MUTED, fontfamily="sans-serif")
ax.text(arrow_x1 + 50, arrow_y, "More integrated", ha="left", va="center",
        fontsize=11, color=ACCENT, fontweight="bold", fontfamily="sans-serif")

# Small Phi symbol in the center of the gradient
ax.text((arrow_x0 + arrow_x1) / 2, arrow_y + 35, "\u03A6",
        ha="center", va="center", fontsize=40, color=ACCENT, fontweight="bold",
        fontfamily="serif", alpha=0.15)

# Large faint Phi watermark
ax.text(WIDTH / 2, HEIGHT / 2 + 20, "\u03A6",
        ha="center", va="center", fontsize=280, color=ACCENT,
        fontweight="bold", fontfamily="serif", alpha=0.04)

fig.savefig(OUT, dpi=DPI, facecolor=BG, bbox_inches="tight", pad_inches=0)
plt.close()
print(f"Saved: {OUT}")
