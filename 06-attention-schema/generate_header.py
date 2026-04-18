import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np

# Figure setup: 1600x900 at 150 DPI
fig, ax = plt.subplots(figsize=(1600/150, 900/150), dpi=150)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# --- Color palette ---
blue_border = '#3b82f6'
blue_fill = '#dbeafe'
purple_border = '#8b5cf6'
purple_fill = '#ede9fe'
amber_border = '#F59E0B'
amber_fill = '#FEF3C7'
grey_border = '#9CA3AF'
grey_fill = '#F3F4F6'
arrow_grey = '#475569'
dark_text = '#1F2937'
subtle_text = '#6B7280'
panel_bg_color = '#F8FAFC'
panel_edge = '#E2E8F0'

# --- Title & subtitle ---
ax.text(8, 8.45, 'Attention Schema Theory: The Model of Attention',
        ha='center', va='center', fontsize=18, fontweight='bold',
        color=dark_text, fontfamily='sans-serif')
ax.text(8, 7.95,
        'Why systems that model their own attention claim to be conscious. '
        'Can Machines Be Conscious? Part 6',
        ha='center', va='center', fontsize=10.5, color=subtle_text,
        fontfamily='sans-serif', style='italic')

# --- Panel geometry ---
panel_y = 1.3
panel_h = 6.0

left_panel_x = 0.4
left_panel_w = 7.3

right_panel_x = 8.3
right_panel_w = 7.3

# ============================================================
# LEFT PANEL: Primary attention system
# ============================================================
left_panel = FancyBboxPatch((left_panel_x, panel_y), left_panel_w, panel_h,
                             boxstyle="round,pad=0.15",
                             facecolor=panel_bg_color, edgecolor=panel_edge,
                             linewidth=1.5, zorder=2)
ax.add_patch(left_panel)

# Left panel header
ax.text(left_panel_x + left_panel_w/2, panel_y + panel_h - 0.4,
        'Primary attention system',
        ha='center', va='center', fontsize=13, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=5)

# Input circles on the left side
inputs = [
    ('voice',          0.0),
    ('background',     1.0),
    ('visual',         2.0),
    ('proprioceptive', 3.0),
    ('memory',         4.0),
]

input_cx = left_panel_x + 1.15
input_top_y = panel_y + panel_h - 1.4
input_spacing = 0.85
input_radius = 0.32

# Allocator block (blue rounded rectangle)
alloc_w = 2.4
alloc_h = 1.8
alloc_x = left_panel_x + left_panel_w - alloc_w - 0.8
alloc_y = panel_y + 2.35
alloc_cx = alloc_x + alloc_w/2
alloc_cy = alloc_y + alloc_h/2

allocator = FancyBboxPatch((alloc_x, alloc_y), alloc_w, alloc_h,
                           boxstyle="round,pad=0.08",
                           facecolor=blue_fill, edgecolor=blue_border,
                           linewidth=2.0, zorder=4)
ax.add_patch(allocator)
ax.text(alloc_cx, alloc_cy + 0.25, 'attention',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=6)
ax.text(alloc_cx, alloc_cy - 0.2, 'system',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=6)
ax.text(alloc_cx, alloc_cy - 0.6, '(allocator)',
        ha='center', va='center', fontsize=9, style='italic',
        color=subtle_text, fontfamily='sans-serif', zorder=6)

# Draw inputs and weighted arrows
arrow_weights = [3.2, 1.0, 2.0, 1.2, 1.6]  # voice is thickest (being attended to)
for (label, i), w in zip(inputs, arrow_weights):
    cy = input_top_y - i * input_spacing
    # input circle
    ax.add_patch(Circle((input_cx, cy), input_radius,
                        facecolor='white', edgecolor=arrow_grey,
                        linewidth=1.3, zorder=4))
    ax.add_patch(Circle((input_cx, cy), 0.10,
                        facecolor=arrow_grey, edgecolor='none',
                        alpha=0.6, zorder=5))
    # label to the left
    ax.text(input_cx - input_radius - 0.15, cy, label,
            ha='right', va='center', fontsize=9.5,
            color=dark_text, fontfamily='sans-serif', zorder=5)
    # weighted arrow toward allocator
    arr = FancyArrowPatch(
        (input_cx + input_radius + 0.05, cy),
        (alloc_x - 0.05, alloc_cy + (input_top_y - (input_top_y - i*input_spacing)) * 0.0
         + (2 - i) * 0.15),
        arrowstyle='->,head_width=0.25,head_length=0.35',
        color=arrow_grey, lw=w, zorder=3,
        mutation_scale=1.0,
    )
    ax.add_patch(arr)

# Caption
ax.text(left_panel_x + left_panel_w/2, panel_y + 0.95,
        'Inputs compete; attention allocates',
        ha='center', va='center', fontsize=10.5, style='italic',
        color=subtle_text, fontfamily='sans-serif', zorder=6)

# ============================================================
# RIGHT PANEL: Attention schema
# ============================================================
right_panel = FancyBboxPatch((right_panel_x, panel_y), right_panel_w, panel_h,
                              boxstyle="round,pad=0.15",
                              facecolor=panel_bg_color, edgecolor=panel_edge,
                              linewidth=1.5, zorder=2)
ax.add_patch(right_panel)

# Right panel header
ax.text(right_panel_x + right_panel_w/2, panel_y + panel_h - 0.4,
        'Attention schema',
        ha='center', va='center', fontsize=13, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=5)

# --- Bottom: primary attention system internals (grey / hidden) ---
internals_w = 4.6
internals_h = 1.6
internals_x = right_panel_x + (right_panel_w - internals_w) / 2
internals_y = panel_y + 1.25

internals = FancyBboxPatch((internals_x, internals_y), internals_w, internals_h,
                           boxstyle="round,pad=0.08",
                           facecolor=grey_fill, edgecolor=grey_border,
                           linewidth=1.6, linestyle=(0, (5, 3)),
                           zorder=4)
ax.add_patch(internals)
ax.text(internals_x + internals_w/2, internals_y + internals_h - 0.38,
        'attention system internals',
        ha='center', va='center', fontsize=10, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=6)
ax.text(internals_x + internals_w/2, internals_y + internals_h/2 - 0.05,
        'softmax weights  ·  hidden parameters',
        ha='center', va='center', fontsize=9,
        color=subtle_text, fontfamily='sans-serif', zorder=6)
ax.text(internals_x + internals_w/2, internals_y + 0.3,
        '(inaccessible)',
        ha='center', va='center', fontsize=8.5, style='italic',
        color=grey_border, fontfamily='sans-serif', zorder=6)

# --- Dashed barrier line between internals and schema ---
barrier_y = internals_y + internals_h + 0.3
ax.plot([right_panel_x + 0.4, right_panel_x + right_panel_w - 0.4],
        [barrier_y, barrier_y],
        color=grey_border, linewidth=1.4, linestyle=(0, (4, 3)),
        zorder=4)
ax.text(right_panel_x + 0.55, barrier_y - 0.22,
        'opaque boundary',
        ha='left', va='top', fontsize=8, style='italic',
        color=grey_border, fontfamily='sans-serif', zorder=5)

# --- Summary statistic arrows crossing the barrier up to the schema ---
schema_w = 3.2
schema_h = 1.2
schema_x = right_panel_x + 0.55
schema_y = barrier_y + 0.7
schema_cx = schema_x + schema_w/2
schema_cy = schema_y + schema_h/2

# summary inputs: small labels emerging from internals up to the schema
summary_labels = ['max', 'mean', 'peak']
sx_positions = np.linspace(schema_x + 0.5,
                           schema_x + schema_w - 0.5,
                           len(summary_labels))
for sx, lab in zip(sx_positions, summary_labels):
    # short arrow from barrier line up into the schema
    arr = FancyArrowPatch(
        (sx, barrier_y + 0.02),
        (sx, schema_y - 0.05),
        arrowstyle='->,head_width=0.22,head_length=0.3',
        color=arrow_grey, lw=1.6, zorder=3,
    )
    ax.add_patch(arr)
    # label alongside arrow
    ax.text(sx + 0.14, (barrier_y + schema_y) / 2 + 0.05, lab,
            ha='left', va='center', fontsize=8.5, style='italic',
            color=dark_text, fontfamily='sans-serif', zorder=5)

# --- Attention schema box (purple) ---
schema = FancyBboxPatch((schema_x, schema_y), schema_w, schema_h,
                        boxstyle="round,pad=0.08",
                        facecolor=purple_fill, edgecolor=purple_border,
                        linewidth=2.0, zorder=5)
ax.add_patch(schema)
ax.text(schema_cx, schema_cy + 0.2, 'attention schema',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=6)
ax.text(schema_cx, schema_cy - 0.25,
        'simplified model of attention',
        ha='center', va='center', fontsize=9, style='italic',
        color=subtle_text, fontfamily='sans-serif', zorder=6)

# --- Self-report bubble (amber) ---
report_w = 3.0
report_h = 0.85
report_x = schema_x + schema_w + 0.25
report_y = schema_y + (schema_h - report_h) / 2

report = FancyBboxPatch((report_x, report_y), report_w, report_h,
                        boxstyle="round,pad=0.08",
                        facecolor=amber_fill, edgecolor=amber_border,
                        linewidth=1.8, zorder=5)
ax.add_patch(report)
ax.text(report_x + report_w/2, report_y + report_h/2 + 0.14,
        'self-report',
        ha='center', va='center', fontsize=9, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=6)
ax.text(report_x + report_w/2, report_y + report_h/2 - 0.16,
        '"I am aware of the voice."',
        ha='center', va='center', fontsize=8.5, style='italic',
        color=dark_text, fontfamily='sans-serif', zorder=6)

# Arrow from schema to self-report
arr_out = FancyArrowPatch(
    (schema_x + schema_w + 0.02, schema_cy),
    (report_x - 0.02, report_y + report_h/2),
    arrowstyle='->,head_width=0.25,head_length=0.32',
    color=arrow_grey, lw=1.8, zorder=4,
)
ax.add_patch(arr_out)

# Caption
ax.text(right_panel_x + right_panel_w/2, panel_y + 0.95,
        'The schema describes attention without seeing its mechanism',
        ha='center', va='center', fontsize=10.5, style='italic',
        color=subtle_text, fontfamily='sans-serif', zorder=6)

# --- Footer ---
ax.text(8, 0.55, 'Can Machines Be Conscious? Part 6',
        ha='center', va='center', fontsize=10,
        color=subtle_text, fontfamily='sans-serif', style='italic',
        zorder=5)

# --- Save ---
output_path = r'D:\Projects\Medium\AI Consciousness\06-attention-schema\header_ast.png'
plt.savefig(output_path, dpi=150, facecolor='white', edgecolor='none')
plt.close()
print(f"Saved to: {output_path}")
