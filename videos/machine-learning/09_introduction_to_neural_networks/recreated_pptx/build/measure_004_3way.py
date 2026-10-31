"""Side-by-side ink measurements: original frame vs the Oct-27 FAIL render vs the Oct-31 v3 render."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = f"{V}/unique_slides/slide_004.jpg"
OLD = f"{V}/recreated_pptx/build/slide_004_rejudge_rendered-1.png"     # the render the FAIL verdict saw
V3 = f"{V}/recreated_pptx/build/slide_004_rendered-1.png"             # v3 rebuild render
TOP = f"{V}/recreated_pptx/build/slide_004_toplevel_probe_rendered-1.png"

WALL = 13.33


def load(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    return a, a.shape[1] / WALL, a.shape[:2]


def span(a, S, y0, y1, x0, x1, thr=40, gap=5):
    ys, xs = slice(int(y0 * S), int(y1 * S)), slice(int(x0 * S), int(x1 * S))
    blk = a[ys, xs]
    vals, cnts = np.unique(blk.reshape(-1, 3), axis=0, return_counts=True)
    bg = vals[cnts.argmax()]
    d = np.abs(blk - bg).max(axis=2)
    cols = np.where(d.max(axis=0) > thr)[0] + int(x0 * S)
    runs, cur = [], None
    for c in cols:
        if cur is None:
            cur = [c, c]
        elif c - cur[1] <= gap + 1:
            cur[1] = c
        else:
            runs.append(tuple(cur)); cur = [c, c]
    if cur:
        runs.append(tuple(cur))
    big = [r for r in runs if r[1] - r[0] >= 2]
    return (big[0][0] / S, big[-1][1] / S) if big else None


def label(tag, key):
    vals = {name: spans[name].get(key) for name in spans}
    print(f"{tag:<24}" + "".join(f"{nm:>26}" for nm in spans))
    print("  " + " " * 24 + "".join(
        (f"{v[0]:>12.2f}-{v[1]:.2f}    " if v else f"{'NO INK':>24} ") for v in vals))


TARGETS = [
    ("P1 head", (1.55, 1.80, 0.90, 12.4)),
    ("P1 cond line 1", (1.90, 2.15, 0.90, 12.4)),
    ("P1 cond line 2", (2.25, 2.50, 0.90, 12.4)),
    ("P2 head", (3.20, 3.46, 0.85, 12.5)),
    ("P2 explanation", (3.50, 4.00, 5.70, 12.5)),
    ("P2 positive line", (4.10, 4.34, 0.85, 12.5)),
    ("P3 heading", (4.86, 5.14, 1.10, 12.35)),
    ("P3 eq row", (5.38, 6.05, 1.10, 12.35)),
    ("L box equation", (6.26, 6.52, 1.10, 6.75)),
    ("L box sigma cap", (6.68, 6.95, 1.10, 6.75)),
    ("center caption", (6.28, 6.48, 6.80, 8.95)),
    ("arrow band", (6.49, 6.70, 6.80, 8.95)),
    ("R box equation", (6.30, 6.68, 8.98, 12.35)),
]

paths = {"ORIGINAL": ORIG, "OLD(FAIL)": OLD, "V3(current)": V3, "TOPPROBE": TOP}
spans = {}
for name, path in paths.items():
    try:
        a, S, _ = load(path)
    except Exception as e:
        print("skip", name, e); continue
    spans[name] = {}
    for key, (y0, y1, x0, x1) in TARGETS:
        spans[name][key] = span(a, S, y0, y1, x0, x1)

for key, (y0, y1, x0, x1) in TARGETS:
    vals = {n: spans[n].get(key) for n in spans}
    line = f"{key:<24}"
    for n in spans:
        v = vals[n]
        line += f"{(f'{v[0]:.2f}-{v[1]:.2f}' if v else 'NO INK'):>18}"
    print(line)
