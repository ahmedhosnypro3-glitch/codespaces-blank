#!/usr/bin/env python3
"""Probe v4: fixed-window label comparison. Build k14: 'Global Minima' centered
slide (156,455), 'Local Minima' centered (313,458). Extract text windows at both
positions from render and orig; compare ink width + NCC at matched positions."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"
r = Image.open(f"{RJ}/slide025/render.png").convert("RGB").resize((960, 540), Image.LANCZOS)
o = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")
R = np.asarray(r).astype(int); O = np.asarray(o).astype(int)
# text is dark on colored surface; use darkness relative to local background
def darkmask(A, x0, y0, x1, y1):
    sub = A[y0:y1, x0:x1]
    lum = sub.sum(axis=2) / 3.0
    med = np.median(lum)
    return lum < med - 45  # darker than local surface

POS = {"left@156": (156, 455), "right@313": (313, 458)}
def win(A, cx, cy, hw=42, hh=10):
    return darkmask(A, cx - hw, cy - hh, cx + hw, cy + hh)

for nm, A in (("render", R), ("orig", O)):
    for lbl, (cx, cy) in POS.items():
        m = win(A, cx, cy)
        cols = m.sum(axis=0)
        xs = np.where(cols > 0)[0]
        w = (xs.max() - xs.min() + 1) if len(xs) else 0
        hw2 = 42
        print(f"{nm} {lbl}: ink={int(m.sum()):4d} x-width={w:3d} x-range={(cx-hw2+xs.min(), cx-hw2+xs.max()) if len(xs) else None}")

def ncc(a, b):
    A = a.astype(float); B = b.astype(float)
    A -= A.mean(); B -= B.mean()
    d = np.sqrt((A*A).sum()) * np.sqrt((B*B).sum())
    return float((A*B).sum()/d) if d else 0.0

rl = win(R, 156, 455); rr = win(R, 313, 458)
ol = win(O, 156, 455); orr = win(O, 313, 458)
print(f"NCC(render-left, orig-left)   = {ncc(rl, ol):.3f}")
print(f"NCC(render-left, orig-right)  = {ncc(rl, orr):.3f}")
print(f"NCC(render-right, orig-right) = {ncc(rr, orr):.3f}")
print(f"NCC(render-right, orig-left)  = {ncc(rr, ol):.3f}")
# also y-scan: where is the text row in each window?
for nm, A in (("render", R), ("orig", O)):
    for lbl, (cx, cy) in POS.items():
        m = win(A, cx, cy, hw=42, hh=16)
        rows = m.sum(axis=1)
        hot = [i for i, v in enumerate(rows) if v >= 2]
        print(f"{nm} {lbl} text rows (y = {cy-16}+i): {[(cy-16+i, int(rows[i])) for i in hot]}")
