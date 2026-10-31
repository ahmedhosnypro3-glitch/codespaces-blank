"""Measure build/slide_004_rejudge... no -- measure the v3 render slide_004_rendered-1.png (2001x1125)."""
from PIL import Image
import numpy as np

R = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_004_rendered-1.png"
im = Image.open(R).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print("size", W, H, " scale px/in =", W / 13.33)
S = W / 13.33


def band(y0, y1, x0, x1, thr=40):
    ys, xs = slice(int(y0 * S), int(y1 * S)), slice(int(x0 * S), int(x1 * S))
    blk = a[ys, xs]
    vals, cnts = np.unique(blk.reshape(-1, 3), axis=0, return_counts=True)
    bg = vals[cnts.argmax()]
    d = np.abs(blk - bg).max(axis=2)
    cols = np.where(d.max(axis=0) > thr)[0] + int(x0 * S)
    runs = []
    if len(cols):
        cur = [cols[0], cols[0]]
        for c in cols[1:]:
            if c - cur[1] <= int(0.05 * S):
                cur[1] = c
            else:
                runs.append(tuple(cur)); cur = [c, c]
        runs.append(tuple(cur))
    big = [r for r in runs if r[1] - r[0] >= 3]
    if big:
        print(f"y[{y0:.2f},{y1:.2f}] x[{x0:.2f},{x1:.2f}] bg={tuple(bg)} ink {big[0][0]/S:.2f}-{big[-1][1]/S:.2f}")
    else:
        print(f"y[{y0:.2f},{y1:.2f}] x[{x0:.2f},{x1:.2f}] bg={tuple(bg)} NO INK")
    return big


print("== PANEL 1 ==")
band(1.53, 1.80, 0.95, 12.5)
band(1.89, 2.19, 0.95, 12.5)
band(2.24, 2.54, 0.95, 12.5)
print("== PANEL 2 ==")
band(3.18, 3.46, 0.95, 12.5)
band(3.45, 4.08, 0.95, 12.5)
band(3.55, 4.00, 5.8, 12.5)
band(4.10, 4.36, 0.95, 12.5)
print("== PANEL 3 ==")
band(4.86, 5.14, 1.15, 12.5)
band(5.38, 6.02, 1.15, 12.5)
print("== BOTTOM ROW ==")
band(6.25, 6.56, 1.2, 6.7)
band(6.70, 6.95, 1.2, 6.7)
band(6.28, 6.48, 6.8, 8.95)
band(6.49, 6.70, 6.8, 8.95)
band(6.30, 6.68, 9.1, 12.25)

print("\n== box borders (render) ==")


def find_border(x, y0, y1):
    col = a[int(y0 * S):int(y1 * S), int(x * S)]
    return tuple(col[len(col) // 2])


def hscan(y, x0, x1, tag):
    row = a[int(y * S)]
    out = []
    for x in range(int(x0 * S), int(x1 * S)):
        r, g, b = row[x]
        if r < 200 and g < 200 and b < 200:
            out.append(x)
    if out:
        print(f"{tag}: y={y} dark x {out[0]/S:.2f}-{out[-1]/S:.2f}")


# find vertical borders of bottom boxes by scanning row y=6.55 for green-ish dark
row = a[int(6.55 * S)]
darks = [x for x in range(int(1.0 * S), int(13.0 * S))
         if row[x][0] < 150 and row[x][1] < 190 and row[x][2] < 150]
print("dark px at y=6.55:", [round(x / S, 2) for x in darks][:60])
