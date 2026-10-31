"""Resolve: (a) original glyph heights, (b) where RED ink lives in the original,
(c) whether '(W^T Xi)' is underlined, (d) P1 trailing '>0' colour."""
from PIL import Image
import numpy as np

IM = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_004.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
P = 72.0


def px(x, y):
    return tuple(a[int(round(y * P)), int(round(x * P))])


def profile(tag, x0, x1, y0, y1, thr=45):
    """row-by-row ink counts in a column window"""
    blk = a[int(round(y0 * P)):int(round(y1 * P)), int(round(x0 * P)):int(round(x1 * P))]
    vals, cnts = np.unique(blk.reshape(-1, 3), axis=0, return_counts=True)
    bg = vals[cnts.argmax()]
    d = np.abs(blk - bg).max(axis=2)
    rows = [(y0 + i / P, int((d[i] > thr).sum())) for i in range(d.shape[0])]
    seg = [(r, n) for r, n in rows if n > 0]
    if seg:
        print(f"{tag:<30} ink rows {seg[0][0]:.3f}-{seg[-1][0]:.3f} (h={seg[-1][0]-seg[0][0]:.3f}in={((seg[-1][0]-seg[0][0])*72):.1f}pt)")
    else:
        print(f"{tag:<30} NO INK")


print("=== (a) glyph heights (original) ===")
profile("P1 'If' (x1.07-1.45)", 1.07, 1.45, 1.85, 2.25)
profile("P1 'If' f-only (1.25-1.45)", 1.25, 1.45, 1.85, 2.25)
profile("P1 'Define' (1.07-1.60)", 1.07, 1.60, 1.50, 1.90)
profile("P1 title? no; P2 head 'Red'(.95-1.6)", 0.95, 1.60, 3.15, 3.55)
profile("P2 expl '(W' (5.70-6.25)", 5.70, 6.25, 3.45, 4.00)
profile("P3 head 'Minim' (1.15-1.85)", 1.15, 1.85, 4.80, 5.25)
profile("P2 positive (0.95-1.60)", 0.95, 1.60, 4.05, 4.45)
profile("center caption 'Update' (6.89-7.45)", 6.89, 7.45, 6.24, 6.52)

print("\n=== (b) RED ink clusters in the original ===")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 110) & (r - g > 55) & (r - b > 55)
ys, xs = np.nonzero(red)
# cluster by y band
bands = {}
for y, x in zip(ys, xs):
    key = int(y // 12)
    bands.setdefault(key, []).append(x)
for key in sorted(bands):
    xs2 = bands[key]
    print(f"  y {key*12/72:.2f}-{(key+1)*12/72:.2f} in : red x {min(xs2)/72:.2f}-{max(xs2)/72:.2f} n={len(xs2)}")

print("\n=== (c) underline probe under '(W^T Xi)' ===")
for y in np.arange(3.78, 4.02, 0.01):
    row = a[int(round(y * P))]
    xs = [x for x in range(int(5.6 * P), int(7.0 * P)) if row[x].max() < 170]
    if len(xs) > 8:
        print(f"  y={y:.2f} dark-ish x {min(xs)/72:.2f}-{max(xs)/72:.2f} n={len(xs)}")
print("  (W^T Xi) region colour samples:")
for x in [5.90, 6.05, 6.20, 6.40]:
    print(f"    x={x}: " + " ".join(f"y{y:.2f}={px(x,y)}" for y in [3.50, 3.55, 3.60, 3.65, 3.70, 3.75, 3.80, 3.85, 3.90]))

print("\n=== (d) P1 trailing '>0' colours (original) ===")
for y in [1.95, 2.00, 2.05, 2.10]:
    row = a[int(round(y * P))]
    out = []
    for x in range(int(11.3 * P), int(11.8 * P)):
        rr, gg, bb = row[x]
        if not (rr > 240 and gg > 240 and bb > 240):
            out.append((round(x / P, 3), (rr, gg, bb)))
    print(f"  y={y}: " + " ".join(f"{x}:{c}" for x, c in out[:14]))
print("\n  P1 line2 trailing:")
for y in [2.32, 2.37, 2.42]:
    row = a[int(round(y * P))]
    out = []
    for x in range(int(11.3 * P), int(11.8 * P)):
        rr, gg, bb = row[x]
        if not (rr > 240 and gg > 240 and bb > 240):
            out.append((round(x / P, 3), (rr, gg, bb)))
    print(f"  y={y}: " + " ".join(f"{x}:{c}" for x, c in out[:14]))

print("\n=== (e) panel-2 sigma limit region colours ===")
for y in [3.86, 3.90, 3.95, 4.00, 4.03]:
    row = a[int(round(y * P))]
    out = []
    for x in range(int(1.2 * P), int(3.6 * P)):
        rr, gg, bb = row[x]
        if not (rr > 240 and gg > 240 and bb > 215):
            out.append((round(x / P, 3), (rr, gg, bb)))
    print(f"  y={y}: " + " ".join(f"{x}:{c}" for x, c in out[:16]))
