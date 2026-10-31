"""Focused PIL measurement of unique_slides/slide_004.jpg (960x540 -> 13.33x7.5in, 1px=1pt)."""
from PIL import Image
import numpy as np

IM = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_004.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
P = 72.0  # px per inch


def p(v):
    return int(round(v * P))


def runs_of(mask_cols, gap):
    if len(mask_cols) == 0:
        return []
    out, cur = [], [mask_cols[0], mask_cols[0]]
    for c in mask_cols[1:]:
        if c - cur[1] <= gap + 1:
            cur[1] = c
        else:
            out.append(tuple(cur)); cur = [c, c]
    out.append(tuple(cur))
    return out


def scan(tag, y0, y1, x0, x1, gap=5):
    blk = a[p(y0):p(y1), p(x0):p(x1)]
    vals, cnts = np.unique(blk.reshape(-1, 3), axis=0, return_counts=True)
    bg = vals[cnts.argmax()]
    d = np.abs(blk - bg).max(axis=2)
    cols = np.where(d.max(axis=0) > 40)[0] + p(x0)
    rr = [r for r in runs_of(cols, gap) if r[1] - r[0] >= 2]
    if rr:
        print(f"{tag:<26} y[{y0:.2f},{y1:.2f}] bg={tuple(bg)} ink x {rr[0][0]/P:.3f}-{rr[-1][1]/P:.3f}")
    else:
        print(f"{tag:<26} y[{y0:.2f},{y1:.2f}] bg={tuple(bg)} NO INK")


def vscan(tag, x0, x1, y0, y1, gap=3):
    """vertical ink extent of a column band"""
    ys0, ys1, xs0, xs1 = p(y0), p(y1), p(x0), p(x1)
    blk = a[ys0:ys1, xs0:xs1]
    vals, cnts = np.unique(blk.reshape(-1, 3), axis=0, return_counts=True)
    bg = vals[cnts.argmax()]
    d = np.abs(blk - bg).max(axis=2)
    rows = np.where(d.max(axis=1) > 40)[0] + ys0
    rr = [r for r in runs_of(list(rows), gap) if r[1] - r[0] >= 1]
    print(f"{tag:<26} x[{x0:.2f},{x1:.2f}] bg={tuple(bg)} ink y "
          + ", ".join(f"{r[0]/P:.3f}-{r[1]/P:.3f}" for r in rr))


def colors_in(tag, y0, y1, x0, x1, top=6):
    """dominant non-bg colours in a box"""
    blk = a[p(y0):p(y1), p(x0):p(x1)].reshape(-1, 3)
    vals, cnts = np.unique(blk, axis=0, return_counts=True)
    order = cnts.argsort()[::-1]
    vals, cnts = vals[order], cnts[order]
    bg = vals[0]
    print(f"{tag:<26} bg={tuple(bg)}; next colours: " +
          ", ".join(f"{tuple(v)}({c})" for v, c in zip(vals[1:1 + top], cnts[1:1 + top])))


print("### PANEL 1 text geometry")
scan("head", 1.55, 1.80, 0.9, 12.4)
scan("line1", 1.90, 2.15, 0.9, 12.4)
scan("line2", 2.25, 2.50, 0.9, 12.4)
vscan("head vert", 1.08, 2.54, 1.4, 1.95)
vscan("line1 vert", 1.08, 11.7, 1.4, 2.55)
vscan("line2 vert", 1.08, 11.7, 2.05, 3.0)
print()
print("### PANEL 2")
scan("head", 3.20, 3.46, 0.85, 12.5)
scan("eq row", 3.45, 4.08, 0.85, 12.5)
scan("expl clause", 3.50, 4.00, 5.7, 12.5)
scan("positive", 4.10, 4.34, 0.85, 12.5)
vscan("eq row vert L", 1.15, 5.7, 3.4, 4.1)
vscan("expl vert", 5.82, 12.05, 3.4, 4.1)
print()
print("### PANEL 3")
scan("head", 4.86, 5.14, 1.10, 12.35)
scan("eq row", 5.38, 6.05, 1.10, 12.35)
vscan("eq row vert L", 1.15, 4.65, 5.3, 6.1)
vscan("eq row vert R", 7.11, 10.57, 5.3, 6.1)
print()
print("### BOTTOM ROW")
scan("L box eq", 6.26, 6.52, 1.10, 6.75)
scan("L box caption", 6.68, 6.95, 1.10, 6.75)
scan("R box eq", 6.30, 6.68, 8.98, 12.35)
scan("center caption", 6.28, 6.48, 6.80, 8.95)
print()
print("### UNDERLINE detection (long horizontal dark runs)")
for y in np.arange(3.28, 3.75, 0.02):
    row = a[p(y)]
    xs = [x for x in range(p(5.7), p(12.4)) if row[x].max() < 150]
    rr = [r for r in runs_of(xs, 4) if r[1] - r[0] > 6]
    if rr:
        print(f"  y={y:.2f} dark runs: " + ", ".join(f"{r[0]/P:.2f}-{r[1]/P:.2f}" for r in rr))
print()
for y in np.arange(4.90, 5.30, 0.02):
    row = a[p(y)]
    xs = [x for x in range(p(1.10), p(7.6)) if row[x].max() < 150]
    rr = [r for r in runs_of(xs, 4) if r[1] - r[0] > 6]
    if rr:
        print(f"  P3head y={y:.2f} dark runs: " + ", ".join(f"{r[0]/P:.2f}-{r[1]/P:.2f}" for r in rr))
print()
print("### ARROW + RULE bottoms")
for y in np.arange(6.48, 6.72, 0.015):
    row = a[p(y)]
    rred = [x for x in range(p(6.4), p(8.0)) if row[x][0] > 150 and row[x][1] < 110]
    rdark = [x for x in range(p(6.4), p(9.5)) if row[x].max() < 120]
    if rred or rdark:
        print(f"  y={y:.3f} red x {rred[0]/P:.2f}-{rred[-1]/P:.2f} (n={len(rred)})" if rred
              else f"  y={y:.3f} dark x {rdark[0]/P:.2f}-{rdark[-1]/P:.2f} (n={len(rdark)})" if rdark else "")
print()
print("### COLOUR CENSUS")
colors_in("P1 line1 tail >0", 1.90, 2.15, 11.0, 11.8)
colors_in("P2 sigma limit", 3.72, 4.02, 1.30, 3.30)
colors_in("P3 sigma limit", 5.62, 5.98, 7.30, 8.20)
colors_in("Lbox sigma limit", 6.70, 6.95, 3.5, 6.2)
colors_in("arrow glyph", 6.50, 6.70, 6.40, 8.0)
colors_in("rule", 6.46, 6.52, 6.85, 9.2)
