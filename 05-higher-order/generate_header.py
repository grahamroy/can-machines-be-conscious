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
blue_border = '#3b82f6'
blue_fill = '#dbeafe'
purple_border = '#8b5cf6'
purple_fill = '#ede9fe'
arrow_grey = '#475569'
dark_text = '#1F2937'
subtle_text = '#6B7280'
panel_bg_color = '#F8FAFC'
panel_edge = '#E2E8F0'

# ─── Title & subtitle ───
ax.text(8, 8.45, 'Higher-Order Theories of Consciousness',
        ha='center', va='center', fontsize=18, fontweight='bold',
        color=dark_text, fontfamily='sans-serif')
ax.text(8, 7.95, 'A mental state becomes conscious when there is a thought about it',
        ha='center', va='center', fontsize=11, color=subtle_text,
        fontfamily='sans-serif', style='italic')

# ─── Left half: two-level architecture ───
left_box_w = 7.2
left_box_h = 1.7
left_box_x = 0.8

first_order_y = 1.6
meta_y = 5.0

# ----- First-order box (bottom, blue) -----
first_box = FancyBboxPatch((left_box_x, first_order_y), left_box_w, left_box_h,
                            boxstyle="round,pad=0.15",
                            facecolor=blue_fill, edgecolor=blue_border,
                            linewidth=2.2, zorder=3)
ax.add_patch(first_box)

# Header label for first-order box
ax.text(left_box_x + left_box_w/2, first_order_y + left_box_h - 0.35,
        'First-order net: Is this a cat?',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=4)

# Miniature neural network inside the first-order box
def draw_mini_network(ax, cx, cy, layers=(3, 4, 3, 2), width=2.6, height=0.85,
                      node_color=blue_border, line_color=blue_border, alpha=0.55):
    """Draw a tiny feed-forward net centred at (cx, cy)."""
    n_layers = len(layers)
    xs = np.linspace(cx - width/2, cx + width/2, n_layers)
    positions = []
    for li, nnodes in enumerate(layers):
        ys = np.linspace(cy - height/2, cy + height/2, nnodes)
        layer_pos = [(xs[li], y) for y in ys]
        positions.append(layer_pos)
    # connections
    for li in range(n_layers - 1):
        for (x0, y0) in positions[li]:
            for (x1, y1) in positions[li + 1]:
                ax.plot([x0, x1], [y0, y1], color=line_color,
                        alpha=alpha * 0.35, lw=0.7, zorder=3)
    # nodes
    for layer_pos in positions:
        for (x, y) in layer_pos:
            ax.add_patch(Circle((x, y), 0.08, facecolor='white',
                                edgecolor=node_color, linewidth=1.2,
                                zorder=5))
    return positions

first_net_pos = draw_mini_network(
    ax, cx=left_box_x + 2.1, cy=first_order_y + 0.85,
    layers=(3, 4, 4, 2), width=2.8, height=0.95,
    node_color=blue_border, line_color=blue_border, alpha=0.9,
)

# Prediction label (inside first-order box, right of network)
pred_x = left_box_x + 5.2
pred_y = first_order_y + 0.85
ax.text(pred_x, pred_y + 0.25, 'Prediction:',
        ha='center', va='center', fontsize=10,
        color=subtle_text, fontfamily='sans-serif', zorder=4)
ax.text(pred_x, pred_y - 0.1, 'cat',
        ha='center', va='center', fontsize=13, fontweight='bold',
        color=blue_border, fontfamily='sans-serif', zorder=4)
ax.text(pred_x, pred_y - 0.42, '(p = 0.87)',
        ha='center', va='center', fontsize=9,
        color=subtle_text, fontfamily='sans-serif', zorder=4)

# Small "input image" indicator to the left of the first-order net
img_x = left_box_x + 0.6
img_y = first_order_y + 0.85
img_rect = FancyBboxPatch((img_x - 0.25, img_y - 0.3), 0.5, 0.6,
                          boxstyle="round,pad=0.02",
                          facecolor='white', edgecolor=blue_border,
                          linewidth=1.2, zorder=4)
ax.add_patch(img_rect)
# Tiny circle inside the "image" to suggest content
ax.add_patch(Circle((img_x, img_y + 0.02), 0.12,
                    facecolor=blue_fill, edgecolor=blue_border,
                    linewidth=0.8, zorder=5))
ax.text(img_x, img_y - 0.55, 'input',
        ha='center', va='center', fontsize=7,
        color=subtle_text, fontfamily='sans-serif', zorder=4)

# ----- Meta-net box (top, purple) -----
meta_box = FancyBboxPatch((left_box_x, meta_y), left_box_w, left_box_h,
                           boxstyle="round,pad=0.15",
                           facecolor=purple_fill, edgecolor=purple_border,
                           linewidth=2.2, zorder=3)
ax.add_patch(meta_box)

ax.text(left_box_x + left_box_w/2, meta_y + left_box_h - 0.35,
        'Meta-net: Is the first-order net right?',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=4)

meta_net_pos = draw_mini_network(
    ax, cx=left_box_x + 2.1, cy=meta_y + 0.85,
    layers=(4, 5, 3, 1), width=2.8, height=0.95,
    node_color=purple_border, line_color=purple_border, alpha=0.9,
)

# Confidence readout
conf_x = left_box_x + 5.2
conf_y = meta_y + 0.85
ax.text(conf_x, conf_y + 0.25, 'Confidence:',
        ha='center', va='center', fontsize=10,
        color=subtle_text, fontfamily='sans-serif', zorder=4)
ax.text(conf_x, conf_y - 0.1, '0.92',
        ha='center', va='center', fontsize=14, fontweight='bold',
        color=purple_border, fontfamily='sans-serif', zorder=4)
ax.text(conf_x, conf_y - 0.42, '(well-calibrated)',
        ha='center', va='center', fontsize=9,
        color=subtle_text, fontfamily='sans-serif', zorder=4)

# ─── Upward arrow: features/logits from first-order to meta ───
arrow_up_x = left_box_x + left_box_w/2
arrow_up = FancyArrowPatch(
    (arrow_up_x, first_order_y + left_box_h + 0.15),
    (arrow_up_x, meta_y - 0.15),
    arrowstyle='->,head_width=0.35,head_length=0.5',
    color=arrow_grey, lw=2.4, zorder=5,
    mutation_scale=1.0,
)
ax.add_patch(arrow_up)

ax.text(arrow_up_x + 0.25,
        (first_order_y + left_box_h + meta_y) / 2,
        'features / logits',
        ha='left', va='center', fontsize=10, fontweight='bold',
        color=arrow_grey, fontfamily='sans-serif', zorder=6)

# ─── Reflexive arrow on meta-net ("awareness of one's own state") ───
# A curved self-loop on the right side of the meta box
reflex_cx = left_box_x + left_box_w + 0.05
reflex_cy = meta_y + left_box_h / 2
theta = np.linspace(-np.pi * 0.75, np.pi * 0.75, 80)
rr = 0.55
curve_x = reflex_cx + rr * np.cos(theta)
curve_y = reflex_cy + rr * np.sin(theta)
ax.plot(curve_x, curve_y, color=purple_border, lw=2.0, zorder=5)
# Arrowhead at the tail end
ah = FancyArrowPatch(
    (curve_x[-3], curve_y[-3]),
    (curve_x[-1], curve_y[-1]),
    arrowstyle='->,head_width=0.3,head_length=0.4',
    color=purple_border, lw=2.0, zorder=6,
    mutation_scale=1.0,
)
ax.add_patch(ah)

ax.text(reflex_cx + 0.75, reflex_cy + 0.05,
        "awareness of\none's own state",
        ha='left', va='center', fontsize=8.5, style='italic',
        color=purple_border, fontfamily='sans-serif', zorder=6)

# ─── Right panel: calibration / reliability diagram ───
panel_x = 10.6
panel_y = 1.6
panel_w = 4.7
panel_h = 5.1

panel_bg = FancyBboxPatch((panel_x, panel_y), panel_w, panel_h,
                           boxstyle="round,pad=0.2",
                           facecolor=panel_bg_color, edgecolor=panel_edge,
                           linewidth=1.5, zorder=2)
ax.add_patch(panel_bg)

ax.text(panel_x + panel_w/2, panel_y + panel_h - 0.35,
        'Calibration curve',
        ha='center', va='center', fontsize=11, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=3)
ax.text(panel_x + panel_w/2, panel_y + panel_h - 0.75,
        'Does confidence match accuracy?',
        ha='center', va='center', fontsize=8.5, style='italic',
        color=subtle_text, fontfamily='sans-serif', zorder=3)

# Inset axes for the calibration curve.
# Using fig.add_axes with normalized figure coords.
# Figure is 1600x900 -> width frac per x-unit = 1/16, height frac per y-unit = 1/9.
inset_left = (panel_x + 0.7) / 16
inset_bottom = (panel_y + 0.7) / 9
inset_width = (panel_w - 1.3) / 16
inset_height = (panel_h - 2.0) / 9

ax_inset = fig.add_axes([inset_left, inset_bottom, inset_width, inset_height])
ax_inset.set_facecolor('white')

# Ideal diagonal
xs = np.linspace(0, 1, 200)
ax_inset.plot(xs, xs, linestyle='--', color='#9CA3AF', lw=1.6,
              label='Ideal', zorder=3)

# Measured calibration curve: slightly under-confident in low range, slight
# over-confidence bump in the middle, tracks well near 1.0
pred_conf = np.linspace(0.0, 1.0, 9)
actual_acc = np.array([0.04, 0.14, 0.22, 0.33, 0.47, 0.60, 0.72, 0.84, 0.96])
# smooth interpolation for a nicer curve
from numpy.polynomial import polynomial as P  # std-lib via numpy
# cubic-like smoothing via numpy polyfit
coeffs = np.polyfit(pred_conf, actual_acc, 3)
smooth_x = np.linspace(0, 1, 200)
smooth_y = np.polyval(coeffs, smooth_x)
smooth_y = np.clip(smooth_y, 0, 1)

ax_inset.plot(smooth_x, smooth_y, color=purple_border, lw=2.4,
              label='Meta-net', zorder=5)
ax_inset.scatter(pred_conf, actual_acc, s=28, color=purple_border,
                 edgecolor='white', linewidth=1.0, zorder=6)

# Shade gap between curve and diagonal (miscalibration region)
ax_inset.fill_between(smooth_x, smooth_x, smooth_y,
                      where=(smooth_y < smooth_x),
                      color=purple_border, alpha=0.10, zorder=2)

ax_inset.set_xlim(0, 1)
ax_inset.set_ylim(0, 1)
ax_inset.set_xlabel('Predicted confidence', fontsize=8,
                    color=dark_text, fontfamily='sans-serif')
ax_inset.set_ylabel('Actual accuracy', fontsize=8,
                    color=dark_text, fontfamily='sans-serif')
ax_inset.tick_params(axis='both', which='both', labelsize=7,
                     colors=subtle_text)
ax_inset.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax_inset.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
for spine in ('top', 'right'):
    ax_inset.spines[spine].set_visible(False)
ax_inset.spines['left'].set_color('#D1D5DB')
ax_inset.spines['bottom'].set_color('#D1D5DB')
ax_inset.grid(True, which='major', color='#E5E7EB', lw=0.6, zorder=1)

leg = ax_inset.legend(loc='upper left', fontsize=7, frameon=True,
                      facecolor='white', edgecolor='#E5E7EB')
for text in leg.get_texts():
    text.set_color(dark_text)

# ─── Footer caption ───
ax.text(8, 0.55, 'Can Machines Be Conscious? Part 4',
        ha='center', va='center', fontsize=10,
        color=subtle_text, fontfamily='sans-serif', style='italic',
        zorder=5)

# ─── Save ───
output_path = r'D:\Projects\Medium\AI Consciousness\04-higher-order\header_metacognition.png'
plt.savefig(output_path, dpi=150, facecolor='white', edgecolor='none')
plt.close()
print(f"Saved to: {output_path}")
