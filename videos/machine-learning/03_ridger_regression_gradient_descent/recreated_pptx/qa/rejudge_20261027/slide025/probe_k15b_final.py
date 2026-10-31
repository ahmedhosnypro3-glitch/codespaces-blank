#!/usr/bin/env python3
"""Verify assets_k15b: BL red-x marker comps mapped to slide px; BR surface
silhouette/winding/margin vs orig; TR red segment coverage orig vs promoted render."""
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
SPEC = {"bl": dict(x0=83, y0=290, w=293, h=237),
        "br": dict(x0=615, y0=344, w=265, h=187)}

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)


def red_mask(a):
    return (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)


def comps(mask, min_area=6):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        area = len(xs)
        if area < min_area:
            continue
        bw, bh = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        out.append((area, xs.min(), ys.min(), xs.max(), ys.max(), bw, bh,
                    area / (bw * bh)))
    return out


# ── BL markers in assets_k15b/plot_025_bl.png ────────────────────────────────
print("== BL assets_k15b red comps (panel px -> slide px) ==")
bl = np.array(Image.open(RJ + "/assets_k15b/plot_025_bl.png").convert("RGB")).astype(np.int32)
H, W = bl.shape[:2]
s = SPEC["bl"]
rm = red_mask(bl)
# exclude redrect frame: border inset 3 slide px -> 3/293*W etc.
bx = int(round(3 / s["w"] * W)) + 2
by = int(round(3 / s["h"] * H)) + 2
rm[:by, :] = False; rm[-by:, :] = False; rm[:, :bx] = False; rm[:, -bx:] = False
for (area, x0, y0, x1, y1, bw, bh, fill) in comps(rm, 6):
    if bw > 40 or bh > 40:  # hilltop blobs are big; markers are small x's
        continue
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    sx = s["x0"] + cx / W * s["w"]
    sy = s["y0"] + (1 - cy / H) * s["h"]
    print("  marker-like area=%d bbox=%dx%d fill=%.2f slide=(%.0f,%.0f)" % (
        area, bw, bh, fill, sx, sy))

# same for the promoted k15 asset for contrast
print("== BL build/assets (promoted k15) red comps ==")
bl0 = np.array(Image.open(NS + "/recreated_pptx/build/assets/plot_025_bl.png").convert("RGB")).astype(np.int32)
H0, W0 = bl0.shape[:2]
rm0 = red_mask(bl0)
rm0[:by, :] = False; rm0[-by:, :] = False; rm0[:, :bx] = False; rm0[:, -bx:] = False
for (area, x0, y0, x1, y1, bw, bh, fill) in comps(rm0, 6):
    if bw > 40 or bh > 40:
        continue
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    sx = s["x0"] + cx / W0 * s["w"]
    sy = s["y0"] + (1 - cy / H0) * s["h"]
    print("  marker-like area=%d bbox=%dx%d fill=%.2f slide=(%.0f,%.0f)" % (
        area, bw, bh, fill, sx, sy))

# orig markers for reference
print("== BL orig red comps (slide px, small only) ==")
rmo = red_mask(orig)
rmo[290:527, 83:376]
sub = np.zeros_like(rmo); sub[290:527, 83:376] = rmo[290:527, 83:376]
for (area, x0, y0, x1, y1, bw, bh, fill) in comps(sub, 6):
    if bw > 25 or bh > 25:
        continue
    print("  marker-like area=%d bbox=%dx%d fill=%.2f slide=(%.0f,%.0f)" % (
        area, bw, bh, fill, (x0 + x1) / 2, (y0 + y1) / 2))

# ── BR: paste assets_k15b br at box, compare to orig ─────────────────────────
print("== BR silhouette: orig vs assets_k15b pasted at box ==")


def br_stats(canvas):
    b = SPEC["br"]
    ob = canvas[b["y0"]:b["y0"] + b["h"], b["x0"]:b["x0"] + b["w"]]
    mx, mn = ob.max(2), ob.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    m &= ~red_mask(ob)
    ys, xs = np.nonzero(m)
    row = 100.0 * m.mean(1)
    return (b["x0"] + xs.min(), b["x0"] + xs.max(), b["y0"] + ys.min(),
            b["y0"] + ys.max(), row, m)


ox0, ox1, oy0, oy1, orow, om = br_stats(orig)
print("orig: bbox x%d..%d y%d..%d  row%% @455=%d @490=%d @517=%d @524=%d" % (
    ox0, ox1, oy0, oy1, orow[455 - 344], orow[490 - 344], orow[517 - 344],
    orow[524 - 344]))

for tag, path in (("k15b", RJ + "/assets_k15b/plot_025_br.png"),
                  ("k15", NS + "/recreated_pptx/build/assets/plot_025_br.png")):
    im = Image.open(path).convert("RGB").resize((SPEC["br"]["w"], SPEC["br"]["h"]), Image.LANCZOS)
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[SPEC["br"]["y0"]:SPEC["br"]["y0"] + SPEC["br"]["h"],
           SPEC["br"]["x0"]:SPEC["br"]["x0"] + SPEC["br"]["w"]] = np.array(im).astype(np.int32)
    x0, x1, y0, y1, row, m = br_stats(canvas)
    print("%s: bbox x%d..%d y%d..%d (w=%d h=%d)  row%% @455=%d @490=%d @517=%d @524=%d" % (
        tag, x0, x1, y0, y1, x1 - x0, y1 - y0, row[455 - 344], row[490 - 344],
        row[517 - 344], row[524 - 344]))
    # winding: dark path ink
    dk = (canvas[:, :, 0] < 80) & (canvas[:, :, 1] < 80) & (canvas[:, :, 2] < 80)
    b = SPEC["br"]
    sub = np.zeros_like(dk); sub[b["y0"]:b["y0"] + b["h"], b["x0"]:b["x0"] + b["w"]] = dk[b["y0"]:b["y0"] + b["h"], b["x0"]:b["x0"] + b["w"]]
    lab, n = ndimage.label(sub, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 40:
            continue
        pts = np.stack([xs, ys], 1).astype(float)
        # path length via sorted-by-x chain is unreliable; use comp span vs euclid of ends
        if best is None or len(xs) > best[0]:
            best = (len(xs), xs.min(), xs.max(), ys.min(), ys.max())
    if best:
        area, bx0, bx1, by0, by1 = best
        span = np.hypot(bx1 - bx0, by1 - by0)
        print("   dark path comp area=%d spanx=%d spany=%d diag=%.1f" % (area, bx1 - bx0, by1 - by0, span))

# ── TR red segments: orig vs promoted render.png ────────────────────────────
print("== TR red segment coverage (slide px) ==")


def seg_cov(a, x0, y0, x1, y1):
    n = 60
    xs = np.linspace(x0, x1, n).astype(int)
    ys = np.linspace(y0, y1, n).astype(int)
    m = red_mask(a)[ys, xs]
    return 100.0 * m.mean()


rend = np.array(Image.open(RJ + "/render.png").convert("RGB")).astype(np.int32)
SX, SY = 2001 / 960.0, 1125 / 540.0


def ren(x, y):
    return int(round(x * SX)), int(round(y * SY))


segs = {"A_long(655,189)->(860,209)": (655, 189, 860, 209),
        "B(737,210)->(755,225)": (737, 210, 755, 225),
        "steep(652,165)->(667,189)": (652, 165, 667, 189),
        "horiz y226 x620..875": None}
for name, s_ in segs.items():
    if s_ is None:
        m_o = red_mask(orig)[226, 620:876].mean() * 100
        xs = np.arange(620, 876) * SX
        m_r = red_mask(rend)[int(226 * SY), np.round(xs).astype(int)].mean() * 100
    else:
        x0, y0, x1, y1 = s_
        m_o = seg_cov(orig, x0, y0, x1, y1)
        rx0, ry0 = ren(x0, y0); rx1, ry1 = ren(x1, y1)
        m_r = seg_cov(rend, rx0, ry0, rx1, ry1)
    print("  %-28s orig=%5.1f%%  render=%5.1f%%" % (name, m_o, m_r))
