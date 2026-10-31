"""Final measurement pass: clean ink runs per band (borders excluded),
sigma-limit extents + colours, underline detection under '(W^T Xi)'."""
from PIL import Image
import numpy as np

IM = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_004.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
P = 72.0
BORDER_X = [0.819, 12.525]


def runs_of(cols, gap):
    out, cur = [], None
    for c in cols:
        if cur is None:
            cur = [c, c]
        elif c - cur[1] <= gap + 1:
            cur[1] = c
        else:
            out.append(tuple(cur)); cur = [c, c]
    if cur:
        out.append(tuple(cur))
    return out


def band_runs(y0, y1, x0, x1, thr=45, gap=5, drop_borders=True):
    blk = a[int(y0 * P):int(y1 * P), int(x0 * P):int(x1 * P)]
    vals, cnts = np.unique(blk.reshape(-1, 3), axis=0, return_counts=True)
    bg = vals[cnts.argmax()]
    d = np.abs(blk - bg).max(axis=2)
    cols = np.where(d.max(axis=0) > thr)[0] + int(x0 * P)
    rr = [(r[0] / P, r[1] / P) for r in runs_of(list(cols), gap) if r[1] - r[0] >= 2]
    if drop_borders:
        rr = [r for r in rr if (r[1] - r[0]) >= 0.05 and not any(abs(r[0]-b) < 0.04 or abs(r[1]-b) < 0.04 for b in BORDER_X)]
    return rr, tuple(bg)


def band_vert(y0, y1, x0, x1, thr=45, gap=3):
    blk = a[int(y0 * P):int(y1 * P), int(x0 * P):int(x1 * P)]
    vals, cnts = np.unique(blk.reshape(-1, 3), axis=0, return_counts=True)
    bg = vals[cnts.argmax()]
    d = np.abs(blk - bg).max(axis=2)
    rows = np.where(d.max(axis=1) > thr)[0] + int(y0 * P)
    return [(r[0] / P, r[1] / P) for r in runs_of(list(rows), gap) if r[1] - r[0] >= 1]


BANDS = [
    ("P1 head", 1.52, 1.82, 0.95, 12.30),
    ("P1 line1", 1.88, 2.18, 0.95, 12.30),
    ("P1 line2", 2.24, 2.54, 0.95, 12.30),
    ("P2 head", 3.18, 3.46, 0.95, 12.30),
    ("P2 eq+expl", 3.45, 4.08, 0.95, 12.30),
    ("P2 positive", 4.10, 4.44, 0.95, 12.30),
    ("P3 heading", 4.84, 5.12, 1.00, 12.30),
    ("P3 eqrow", 5.34, 6.10, 1.00, 12.30),
    ("L box eq", 6.24, 6.60, 1.20, 6.70),
    ("L box limit", 6.66, 6.95, 1.20, 6.70),
    ("R box eq", 6.28, 6.70, 9.10, 12.30),
    ("caption", 6.26, 6.52, 6.85, 8.80),
]
print("=== clean ink runs (borders dropped) ===")
for tag, y0, y1, x0, x1 in BANDS:
    rr, bg = band_runs(y0, y1, x0, x1)
    vv = band_vert(y0, y1, x0, x1)
    print(f"{tag:<14} x: " + " ".join(f"{s:.2f}-{e:.2f}" for s, e in rr))
    print(f"{'':14} y: " + ", ".join(f"{s:.3f}-{e:.3f}" for s, e in vv))

print("\n=== RED ink extents (frame borders excluded) ===")
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 90) & (r - g > 40) & (r - b > 40)
red[:, :int(0.86 * P)] = False
red[:, int(12.42 * P):] = False
for tag, y0, y1 in [("P2 sigma limit", 3.80, 4.10), ("P3 sigma limit", 5.70, 6.06),
                    ("mint sigma limit", 6.66, 6.96), ("P1 red bits", 1.88, 2.54),
                    ("P3 heading red", 4.84, 5.12), ("P2 positive red", 4.10, 4.44),
                    ("caption red", 6.26, 6.70)]:
    sub = red[int(y0 * P):int(y1 * P)]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        print(f"  {tag:<20} NO RED")
        continue
    print(f"  {tag:<20} red x {xs.min()/P:.2f}-{xs.max()/P:.2f} y {ys.min()/P+y0:.2f}-{ys.max()/P+y0:.2f} n={len(xs)}")
    for s, e in runs_of(list(sorted(set(xs))), 6)[:14]:
        print(f"        x {s/P:.2f}-{(e+1)/P:.2f}")

print("\n=== underline hunt: long horizontal dark runs under '(W^T Xi)' ===")
for y in np.arange(3.74, 4.00, 0.008):
    row = a[int(round(y * P))]
    xs = [x for x in range(int(5.60 * P), int(6.60 * P)) if row[x].max() < 175]
    rr = [r for r in runs_of(xs, 3) if r[1] - r[0] >= 10]
    if rr:
        print(f"  y={y:.3f}: " + ", ".join(f"{s/P:.2f}-{(e+1)/P:.2f}" for s, e in rr))

print("\n=== underline hunt: P3 heading underline ===")
for y in np.arange(4.98, 5.14, 0.008):
    row = a[int(round(y * P))]
    xs = [x for x in range(int(1.10 * P), int(7.60 * P)) if row[x].max() < 175]
    rr = [r for r in runs_of(xs, 8) if r[1] - r[0] >= 30]
    if rr:
        print(f"  y={y:.3f}: " + ", ".join(f"{s/P:.2f}-{(e+1)/P:.2f}" for s, e in rr))
