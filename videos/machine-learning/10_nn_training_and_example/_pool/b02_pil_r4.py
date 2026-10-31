#!/usr/bin/env python3
# b02 closed-loop PIL check: fresh renders vs original frames (150dpi, 4px tolerance).
from PIL import Image
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TOL_PX = 4
SCALE = 2000 / 960

def load(p): return Image.open(p).convert("RGB")

def edge_map(arr, bg):
    d = np.abs(arr.astype(int) - np.array(bg)).mean(axis=2)
    return d > 20

def check(label, orig_p, render_p, regions):
    orig, render = load(orig_p), load(render_p)
    rs = render.resize(orig.size, Image.LANCZOS)
    o, r = np.asarray(orig).astype(int), np.asarray(rs).astype(int)
    bg_o = int(np.median(o.reshape(-1, 3), axis=0).mean())
    om, rm = edge_map(o, [bg_o] * 3), edge_map(r, [bg_o] * 3)
    print(f"\n=== {label} (render {render.size}, orig {orig.size}, tol {TOL_PX}px @ {SCALE:.2f}x) ===")
    worst = 0.0
    for name, (x0, y0, x1, y1) in regions.items():
        oc, rc = om[y0:y1, x0:x1], rm[y0:y1, x0:x1]
        # chamfer-free: per-row/col ink-profile shift, crude but reports misalignment in px
        oy, ry = oc.mean(axis=1), rc.mean(axis=1)
        ox, rx = oc.mean(axis=0), rc.mean(axis=0)
        def shift(a, b):
            L = min(len(a), len(b)); a, b = a[:L], b[:L]
            best, bi = 1e9, 0
            for k in range(-TOL_PX * 2, TOL_PX * 2 + 1):
                bb = np.roll(b, k)
                d = np.abs(a - bb).mean()
                if d < best: best, bi = d, k
            return best, bi / SCALE
        dy, sy = shift(oy, ry); dx, sx = shift(ox, rx)
        ink_o, ink_r = oc.mean() * 100, rc.mean() * 100
        ok = (abs(sy) <= TOL_PX / SCALE + 0.01) and (abs(sx) <= TOL_PX / SCALE + 0.01)
        worst = max(worst, max(abs(sy), abs(sx)))
        print(f"  {name:<22} ink {ink_o:5.1f}%/{ink_r:5.1f}%  dx={sx:+.2f}px dy={sy:+.2f}px  {'OK' if ok else 'CHECK'}")
    print(f"  worst shift: {worst:.2f}px (budget {TOL_PX}px)")
    return worst <= TOL_PX

r3 = {
    "title": (60, 20, 500, 100), "badge": (860, 10, 930, 60),
    "input_target": (30, 75, 930, 120), "diagram": (60, 100, 880, 400),
    "input_dots": (65, 130, 95, 340), "cols_1_3": (150, 100, 560, 400),
    "error_bar": (560, 100, 625, 450), "outputs": (640, 120, 760, 360),
    "classes": (840, 120, 935, 360), "bottom_strip": (30, 405, 935, 540),
}
r4 = {
    "title": (40, 30, 430, 90), "badge": (860, 30, 935, 90),
    "left_eq": (55, 115, 400, 185), "diagram": (245, 130, 400, 210),
    "sigmoid_def": (495, 55, 665, 125), "graph": (650, 50, 890, 180),
    "eq_row2": (55, 200, 900, 275), "eq_row3": (55, 265, 700, 350),
    "final_box": (600, 320, 900, 420),
}
ok3 = check("SLIDE 3", f"{NS}/unique_slides/slide_003.jpg", f"{NS}/qa/slide003/rejudge/r4/render-1.png", r3)
ok4 = check("SLIDE 4", f"{NS}/unique_slides/slide_004.jpg", f"{NS}/qa/slide004/rejudge/r3/render-1.png", r4)
print(f"\nRESULT slide3={'PASS' if ok3 else 'FAIL'} slide4={'PASS' if ok4 else 'FAIL'}")
