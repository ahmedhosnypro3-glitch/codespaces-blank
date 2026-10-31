#!/usr/bin/env python3
"""Render slide 005's banner assets: the decision equation and the class rules.

Both come out as 600-dpi transparent-free PNGs whose axes map 1:1 onto the
original lecture-frame pixels, so the build script can place them at
px/72 inches without rescaling.

Equation colours follow the original frame: the X inside d(X) and the b*1 tail
are red, everything else black, W is bold with an underline.
"""
import json
import os
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["mathtext.fontset"] = "stix"
matplotlib.rcParams["font.family"] = "STIXGeneral"
import matplotlib.pyplot as plt
import numpy as np

BUILD = os.path.dirname(os.path.abspath(__file__))
DPI = 600
BLACK = "#000000"
RED = "#C00000"
BLUE = "#0000FF"

EQ_X0, EQ_X1 = 84, 526
EQ_Y0, EQ_Y1 = 279, 310          # y grows downward in the original frame

# body: everything up to the red "b*1" tail, rendered as one mathtext string so
# the operator/subscript kerning comes from the font rather than from hand-placed
# pieces (mathtext's "=" is wider than Times' and drifts when piece-placed).
EQ_BODY = (88, 300, BLACK, 20,
           r"$\mathrm{d}(X) = \mathbf{W}^{\mathrm{T}} \mathbf{X} = "
           r"w_1x_1 + w_2x_2 + ..... + w_nx_n + $")
# superscript T sits on its own baseline
EQ_SUP = (175, 290, BLACK, 13, r"$\mathrm{T}$")
# red tail, bold, on the original's baseline
EQ_TAIL = (426, 301, RED, 20, r"$b*1$")
# red double arrow between the equation and the rule group
EQ_ARROW = (503, 300, RED, 20, r"$\Rightarrow$")

RULES_X0, RULES_X1 = 555, 745
RULES_Y0, RULES_Y1 = 264, 328
RULE_LINES = [
    (559, 280, u">0 ⇒ Class I"),
    (558, 302, u"<0 ⇒ Class II"),
    (559, 324, u"=0 ⇒ Undefined Class"),
]


def make_axes(x0, x1, y0, y1):
    fig = plt.figure(figsize=((x1 - x0) / 72.0, (y1 - y0) / 72.0), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)          # inverted: frame y grows downward
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    return fig, ax


def _measure_string(txt, size):
    """Render a single mathtext string and return its data-space ink width."""
    fig, ax = make_axes(0, 100, 0, 1)
    ax.text(0, 0, txt, ha="left", va="baseline", fontsize=size, color=BLACK)
    fig.canvas.draw()
    bb = ax.texts[0].get_window_extent(fig.canvas.get_renderer())
    (x0, _), (x1, _) = ax.transData.inverted().transform(
        [(bb.x0, bb.y0), (bb.x1, bb.y1)])
    plt.close(fig)
    return x1 - x0


def render_equation():
    fig, ax = make_axes(EQ_X0, EQ_X1, EQ_Y0, EQ_Y1)
    for spec in (EQ_BODY, EQ_SUP, EQ_TAIL, EQ_ARROW):
        x, base, colour, size, txt = spec
        ax.text(x, base, txt, ha="left", va="baseline", fontsize=size,
                color=colour)
    # underline under the bold W: it starts after "d(X) = "
    prefix_w = _measure_string(r"$\mathrm{d}(X) = $", 20)
    w_w = _measure_string(r"$\mathbf{W}$", 20)
    xw0 = EQ_BODY[0] + prefix_w
    ax.plot([xw0, xw0 + w_w], [301, 301], color=BLACK, linewidth=0.8,
            solid_capstyle="butt")
    out = os.path.join(BUILD, "slide_005_eq.png")
    fig.savefig(out, dpi=DPI, facecolor="white")
    plt.close(fig)
    return out


def render_rules():
    fig, ax = make_axes(RULES_X0, RULES_X1, RULES_Y0, RULES_Y1)
    for x, base, txt in RULE_LINES:
        ax.text(x, base, txt, ha="left", va="baseline", fontsize=18,
                color=BLUE)
    out = os.path.join(BUILD, "slide_005_rules.png")
    fig.savefig(out, dpi=DPI, facecolor="white")
    plt.close(fig)
    return out


if __name__ == "__main__":
    eq = render_equation()
    rules = render_rules()
    meta = {
        "equation": {
            "image": "slide_005_eq.png",
            "x_px": EQ_X0, "y_px": EQ_Y0,
            "w_px": EQ_X1 - EQ_X0, "h_px": EQ_Y1 - EQ_Y0,
            "dpi": DPI,
            "mathtext": ("d(X) = \\mathbf{W}^{\\mathrm{T}} \\mathbf{X} = "
                         "w_1x_1 + w_2x_2 + ...... + w_nx_n + b*1"),
            "font_size_pt": 20, "color": "#000000",
        },
        "rules": {
            "image": "slide_005_rules.png",
            "x_px": RULES_X0, "y_px": RULES_Y0,
            "w_px": RULES_X1 - RULES_X0, "h_px": RULES_Y1 - RULES_Y0,
            "dpi": DPI,
        },
    }
    with open(os.path.join(BUILD, "slide_005_assets.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    print(json.dumps(meta, indent=2))
