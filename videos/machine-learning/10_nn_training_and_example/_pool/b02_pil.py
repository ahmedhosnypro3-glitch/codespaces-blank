#!/usr/bin/env python3
"""Ink-coverage probe for b02 renders vs originals (960-space coords)."""
import sys
from PIL import Image

def ink(im, box, bg_tol=28):
    x0, y0, x1, y1 = box
    sx = im.width / 960.0
    sy = im.height / 540.0
    crop = im.crop((int(x0 * sx), int(y0 * sy), int(x1 * sx), int(y1 * sy)))
    px = list(crop.convert("RGB").getdata())
    if not px:
        return 0.0, (0, 0, 0)
    n = len(px)
    dark = sum(1 for r, g, b in px if max(r, g, b) < 190)
    mean = tuple(sum(c[i] for c in px) // n for i in range(3))
    return dark / n, mean

CASES = {
    "s3_for_layer_box": [(58, 405, 308, 515), (58, 405, 308, 515)],
    "s3_error_box":     [(740, 405, 915, 485), (740, 405, 915, 485)],
    "s3_node_bias":     [(95, 365, 185, 398), (95, 365, 185, 398)],
    "s3_outputs":       [(615, 160, 720, 350), (615, 160, 720, 350)],
    "s4_def_box":       [(135, 103, 300, 146), (135, 103, 300, 146)],
    "s4_deriv_row1":    [(135, 243, 640, 280), (135, 243, 640, 280)],
    "s4_deriv_row2":    [(135, 323, 640, 360), (135, 323, 640, 360)],
    "s4_deriv_row3":    [(135, 403, 640, 445), (135, 403, 640, 445)],
    "s4_final_box":     [(695, 375, 960, 480), (695, 375, 960, 480)],
    "s4_plot":          [(695, 75, 900, 320), (695, 75, 900, 320)],
}

def main():
    render, original = sys.argv[1], sys.argv[2]
    r = Image.open(render).convert("RGB")
    o = Image.open(original).convert("RGB")
    for name, (rbox, obox) in CASES.items():
        ri, rm = ink(r, rbox)
        oi, om = ink(o, obox)
        print(f"{name:20s} render_ink={ri:6.3f} mean={rm}  orig_ink={oi:6.3f} mean={om}")

main()
