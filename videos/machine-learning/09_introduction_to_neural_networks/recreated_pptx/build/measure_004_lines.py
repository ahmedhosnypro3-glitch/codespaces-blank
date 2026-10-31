"""Rigorous per-line ink extents (border-aware) for original + renders."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
FILES = {
    "ORIGINAL": (f"{V}/unique_slides/slide_004.jpg", 72.0),
    "OLD(FAIL)": (f"{V}/recreated_pptx/build/slide_004_rejudge_rendered-1.png", 2001 / 13.33),
    "V3": (f"{V}/recreated_pptx/build/slide_004_rendered-1.png", 2001 / 13.33),
}


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


def analyse(path, S):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    H, W = a.shape[:2]

    def runs(y0, y1, x0, x1, thr=45, gap=5):
        ys, xs = slice(int(y0 * S), int(y1 * S)), slice(int(x0 * S), int(x1 * S))
        blk = a[ys, xs]
        vals, cnts = np.unique(blk.reshape(-1, 3), axis=0, return_counts=True)
        bg = vals[cnts.argmax()]
        d = np.abs(blk - bg).max(axis=2)
        cols = np.where(d.max(axis=0) > thr)[0] + int(x0 * S)
        rr = [r for r in runs_of(list(cols), gap) if r[1] - r[0] >= 2]
        return [(r[0] / S, r[1] / S) for r in rr], tuple(bg)

    def vert(y0, y1, x0, x1, thr=45, gap=3):
        ys, xs = slice(int(y0 * S), int(y1 * S)), slice(int(x0 * S), int(x1 * S))
        blk = a[ys, xs]
        vals, cnts = np.unique(blk.reshape(-1, 3), axis=0, return_counts=True)
        bg = vals[cnts.argmax()]
        d = np.abs(blk - bg).max(axis=2)
        rows = np.where(d.max(axis=1) > thr)[0] + int(y0 * S)
        rr = [r for r in runs_of(list(rows), gap) if r[1] - r[0] >= 1]
        return [(r[0] / S, r[1] / S) for r in rr]

    print(f"--- {path.split('/')[-1]} ({W}x{H}) ---")
    print("P1 line1 runs:")
    rr, bg = runs(1.90, 2.15, 0.90, 12.45)
    print("   ", " ".join(f"{a0:.2f}-{b0:.2f}" for a0, b0 in rr))
    print("P1 line2 runs:")
    rr, bg = runs(2.25, 2.50, 0.90, 12.45)
    print("   ", " ".join(f"{a0:.2f}-{b0:.2f}" for a0, b0 in rr))
    # cap-height probe: vertical ink of 'If' at start of line1 (x 1.05..1.45)
    print("P1 line1 'If' vertical:", vert(1.80, 2.25, 1.05, 1.60))
    print("P1 line2 'If' vertical:", vert(2.15, 2.60, 1.05, 1.60))
    print("P1 head vertical:", vert(1.45, 1.88, 0.95, 2.60))
    print("P2 expl vertical:", vert(3.45, 4.00, 5.75, 12.05))
    print("P3 head vertical:", vert(4.80, 5.20, 1.10, 7.30))
    print("P2 positive vertical:", vert(4.05, 4.40, 0.95, 4.20))
    print("Lbox eq vertical:", vert(6.20, 6.60, 1.15, 5.00))
    print("center caption vertical:", vert(6.24, 6.50, 6.85, 8.82))
    print("P2 explanation runs:", " ".join(f"{a0:.2f}-{b0:.2f}" for a0, b0 in runs(3.50, 4.00, 5.70, 12.45)[0]))
    print()


for name, (path, S) in FILES.items():
    print(f"===== {name} =====")
    analyse(path, S)
