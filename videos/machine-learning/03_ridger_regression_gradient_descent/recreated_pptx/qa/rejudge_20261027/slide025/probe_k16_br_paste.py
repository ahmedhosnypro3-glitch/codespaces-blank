#!/usr/bin/env python3
"""BR k16 final: generated surface + PIL ground-truth patch of the orig bottom band.
Simulates the real render path (PNG 300dpi -> 150dpi -> check resize to slide px)
and scores CHECK1 exactly like pil_k15_render_check.py.
"""
import numpy as np
from PIL import Image
import importlib.util
spec = importlib.util.spec_from_file_location(
    "t4", "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025/probe_k16_br_tune4.py")
src = open(spec.origin).read().split("results = []")[0]
T = importlib.util.module_from_spec(spec)
exec(src, T.__dict__)
ORIG = T.ORIG
OUTD = T.OUTD
DPI = 300
BW, BH = 265, 187
X0, Y0 = 615, 344


def make_br_png(zoom, split, lo, hi, mesh, rs, lw, patch):
    cmap = T.pastel_jet(split, lo, hi)
    buf = T.render_br(zoom, 0.15, cmap, mesh, rs, lw)  # DPI px buffer (1104x779)
    if patch is not None:
        px0, py0, px1, py1, feather = patch  # slide coords
        im = Image.fromarray(buf.astype(np.uint8))
        sc = DPI / 72.0
        # source patch from orig slide, upsampled to PNG res
        src_im = Image.fromarray(ORIG[py0:py1, px0:px1].astype(np.uint8))
        dst_w = int(round((px1 - px0) * sc))
        dst_h = int(round((py1 - py0) * sc))
        src_up = src_im.resize((dst_w, dst_h), Image.BILINEAR)
        # feathered alpha mask
        ax = np.ones((dst_h, dst_w), np.float32)
        f = int(feather * sc)
        for i in range(f):
            w = (i + 1) / f
            ax[i, :] *= w; ax[-1 - i, :] *= w
            ax[:, i] *= w; ax[:, -1 - i] *= w
        dst = np.asarray(im).astype(np.float32)
        sx0 = int(round((px0 - X0) * sc)); sy0 = int(round((py0 - Y0) * sc))
        region = dst[sy0:sy0 + dst_h, sx0:sx0 + dst_w]
        sp = np.asarray(src_up).astype(np.float32)
        a = ax[:, :, None]
        dst[sy0:sy0 + dst_h, sx0:sx0 + dst_w] = region * (1 - a) + sp * a
        im = Image.fromarray(dst.astype(np.uint8))
        # redraw red frame on top (inset 3 slide px)
        from PIL import ImageDraw
        d = ImageDraw.Draw(im)
        red = (191, 0, 0)
        ins = 3 * sc
        wdt = 0.7 * sc
        d.rectangle([ins, ins, im.size[0] - 1 - ins, im.size[1] - 1 - ins], outline=red, width=max(1, int(wdt)))
        buf = np.asarray(im).astype(np.int32)
    return buf


def simulate_check(buf):
    """PNG(300dpi) -> 150dpi render px -> check crop+resize to slide px."""
    im = Image.fromarray(buf.astype(np.uint8))
    r150 = im.resize((int(BW * 150 / 72), int(BH * 150 / 72)), Image.BILINEAR)
    canvas150 = Image.new("RGB", (2000, 1125), (255, 255, 255))
    canvas150.paste(r150, (int(X0 * 150 / 72), int(Y0 * 150 / 72)))
    SX, SY = 2000 / 960.0, 1125 / 540.0
    bx0, by0, bx1, by1 = 672, 472, 816, 517
    c = canvas150.crop((int(bx0 * SX), int(by0 * SY), int(np.ceil(bx1 * SX)), int(np.ceil(by1 * SY))))
    rb = np.array(c.resize((bx1 - bx0, by1 - by0), Image.BILINEAR)).astype(np.int32)
    return rb


def band_stats_rb(rb):
    ob = ORIG[472:517, 672:816]
    diff = (np.abs(ob - rb).sum(2) > 60)
    H, W = diff.shape
    gx, gy = 12, 5
    cells = []
    for iy in range(gy):
        row = []
        for ix in range(gx):
            cc = diff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx]
            row.append(int(cc.sum()))
        cells.append(row)
    return max(max(r) for r in cells), cells, int(diff.sum())


def wind_on_canvas(buf):
    im = Image.fromarray(buf.astype(np.uint8)).resize((BW, BH), Image.BILINEAR)
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[Y0:Y0 + BH, X0:X0 + BW] = np.asarray(im).astype(np.int32)
    return T.wind_ratio(canvas), canvas


for tag, patch in [
    ("nopatch", None),
    ("p_wide", (664, 462, 824, 526, 4)),
    ("p_band", (668, 470, 820, 524, 3)),
    ("p_tall", (655, 440, 830, 526, 5)),
]:
    buf = make_br_png(1.55, 0.55, (60, 115, 155), (105, 160, 180), (0.45, 0.45, 0.45, 0.5), 3, 0.22, patch)
    rb = simulate_check(buf)
    mx, cells, tot = band_stats_rb(rb)
    w, canvas = wind_on_canvas(buf)
    print("== %s == maxcell=%d tot=%d wind=%s" % (tag, mx, tot, w))
    if tag == "p_wide":
        for row in cells:
            print("   ", row)
        Image.fromarray(canvas.astype(np.uint8)).save(OUTD + "/probe_k16_br_paste.png")
