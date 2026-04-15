import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Figure setup: 1600x900 at 150 DPI
fig, ax = plt.subplots(figsize=(1600/150, 900/150), dpi=150)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Color palette
blue_pred = '#2563EB'
blue_light = '#DBEAFE'
blue_box = '#EFF6FF'
orange_err = '#EA580C'
orange_light = '#FFF7ED'
grey_struct = '#6B7280'
grey_light = '#F3F4F6'
dark_text = '#1F2937'
subtle_text = '#6B7280'

# ─── Title ───
ax.text(8, 8.35, 'Predictive Processing Hierarchy',
        ha='center', va='center', fontsize=18, fontweight='bold',
        color=dark_text, fontfamily='sans-serif')
ax.text(8, 7.85, 'Minimising surprise through hierarchical prediction',
        ha='center', va='center', fontsize=11, color=subtle_text,
        fontfamily='sans-serif', style='italic')

# ─── Rounded rectangle helper ───
def draw_level_box(ax, x, y, w, h, label, sublabel, fill_color, edge_color):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0.15",
                         facecolor=fill_color, edgecolor=edge_color,
                         linewidth=2, zorder=3)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2 + 0.15, label,
            ha='center', va='center', fontsize=12, fontweight='bold',
            color=dark_text, fontfamily='sans-serif', zorder=4)
    ax.text(x + w/2, y + h/2 - 0.25, sublabel,
            ha='center', va='center', fontsize=9, color=subtle_text,
            fontfamily='sans-serif', zorder=4)

# Level 2 (top) and Level 1 (bottom)
box_w = 8.5
box_h = 1.4
box_x = 1.5
level2_y = 5.8
level1_y = 2.2

draw_level_box(ax, box_x, level2_y, box_w, box_h,
               'Level 2: Hidden Cause', '(e.g. frequency, object identity)',
               blue_box, blue_pred)

draw_level_box(ax, box_x, level1_y, box_w, box_h,
               'Level 1: Sensory Prediction', '(e.g. expected pixel intensities)',
               orange_light, orange_err)

# ─── Arrows between levels ───
# Prediction arrows (downward, blue) - left side
arrow_left_x = 4.2
arrow_right_x = 7.5

for ax_pos in [arrow_left_x]:
    ax.annotate('', xy=(ax_pos, level1_y + box_h + 0.05),
                xytext=(ax_pos, level2_y - 0.05),
                arrowprops=dict(arrowstyle='->', color=blue_pred,
                                lw=2.5, mutation_scale=18),
                zorder=5)

# Prediction label
ax.text(arrow_left_x - 0.7, (level2_y + level1_y + box_h) / 2 + 0.05,
        'Predictions', ha='center', va='center', fontsize=10,
        color=blue_pred, fontweight='bold', fontfamily='sans-serif',
        rotation=90, zorder=5)
ax.text(arrow_left_x - 0.7, (level2_y + level1_y + box_h) / 2 - 0.45,
        r'$\downarrow$', ha='center', va='center', fontsize=14,
        color=blue_pred, fontfamily='sans-serif', zorder=5)

# Prediction error arrows (upward, orange) - right side
for ax_pos in [arrow_right_x]:
    ax.annotate('', xy=(ax_pos, level2_y - 0.05),
                xytext=(ax_pos, level1_y + box_h + 0.05),
                arrowprops=dict(arrowstyle='->', color=orange_err,
                                lw=2.5, mutation_scale=18),
                zorder=5)

# Error label
ax.text(arrow_right_x + 0.75, (level2_y + level1_y + box_h) / 2 + 0.05,
        'Prediction Errors', ha='center', va='center', fontsize=10,
        color=orange_err, fontweight='bold', fontfamily='sans-serif',
        rotation=270, zorder=5)
ax.text(arrow_right_x + 0.75, (level2_y + level1_y + box_h) / 2 - 0.5,
        r'$\uparrow$', ha='center', va='center', fontsize=14,
        color=orange_err, fontfamily='sans-serif', zorder=5)

# ─── Small decorative elements on the arrows ───
# Dashed lines connecting the arrows to show message flow
mid_y = (level2_y + level1_y + box_h) / 2
for yy in np.linspace(level1_y + box_h + 0.3, level2_y - 0.3, 6):
    # small dots along the arrow paths
    ax.plot(arrow_left_x, yy, 'o', color=blue_pred, markersize=2, alpha=0.4, zorder=2)
    ax.plot(arrow_right_x, yy, 'o', color=orange_err, markersize=2, alpha=0.4, zorder=2)

# ─── Free Energy Curve (right panel) ───
# Background panel
panel_x = 11.2
panel_y = 2.0
panel_w = 3.8
panel_h = 5.2

panel_bg = FancyBboxPatch((panel_x, panel_y), panel_w, panel_h,
                           boxstyle="round,pad=0.2",
                           facecolor=grey_light, edgecolor='#D1D5DB',
                           linewidth=1.5, zorder=2)
ax.add_patch(panel_bg)

ax.text(panel_x + panel_w/2, panel_y + panel_h - 0.25,
        'Free Energy  F', ha='center', va='center', fontsize=11,
        fontweight='bold', color=dark_text, fontfamily='sans-serif',
        zorder=3)

# Inset axes for the curve
ax_inset = fig.add_axes([0.72, 0.28, 0.2, 0.45])  # [left, bottom, width, height]
ax_inset.set_facecolor(grey_light)

# Free energy curve: learning -> surprise -> adaptation
t = np.linspace(0, 10, 300)
# Starts moderate, drops (learning), spikes (surprise), drops again (adaptation)
fe = (2.0 * np.exp(-0.5 * t) +
      2.5 * np.exp(-2.0 * (t - 5)**2) +
      0.3 + 0.05 * np.sin(t * 2) * np.exp(-0.1 * t))

ax_inset.fill_between(t, fe, alpha=0.15, color=blue_pred)
ax_inset.plot(t, fe, color=blue_pred, linewidth=2.2, zorder=5)

# Mark regions
ax_inset.axvspan(0, 3, alpha=0.05, color='green')
ax_inset.axvspan(3.5, 6.5, alpha=0.05, color='red')
ax_inset.axvspan(7, 10, alpha=0.05, color='green')

# Labels for regions
ax_inset.text(1.5, 0.15, 'learning', ha='center', fontsize=6.5,
              color='#059669', fontfamily='sans-serif', style='italic')
ax_inset.text(5, 0.15, 'surprise', ha='center', fontsize=6.5,
              color=orange_err, fontfamily='sans-serif', style='italic')
ax_inset.text(8.5, 0.15, 'adaptation', ha='center', fontsize=6.5,
              color='#059669', fontfamily='sans-serif', style='italic')

# Small spike annotation
spike_idx = np.argmax(fe[100:200]) + 100
ax_inset.annotate('prediction\nerror spike',
                  xy=(t[spike_idx], fe[spike_idx]),
                  xytext=(t[spike_idx] + 1.8, fe[spike_idx] + 0.15),
                  fontsize=5.5, color=orange_err, fontfamily='sans-serif',
                  arrowprops=dict(arrowstyle='->', color=orange_err, lw=0.8),
                  ha='center', zorder=6)

ax_inset.set_xlabel('Time', fontsize=7, color=subtle_text, fontfamily='sans-serif')
ax_inset.set_ylabel('F', fontsize=8, color=dark_text, fontfamily='sans-serif',
                     fontweight='bold', rotation=0, labelpad=10)
ax_inset.tick_params(axis='both', which='both', labelsize=6, colors=subtle_text)
ax_inset.spines['top'].set_visible(False)
ax_inset.spines['right'].set_visible(False)
ax_inset.spines['left'].set_color('#D1D5DB')
ax_inset.spines['bottom'].set_color('#D1D5DB')
ax_inset.set_xlim(0, 10)
ax_inset.set_ylim(0, max(fe) * 1.15)

# ─── Bottom annotation ───
ax.text(8, 0.55, 'The brain minimises free energy by updating its generative model',
        ha='center', va='center', fontsize=9, color=subtle_text,
        fontfamily='sans-serif', style='italic', zorder=5)

# ─── Subtle brain icon hint (decorative circles) ───
# Small network nodes to suggest neural processing
node_positions = [
    (5.75, 4.85), (5.3, 4.5), (6.2, 4.5),
    (5.0, 4.15), (5.75, 4.05), (6.5, 4.15),
]
for (nx, ny) in node_positions:
    circle = plt.Circle((nx, ny), 0.08, color=blue_pred, alpha=0.2, zorder=2)
    ax.add_patch(circle)

# Connect some nodes
connections = [(0,1),(0,2),(1,3),(1,4),(2,4),(2,5),(3,4),(4,5)]
for i, j in connections:
    x0, y0 = node_positions[i]
    x1, y1 = node_positions[j]
    ax.plot([x0, x1], [y0, y1], color=blue_pred, alpha=0.12, lw=0.8, zorder=1)

# ─── Save ───
output_path = r'D:\Projects\Medium\AI Consciousness\03-free-energy\header_predictive_processing.png'
plt.savefig(output_path, dpi=150,
            facecolor='white', edgecolor='none')
plt.close()
print(f"Saved to: {output_path}")
