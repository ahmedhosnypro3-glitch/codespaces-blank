#!/usr/bin/env python3
"""Adjudicate_9i — final glyph comparison for the right point label.

1. Prints the build font's templates for the candidate glyphs at 10/11pt.
2. Prints each label group isolated from BOTH images at 1 px/frame-px.
3. Shape distance (best-aligned XOR) of every ORIGINAL group against every
   template AND against the RENDER's own "(7, 7)" glyphs (ground truth, since
   build/slide_032.js:200 draws that string).
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

o = np.asarray(Image.open(V + "/unique_slides/slide_032.jpg").convert("L")).astype(float)
rim = Image.open(V + "/recreated_pptx/qa/slide032/render_9.png").convert("L")
S = rim.size[1] / 540.0

# ---- render patch helper: frame bbox -> array downsampled to 1 px per frame px
def rframe(x0, y0, x1, y1):
    sub = rim.crop((int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S)))
    return np.asarray(sub.resize((x1 - x0, y1 - y0), Image.LANCZOS)).astype(float)


def amap(a, label, x0=None):
    if x0 is not None:
        print("      " + "".join(f"\\" if (x0 + c) % 5 == 0 else " " for c in range(a.shape[1])))
        print("      " + "".join(str((x0 + c) // 10 % 10) if (x0 + c) % 10 == 0 else " "
                                 for c in range(a.shape[1])))
    print(f"--- {label} ({a.shape[1]}x{a.shape[0]}) ---")
    for ry in range(a.shape[0]):
        print("   " + "".join("#" if v < 130 else ("+" if v < 185 else ("." if v < 230 else " "))
                              for v in a[ry, :]))
    print()


def dist(A, B):
    """best-aligned XOR distance over shifts; returns (1 - iou)"""
    ha, wa = A.shape; hb, wb = B.shape
    pad = 2
    Ap = np.zeros((ha + 2 * pad, wa + 2 * pad), bool); Ap[pad:pad + ha, pad:pad + wa] = A < 200
    Bp = np.zeros((hb + 2 * pad, wb + 2 * pad), bool); Bp[pad:pad + hb, pad:pad + wb] = B < 200
    best = 1.0
    for dy in range(2 * pad + 1):
        for dx in range(2 * pad + 1):
            Bs = np.roll(np.roll(Bp, dy - pad, axis=0), dx - pad, axis=1)
            inter = (Ap & Bs).sum(); union = (Ap | Bs).sum()
            if union:
                best = min(best, 1 - inter / union)
    return best


def tmpl(ch, size):
    f = ImageFont.truetype(FONT, size)
    bb = f.getbbox(ch)
    im = Image.new("L", (bb[2] - bb[0] + 2, bb[3] - bb[1] + 2), 255)
    ImageDraw.Draw(im).text((1 - bb[0], 1 - bb[1]), ch, font=f, fill=100)
    a = np.asarray(im).astype(float)
    ink = a < 200
    rs = np.nonzero(ink.sum(axis=1))[0]; cs = np.nonzero(ink.sum(axis=0))[0]
    return a[rs[0]:rs[-1] + 1, cs[0]:cs[-1] + 1]


def dist(A, B):
    """best-aligned XOR distance over shifts; returns (1 - iou)"""
    ha, wa = A.shape; hb, wb = B.shape
    pad = 2
    Ap = np.zeros((ha + 2 * pad, wa + 2 * pad), bool); Ap[pad:pad + ha, pad:pad + wa] = A < 200
    Bp = np.zeros((hb + 2 * pad, wb + 2 * pad), bool); Bp[pad:pad + hb, pad:pad + wb] = B < 200
    best = 1.0
    for dy in range(5):
        for dx in range(5):
            Bs = np.roll(np.roll(Bp, dy - 2, axis=0), dx - 2, axis=1)
            inter = (Ap & Bs).sum(); union = (Ap | Bs).sum()
            if union:
                best = min(best, 1 - inter / union)
    return best


print("=" * 74)
print("1. FONT TEMPLATES (Liberation Serif, the build's family)")
print("=" * 74)
T = {}
for ch in "()7?3,1 ":
    for sz in (10, 11):
        if ch == " ":
            continue
        t = tmpl(ch, sz)
        T[(ch, sz)] = t
        amap(t, f"template {ch!r} @ {sz}pt")

print("=" * 74)
print("2. LABEL GROUPS (1 px per frame px)")
print("=" * 74)
# ORIGINAL groups: g1 x727..837 y141..153 ; g3 x739..750 y141..153
G1o = o[141:153, 727:737]
G3o = o[141:153, 739:751]
# RENDER groups: g1 x723..737 (dot overlaps; keep) ; g3 x735..748
G1r = rframe(723, 141, 738, 153)
G3r = rframe(735, 141, 749, 153)
amap(G1o, "ORIG group1 (x727..837)", 727)
amap(G1r, "REND9 group1 (x723..737) — ground truth '(' + '7'")
amap(G3o, "ORIG group3 (x739..750)", 739)
amap(G3r, "REND9 group3 (x735..748) — ground truth ',' + '7' + ')'")

print("=" * 74)
print("3. SHAPE DISTANCE (0 = identical, 1 = disjoint) vs every template")
print("=" * 74)
for gname, g in (("ORIG g1", G1o), ("ORIG g3", G3o), ("REND g1 (truth)", G1r),
                 ("REND g3 (truth)", G3r)):
    rows = sorted((dist(g, t), ch, sz) for (ch, sz), t in T.items())
    print(f"\n  {gname}: nearest templates")
    for d, ch, sz in rows[:6]:
        print(f"     {d:.3f}   {ch!r} @ {sz}pt")

print("\n  cross-image: ORIG g1 vs REND g1 =", round(dist(G1o, G1r), 3),
      "  ORIG g3 vs REND g3 =", round(dist(G3o, G3r), 3))
