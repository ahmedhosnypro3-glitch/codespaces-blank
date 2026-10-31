#!/usr/bin/env python3
"""Multi-class perceptron diagram for slide 006 (v2).

Measured against unique_slides/slide_006.jpg:
- activation boxes: white interior, pink border, blue step-function glyph (v1: empty)
- fan-in lines and Σ->activation arrows colour-coded red/blue/green (v1: gray)
- Σ circles pale-cyan with teal outlines + three small continuation dots
- input labels are plain bold text, no drawn circles (v1 circles bisected the glyphs)
- weight labels sit on their own fan-in diagonal, staggered in x (v1: table grid)
- no invented "Inputs/Weights" column headers (absent from the original)
- panel: white interior, thin steel-blue border (v1: red-bordered box)
- saved without bbox_inches='tight' so the PNG keeps its declared aspect ratio
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
import numpy as np
from pathlib import Path
import json

OUT_DIR = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FIG_W, FIG_H = 6.55, 4.71
DPI = 600

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_aspect('equal')
ax.axis('off')
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

WHITE = '#ffffff'
RED = '#cc0000'
BLUE = '#1a34c8'
GREEN = '#00a600'
BLACK = '#000000'
GLYPH = '#0000ee'
CYAN_FILL = '#ccffff'
CYAN_EDGE = '#40a0a0'
PINK_EDGE = '#ff44ff'
PANEL_EDGE = '#9aa8e0'


def gx(px):
    """Original frame x (px) -> graph inches from the panel's left edge."""
    return (px - 424) * (FIG_W / 472.0)


def gy(px):
    """Original frame y (px) -> graph inches (matplotlib y-up) from the panel bottom."""
    return FIG_H - (px - 160) * (FIG_H / 339.0)


SUM_Y = {'1': 186.0, '2': 319.0, 'm': 455.0}
X_SUM = gx(680)
X_INPUT = gx(432)
X_BOX = gx(719)
BOX_W = 47 * (FIG_W / 472.0)
BOX_H = 32 * (FIG_H / 339.0)
X_OUT = gx(790)

INPUT_ROWS = [212, 240, 285, 308, 332, 418]
INPUT_LABELS = ['x_1', 'x_2', 'x_3', r'\ldots', 'x_n', '1']

WEIGHTS = [
    (RED, [('w_{11}', 212, 498), ('w_{12}', 240, 538), ('w_{13}', 285, 512),
           ('w_{1n}', 332, 542), ('b_1', 418, 486)]),
    (BLUE, [('w_{21}', 205, 545), ('w_{22}', 232, 588), ('w_{23}', 282, 562),
            ('w_{2n}', 310, 600), ('b_2', 366, 518)]),
    (GREEN, [('w_{m1}', 215, 596), ('w_{m2}', 255, 624), ('w_{m3}', 300, 598),
             ('w_{mn}', 392, 618), ('b_m', 432, 572)]),
]
