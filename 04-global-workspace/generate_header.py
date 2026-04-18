import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Ellipse
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

# Workspace highlight (broadcast): blue
blue_fill = '#dbeafe'
blue_border = '#3b82f6'

# Specialised modules (unconscious): grey
grey_fill = '#F3F4F6'
grey_border = '#9CA3AF'

# Active / winning module: amber
amber_fill = '#FEF3C7'
amber_border = '#F59E0B'

# Broadcast arrows
arrow_grey = '#475569'

# Activation bar fill (darker grey for contrast on light modules)
bar_fill = '#6B7280'
bar_bg = '#E5E7EB'

# ─── Title & subtitle ───
ax.text(8, 8.45, 'Global Workspace Theory: Consciousness as Broadcast',
        ha='center', va='center', fontsize=18, fontweight='bold',
        color=dark_text, fontfamily='sans-serif')
ax.text(8, 7.95, 'Can Machines Be Conscious? Part 4',
        ha='center', va='center', fontsize=11, color=subtle_text,
        fontfamily='sans-serif', style='italic')

# ─── Panel geometry ───
panel_y = 1.3
panel_h = 6.1

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
        'Specialised modules',
        ha='center', va='center', fontsize=13, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=5)

# ─── Stack of 5 modules ───
modules = [
    ('visual cortex',    0.92, True),   # winner → amber
    ('auditory',         0.22, False),
    ('semantic',         0.55, False),
    ('motor planning',   0.38, False),
    ('proprioceptive',   0.18, False),
]

mod_x = left_panel_x + 0.6
mod_w = left_panel_w - 1.2
mod_h = 0.65
mod_gap = 0.22

stack_top = panel_y + panel_h - 1.0
n_mods = len(modules)
total_stack = n_mods * mod_h + (n_mods - 1) * mod_gap
stack_bottom = stack_top - total_stack

# Remember winner coords for arrow into workspace
winner_right_x = None
winner_cy = None

for i, (label, strength, is_winner) in enumerate(modules):
    y_top = stack_top - i * (mod_h + mod_gap)
    y = y_top - mod_h

    fill = amber_fill if is_winner else grey_fill
    border = amber_border if is_winner else grey_border
    lw = 1.8 if is_winner else 1.2

    box = FancyBboxPatch((mod_x, y), mod_w, mod_h,
                         boxstyle="round,pad=0.02,rounding_size=0.12",
                         facecolor=fill, edgecolor=border,
                         linewidth=lw, zorder=4)
    ax.add_patch(box)

    # Module label (left side of box)
    ax.text(mod_x + 0.25, y + mod_h/2, label,
            ha='left', va='center', fontsize=10.5,
            fontweight='bold' if is_winner else 'normal',
            color=dark_text, fontfamily='sans-serif', zorder=6)

    # Activation bar (right side of box)
    bar_total_w = 2.0
    bar_h = 0.22
    bar_x = mod_x + mod_w - bar_total_w - 0.25
    bar_y = y + mod_h/2 - bar_h/2

    # Bar background track
    ax.add_patch(Rectangle((bar_x, bar_y), bar_total_w, bar_h,
                           facecolor=bar_bg, edgecolor=border,
                           linewidth=0.8, zorder=5))
    # Filled portion proportional to strength
    fill_color = amber_border if is_winner else bar_fill
    ax.add_patch(Rectangle((bar_x, bar_y), bar_total_w * strength, bar_h,
                           facecolor=fill_color, edgecolor='none',
                           zorder=6))

    if is_winner:
        winner_right_x = mod_x + mod_w
        winner_cy = y + mod_h/2

# Caption beneath the stack
ax.text(left_panel_x + left_panel_w/2, panel_y + 0.55,
        'Unconscious specialists compete for broadcast',
        ha='center', va='center', fontsize=10, style='italic',
        color=subtle_text, fontfamily='sans-serif', zorder=6)

# ─── Right panel background ───
right_panel = FancyBboxPatch((right_panel_x, panel_y), right_panel_w, panel_h,
                              boxstyle="round,pad=0.15",
                              facecolor=panel_bg_color, edgecolor=panel_edge,
                              linewidth=1.5, zorder=2)
ax.add_patch(right_panel)

# Right panel header
ax.text(right_panel_x + right_panel_w/2, panel_y + panel_h - 0.4,
        'The workspace (ignition)',
        ha='center', va='center', fontsize=13, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=5)

# ─── Central workspace oval ───
ws_cx = right_panel_x + right_panel_w/2
ws_cy = panel_y + panel_h/2 - 0.1
ws_rx = 1.35
ws_ry = 0.95

workspace = Ellipse((ws_cx, ws_cy), 2*ws_rx, 2*ws_ry,
                    facecolor=blue_fill, edgecolor=blue_border,
                    linewidth=2.2, zorder=5)
ax.add_patch(workspace)

ax.text(ws_cx, ws_cy, 'WORKSPACE',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=6)

# ─── Incoming arrow from the winning module (left panel) into workspace ───
# Arrow starts at right edge of left panel winner, ends at left edge of workspace ellipse
in_start = (winner_right_x + 0.15, winner_cy)
# entry point on ellipse: left-ish, biased slightly upward to feel natural
in_end = (ws_cx - ws_rx - 0.05, ws_cy + 0.05)

incoming = FancyArrowPatch(
    in_start, in_end,
    arrowstyle='->,head_width=0.4,head_length=0.55',
    color=amber_border, lw=2.4, zorder=7,
    mutation_scale=1.0,
    connectionstyle="arc3,rad=0.0",
)
ax.add_patch(incoming)

# Small "winner" label on the incoming arrow
mid_in_x = (in_start[0] + in_end[0]) / 2
mid_in_y = (in_start[1] + in_end[1]) / 2 + 0.28
ax.text(mid_in_x, mid_in_y, 'winner',
        ha='center', va='center', fontsize=9, style='italic',
        color=amber_border, fontfamily='sans-serif', zorder=8)

# ─── Broadcast consumers around the workspace ───
consumers = [
    ('working memory',  ws_cx - 0.1,  ws_cy + 1.85),  # top
    ('verbal report',   ws_cx + 2.4,  ws_cy + 1.25),  # upper right
    ('decision',        ws_cx + 2.7,  ws_cy - 0.25),  # right
    ('motor planning',  ws_cx + 2.0,  ws_cy - 1.5),   # lower right
    ('episodic memory', ws_cx - 0.2,  ws_cy - 1.75),  # bottom
]

cons_w = 1.7
cons_h = 0.55

for (label, cx, cy) in consumers:
    box = FancyBboxPatch((cx - cons_w/2, cy - cons_h/2), cons_w, cons_h,
                         boxstyle="round,pad=0.02,rounding_size=0.1",
                         facecolor='white', edgecolor=blue_border,
                         linewidth=1.3, zorder=6)
    ax.add_patch(box)
    ax.text(cx, cy, label,
            ha='center', va='center', fontsize=9.5,
            color=dark_text, fontfamily='sans-serif', zorder=7)

    # Arrow from workspace edge to near box edge
    # Compute direction from ws center to consumer center
    dx = cx - ws_cx
    dy = cy - ws_cy
    dist = np.hypot(dx, dy)
    ux, uy = dx/dist, dy/dist

    # Start on ellipse boundary (approx): scale unit vector by ellipse radius in that direction
    # Ellipse boundary: r(theta) along (ux,uy) s.t. (r*ux/rx)^2 + (r*uy/ry)^2 = 1
    r_start = 1.0 / np.sqrt((ux/ws_rx)**2 + (uy/ws_ry)**2)
    sx = ws_cx + ux * (r_start + 0.05)
    sy = ws_cy + uy * (r_start + 0.05)

    # End just before the consumer box edge
    # Simple: back off along same direction by (cons_w/2 or cons_h/2 ish) — use a conservative back-off
    back = 0.55
    ex = cx - ux * back
    ey = cy - uy * back

    arrow = FancyArrowPatch(
        (sx, sy), (ex, ey),
        arrowstyle='->,head_width=0.32,head_length=0.45',
        color=arrow_grey, lw=1.8, zorder=5,
        mutation_scale=1.0,
    )
    ax.add_patch(arrow)

# Caption beneath the right panel
ax.text(right_panel_x + right_panel_w/2, panel_y + 0.55,
        'Ignition broadcasts the winner to the whole system',
        ha='center', va='center', fontsize=10, style='italic',
        color=subtle_text, fontfamily='sans-serif', zorder=6)

# ─── Save ───
output_path = r'D:\Projects\Medium\AI Consciousness\04-global-workspace\header_workspace.png'
plt.savefig(output_path, dpi=150, facecolor='white', edgecolor='none')
plt.close()
print(f"Saved to: {output_path}")
