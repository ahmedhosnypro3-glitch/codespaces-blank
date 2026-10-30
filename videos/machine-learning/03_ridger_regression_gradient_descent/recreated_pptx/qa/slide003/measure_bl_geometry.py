#!/usr/bin/env python3
"""PIL ground truth: exact geometry of the bottom-left box (y-vector, "=",
design matrix bands + bracket + columns, "]" bracket, w-vector brackets).
Adjudicates the planned matrix shift: does the original really place the matrix
at x~205..395 with columns at 209/237/283/329/369 and a "]" right after?"""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
QA = B + "/recreated_pptx/qa/slide003"

a = np.asarray(Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(QA + "/render_17.png").convert("RGB").resize((960, 540), Image.LANCZOS)).astype(int)


def ink(im):
    return im.sum(axis=2) < 330


def vruns(im, x0, x1, y0, y1, minlen=4):
    """Vertical ink runs in a column strip -> bracket strokes / long rules."""
    m = ink(im)[y0:y1, x0:x1]
    colsum = m.sum(axis=0)
    present = colsum > (y1 - y0) * 0.25
    out, s = [], None
    for i, p in enumerate(present):
        if p and s is None:
            s = i
        elif not p and s is not None:
            if i - s >= minlen:
                out.append((s + x0, i - 1 + x0))
            s = None
    if s is not None and len(present) - s >= minlen:
        out.append((s + x0, len(present) - 1 + x0))
    return out


def hruns(im, y0, y1, x0, x1, minlen=4):
    """Horizontal ink runs in a row strip."""
    m = ink(im)[y0:y1, x0:x1]
    rowsum = m.sum(axis=1)
    present = rowsum > (x1 - x0) * 0.25
    out, s = [], None
    for i, p in enumerate(present):
        if p and s is None:
            s = i
        elif not p and s is not None:
            if i - s >= minlen:
                out.append((s + y0, i - 1 + y0))
            s = None
    if s is not None and len(present) - s >= minlen:
        out.append((s + y0, len(present) - 1 + y0))
    return out


def glyph_runs(im, y0, y1, x0, x1, gap=11):
    m = ink(im)[y0:y1, x0:x1]
    if m.sum() == 0:
        return []
    colsum = m.sum(axis=0)
    present = colsum > 0
    runs, s = [], None
    for i, p in enumerate(present):
        if p and s is None:
            s = i
        elif not p and s is not None:
            runs.append((s + x0, i - 1 + x0))
            s = None
    if s is not None:
        runs.append((s + x0, len(present) - 1 + x0))
    merged = []
    for rn in runs:
        if merged and rn[0] - merged[-1][1] < gap:
            merged[-1] = (merged[-1][0], rn[1])
        else:
            merged.append(rn)
    return merged


def bandfill(im):
    """Colored (non-white, non-dark) x-extent per matrix row band."""
    out = []
    for (nm, y0, y1) in [("yellow", 366, 392), ("cyan", 396, 424),
                         ("white", 426, 453), ("pink", 455, 479)]:
        strip = im[y0:y1, 150:540]
        colored = ((strip.max(axis=2) - strip.min(axis=2)) > 25) | (strip.sum(axis=2) < 700)
        cols = colored.any(axis=0)
        xs = np.where(cols)[0]
        if len(xs):
            out.append((nm, xs.min() + 150, xs.max() + 150))
        else:
            out.append((nm, None, None))
    return out


for tag, im in (("ORIG", a), ("REND17", r)):
    print(f"===== {tag} =====")
    print(" band fills (colored strip extents):")
    for nm, x0, x1 in bandfill(im):
        print(f"   {nm:7s} x{x0}..{x1}  (w {None if x0 is None else x1-x0+1})")
    print(" vertical bracket strokes (x150..540, y340..490, >=25% col ink):")
    for x0, x1 in vruns(im, 150, 540, 340, 490):
        print(f"   stroke x{x0}..{x1}")
    print(" long horizontal rules (x60..540, y330..500):")
    for y0, y1 in hruns(im, 60, 540, 330, 500):
        print(f"   rule y{y0}..{y1}")
    print(" matrix row glyph runs (x150..432):")
    for nm, y0, y1 in [("r1", 366, 392), ("r2", 396, 424),
                       ("r3", 426, 453), ("r4", 455, 479)]:
        rr = glyph_runs(im, y0, y1, 150, 432, gap=11)
        print(f"   {nm}: n={len(rr)} starts={[x0 for x0, _ in rr]}")
    print(" '=' zone glyph runs (x110..205, y350..470):")
    print("   ", glyph_runs(im, 350, 470, 110, 205, gap=11))
    print(" w-vector bracket strokes (x430..540, y330..490):")
    for x0, x1 in vruns(im, 430, 540, 330, 490):
        print(f"   stroke x{x0}..{x1}")
    print()
