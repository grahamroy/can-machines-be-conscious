import matplotlib.pyplot as plt
from matplotlib.patches import (
    FancyBboxPatch,
    FancyArrowPatch,
    Circle,
    Rectangle,
    Polygon,
    Ellipse,
)
from matplotlib.lines import Line2D
import numpy as np

# ─── Figure setup: 1600x900 at 150 DPI ───
fig, ax = plt.subplots(figsize=(1600 / 150, 900 / 150), dpi=150)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.set_aspect('equal')
ax.axis('off')
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# ─── Color palette (shared with the rest of the series) ───
blue_border   = '#3b82f6'
blue_fill     = '#dbeafe'
purple_border = '#8b5cf6'
purple_fill   = '#ede9fe'
arrow_grey    = '#475569'
dark_text     = '#1F2937'
subtle_text   = '#6B7280'
panel_bg      = '#F8FAFC'
panel_edge    = '#E2E8F0'
dull_grey     = '#9CA3AF'
dull_grey_fill = '#E5E7EB'

# ─── Title & subtitle ───
ax.text(8, 8.45, 'The Chinese Room, the Zombie, and the Lived Body',
        ha='center', va='center', fontsize=18, fontweight='bold',
        color=dark_text, fontfamily='sans-serif')
ax.text(8, 7.95, 'Three arguments against machine consciousness',
        ha='center', va='center', fontsize=11, color=subtle_text,
        fontfamily='sans-serif', style='italic')

# ─── Panel layout ───
panel_w = 4.8
panel_h = 5.0
panel_y = 1.35
gap = 0.30
total_w = 3 * panel_w + 2 * gap
start_x = (16 - total_w) / 2

panels_x = [start_x + i * (panel_w + gap) for i in range(3)]

# Background rounded panels
for px in panels_x:
    ax.add_patch(FancyBboxPatch(
        (px, panel_y), panel_w, panel_h,
        boxstyle="round,pad=0.18",
        facecolor=panel_bg, edgecolor=panel_edge,
        linewidth=1.5, zorder=1,
    ))

# ─── Panel 1: Chinese Room ──────────────────────────────────────────
p1x = panels_x[0]
p1_cx = p1x + panel_w / 2
p1_cy = panel_y + panel_h / 2 + 0.15

# Room (box)
room_w = 2.9
room_h = 2.2
room_x = p1_cx - room_w / 2
room_y = p1_cy - room_h / 2

room = FancyBboxPatch(
    (room_x, room_y), room_w, room_h,
    boxstyle="round,pad=0.05",
    facecolor='white', edgecolor=blue_border,
    linewidth=2.0, zorder=3,
)
ax.add_patch(room)

# Small figure inside (abstract head pictogram)
head_cx = p1_cx
head_cy = p1_cy - 0.05
# Head
ax.add_patch(Circle((head_cx, head_cy + 0.30), 0.26,
                    facecolor=blue_fill, edgecolor=blue_border,
                    linewidth=1.6, zorder=5))
# Shoulders / body
body_w = 0.85
body_h = 0.55
body = FancyBboxPatch(
    (head_cx - body_w / 2, head_cy - 0.55),
    body_w, body_h,
    boxstyle="round,pad=0.03,rounding_size=0.18",
    facecolor=blue_fill, edgecolor=blue_border,
    linewidth=1.6, zorder=4,
)
ax.add_patch(body)

# Rulebook next to the figure
book_x = head_cx + 0.55
book_y = head_cy - 0.45
ax.add_patch(Rectangle(
    (book_x, book_y), 0.5, 0.35,
    facecolor='white', edgecolor=arrow_grey,
    linewidth=1.1, zorder=5,
))
for i in range(3):
    ax.plot([book_x + 0.08, book_x + 0.42],
            [book_y + 0.08 + i * 0.08, book_y + 0.08 + i * 0.08],
            color=dull_grey, lw=0.6, zorder=6)

# Abstract "Chinese-looking" symbols (dots / squares) flowing IN on the left
def draw_symbol(ax, cx, cy, size=0.18, color=dark_text):
    """Draw an abstract glyph made of a square border with an internal pattern."""
    ax.add_patch(Rectangle(
        (cx - size / 2, cy - size / 2), size, size,
        facecolor='white', edgecolor=color, linewidth=1.1, zorder=6,
    ))
    # Internal dots forming simple patterns
    pattern = np.random.rand()
    if pattern < 0.33:
        # horizontal bar
        ax.plot([cx - size * 0.3, cx + size * 0.3],
                [cy, cy], color=color, lw=1.0, zorder=7)
    elif pattern < 0.66:
        # cross
        ax.plot([cx - size * 0.3, cx + size * 0.3],
                [cy, cy], color=color, lw=0.9, zorder=7)
        ax.plot([cx, cx],
                [cy - size * 0.3, cy + size * 0.3],
                color=color, lw=0.9, zorder=7)
    else:
        # dot
        ax.add_patch(Circle((cx, cy), size * 0.15,
                            facecolor=color, edgecolor='none', zorder=7))

np.random.seed(7)

# Incoming symbols (left of the room)
in_symbols_x = room_x - 0.45
in_ys = np.linspace(room_y + 0.4, room_y + room_h - 0.4, 4)
for y in in_ys:
    draw_symbol(ax, in_symbols_x, y, size=0.24, color=dark_text)

# Outgoing symbols (right of the room)
out_symbols_x = room_x + room_w + 0.45
out_ys = np.linspace(room_y + 0.4, room_y + room_h - 0.4, 4)
for y in out_ys:
    draw_symbol(ax, out_symbols_x, y, size=0.24, color=dark_text)

# Arrow IN (pointing into the room)
ax.add_patch(FancyArrowPatch(
    (in_symbols_x + 0.25, p1_cy),
    (room_x - 0.02, p1_cy),
    arrowstyle='->,head_width=0.28,head_length=0.35',
    color=arrow_grey, lw=1.8, zorder=5, mutation_scale=1.0,
))
# Arrow OUT (pointing away from the room)
ax.add_patch(FancyArrowPatch(
    (room_x + room_w + 0.02, p1_cy),
    (out_symbols_x - 0.25, p1_cy),
    arrowstyle='->,head_width=0.28,head_length=0.35',
    color=arrow_grey, lw=1.8, zorder=5, mutation_scale=1.0,
))

# Tiny "in / out" captions
ax.text(in_symbols_x, room_y - 0.30, 'input',
        ha='center', va='center', fontsize=7.5,
        color=subtle_text, fontfamily='sans-serif', zorder=6)
ax.text(out_symbols_x, room_y - 0.30, 'output',
        ha='center', va='center', fontsize=7.5,
        color=subtle_text, fontfamily='sans-serif', zorder=6)

# Panel label + tagline
ax.text(p1_cx, panel_y + panel_h - 0.45, 'Chinese Room',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=8)
ax.text(p1_cx, panel_y + 0.42, 'Syntax without semantics',
        ha='center', va='center', fontsize=9,
        color=subtle_text, fontfamily='sans-serif',
        style='italic', zorder=8)


# ─── Panel 2: Zombie ────────────────────────────────────────────────
p2x = panels_x[1]
p2_cx = p2x + panel_w / 2
p2_cy = panel_y + panel_h / 2 + 0.15


def draw_silhouette(ax, cx, cy, edge_color, fill_color,
                    line_width=2.0, zorder=3, alpha=1.0):
    """Draw a simple stylised human silhouette centred at (cx, cy)."""
    # Head
    head_r = 0.35
    head_cy_local = cy + 1.05
    ax.add_patch(Circle(
        (cx, head_cy_local), head_r,
        facecolor=fill_color, edgecolor=edge_color,
        linewidth=line_width, zorder=zorder, alpha=alpha,
    ))
    # Body / torso as a rounded trapezoid-ish polygon
    body_pts = np.array([
        [cx - 0.55, cy + 0.55],   # upper left shoulder
        [cx + 0.55, cy + 0.55],   # upper right shoulder
        [cx + 0.75, cy - 0.10],   # right side waist
        [cx + 0.55, cy - 1.15],   # right leg outer
        [cx + 0.10, cy - 1.15],   # right leg inner
        [cx + 0.05, cy - 0.25],   # crotch right
        [cx - 0.05, cy - 0.25],   # crotch left
        [cx - 0.10, cy - 1.15],   # left leg inner
        [cx - 0.55, cy - 1.15],   # left leg outer
        [cx - 0.75, cy - 0.10],   # left side waist
    ])
    ax.add_patch(Polygon(
        body_pts, closed=True,
        facecolor=fill_color, edgecolor=edge_color,
        linewidth=line_width, zorder=zorder, alpha=alpha,
        joinstyle='round',
    ))
    # Arms
    left_arm = np.array([
        [cx - 0.55, cy + 0.50],
        [cx - 0.92, cy + 0.15],
        [cx - 1.02, cy - 0.45],
        [cx - 0.75, cy - 0.50],
        [cx - 0.68, cy + 0.05],
        [cx - 0.45, cy + 0.35],
    ])
    right_arm = np.array([
        [cx + 0.55, cy + 0.50],
        [cx + 0.92, cy + 0.15],
        [cx + 1.02, cy - 0.45],
        [cx + 0.75, cy - 0.50],
        [cx + 0.68, cy + 0.05],
        [cx + 0.45, cy + 0.35],
    ])
    ax.add_patch(Polygon(left_arm, closed=True,
                        facecolor=fill_color, edgecolor=edge_color,
                        linewidth=line_width, zorder=zorder, alpha=alpha,
                        joinstyle='round'))
    ax.add_patch(Polygon(right_arm, closed=True,
                        facecolor=fill_color, edgecolor=edge_color,
                        linewidth=line_width, zorder=zorder, alpha=alpha,
                        joinstyle='round'))


# LEFT: vibrant / conscious figure (purple with glow)
vib_cx = p2_cx - 1.25
vib_cy = p2_cy - 0.20

# Glow halo behind the head — several translucent ellipses
for r, a in [(0.75, 0.10), (0.60, 0.16), (0.48, 0.22)]:
    ax.add_patch(Circle(
        (vib_cx, vib_cy + 1.05), r,
        facecolor=purple_border, edgecolor='none',
        alpha=a, zorder=2,
    ))

draw_silhouette(ax, vib_cx, vib_cy,
                edge_color=purple_border,
                fill_color=purple_fill,
                line_width=2.0, zorder=4)

# Small spark inside head = "experience"
ax.add_patch(Circle((vib_cx, vib_cy + 1.05), 0.10,
                    facecolor=purple_border, edgecolor='none', zorder=6))
# A few radiating lines for the spark
for ang in np.linspace(0, 2 * np.pi, 8, endpoint=False):
    x0 = vib_cx + 0.14 * np.cos(ang)
    y0 = vib_cy + 1.05 + 0.14 * np.sin(ang)
    x1 = vib_cx + 0.24 * np.cos(ang)
    y1 = vib_cy + 1.05 + 0.24 * np.sin(ang)
    ax.plot([x0, x1], [y0, y1], color=purple_border, lw=1.2, zorder=6)

# RIGHT: hollow zombie figure (grey, empty)
zom_cx = p2_cx + 1.25
zom_cy = p2_cy - 0.20

draw_silhouette(ax, zom_cx, zom_cy,
                edge_color=dull_grey,
                fill_color=dull_grey_fill,
                line_width=1.8, zorder=4, alpha=0.95)

# Empty head — a faint hollow circle to emphasise "nothing inside"
ax.add_patch(Circle((zom_cx, zom_cy + 1.05), 0.12,
                    facecolor='white', edgecolor=dull_grey,
                    linewidth=1.0, linestyle='--', zorder=6))

# Small labels above each figure
ax.text(vib_cx, vib_cy + 1.70, 'conscious',
        ha='center', va='center', fontsize=8.5,
        color=purple_border, fontfamily='sans-serif',
        fontweight='bold', zorder=7)
ax.text(zom_cx, zom_cy + 1.70, 'zombie',
        ha='center', va='center', fontsize=8.5,
        color=dull_grey, fontfamily='sans-serif',
        fontweight='bold', zorder=7)

# Equals-behaviour / not-equals-experience annotation between them
eq_y = p2_cy - 0.20
ax.plot([p2_cx - 0.25, p2_cx + 0.25], [eq_y + 0.10, eq_y + 0.10],
        color=subtle_text, lw=1.3, zorder=5)
ax.plot([p2_cx - 0.25, p2_cx + 0.25], [eq_y - 0.10, eq_y - 0.10],
        color=subtle_text, lw=1.3, zorder=5)
ax.text(p2_cx, eq_y + 0.55, 'same behaviour',
        ha='center', va='center', fontsize=7.5,
        color=subtle_text, fontfamily='sans-serif', style='italic',
        zorder=7)
ax.text(p2_cx, eq_y - 0.55, 'different inside',
        ha='center', va='center', fontsize=7.5,
        color=subtle_text, fontfamily='sans-serif', style='italic',
        zorder=7)

# Panel label + tagline
ax.text(p2_cx, panel_y + panel_h - 0.45, 'Zombie',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=8)
ax.text(p2_cx, panel_y + 0.42, 'Functional identity without experience',
        ha='center', va='center', fontsize=9,
        color=subtle_text, fontfamily='sans-serif',
        style='italic', zorder=8)


# ─── Panel 3: Lived Body ────────────────────────────────────────────
p3x = panels_x[2]
p3_cx = p3x + panel_w / 2
p3_cy = panel_y + panel_h / 2 + 0.05

# Draw ground line (subtle)
ground_y = panel_y + 0.95
ax.plot([p3x + 0.35, p3x + panel_w - 0.35], [ground_y, ground_y],
        color=panel_edge, lw=1.0, zorder=2)

# Figure: head + body, with branches spreading from the arms
fig_cx = p3_cx
fig_cy = p3_cy + 0.05

# Halo / aura suggesting embeddedness
for r, a in [(1.85, 0.06), (1.40, 0.10), (1.00, 0.12)]:
    ax.add_patch(Circle(
        (fig_cx, fig_cy + 0.25), r,
        facecolor=blue_border, edgecolor='none',
        alpha=a, zorder=2,
    ))

# Head
ax.add_patch(Circle(
    (fig_cx, fig_cy + 1.15), 0.32,
    facecolor=blue_fill, edgecolor=blue_border,
    linewidth=2.0, zorder=5,
))

# Torso (tapered)
torso_pts = np.array([
    [fig_cx - 0.40, fig_cy + 0.80],
    [fig_cx + 0.40, fig_cy + 0.80],
    [fig_cx + 0.25, fig_cy - 0.20],
    [fig_cx - 0.25, fig_cy - 0.20],
])
ax.add_patch(Polygon(
    torso_pts, closed=True,
    facecolor=blue_fill, edgecolor=blue_border,
    linewidth=2.0, zorder=5, joinstyle='round',
))

# ─── Branches spreading from the arms into the environment ──────────
def draw_branch(ax, x0, y0, angle_deg, length, depth,
                color=blue_border, lw=2.2, zorder=6):
    """Recursively draw a branching tree limb."""
    if depth == 0 or length < 0.08:
        # A little leaf dot at the tip
        ax.add_patch(Circle(
            (x0, y0), 0.06,
            facecolor=blue_fill, edgecolor=color,
            linewidth=0.9, zorder=zorder + 1,
        ))
        return
    angle = np.deg2rad(angle_deg)
    x1 = x0 + length * np.cos(angle)
    y1 = y0 + length * np.sin(angle)
    ax.plot([x0, x1], [y0, y1], color=color,
            lw=lw, solid_capstyle='round', zorder=zorder)
    # Recurse into two sub-branches
    new_len = length * 0.68
    new_lw = max(lw * 0.68, 0.7)
    draw_branch(ax, x1, y1, angle_deg - 28, new_len, depth - 1,
                color=color, lw=new_lw, zorder=zorder)
    draw_branch(ax, x1, y1, angle_deg + 28, new_len, depth - 1,
                color=color, lw=new_lw, zorder=zorder)


# Left arm -> branch going up-left
left_shoulder = (fig_cx - 0.38, fig_cy + 0.75)
draw_branch(ax, left_shoulder[0], left_shoulder[1],
            angle_deg=155, length=0.75, depth=3,
            color=blue_border, lw=2.4, zorder=6)

# Right arm -> branch going up-right
right_shoulder = (fig_cx + 0.38, fig_cy + 0.75)
draw_branch(ax, right_shoulder[0], right_shoulder[1],
            angle_deg=25, length=0.75, depth=3,
            color=blue_border, lw=2.4, zorder=6)

# ─── Roots going down from the base into the ground ─────────────────
def draw_root(ax, x0, y0, angle_deg, length, depth,
              color=arrow_grey, lw=1.8, zorder=4):
    if depth == 0 or length < 0.08:
        return
    angle = np.deg2rad(angle_deg)
    x1 = x0 + length * np.cos(angle)
    y1 = y0 + length * np.sin(angle)
    ax.plot([x0, x1], [y0, y1], color=color,
            lw=lw, alpha=0.85, solid_capstyle='round', zorder=zorder)
    new_len = length * 0.62
    new_lw = max(lw * 0.65, 0.6)
    draw_root(ax, x1, y1, angle_deg - 22, new_len, depth - 1,
              color=color, lw=new_lw, zorder=zorder)
    draw_root(ax, x1, y1, angle_deg + 22, new_len, depth - 1,
              color=color, lw=new_lw, zorder=zorder)


root_start_y = fig_cy - 0.20
# central root
draw_root(ax, fig_cx, root_start_y, -90, 0.55, 3,
          color=arrow_grey, lw=1.7)
# side roots
draw_root(ax, fig_cx - 0.15, root_start_y, -110, 0.45, 3,
          color=arrow_grey, lw=1.4)
draw_root(ax, fig_cx + 0.15, root_start_y, -70, 0.45, 3,
          color=arrow_grey, lw=1.4)

# Panel label + tagline
ax.text(p3_cx, panel_y + panel_h - 0.45, 'Lived Body',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=8)
ax.text(p3_cx, panel_y + 0.42, 'Mind requires an organism',
        ha='center', va='center', fontsize=9,
        color=subtle_text, fontfamily='sans-serif',
        style='italic', zorder=8)


# ─── Footer caption ───
ax.text(8, 0.30, 'Can Machines Be Conscious? Part 5',
        ha='center', va='center', fontsize=10,
        color=subtle_text, fontfamily='sans-serif', style='italic',
        zorder=5)

# ─── Save ───
output_path = r'D:\Projects\Medium\AI Consciousness\05-objections\header_objections.png'
plt.savefig(output_path, dpi=150, facecolor='white', edgecolor='none')
plt.close()
print(f"Saved to: {output_path}")
