#!/usr/bin/env python3
"""Probe v5: column-ink-profile signature comparison for the 4 BL annotation labels.
Render labels are known by construction (k14): GM(254,307)='Global Maxima',
LMx(312,396)='Local Maxima', LMn(313,458)='Local Minima', GMn(156,455)='Global Minima'.
Test: does orig label at each position match the render label at the SAME position
(same text) or at the crossed position (swapped)?"""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"
r = Image.open(f"{RJ}/slide025/render.png").convert("RGB").resize((960, 540), Image.LANCZOS)
o = Image.open(f"{NS}/unique_slides/slide_025.jpg").convert("RGB")
R = np.asarray(r).astype(int); O = np.asarray(o).astype(int)

POS = {"GM": (254, 307), "LMx": (312, 396), "LMn": (313, 458), "GMn": (156, 455)}
HW, HH = 46, 12

def textstrip(A, cx, cy):
    sub = A[cy - HH:cy + HH, cx - HW:cx + HW]
    lum = sub.sum(axis=2) / 3.0
    med = np.median(lum)
    m = (lum < med - 55)  # clearly darker than local background
    prof = m.sum(axis=0).astype(float)
    return prof, m

def prof_corr(p, q):
    # normalize to common length 60 and correlate
    n = 60
    pi = np.interp(np.linspace(0, len(p) - 1, n), np.arange(len(p)), p)
    qi = np.interp(np.linspace(0, len(q) - 1, n), np.arange(len(q)), q)
    pi -= pi.mean(); qi -= qi.mean()
    d = np.sqrt((pi * pi).sum()) * np.sqrt((qi * qi).sum())
    return float((pi * qi).sum() / d) if d else 0.0

strips = {}
for nm, A in (("R", R), ("O", O)):
    for k, (cx, cy) in POS.items():
        p, m = textstrip(A, cx, cy)
        strips[(nm, k)] = p
        xs = np.where(p > 0)[0]
        w = (xs.max() - xs.min() + 1) if len(xs) else 0
        print(f"{nm} {k} @({cx},{cy}): ink={int(m.sum()):4d} width={w:3d} peak_col={int(np.argmax(p)) if len(p) else '-'}")

print("\ncross-correlations (same-position vs swapped):")
# minima pair: GMn (left) <-> LMn (right)
for a, b in (("GMn", "LMn"),):
    print(f"  R-{a} vs O-{a} (same pos): {prof_corr(strips[('R', a)], strips[('O', a)]):.3f}")
    print(f"  R-{a} vs O-{b} (crossed) : {prof_corr(strips[('R', a)], strips[('O', b)]):.3f}")
    print(f"  R-{b} vs O-{b} (same pos): {prof_corr(strips[('R', b)], strips[('O', b)]):.3f}")
    print(f"  R-{b} vs O-{a} (crossed) : {prof_corr(strips[('R', b)], strips[('O', a)]):.3f}")
# maxima pair as control
for a, b in (("GM", "LMx"),):
    print(f"  R-{a} vs O-{a} (same pos): {prof_corr(strips[('R', a)], strips[('O', a)]):.3f}")
    print(f"  R-{a} vs O-{b} (crossed) : {prof_corr(strips[('R', a)], strips[('O', b)]):.3f}")
    print(f"  R-{b} vs O-{b} (same pos): {prof_corr(strips[('R', b)], strips[('O', b)]):.3f}")
    print(f"  R-{b} vs O-{a} (crossed) : {prof_corr(strips[('R', b)], strips[('O', a)]):.3f}")
