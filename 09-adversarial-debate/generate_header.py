import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon
import numpy as np

# Figure setup: 1600x900 at 150 DPI
fig, ax = plt.subplots(figsize=(1600 / 150, 900 / 150), dpi=150)
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

blue_border = '#3b82f6'
blue_fill = '#dbeafe'

red_border = '#ef4444'
red_fill = '#fee2e2'

purple_border = '#8b5cf6'
purple_fill = '#ede9fe'

arrow_grey = '#475569'
bubble_edge = '#CBD5E1'

# ─── Title & subtitle ───
ax.text(8, 8.15, 'Two AI Philosophers Argue About Consciousness',
        ha='center', va='center', fontsize=18, fontweight='bold',
        color=dark_text, fontfamily='sans-serif')
ax.text(8, 7.65, 'Can Machines Be Conscious?  Part 7',
        ha='center', va='center', fontsize=11, color=subtle_text,
        fontfamily='sans-serif', style='italic')

# ─── Single wide panel ───
panel_x = 0.5
panel_y = 1.1
panel_w = 15.0
panel_h = 5.85

panel = FancyBboxPatch((panel_x, panel_y), panel_w, panel_h,
                       boxstyle="round,pad=0.15",
                       facecolor=panel_bg_color, edgecolor=panel_edge,
                       linewidth=1.5, zorder=2)
ax.add_patch(panel)


# ─── Helper to draw a stylized robot/agent ───
def draw_agent(cx, cy, body_fill, body_border, scale=1.0, zorder=5):
    """
    Stylized robot icon:
    - trapezoidal body
    - circular head
    - short antenna with small ball on top
    - two small square 'eyes'
    """
    # Body (trapezoid)
    body_top_w = 1.4 * scale
    body_bot_w = 1.8 * scale
    body_h = 1.2 * scale
    body_top_y = cy - 0.1 * scale
    body_bot_y = body_top_y - body_h
    body_pts = [
        (cx - body_top_w / 2, body_top_y),
        (cx + body_top_w / 2, body_top_y),
        (cx + body_bot_w / 2, body_bot_y),
        (cx - body_bot_w / 2, body_bot_y),
    ]
    body = Polygon(body_pts, closed=True, facecolor=body_fill,
                   edgecolor=body_border, linewidth=1.8, zorder=zorder)
    ax.add_patch(body)

    # Neck
    neck_w = 0.35 * scale
    neck_h = 0.15 * scale
    ax.add_patch(Rectangle((cx - neck_w / 2, body_top_y),
                           neck_w, neck_h,
                           facecolor=body_fill, edgecolor=body_border,
                           linewidth=1.5, zorder=zorder))

    # Head
    head_r = 0.65 * scale
    head_cy = body_top_y + neck_h + head_r
    head = Circle((cx, head_cy), head_r,
                  facecolor=body_fill, edgecolor=body_border,
                  linewidth=1.8, zorder=zorder)
    ax.add_patch(head)

    # Eyes (small squares)
    eye_s = 0.12 * scale
    eye_off_x = 0.22 * scale
    eye_y = head_cy + 0.05 * scale
    for ex in (cx - eye_off_x, cx + eye_off_x):
        ax.add_patch(Rectangle((ex - eye_s / 2, eye_y - eye_s / 2),
                               eye_s, eye_s,
                               facecolor=body_border, edgecolor='none',
                               zorder=zorder + 1))

    # Mouth line
    mouth_w = 0.28 * scale
    mouth_y = head_cy - 0.25 * scale
    ax.plot([cx - mouth_w / 2, cx + mouth_w / 2],
            [mouth_y, mouth_y],
            color=body_border, linewidth=1.6, zorder=zorder + 1,
            solid_capstyle='round')

    # Antenna
    ant_base_y = head_cy + head_r
    ant_top_y = ant_base_y + 0.35 * scale
    ax.plot([cx, cx], [ant_base_y, ant_top_y],
            color=body_border, linewidth=1.6, zorder=zorder)
    ax.add_patch(Circle((cx, ant_top_y + 0.08 * scale), 0.1 * scale,
                        facecolor=body_border, edgecolor='none',
                        zorder=zorder + 1))

    # Return the top of the head / antenna for labels
    return ant_top_y + 0.18 * scale


# ─── Helper to draw a speech bubble ───
def draw_speech_bubble(cx, cy, w, h, text, text_color, fill, border,
                       tail_side='down-left', zorder=6):
    """
    Rounded-rectangle speech bubble with a small triangular tail.
    tail_side: 'down-left', 'down-right', 'down-center'
    """
    # Bubble body
    bub = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                         boxstyle="round,pad=0.05,rounding_size=0.18",
                         facecolor=fill, edgecolor=border,
                         linewidth=1.5, zorder=zorder)
    ax.add_patch(bub)

    # Tail
    if tail_side == 'down-left':
        tail_pts = [(cx - w / 2 + 0.25, cy - h / 2),
                    (cx - w / 2 + 0.55, cy - h / 2),
                    (cx - w / 2 + 0.15, cy - h / 2 - 0.3)]
    elif tail_side == 'down-right':
        tail_pts = [(cx + w / 2 - 0.55, cy - h / 2),
                    (cx + w / 2 - 0.25, cy - h / 2),
                    (cx + w / 2 - 0.15, cy - h / 2 - 0.3)]
    else:  # down-center
        tail_pts = [(cx - 0.15, cy - h / 2),
                    (cx + 0.15, cy - h / 2),
                    (cx, cy - h / 2 - 0.3)]
    tail = Polygon(tail_pts, closed=True,
                   facecolor=fill, edgecolor=border,
                   linewidth=1.5, zorder=zorder)
    ax.add_patch(tail)
    # Cover the top seam of the tail so outline looks clean
    ax.plot([tail_pts[0][0] + 0.02, tail_pts[1][0] - 0.02],
            [tail_pts[0][1], tail_pts[1][1]],
            color=fill, linewidth=2.0, zorder=zorder + 0.5)

    # Text
    ax.text(cx, cy, text,
            ha='center', va='center', fontsize=11, color=text_color,
            fontfamily='monospace', fontweight='bold', zorder=zorder + 2)


# ─── Layout: three agents across the wide panel ───
panel_cx = panel_x + panel_w / 2

# Positions
left_cx = panel_x + 3.0       # Professor Turing (FOR)
right_cx = panel_x + panel_w - 3.0  # Professor Searle-Thompson (AGAINST)
judge_cx = panel_cx           # Judge

# Baseline y for bodies (feet line up)
debater_baseline = panel_y + 2.1
judge_baseline = panel_y + 2.55  # judge slightly elevated

# ─── Left: Professor Turing (blue, FOR) ───
draw_agent(left_cx, debater_baseline, blue_fill, blue_border, scale=1.05)

# Speech bubble for Turing: "Φ > 0"
draw_speech_bubble(
    cx=left_cx + 1.6, cy=debater_baseline + 2.25,
    w=1.7, h=0.9,
    text='Φ > 0',
    text_color=blue_border, fill='white', border=blue_border,
    tail_side='down-left',
)

# Label below
ax.text(left_cx, panel_y + 0.85, 'Professor Turing',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=6)
ax.text(left_cx, panel_y + 0.5, 'FOR machine consciousness',
        ha='center', va='center', fontsize=9.5, style='italic',
        color=blue_border, fontfamily='sans-serif', zorder=6)

# ─── Right: Professor Searle-Thompson (red, AGAINST) ───
draw_agent(right_cx, debater_baseline, red_fill, red_border, scale=1.05)

# Speech bubble: "just symbols"
draw_speech_bubble(
    cx=right_cx - 1.75, cy=debater_baseline + 2.25,
    w=2.1, h=0.9,
    text='"just symbols"',
    text_color=red_border, fill='white', border=red_border,
    tail_side='down-right',
)

ax.text(right_cx, panel_y + 0.85, 'Professor Searle-Thompson',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=6)
ax.text(right_cx, panel_y + 0.5, 'AGAINST machine consciousness',
        ha='center', va='center', fontsize=9.5, style='italic',
        color=red_border, fontfamily='sans-serif', zorder=6)

# ─── Centre: Judge (purple, smaller, elevated) ───
judge_top = draw_agent(judge_cx, judge_baseline, purple_fill, purple_border,
                       scale=0.82)

# Small geometric gavel above judge's head (hammer shape)
gavel_cx = judge_cx + 0.95
gavel_cy = judge_baseline + 1.9
# Gavel head (rectangle)
gh_w, gh_h = 0.55, 0.22
ax.add_patch(Rectangle((gavel_cx - gh_w / 2, gavel_cy - gh_h / 2),
                       gh_w, gh_h,
                       facecolor=purple_fill, edgecolor=purple_border,
                       linewidth=1.5, zorder=6))
# Gavel band
ax.add_patch(Rectangle((gavel_cx - 0.08, gavel_cy - gh_h / 2),
                       0.16, gh_h,
                       facecolor=purple_border, edgecolor='none',
                       zorder=7))
# Gavel handle
ax.plot([gavel_cx, gavel_cx + 0.7],
        [gavel_cy - 0.01, gavel_cy - 0.45],
        color=purple_border, linewidth=2.4, zorder=6,
        solid_capstyle='round')

# Judge label
ax.text(judge_cx, panel_y + 0.85, 'Judge',
        ha='center', va='center', fontsize=12, fontweight='bold',
        color=dark_text, fontfamily='sans-serif', zorder=6)
ax.text(judge_cx, panel_y + 0.5, 'moderator',
        ha='center', va='center', fontsize=9.5, style='italic',
        color=purple_border, fontfamily='sans-serif', zorder=6)

# ─── Bi-directional arrows between the two debaters ───
# Arrows sit in the lower chest region, going around (over) the judge.
# Two separate arrows at slightly different y for a clean look.

arrow_y_top = debater_baseline + 0.55      # top arrow: left -> right
arrow_y_bot = debater_baseline + 0.20      # bottom arrow: right -> left

left_edge = left_cx + 1.15      # just outside Turing's body
right_edge = right_cx - 1.15    # just outside Searle-Thompson's body
judge_gap_left = judge_cx - 1.0
judge_gap_right = judge_cx + 1.0

# Top arrow: left -> right, drawn in two segments that skip over the judge
ax.annotate('', xy=(judge_gap_left, arrow_y_top),
            xytext=(left_edge, arrow_y_top),
            arrowprops=dict(arrowstyle='-', color=arrow_grey,
                            lw=1.8), zorder=4)
arr_top = FancyArrowPatch(
    (judge_gap_right, arrow_y_top),
    (right_edge, arrow_y_top),
    arrowstyle='->,head_width=0.28,head_length=0.42',
    color=arrow_grey, lw=1.8, zorder=4,
)
ax.add_patch(arr_top)

# Bottom arrow: right -> left
ax.annotate('', xy=(judge_gap_right, arrow_y_bot),
            xytext=(right_edge, arrow_y_bot),
            arrowprops=dict(arrowstyle='-', color=arrow_grey,
                            lw=1.8), zorder=4)
arr_bot = FancyArrowPatch(
    (judge_gap_left, arrow_y_bot),
    (left_edge, arrow_y_bot),
    arrowstyle='->,head_width=0.28,head_length=0.42',
    color=arrow_grey, lw=1.8, zorder=4,
)
ax.add_patch(arr_bot)

# Subtle "3 rounds" label between the two arrows, placed just below the judge
ax.text(judge_cx, debater_baseline - 0.15, '3 rounds',
        ha='center', va='center', fontsize=9, style='italic',
        color=subtle_text, fontfamily='sans-serif', zorder=6)

# ─── Footer caption ───
ax.text(8, 0.55, 'An adversarial debate between two LLM agents',
        ha='center', va='center', fontsize=10,
        color=subtle_text, fontfamily='sans-serif', style='italic',
        zorder=5)

# ─── Save ───
output_path = r'D:\Projects\Medium\AI Consciousness\07-adversarial-debate\header_debate.png'
plt.savefig(output_path, dpi=150, facecolor='white', edgecolor='none')
plt.close()
print(f"Saved to: {output_path}")
