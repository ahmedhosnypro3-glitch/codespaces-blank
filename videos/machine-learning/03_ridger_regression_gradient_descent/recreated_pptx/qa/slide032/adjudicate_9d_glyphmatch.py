#!/usr/bin/env python3
"""Adjudicate_9d — glyph-by-glyph comparison of the right label, ORIG vs REND9.

The RENDER definitively prints "(7, 7)" (build/slide_032.js:200 draws it), so its
right chip is a ground-truth "7" template. If the ORIGINAL's right chip has the
same shape, the original reads "(7, 7)"; if not, the judge's "(?, ?)" claim is
upheld. Rendered "?" and digit templates at matched size are the tiebreaker.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

o = np.asarray(Image.open(V + "/unique_slides/slide_032.jpg").convert("L")).astype(float)
rim = Image.open(V + "/recreated_pptx/qa/slide032/render_9.png").convert("L")
S = rim.size[1] / 540.0


def frame_crop_render(x0, y0, x1, y1):
    """render patch for a frame-px bbox, downsampled to ~1 render px per frame px"""
    sub = rim.crop((int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S)))
    w = max(1, int(round((x1 - x0)))); h = max(1, int(round((y1 - y0))))
    return np.asarray(sub.resize((w, h), Image.LANCZOS)).astype(float)


def amap(a, label, x0, y0):
    print(f"--- {label} (frame x{x0}..{x0 + a.shape[1]} y{y0}..{y0 + a.shape[0]}) ---")
    for ry in range(a.shape[0]):
        print(f"  {int(y0) + ry:>3} " + "".join(
            "#" if v < 120 else ("+" if v < 175 else ("." if v < 225 else " ")) for v in a[ry, :]))
    print()


def tmpl(ch, px_size):
    f = ImageFont.truetype(FONT, px_size)
    bb = f.getbbox(ch)
    im = Image.new("L", (bb[2] - bb[0] + 4, bb[3] - bb[1] + 4), 255)
    d = ImageDraw.Draw(im)
    d.text((2 - bb[0], 2 - bb[1]), ch, font=f, fill=0)
    a = np.asarray(im).astype(float)
    ink = (a < 200)
    rs = np.nonzero(ink.sum(axis=1))[0]; cs = np.nonzero(ink.sum(axis=0))[0]
    return a[rs[0]:rs[-1] + 1, cs[0]:cs[-1] + 1]


def fit(t, w):
    """best ink-IoU of template t inside window w over all alignments"""
    th, tw = t.shape; wh, ww = w.shape
    ti = (t < 200); wi = (w < 200)
    best = 0.0; bp = None
    for dy in range(wh - th + 1):
        for dx in range(ww - tw + 1):
            a = wi[dy:dy + th, dx:dx + tw]
            inter = (a & ti).sum(); union = (a | ti).sum()
            s = inter / union if union else 0.0
            if s > best:
                best, bp = s, (dx, dy)
    return best, bp


print("#" * 74)
print("# RIGHT chip — the decisive glyph")
print("#" * 74)
print("  ORIGINAL (frame, 1 char = 1 px):")
amap(o[138:157, 742:762], "ORIG right chip", 742, 138)
rc = frame_crop_render(742, 138, 762, 157)
print("  RENDER (downsampled to frame scale from 2.0833x):")
amap(rc, "REND9 right chip", 742, 138)
print("  font templates that fitted, scored by ink-IoU into each image:")
w = np.minimum(o[138:157, 742:762] * 1.0, 255)
res = []
for ch in "0123456789?.":
    for size in range(8, 14):
        t = tmpl(ch, size)
        s1, _ = fit(t, o[138:157, 742:762])
        s2, _ = fit(t, rc)
        res.append((s1 + s2, s1, s2, ch, size))
res.sort(reverse=True)
for tot, s1, s2, ch, size in res[:14]:
    print(f"    IoU ORIG {s1:.3f}  REND {s2:.3f}   {ch!r} size {size}")
print()

print("#" * 74)
print("# LEFT chip of the same label — control (render draws '7' there too)")
print("#" * 74)
print("  ORIGINAL:")
amap(o[138:157, 729:744], "ORIG left chip", 729, 138)
lc = frame_crop_render(729, 138, 744, 157)
print("  RENDER:")
amap(lc, "REND9 left chip", 729, 138)
res = []
for ch in "0123456789?.":
    for size in range(8, 14):
        t = tmpl(ch, size)
        s1, _ = fit(t, o[138:157, 729:744])
        s2, _ = fit(t, lc)
        res.append((s1 + s2, s1, s2, ch, size))
res.sort(reverse=True)
for tot, s1, s2, ch, size in res[:14]:
    print(f"    IoU ORIG {s1:.3f}  REND {s2:.3f}   {ch!r} size {size}")
print()

print("#" * 74)
print("# shape distance ORIG-right vs REND-right, both normalized to the same box")
print("#" * 74)
a = (o[138:157, 742:762] < 200).astype(float)
b = (rc < 200).astype(float)


def norm(mask):
    ys, xs = np.nonzero(mask)
    m = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return m / 255.0 * 0 + m


na, nb = norm(a), norm(b)
h = max(na.shape[0], nb.shape[0]); w_ = max(na.shape[1], nb.shape[1])
pa = np.zeros((h, w_)); pb = np.zeros((h, w_))
pa[:na.shape[0], :na.shape[1]] = na
pb[:nb.shape[0], :nb.shape[1]] = nb
# best-align shift
best = 1e9
for dy in range(-2, 3):
    for dx in range(-2, 3):
        sb = np.roll(np.roll(pb, dy, axis=0), dx, axis=1)
        d = (pa ^ sb).sum() / max(1, (pa | sb).sum())
        best = min(best, d)
print(f"  XOR distance ORIG-right vs REND-right (normalized): {best:.3f}")
print(f"  ink px ORIG-right {int(a.sum())}   REND-right {int(b.sum())}")
print(f"  bbox ORIG-right {a.shape}   REND-right {b.shape}")
