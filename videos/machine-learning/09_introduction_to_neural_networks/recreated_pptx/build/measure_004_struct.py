"""Resolve remaining structure questions with colour-tagged output."""
from PIL import Image
import numpy as np
import subprocess

IM = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_004.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
P = 72.0


def tag(px):
    r, g, b = px
    if r > 90 and r - g > 45 and r - b > 45:
        return "RED"
    if g > 80 and g - r > 35 and g - b > 35:
        return "GRN"
    if b > 90 and b - r > 45 and b - g > 35:
        return "BLU"
    if max(r, g, b) < 140:
        return "blk"
    return "-"


def region_ink(tagname, y0, y1, x0, x1, gap=4):
    """column runs with the dominant colour tag of the darkest pixel in each column"""
    print(f"--- {tagname}: x {x0:.2f}-{x1:.2f} y {y0:.2f}-{y1:.2f} ---")
    yA, yB = int(round(y0 * P)), int(round(y1 * P))
    xA, xB = int(round(x0 * P)), int(round(x1 * P))
    blk = a[yA:yB, xA:xB]
    vals, cnts = np.unique(blk.reshape(-1, 3), axis=0, return_counts=True)
    bg = vals[cnts.argmax()]
    d = np.abs(blk - bg).max(axis=2)
    cols = []
    for i in range(blk.shape[1]):
        col = blk[:, i]
        m = d[:, i].max()
        if m > 40:
            # dominant colour among the most-differing pixels
            idx = np.argsort(d[:, i])[-4:]
            tags = [tag(tuple(col[j])) for j in idx]
            cols.append((xA + i, tags[0], m))
    runs = []
    cur = None
    for x, t, m in cols:
        if cur is None:
            cur = [x, x, t, t]
        elif x - cur[1] <= gap + 1:
            cur[1] = x
            if t != "-":
                cur[3] = t
        else:
            runs.append(tuple(cur)); cur = [x, x, t, t]
    if cur:
        runs.append(tuple(cur))
    for s, e, t0, t1 in runs:
        print(f"   x {s/P:.3f}-{e/P:.3f}  ({t0}->{t1})")
    print()


region_ink("MINT BOX equation row", 6.24, 6.66, 1.15, 6.70)
region_ink("MINT BOX limit row", 6.68, 6.95, 1.15, 6.70)
region_ink("P2 equation area", 3.44, 4.08, 1.05, 5.00)
region_ink("P3 gradient equation", 5.34, 6.06, 7.05, 10.62)
region_ink("P3 update equation", 5.34, 6.06, 1.10, 4.70)
region_ink("YELLOW BOX equation", 6.24, 6.70, 9.10, 12.25)
region_ink("CENTRE caption+rule+arrow", 6.28, 6.70, 6.40, 9.40)

print("=== fonts available (narrow variants?) ===")
out = subprocess.run(["fc-list", ":", "family"], capture_output=True, text=True).stdout
fams = sorted({l.strip() for l in out.splitlines() if l.strip()})
narrow = [f for f in fams if any(k in f.lower() for k in ("narrow", "condensed", "arial", "liberation", "dejavu", "helvet"))]
for f in narrow:
    print("  ", f)

print("\n=== original P1 line 1, 1px glyph map (x 3.10-4.55) ===")
for y in range(int(1.90 * P), int(2.14 * P)):
    row = "".join(tag(tuple(a[y, x]))[0] if tag(tuple(a[y, x])) != "-" else "." for x in range(int(3.10 * P), int(4.55 * P)))
    print(f"{y/P:5.3f} {row}")
