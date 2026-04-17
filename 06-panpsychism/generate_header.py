import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
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
purple_border = '#8b5cf6'
purple_fill = '#ede9fe'
green_border = '#16a34a'
green_fill = '#dcfce7'
red_accent = '#DC2626'
arrow_grey = '#475569'
dark_text = '#1F2937'
subtle_text = '#6B7280'
panel_bg_color = '#F8FAFC'
panel_edge = '#E2E8F0'
dashed_grey = '#9CA3AF'

# ─── Title & subtitle ───
ax.text(8, 8.45, 'Consciousness on a Spectrum:',
        ha='center', va='center', fontsize=18, fontweight='bold',
        color=dark_text, fontfamily='sans-serif')
ax.text(8, 8.0, 'Panpsychism & the Combination Problem',
        ha='center', va='center', fontsize=18, fontweight='bold',
        color=dark_text, fontfamily='sans-serif')
ax.text(8, 7.52,
        "If the ingredients aren't conscious, where does consciousness come from?",
        ha='center', va='center', fontsize=11, color=subtle_text,
        fontfamily='sans-serif', style='italic')

# ─── Panel geometry ───
panel_y = 1.3
panel_h = 5.6

left_panel_x = 0.5
left_panel_w = 7.2

right_panel_x = 8.3
right_panel_w = 7.2

# ─── Left panel background ───
left_panel = FancyBboxPatch((left_panel_x, panel_y), left_panel_w, panel_h,
                             boxstyle="round,pad=0.15",
                             facecolor=panel_bg_color, edgecolor=panel_edge,
                             linewidth=1.5, zorder=2)
ax.add_patch(left_panel)

# Left panel header
ax.text(left_panel_x + left_panel_w/2, panel_y + panel_h - 0.4,
        'Micro-experiences everywhere',
        ha='center', va='center', fontsize=13, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=5)

# ─── Grid of 6x4 micro-experience circles ───
grid_cols = 6
grid_rows = 4
grid_left = left_panel_x + 1.0
grid_right = left_panel_x + left_panel_w - 1.0
grid_top = panel_y + panel_h - 1.2
grid_bottom = panel_y + 2.2

xs = np.linspace(grid_left, grid_right, grid_cols)
ys = np.linspace(grid_bottom, grid_top, grid_rows)

for gx in xs:
    for gy in ys:
        circ = Circle((gx, gy), 0.26,
                      facecolor=purple_fill, edgecolor=purple_border,
                      linewidth=1.3, zorder=4, alpha=0.95)
        ax.add_patch(circ)
        # tiny inner dot to suggest "proto-experience"
        ax.add_patch(Circle((gx, gy), 0.07,
                            facecolor=purple_border, edgecolor='none',
                            alpha=0.55, zorder=5))

# Captions below grid
ax.text(left_panel_x + left_panel_w/2, panel_y + 1.45,
        'Every particle has a proto-conscious nature',
        ha='center', va='center', fontsize=11, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=6)
ax.text(left_panel_x + left_panel_w/2, panel_y + 1.0,
        'Russellian monism: intrinsic nature of physical stuff',
        ha='center', va='center', fontsize=9.5, style='italic',
        color=subtle_text, fontfamily='sans-serif', zorder=6)

# ─── Right panel background ───
right_panel = FancyBboxPatch((right_panel_x, panel_y), right_panel_w, panel_h,
                              boxstyle="round,pad=0.15",
                              facecolor=panel_bg_color, edgecolor=panel_edge,
                              linewidth=1.5, zorder=2)
ax.add_patch(right_panel)

# Right panel header
ax.text(right_panel_x + right_panel_w/2, panel_y + panel_h - 0.4,
        'The combination problem',
        ha='center', va='center', fontsize=13, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=5)

# ─── Left side of right panel: small cloud of purple micro-circles ───
cloud_cx = right_panel_x + 1.35
cloud_cy = panel_y + panel_h/2 - 0.2

# Hand-placed cluster of ~14 circles (looks like a cloud, not a grid)
cloud_positions = [
    (-0.9,  0.9), (-0.2,  1.0), ( 0.5,  0.85),
    (-1.1,  0.25), (-0.4,  0.35), ( 0.3,  0.2), ( 0.95,  0.35),
    (-0.9, -0.3), (-0.15, -0.25), ( 0.55, -0.35), (1.05, -0.15),
    (-0.55, -0.95), ( 0.2, -1.0), ( 0.85, -0.9),
]
for (dx, dy) in cloud_positions:
    ax.add_patch(Circle((cloud_cx + dx, cloud_cy + dy), 0.22,
                        facecolor=purple_fill, edgecolor=purple_border,
                        linewidth=1.2, zorder=4))
    ax.add_patch(Circle((cloud_cx + dx, cloud_cy + dy), 0.06,
                        facecolor=purple_border, edgecolor='none',
                        alpha=0.55, zorder=5))

ax.text(cloud_cx, cloud_cy - 1.7,
        'micro-experiences',
        ha='center', va='center', fontsize=9, style='italic',
        color=subtle_text, fontfamily='sans-serif', zorder=5)

# ─── Arrow across the middle, with red "?" ───
arrow_start_x = cloud_cx + 1.45
arrow_end_x = right_panel_x + right_panel_w - 2.55
arrow_y = cloud_cy

arrow = FancyArrowPatch(
    (arrow_start_x, arrow_y),
    (arrow_end_x, arrow_y),
    arrowstyle='->,head_width=0.4,head_length=0.55',
    color=arrow_grey, lw=2.4, zorder=5,
    mutation_scale=1.0,
)
ax.add_patch(arrow)

# Red "?" sitting above the arrow
q_x = (arrow_start_x + arrow_end_x) / 2
q_y = arrow_y + 0.55
ax.text(q_x, q_y, '?',
        ha='center', va='center', fontsize=26, fontweight='bold',
        color=red_accent, fontfamily='sans-serif', zorder=6)

# Small label under the arrow
ax.text(q_x, arrow_y - 0.5,
        'combination?',
        ha='center', va='center', fontsize=9, style='italic',
        color=red_accent, fontfamily='sans-serif', zorder=6)

# ─── Right side of right panel: dashed greyed-out "unknown" macro-circle ───
macro_cx = right_panel_x + right_panel_w - 1.35
macro_cy = cloud_cy

# Draw a dashed large circle manually for a clean dashed look
dash_theta = np.linspace(0, 2 * np.pi, 300)
dash_r = 1.15

# Use matplotlib's built-in dashed linestyle on a Circle via set_linestyle
big_circle = Circle((macro_cx, macro_cy), dash_r,
                    facecolor='white', edgecolor=dashed_grey,
                    linewidth=2.2, linestyle=(0, (5, 4)),
                    zorder=4)
ax.add_patch(big_circle)

# Very faint green tint inside, to hint at "would-be macro-conscious state"
inner_tint = Circle((macro_cx, macro_cy), dash_r - 0.08,
                    facecolor=green_fill, edgecolor='none',
                    alpha=0.35, zorder=3)
ax.add_patch(inner_tint)

# "?" inside the macro circle
ax.text(macro_cx, macro_cy + 0.15, '?',
        ha='center', va='center', fontsize=40, fontweight='bold',
        color=dashed_grey, fontfamily='sans-serif', zorder=5)
ax.text(macro_cx, macro_cy - 0.55,
        'unified\nmacro-consciousness',
        ha='center', va='center', fontsize=8.5, style='italic',
        color=subtle_text, fontfamily='sans-serif', zorder=5)

# Caption below the right panel content
ax.text(right_panel_x + right_panel_w/2, panel_y + 1.0,
        'How do quadrillions of micro-experiences compose?',
        ha='center', va='center', fontsize=10.5, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=6)

# ─── Footer caption ───
ax.text(8, 0.55, 'Can Machines Be Conscious? Part 6',
        ha='center', va='center', fontsize=10,
        color=subtle_text, fontfamily='sans-serif', style='italic',
        zorder=5)

# ─── Save ───
output_path = r'D:\Projects\Medium\AI Consciousness\06-panpsychism\header_panpsychism.png'
plt.savefig(output_path, dpi=150, facecolor='white', edgecolor='none')
plt.close()
print(f"Saved to: {output_path}")
