#!/usr/bin/env python3
"""Adjudicate_9j — objective glyph strings for the ORIGINAL's right point label.

Compares the ORIGINAL's two label glyph groups against:
  (a) the RENDER's own glyphs at the same place (ground truth "(7, 7)" —
      build/slide_032.js:200 draws exactly that string), and
  (b) Liberation Serif templates of the candidate glyph pairs at 9/10/11pt.

Best-aligned ink IoU over +/-2px shifts. Reports both per-group and whole-label.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

o = np.asarray(Image.open(V + "/unique_slides/slide_032.jpg").convert("L")).astype(float)
rim = Image.open(V + "/recreated_pptx/qa/slide032/render_9.png").convert("L")
S = rim.size[1] / 540.0


def rframe(x0, y0, x1, y1):
    sub = rim.crop((int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S)))
    return np.asarray(sub.resize((x1 - x0, y1 - y0), Image.LANCZOS)).astype(float)


def inkmask(a, thr=200):
    return a < thr


def iou(A, B):
    """best-aligned IoU of two ink masks, shifts in -2..2 both axes"""
    h = max(A.shape[0], B.shape[0]) + 5
    w = max(A.shape[1], B.shape[1]) + 5
    Ap = np.zeros((h, w), bool); Ap[2:2 + A.shape[0], 2:2 + A.shape[1]] = A
    Bp = np.zeros((h, w), bool); Bp[2:2 + B.shape[0], 2:2 + B.shape[1]] = B
    best = 0.0
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            Bs = np.roll(np.roll(Bp, dy, axis=0), dx, axis=1)
            u = (Ap | Bs).sum()
            if u:
                best = max(best, (Ap & Bs).sum() / u)
    return best


def render_str(text, size):
    f = ImageFont.truetype(FONT, size)
    bb = f.getbbox(text)
    im = Image.new("L", (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), 255)
    ImageDraw.Draw(im).text((4 - bb[0], 4 - bb[1]), text, font=f, fill=100)
    return np.asarray(im).astype(float)


print("=" * 76)
print("GROUP 1 — ORIGINAL x828..839 y141..153  (two glyphs: '(' + digit)")
print("=" * 76)
G1o = inkmask(o[141:153, 828:839])
G1r = inkmask(rframe(724, 141, 738, 153))
rows = []
for s in ("(7", "(?", "(3", "(1", "(2", "(9", "(8"):
    for sz in (9, 10, 11):
        t = inkmask(render_str(s, sz))
        rows.append((iou(G1o, t), f"template {s!r} @{sz}", iou(G1r, t), ""))
rows.append((iou(G1o, G1r), "RENDER group1 (ground truth '(7')", 1.0, "<-- control"))
rows.sort(reverse=True)
for so, lab, sr, note in rows:
    print(f"  ORIG IoU {so:.3f}   REND IoU {sr:.3f}   {lab} {note}")

print()
print("=" * 76)
print("GROUP 3 — ORIGINAL x739..951 y141..153  (comma + digit + ')')")
print("=" * 76)
G3o = inkmask(o[141:153, 739:951])
G3r = inkmask(rframe(736, 141, 752, 153))
rows = []
for s in (", 7)", ", ?)", ", 3)", ", 1)", ", 2)", ", 9)", ", 8)", ")"):
    for sz in (9, 10, 11):
        t = inkmask(render_str(s, sz))
        rows.append((iou(G3o, t), f"template {s!r} @{sz}", iou(G3r, t), ""))
rows.append((iou(G3o, G3r), "RENDER group3 (ground truth ', 7)')", 1.0, "<-- control"))
rows.sort(reverse=True)
for so, lab, sr, note in rows:
    print(f"  ORIG IoU {so:.3f}   REND IoU {sr:.3f}   {lab} {note}")

print()
print("=" * 76)
print("WHOLE LABEL — ORIGINAL x828..951 vs RENDER x724..845 + candidate strings")
print("=" * 76)
LWo = inkmask(o[141:153, 828:951])
LWr = inkmask(rframe(724, 141, 845, 153))
rows = []
for s in ("(7, 7)", "(7,7)", "(?, ?)", "(?,?)", "(3, 3)", "(8, 8)", "(1, 1)"):
    for sz in (9, 10, 11):
        t = inkmask(render_str(s, sz))
        rows.append((iou(LWo, t), f"template {s!r} @{sz}", iou(LWr, t), ""))
rows.append((iou(LWo, LWr), "RENDER whole label (ground truth '(7, 7)')", 1.0, "<-- control"))
rows.sort(reverse=True)
for so, lab, sr, note in rows:
    print(f"  ORIG IoU {so:.3f}   REND IoU {sr:.3f}   {lab} {note}")
