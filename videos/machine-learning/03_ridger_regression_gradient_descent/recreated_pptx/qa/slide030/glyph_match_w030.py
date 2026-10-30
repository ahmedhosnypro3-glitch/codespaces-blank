"""Glyph-level comparison of the ambiguous right-endpoint label: original vs render.

Compares the original frame's two ambiguous glyph clusters (slide x728..737, x741..749)
against every digit glyph rendered by the build (7,7 from "(7, 7)"; 2,1,0 from "(2, 10)";
5,1 from "(5, 1)"), using normalized cross-correlation of column ink profiles after
best alignment. Controls: same-character pairs (orig "(2,10)" digits vs render "(2,10)")
must score higher than cross-character pairs.
"""
import numpy as np
from PIL import Image

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_030.jpg"
REND = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide030/render_6.png"
S = 2001.0 / 960.0

o = np.array(Image.open(ORIG).convert("RGB")).astype(float)
r = np.array(Image.open(REND).convert("RGB")).astype(float)
og = o.sum(axis=2) / 3.0
rg = r.sum(axis=2) / 3.0


def canon(img, keep=2):
    """Normalize an ink map to a fixed canvas (keep original rows/cols, drop empty border)
    then resize to 16x16 for cross-image comparison."""
    arr = np.asarray(img, dtype=float)
    ys, xs = np.nonzero(arr > 0.25)
    if len(xs) < 3:
        return np.zeros((16, 16))
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    sub = arr[y0:y1, x0:x1]
    im = Image.fromarray(np.clip(sub * 255, 0, 255).astype(np.uint8)).resize((16, 16), Image.LANCZOS)
    return np.asarray(im, dtype=float) / 255.0


def orig_prof(x0, x1, y0, y1):
    sub = og[y0:y1, x0:x1]
    bg = np.percentile(sub, 90)
    ink = np.clip((bg - sub) / max(bg - sub.min(), 1.0), 0, 1)
    return canon(ink)


def rend_prof(x0, x1, y0, y1):
    rx0, rx1 = int(round(x0 * S)), int(round(x1 * S))
    ry0, ry1 = int(round(y0 * S)), int(round(y1 * S))
    sub = rg[ry0:ry1, rx0:rx1]
    bg = np.percentile(sub, 90)
    ink = np.clip((bg - sub) / max(bg - sub.min(), 1.0), 0, 1)
    return canon(ink)


def ncc(a, b):
    a = np.ascontiguousarray(a).ravel() - a.mean()
    b = np.ascontiguousarray(b).ravel() - b.mean()
    d = np.linalg.norm(a) * np.linalg.norm(b)
    return float(a @ b / d) if d else 0.0


def best_ncc(A, B, shift=1):
    best = -1.0
    bestsh = (0, 0)
    for dy in range(-shift, shift + 1):
        for dx in range(-shift, shift + 1):
            B2 = np.roll(np.roll(B, dy, axis=0), dx, axis=1)
            v = ncc(A, B2)
            if v > best:
                best, bestsh = v, (dx, dy)
    return best, bestsh


Y0, Y1 = 139, 156
orig_amb = {"amb_A": orig_prof(727, 738, Y0, Y1), "amb_B": orig_prof(740, 750, Y0, Y1)}
orig_ctl = {"ctl_2": orig_prof(632, 641, 149, 158), "ctl_1": orig_prof(646, 651, 149, 158),
            "ctl_0": orig_prof(651, 658, 149, 158)}
rend_dig = {
    "r_7a": rend_prof(729, 737, 143, 157), "r_7b": rend_prof(741, 749, 143, 157),
    "r_2": rend_prof(632, 641, 151, 165), "r_1": rend_prof(646, 651, 151, 165),
    "r_0": rend_prof(651, 658, 151, 165),
    "r_5": rend_prof(695, 703, 243, 257), "r_1b": rend_prof(710, 715, 243, 257),
}

print("=== ambiguous original glyphs vs render digit glyphs (best NCC over +-2px shift)")
for ok, ov in orig_amb.items():
    row = []
    for rk, rv in rend_dig.items():
        v, sh = best_ncc(ov, rv)
        row.append(f"{rk}={v:.3f}@{sh}")
    print(f"{ok}: " + "  ".join(row))

print()
print("=== controls: original '(2,10)' digits vs render '(2,10)' digits (same char expected high)")
for ok, rv in [("ctl_2", "r_2"), ("ctl_1", "r_1"), ("ctl_0", "r_0")]:
    v, sh = best_ncc(orig_ctl[ok], rend_dig[rv])
    print(f"{ok} vs {rv}: NCC={v:.3f} shift={sh}")

print()
print("=== control: original ambiguous vs render digits of DIFFERENT labels (discrimination)")
for ok, ov in orig_amb.items():
    for rk in ["r_2", "r_5", "r_1b", "r_0"]:
        v, sh = best_ncc(ov, rend_dig[rk])
        print(f"{ok} vs {rk}: NCC={v:.3f}")
