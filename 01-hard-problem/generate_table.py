"""
Generate a clean table image for the consciousness theories summary.
Matches the white-theme style of the algorithms-in-python header images.
Output: theory_table.png (1200x520)
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Palette — matches the header image series
BG       = "#ffffff"
PANEL    = "#f5f7fa"
CELL     = "#eef2f7"
CELL_ED  = "#cbd5e0"
ACCENT   = "#ff7a45"
ACCENT2  = "#f6ad3b"
TEXT     = "#0f1724"
MUTED    = "#64748b"
WHITE    = "#ffffff"

# Verdict colour coding
YES_BG   = "#e6f9ed"   # soft green
YES_TX   = "#1a7a3a"
MAYBE_BG = "#fff7e6"   # soft amber
MAYBE_TX = "#b45309"
NO_BG    = "#fde8e8"   # soft red
NO_TX    = "#b91c1c"
UNIV_BG  = "#ede9fe"   # soft purple
UNIV_TX  = "#6d28d9"

DPI = 200
WIDTH = 1600
HEIGHT = 700
FIGSIZE = (WIDTH / DPI, HEIGHT / DPI)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theory_table.png")

# Table data
headers = ["Theory", "Supports machine\nconsciousness?", "Key requirement"]
rows = [
    ("IIT",                    "Maybe",            "High integrated information (Phi)"),
    ("GWT",                    "Yes",              "Global workspace architecture"),
    ("HOT",                    "Maybe",            "Genuine higher-order representation"),
    ("Biological Naturalism",  "No",               "Biological causal powers"),
    ("Phenomenology",          "No",               "Embodied, lived experience"),
    ("Predictive Processing",  "Maybe",            "Self-modelling, hierarchical prediction"),
    ("Panpsychism",            "Universal (micro)", "Macro-unification of micro-experience"),
    ("AST",                    "Yes",              "Accurate self-model of attention"),
]

def verdict_style(v):
    v_lower = v.lower()
    if v_lower == "yes":
        return YES_BG, YES_TX
    elif v_lower == "maybe":
        return MAYBE_BG, MAYBE_TX
    elif v_lower == "no":
        return NO_BG, NO_TX
    else:  # universal
        return UNIV_BG, UNIV_TX

fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(BG)
ax.set_xlim(0, WIDTH)
ax.set_ylim(0, HEIGHT)
ax.axis("off")

# Layout
margin_x = 60
margin_top = 45
col_widths = [400, 320, 760]  # theory, verdict, requirement
row_h = 68
header_h = 72
table_w = sum(col_widths)
table_x = margin_x
table_y_top = HEIGHT - margin_top

n_rows = len(rows)
table_h = header_h + n_rows * row_h

# Draw header row
hx = table_x
hy = table_y_top - header_h
# Header background
ax.add_patch(patches.FancyBboxPatch(
    (hx, hy), table_w, header_h,
    boxstyle="round,pad=0,rounding_size=6",
    facecolor=ACCENT, edgecolor="none"
))

# Header text
col_x = [table_x]
for w in col_widths[:-1]:
    col_x.append(col_x[-1] + w)

for i, (header, cx, cw) in enumerate(zip(headers, col_x, col_widths)):
    ax.text(cx + cw / 2, hy + header_h / 2, header,
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=WHITE, fontfamily="sans-serif")

# Draw data rows
for r, (theory, verdict, requirement) in enumerate(rows):
    ry = table_y_top - header_h - (r + 1) * row_h

    # Alternating row backgrounds
    row_bg = PANEL if r % 2 == 0 else BG

    # Row background with rounded corners for first/last
    if r == n_rows - 1:
        ax.add_patch(patches.FancyBboxPatch(
            (table_x, ry), table_w, row_h,
            boxstyle="round,pad=0,rounding_size=6",
            facecolor=row_bg, edgecolor="none"
        ))
    else:
        ax.add_patch(patches.Rectangle(
            (table_x, ry), table_w, row_h,
            facecolor=row_bg, edgecolor="none"
        ))

    # Column dividers (subtle)
    for cx in col_x[1:]:
        ax.plot([cx, cx], [ry, ry + row_h], color=CELL_ED, linewidth=0.5, alpha=0.5)

    # Theory name (bold)
    ax.text(col_x[0] + 24, ry + row_h / 2, theory,
            ha="left", va="center", fontsize=13, fontweight="bold",
            color=TEXT, fontfamily="sans-serif")

    # Verdict pill
    vbg, vtx = verdict_style(verdict)
    pill_w = min(len(verdict) * 12 + 36, col_widths[1] - 24)
    pill_h = 34
    pill_x = col_x[1] + (col_widths[1] - pill_w) / 2
    pill_y = ry + (row_h - pill_h) / 2
    ax.add_patch(patches.FancyBboxPatch(
        (pill_x, pill_y), pill_w, pill_h,
        boxstyle="round,pad=0,rounding_size=16",
        facecolor=vbg, edgecolor="none"
    ))
    ax.text(col_x[1] + col_widths[1] / 2, ry + row_h / 2, verdict,
            ha="center", va="center", fontsize=12, fontweight="semibold",
            color=vtx, fontfamily="sans-serif")

    # Key requirement
    ax.text(col_x[2] + 24, ry + row_h / 2, requirement,
            ha="left", va="center", fontsize=12,
            color=MUTED, fontfamily="sans-serif")

# Outer border (subtle rounded rect)
border_y = table_y_top - header_h - n_rows * row_h
ax.add_patch(patches.FancyBboxPatch(
    (table_x - 1, border_y - 1), table_w + 2, header_h + n_rows * row_h + 2,
    boxstyle="round,pad=0,rounding_size=8",
    facecolor="none", edgecolor=CELL_ED, linewidth=1.5
))

# Row dividers
for r in range(1, n_rows):
    ry = table_y_top - header_h - r * row_h
    ax.plot([table_x + 8, table_x + table_w - 8], [ry, ry],
            color=CELL_ED, linewidth=0.5, alpha=0.7)

fig.savefig(OUT, dpi=DPI, facecolor=BG, bbox_inches="tight", pad_inches=0.15)
plt.close()
print(f"Saved: {OUT}")
