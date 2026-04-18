import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np

# Figure setup: 1600x900 at 150 DPI
fig, ax = plt.subplots(figsize=(1600/150, 900/150), dpi=150)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# ─── Color palette ───
dark_text = '#1F2937'
subtle_text = '#6B7280'
panel_bg_color = '#F8FAFC'
panel_edge = '#E2E8F0'
arrow_grey = '#475569'

blue_border = '#3b82f6'
blue_fill = '#dbeafe'
red_border = '#ef4444'
red_fill = '#fee2e2'
violet_border = '#8b5cf6'
violet_fill = '#ede9fe'

# ─── Title & subtitle ───
ax.text(8, 8.40, 'Where Do We Stand?',
        ha='center', va='center', fontsize=20, fontweight='bold',
        color=dark_text, fontfamily='sans-serif')
ax.text(8, 7.88,
        'Eight theories of consciousness on one map.  Can Machines Be Conscious? Part 8',
        ha='center', va='center', fontsize=10.5, color=subtle_text,
        fontfamily='sans-serif', style='italic')

# ─── Plot panel ───
panel_x = 2.2
panel_y = 0.7
panel_w = 11.6
panel_h = 6.6

panel = FancyBboxPatch((panel_x, panel_y), panel_w, panel_h,
                       boxstyle="round,pad=0.12",
                       facecolor=panel_bg_color, edgecolor=panel_edge,
                       linewidth=1.5, zorder=2)
ax.add_patch(panel)

# Plot interior geometry — the coordinate system lives inside the panel.
# We map data coords (x: -1..+1, y: -1..+1) into a plot box.
plot_left = panel_x + 1.1
plot_right = panel_x + panel_w - 1.1
plot_bottom = panel_y + 0.9
plot_top = panel_y + panel_h - 0.7

cx = (plot_left + plot_right) / 2   # x=0 in data
cy = (plot_bottom + plot_top) / 2   # y=0 in data
hx = (plot_right - plot_left) / 2   # half-width  (maps data=1)
hy = (plot_top - plot_bottom) / 2   # half-height (maps data=1)

def to_axes(dx, dy):
    return (cx + dx * hx, cy + dy * hy)

# ─── Quadrant tints ───
# upper-right = very light blue (functionalist & testable: machine-friendly)
# lower-right = very light violet (panpsychism-friendly zone)
# upper-left & lower-left = very light red (anti-functionalist)
ax.add_patch(Rectangle((cx, cy), plot_right - cx, plot_top - cy,
                       facecolor=blue_fill, alpha=0.35,
                       edgecolor='none', zorder=2.3))
ax.add_patch(Rectangle((cx, cy), plot_right - cx, plot_bottom - cy,
                       facecolor=violet_fill, alpha=0.35,
                       edgecolor='none', zorder=2.3))
ax.add_patch(Rectangle((plot_left, cy), cx - plot_left, plot_top - cy,
                       facecolor=red_fill, alpha=0.28,
                       edgecolor='none', zorder=2.3))
ax.add_patch(Rectangle((plot_left, cy), cx - plot_left, plot_bottom - cy,
                       facecolor=red_fill, alpha=0.28,
                       edgecolor='none', zorder=2.3))

# ─── Crosshair axes ───
ax.plot([plot_left, plot_right], [cy, cy],
        color=arrow_grey, linewidth=1.3, zorder=3, solid_capstyle='round')
ax.plot([cx, cx], [plot_bottom, plot_top],
        color=arrow_grey, linewidth=1.3, zorder=3, solid_capstyle='round')

# Tiny arrowheads at axis ends (triangles)
def arrow_tip(x, y, direction):
    size = 0.12
    if direction == 'right':
        pts = [[x, y], [x - size, y + size*0.7], [x - size, y - size*0.7]]
    elif direction == 'left':
        pts = [[x, y], [x + size, y + size*0.7], [x + size, y - size*0.7]]
    elif direction == 'up':
        pts = [[x, y], [x - size*0.7, y - size], [x + size*0.7, y - size]]
    else:  # down
        pts = [[x, y], [x - size*0.7, y + size], [x + size*0.7, y + size]]
    tri = plt.Polygon(pts, closed=True, facecolor=arrow_grey,
                      edgecolor=arrow_grey, zorder=3.5)
    ax.add_patch(tri)

arrow_tip(plot_right, cy, 'right')
arrow_tip(plot_left, cy, 'left')
arrow_tip(cx, plot_top, 'up')
arrow_tip(cx, plot_bottom, 'down')

# ─── Axis labels ───
# X-axis label (centered below axis)
ax.text(cx, plot_bottom - 0.50,
        'supports machine consciousness  \u2192',
        ha='center', va='center', fontsize=10, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=4)
# X-axis end captions
ax.text(plot_left + 0.10, cy - 0.28, 'biological / embodied',
        ha='left', va='top', fontsize=8, color=subtle_text,
        style='italic', fontfamily='sans-serif', zorder=4)
ax.text(plot_right - 0.10, cy - 0.28, 'computational / panpsychist',
        ha='right', va='top', fontsize=8, color=subtle_text,
        style='italic', fontfamily='sans-serif', zorder=4)

# Y-axis label (rotated)
ax.text(plot_left - 0.75, cy,
        'empirically testable  \u2192',
        ha='center', va='center', fontsize=10, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', rotation=90, zorder=4)
# Y-axis end captions
ax.text(cx + 0.15, plot_top - 0.10, 'falsifiable predictions',
        ha='left', va='top', fontsize=8, color=subtle_text,
        style='italic', fontfamily='sans-serif', zorder=4)
ax.text(cx + 0.15, plot_bottom + 0.10, 'pure philosophy',
        ha='left', va='bottom', fontsize=8, color=subtle_text,
        style='italic', fontfamily='sans-serif', zorder=4)

# ─── Theory points ───
# (label, data_x, data_y, color_family, label_offset)
# color_family: 'blue' | 'red' | 'violet'
# label_offset: (dx, dy) in axes units for text placement relative to the dot
theories = [
    ('IIT',           +0.70, +0.80, 'blue',   (0.28,  0.00), 'left'),
    ('GWT',           +0.60, +0.70, 'blue',   (-0.28, 0.22), 'right'),
    ('Free Energy',   +0.50, +0.40, 'blue',   (0.28,  0.00), 'left'),
    ('HOT',           +0.30, +0.30, 'blue',   (0.28,  0.00), 'left'),
    ('Chinese Room',  -0.50, -0.80, 'red',    (0.28,  0.00), 'left'),
    ('Embodiment',    -0.70, -0.30, 'red',    (0.28,  0.00), 'left'),
    ('Zombie',         0.00, -0.90, 'red',    (0.28,  0.00), 'left'),
    ('Panpsychism',   +0.90, -0.70, 'violet', (-0.28, 0.00), 'right'),
]

color_map = {
    'blue':   (blue_fill, blue_border),
    'red':    (red_fill, red_border),
    'violet': (violet_fill, violet_border),
}

dot_r = 0.20

for (name, dx, dy, fam, (lox, loy), ha) in theories:
    px, py = to_axes(dx, dy)
    fill, border = color_map[fam]

    # Outer soft halo
    ax.add_patch(Circle((px, py), dot_r * 1.55,
                        facecolor=fill, edgecolor='none',
                        alpha=0.55, zorder=4))
    # Main dot
    ax.add_patch(Circle((px, py), dot_r,
                        facecolor=fill, edgecolor=border,
                        linewidth=1.6, zorder=5))
    # Inner core
    ax.add_patch(Circle((px, py), dot_r * 0.38,
                        facecolor=border, edgecolor='none',
                        alpha=0.85, zorder=6))

    # Label
    ax.text(px + lox, py + loy, name,
            ha=ha, va='center', fontsize=9.5, fontweight='bold',
            color=dark_text, fontfamily='sans-serif', zorder=7)

# ─── Legend strip (bottom of figure, below the panel) ───
# Three small coloured swatches with labels
legend_y = 0.35
legend_specs = [
    ('permissive (functionalist)', blue_fill, blue_border),
    ('conservative (anti-functionalist)', red_fill, red_border),
    ('radical (panpsychism)', violet_fill, violet_border),
]

# Compute widths roughly and lay out centered
# approximate spacing:
legend_centers_x = [4.4, 8.0, 11.8]
for (label, fill, border), lx in zip(legend_specs, legend_centers_x):
    ax.add_patch(Circle((lx - 1.35, legend_y), 0.12,
                        facecolor=fill, edgecolor=border,
                        linewidth=1.3, zorder=5))
    ax.text(lx - 1.15, legend_y, label,
            ha='left', va='center', fontsize=8.5,
            color=subtle_text, fontfamily='sans-serif',
            style='italic', zorder=5)

# ─── Save ───
output_path = r'D:\Projects\Medium\AI Consciousness\08-synthesis\header_synthesis.png'
plt.savefig(output_path, dpi=150, facecolor='white', edgecolor='none')
plt.close()
print(f"Saved to: {output_path}")
