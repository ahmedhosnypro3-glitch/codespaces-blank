#!/usr/bin/env python3
"""Region-specific PIL adjudication for the four remaining slide-021 crop verdicts.

Frame space is 960x540, 1px = 1pt (AGENTS.md). render_10.png is the 150dpi render
(2001x1125, SC = 2001/960). ALL bboxes are reported in FRAME px on both images so a
claim can be checked directly. Every crop claim is measured in BOTH images before any
build change is proposed; a claim the original does not show is refuted with numbers.
"""
import sys

import numpy as np
from PIL import Image

R = "/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
SC = 2001 / 960.0
o = np.asarray(Image.open(R + "unique_slides/slide_021.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(R + "recreated_pptx/qa/slide021/render_10.png").convert("RGB")).astype(int)


def cls(name):
    def p(s):
        if name == "blue":
            return (s[:, :, 2] > s[:, :, 0] + 40) & (s[:, :, 2] > s[:, :, 1] + 40) & (s[:, :, 2] > 90)
        if name == "red":
            return (s[:, :, 0] > 120) & (s[:, :, 1] < 95) & (s[:, :, 2] < 95)
        if name == "green":
            return (s[:, :, 1] > 110) & (s[:, :, 0] < 110) & (s[:, :, 2] < 110)
        if name == "hilite":
            return (s[:, :, 0] > 200) & (s[:, :, 1] > 200) & (np.abs(s[:, :, 2].astype(int) - 150) < 60)
        return s.mean(axis=2) < 150
    return p


def measure(nm, x0, y0, x1, y1, col):
    out = {}
    for tag, a, inv in (("ORIG", o, False), ("REND", r, True)):
        if inv:
            xa, ya, xb, yb = x0 * SC, y0 * SC, x1 * SC, y1 * SC
            s = a[int(round(ya)):int(round(yb)), int(round(xa)):int(round(xb))]
        else:
            s = a[int(y0):int(y1), int(x0):int(x1)]
        m = cls(col)(s)
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            out[tag] = ("0", None)
            continue
        if inv:
            f = lambda v, base: round((base + v) / SC, 1)
            bb = (f(xs.min(), xa), f(xs.max(), xa), f(ys.min(), ya), f(ys.max(), ya))
        else:
            bb = (x0 + int(xs.min()), x0 + int(xs.max()), y0 + int(ys.min()), y0 + int(ys.max()))
        out[tag] = (str(int(m.sum())), bb)
    print(f"   {nm:<32} [{col:6s}] ORIG n={out['ORIG'][0]:<7} frame-bbox {out['ORIG'][1]}")
    print(f"   {'':<32}          REND n={out['REND'][0]:<7} frame-bbox {out['REND'][1]}")
    return out


print("### CROP-REGION PIL MEASUREMENTS (render_10 vs original), slide 021 — FRAME px ###\n")

print("--- top_chain  x332..802 y182..218 : |X^T X| = 0 / Singular Matrix / No Inverse ---")
measure("chain1 dark ink", 332, 182, 802, 218, "dark")
measure("chain1 red ink (No Inverse)", 332, 182, 802, 218, "red")
measure("chain1 blue ink (two arrows)", 332, 182, 802, 218, "blue")

print("\n--- mid_table_eq x80..322 y290..402 : label / lambda=3 / 3x3 / 3 highlight bands ---")
measure("regmat label + table dark ink", 80, 290, 322, 402, "dark")
measure("lambda=3 green ink", 245, 304, 289, 321, "green")
for i, (bx0, by0, bx1, by1) in enumerate([(107, 344, 143, 357), (173, 362, 210, 374), (243, 379, 279, 392)]):
    measure(f"hilite band r{i+1}c{i+1} ink", bx0, by0, bx1, by1, "dark")
    measure(f"hilite band r{i+1}c{i+1} fill", bx0, by0, bx1, by1, "hilite")

print("\n--- mid_chain  x332..892 y348..382 : |X^T X| = 5685 / Non-Singular / Inverse Exists ---")
measure("chain2 dark ink", 332, 348, 892, 382, "dark")
measure("chain2 red ink", 332, 348, 892, 382, "red")
measure("chain2 blue ink (two arrows)", 332, 348, 892, 382, "blue")

print("\n--- bot_eq_table x148..642 y450..519 : (X^T X + lambda I)^-1 / long arrow / inverse 3x3 ---")
measure("bottom dark ink", 148, 450, 642, 519, "dark")
measure("bottom blue ink (long arrow)", 148, 450, 642, 519, "blue")
measure("invexpr red ink", 155, 466, 289, 492, "red")
measure("P3 inverse table ink", 421, 454, 626, 514, "dark")

print("\n### BANKED REFUTATIONS (do not re-fix) ###")
print("   'strike/slash marker on the 15 cell' (attempt-3 claim 7): REFUTED. The original's")
print("   P1 '15' is a plain digit, x263..275 y177..187, n=49; leg-1 attempt 10 itself")
print("   classified it as a capture artifact. Nothing to fix in either image.")
print("   Missing TOP stroke: house chrome by design (AGENTS.md). Never a discrepancy.")
print("   det5685 typo / row-pitch / saturated-yellow: fixed in the attempt-10 build (see report).")

print("\n### HOUSE CHROME LAWS (settle first) ###")
print("   panel x54..903 y45..540; C00000 strokes L/R/BOTTOM only; NO TOP STROKE; badge FDFD96")
print("   + purple ring 6A5ACD centered (876,73) d~35; typed-vs-handwritten ink <= MINOR;")
print("   professional 2D equation format is a mandated upgrade, not a discrepancy.")
sys.exit(0)
