#!/usr/bin/env python3
r"""Certified equation builder for slide 015 (deck 03).

Regenerates build/assets/eq_015_*.png + eq015_table.json from the banked
qa/slide_015/build_eq_015.py recipe with three corrections measured against
unique_slides/slide_015.jpg:

  1. FONT: matplotlib's default `dejavusans` mathtext draws `J` as a near
     vertical stem, which the visual judge read as a bar ("|)(W)").  The
     `cm` (Computer Modern) fontset draws a serif italic J with a top bar and
     a bottom hook, and also matches the original's serif math face.

  2. COLOUR: the palette is measured from the frame (scratch/tmp/census015c.py
     + scratch/tmp/census015b.py), not assumed:
        body            #000000
        J(W) head       #00008B  (frame core ~#0000B5)
        lambda terms    #267D1E  (frame core25 #267D1E)
        pink-box eq     #1A0090  (frame core #150184 - violet, not black)
        peach-box eq    #3B2408  (frame core #251405 - dark brown, not black)
        solution -1     #B00000  (frame core #910707)

  3. The parts are located in the black skeleton by FFT correlation and pasted
     aligned, so the coloured ink lands exactly ON the black glyphs (a term
     coloured at the wrong offset is the "green scribble over black text"
     defect the judge flagged on the earlier renders).  A per-tag alignment
     report is printed: the composite's ink mask must match the skeleton.

The builder is width-matched to the frame's measured ink widths (INK_W), and
the ink is centred in the frame's own ink band (BAND), so the vertical rhythm
matches the original.
"""
import gc
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["mathtext.fontset"] = "cm"
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
VID = "videos/machine-learning/03_ridger_regression_gradient_descent"
ASSETS = os.path.join(ROOT, VID, "recreated_pptx/build/assets")
TMP = os.path.join(ROOT, "scratch", "tmp")

DPI = 600
PAD = 8
FIG_W, FIG_H = 12, 2
CANVAS_W_PT = FIG_W * 72

BLACK = "#000000"
BLUE = "#00008B"
GREEN = "#267D1E"
VIOLET = "#1A0090"
BROWN = "#3B2408"
RED = "#B00000"

# Frame ink bboxes (unique_slides/slide_015.jpg, 1px = 1pt), verified by the
# banked qa/slide_015/reink_015.py.
EQ = {
    "eq1_l1": (19, r"J(\underline{W}) = \frac{1}{2}(Y-\hat{Y})^{T}(Y-\hat{Y})"
                  r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}"
                  r" = \frac{1}{2}(Y-XW)^{T}(Y-XW)"
                  r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}",
               [(r"J(\underline{W})", BLUE),
                (r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}", GREEN)]),
    "eq1_l2": (20, r"J(\underline{W}) = \frac{1}{2}[Y^{T}Y + (XW)^{T}(XW)"
                  r" - Y^{T}(XW) - (XW)^{T}Y]"
                  r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}",
               [(r"J(\underline{W})", BLUE),
                (r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}", GREEN)]),
    "eq1_l3": (19, r"J(\underline{W}) = \frac{1}{2}[Y^{T}Y + (XW)^{T}(XW)"
                  r" - 2(XW)^{T}Y] + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}",
               [(r"J(\underline{W})", BLUE),
                (r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}", GREEN)]),
    "redbox_eq": (35, r"\frac{\partial J(\underline{W})}{\partial \underline{W}} = 0", []),
    "peach_eq": (20, r"\frac{\partial W^{T}W}{\partial W} = 2W", []),
    "deriv_l1": (22, r"\frac{\partial J(\underline{W})}{\partial \underline{W}} = 0"
                    r" = \frac{1}{2}[(XW)^{T}(X) + (X)^{T}(XW)"
                    r" - 2(X)^{T}Y] + \lambda \underline{W}",
                 [(r"J(\underline{W})", BLUE), (r" + \lambda \underline{W}", GREEN)]),
    "deriv_l2": (21, r"\frac{\partial J(\underline{W})}{\partial \underline{W}} = 0"
                    r" = \frac{1}{2}[2X^{T}XW - 2X^{T}Y] + \lambda I \underline{W}",
                 [(r"J(\underline{W})", BLUE),
                  (r" + \lambda I \underline{W}", GREEN)]),
    "normal": (30, r"(X^{T}X + \lambda I)\underline{W} = X^{T}Y",
               [(r"\lambda I", GREEN)]),
    "solution": (30, r"\underline{W} = (X^{T}X + \lambda I)^{-1}X^{T}Y",
                 [(r"\lambda I", GREEN), (r"^{-1}", RED)]),
}

# Base ink colour of the whole equation when it is not black.
BASE_COLOR = {
    "redbox_eq": VIOLET,
    "peach_eq": BROWN,
}

# Parts that may be dropped without failing the build (the -1 exponent is a
# 2-glyph superscript; if it cannot be located the equation still reads).
OPTIONAL_PARTS = {"solution": {r"^{-1}"}}

BAND = {
    "eq1_l1": (97, 104, 154), "eq1_l2": (97, 163, 213), "eq1_l3": (97, 216, 266),
    "redbox_eq": (81, 275, 334),
    "peach_eq": (791, 295, 329),
    "deriv_l1": (79, 350, 404), "deriv_l2": (79, 415, 468),
    "normal": (229, 468, 519),
    "solution": (553, 472, 516),
}

MAX_EXTENT = {
    "eq1_l1": (705, 50), "eq1_l2": (674, 50), "eq1_l3": (566, 50),
    "redbox_eq": (620, 58), "peach_eq": (106, 54),
    "deriv_l1": (580, 56), "deriv_l2": (430, 56),
    "normal": (300, 52),
    "solution": (333, 44),
}
MIN_FS = 7

INK_W = {
    "eq1_l1": 695, "eq1_l2": 664, "eq1_l3": 556,
    "redbox_eq": 97,
    "peach_eq": 100,
    "deriv_l1": 574, "deriv_l2": 421,
    "normal": 273, "solution": 332,
}

SCRIPT_SCALE = 0.70


def render_canvas(tex, fs, color):
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${tex}$", fontsize=fs, color=color, ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    plt.close(fig)
    return buf


def fft_locate(needle_mask, haystack_mask, min_score=0.80):
    H, W = haystack_mask.shape
    h, w = needle_mask.shape
    if h > H or w > W:
        return []
    fh = np.fft.rfft2(haystack_mask.astype(np.float32), s=(H, W))
    fn = np.fft.rfft2(needle_mask[::-1, ::-1].astype(np.float32), s=(H, W))
    corr = np.fft.irfft2(fh * fn, s=(H, W))
    total = float(needle_mask.sum())
    scores = corr / total
    out = []
    for _ in range(8):
        idx = int(np.argmax(scores))
        y, x = np.unravel_index(idx, scores.shape)
        if scores[y, x] < min_score:
            break
        out.append((int(x), int(y), float(scores[y, x])))
        y0, y1 = max(0, y - h), min(H, y + 2 * h)
        x0, x1 = max(0, x - w), min(W, x + 2 * w)
        scores[y0:y1, x0:x1] = 0.0
    deduped = []
    for hx, hy, sc in out:
        if any(abs(hx - dx) <= max(w // 2, 8) and abs(hy - dy) <= max(h // 2, 8)
               for dx, dy, _ in deduped):
            continue
        deduped.append((hx, hy, sc))
    return deduped


def measure(buf):
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    return (int(cols[-1] - cols[0] + 1) * 72.0 / DPI,
            int(rows[-1] - rows[0] + 1) * 72.0 / DPI)


def build_composite(tex, fs, parts, tag, base=BLACK):
    """Black/base skeleton render + each coloured part located inside it by FFT
    correlation and pasted ink-left/baseline aligned.  Returns (rgba, report)."""
    buf = render_canvas(tex, fs, base)
    skeleton = (buf[:, :, 3] > 8)
    haystack = skeleton.astype(np.float32)
    out = buf.copy()
    h, w = out.shape[:2]
    report = []
    for needle, color in parts:
        cand = None
        for sc in (1.0, SCRIPT_SCALE):
            pbuf = render_canvas(needle, fs * sc, color)
            pm = pbuf[:, :, 3] > 8
            if not pm.any():
                continue
            npys, npxs = np.where(pm)
            part_x0, part_y0 = int(npxs.min()), int(npys.min())
            part_x1, part_y1 = int(npxs.max()) + 1, int(npys.max()) + 1
            core = pm[max(0, part_y0 - 4):part_y1 + 4,
                      max(0, part_x0 - 4):part_x1 + 4].astype(np.float32)
            core_ox, core_oy = max(0, part_x0 - 4), max(0, part_y0 - 4)
            hits = fft_locate(core, haystack)
            if hits:
                cand = (sc, hits, core_ox, core_oy, pbuf)
                break
        if cand is None:
            if needle in OPTIONAL_PARTS.get(tag, ()):
                print(f"  {tag}: OPTIONAL part {needle!r} not located - skipped")
                report.append((needle, color, 0, 0.0))
                continue
            raise SystemExit(f"could not locate {needle!r} in {tag}")
        sc, hits, core_ox, core_oy, pbuf = cand
        n = 0
        for hx, hy, score in hits:
            dx, dy = hx - core_ox, hy - core_oy
            n_ys, n_ye = max(0, dy), min(h, dy + pbuf.shape[0])
            n_xs, n_xe = max(0, dx), min(w, dx + pbuf.shape[1])
            if n_ye <= n_ys or n_xe <= n_xs:
                continue
            region = pbuf[n_ys - dy:n_ye - dy, n_xs - dx:n_xe - dx]
            assert region.shape[:2] == (n_ye - n_ys, n_xe - n_xs)
            out[n_ys:n_ye, n_xs:n_xe] = np.where(region[:, :, 3:4] > 20, region,
                                                 out[n_ys:n_ye, n_xs:n_xe])
            n += 1
        print(f"  {tag}: {needle!r} -> {color} scale {sc:.2f} hits={n} "
              f"scores={[round(s, 3) for _, _, s in hits]}")
        report.append((needle, color, n, hits[0][2] if hits else 0.0))
    # alignment check: every composite ink pixel must sit within 3px of
    # skeleton ink.  The pasted part's own antialias halo legitimately adds a
    # few pixels outside the skeleton, but a mis-aligned part (the "green
    # scribble over black text" defect of the earlier renders) spreads ink
    # far from the glyphs it was meant to colour.
    comp_ink = out[:, :, 3] > 8
    dil = skeleton.copy()
    d = 3
    dil[d:-d, d:-d] |= skeleton[:-2 * d, d:-d]
    dil[d:-d, d:-d] |= skeleton[2 * d:, d:-d]
    dil[d:-d, d:-d] |= skeleton[d:-d, :-2 * d]
    dil[d:-d, d:-d] |= skeleton[d:-d, 2 * d:]
    dil[d:-d, d:-d] |= skeleton[:-2 * d, :-2 * d]
    dil[d:-d, d:-d] |= skeleton[:-2 * d, 2 * d:]
    dil[d:-d, d:-d] |= skeleton[2 * d:, :-2 * d]
    dil[d:-d, d:-d] |= skeleton[2 * d:, 2 * d:]
    stray = int((comp_ink & ~dil).sum())
    print(f"  {tag}: alignment stray={stray}px (composite ink "
          f"{int(comp_ink.sum())}px, skeleton {int(skeleton.sum())}px)")
    if stray > max(64, 0.02 * int(comp_ink.sum())):
        raise SystemExit(f"{tag}: {stray}px of coloured ink sits off the skeleton "
                         "- would render as overstrike, not colour")
    return out, report


def render_fit(tag, fs, tex, parts):
    base = BASE_COLOR.get(tag, BLACK)
    target_w = INK_W.get(tag)
    lim_w, lim_h = MAX_EXTENT[tag]

    def build(f):
        return build_composite(tex, f, parts, tag, base)[0] if parts else \
            render_canvas(tex, f, base)

    if target_w:
        out = build(fs)
        w = measure(out)[0]
        ceiling = fs * (CANVAS_W_PT * 0.92) / max(w, 1e-6)
        for _ in range(3):
            f = fs * target_w / max(w, 1e-6)
            f = max(float(MIN_FS), min(f, ceiling))
            fi = max(MIN_FS, int(round(f)))
            if fi == fs:
                break
            out = build(fi)
            fs, w = fi, measure(out)[0]
        while fs > MIN_FS and w > target_w + 1:
            fs -= 1
            out = build(fs)
            w = measure(out)[0]

    while fs > MIN_FS:
        w, h = measure(out)
        if w <= lim_w + 1 and h <= lim_h + 1:
            break
        shrink = min(lim_w / max(w, 1e-6), lim_h / max(h, 1e-6))
        fs = max(MIN_FS, int(fs * shrink))
        out = build(fs)

    ink = out[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    return fs, out, int(cols[-1] - cols[0] + 1), int(rows[-1] - rows[0] + 1)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    table = {}
    for tag, (fs, tex, parts) in EQ.items():
        fs, out, w_px, h_px = render_fit(tag, fs, tex, parts)
        ink = out[:, :, 3] > 8
        rows = np.where(ink.any(axis=1))[0]
        cols = np.where(ink.any(axis=0))[0]
        y0, y1 = max(rows[0] - PAD, 0), min(rows[-1] + PAD, out.shape[0])
        x0, x1 = max(cols[0] - PAD, 0), min(cols[-1] + PAD, out.shape[1])
        tight = out[y0:y1, x0:x1]
        png = os.path.join(ASSETS, f"eq_015_{tag}.png")
        Image.fromarray(tight).save(png)
        h_px, w_px = int(tight.shape[0]), int(tight.shape[1])
        w_in, h_in = round(w_px / 600, 5), round(h_in / 600, 5)
        ink_x, band_y0, band_y1 = BAND[tag]
        h_pt = h_px * 72.0 / DPI
        py = int(round((band_y0 + band_y1) / 2.0 - h_pt / 2.0))
        px = int(ink_x)
        sidecar = {
            "path": png, "w_px": w_px, "h_px": h_px, "w_in": w_in, "h_in": h_in,
            "dpi": DPI, "pad_px": PAD, "fontsize_pt": fs,
            "color": BASE_COLOR.get(tag, BLACK).lstrip("#"),
            "mathtext": tex,
            "symbol_colors": {"default": BASE_COLOR.get(tag, BLACK).lstrip("#"),
                              **{f"part{i}": c.lstrip("#") for i, (_, c) in enumerate(parts)}},
            "orig_ink_px": [ink_x, ink_x + round(w_in * 72) - 1,
                            py, py + round(h_in * 72) - 1],
            "notes": "2D mathtext (Computer Modern) composite: base skeleton + "
                     "coloured parts located by FFT correlation and pasted on the "
                     "shared canvas baseline",
        }
        json.dump(sidecar, open(os.path.join(ASSETS, f"eq_015_{tag}.json"), "w"), indent=1)
        table[tag] = {"png": png, "w_in": w_in, "h_in": h_in, "x_frame": px,
                      "y_frame": py, "fontsize_pt": fs,
                      "w_pt": round(w_in * 72), "h_pt": round(h_in * 72)}
        arr = np.asarray(Image.open(png).convert("RGBA")).astype(int)
        am = arr[:, :, 3] > 40
        if am.any():
            want = {BASE_COLOR.get(tag, BLACK).lstrip("#").lower()}
            want |= {c.lstrip("#").lower() for _, c in parts}
            rgbpx = arr[:, :, :3][am]

            def nearest(p):
                best, bd = None, 1e9
                for tgt in want:
                    t = [int(tgt[i:i + 2], 16) for i in (0, 2, 4)]
                    d = sum((p[i] - t[i]) ** 2 for i in range(3))
                    if d < bd:
                        best, bd = tgt, d
                return best

            uniq = {}
            for p in rgbpx[:: max(1, len(rgbpx) // 4000)]:
                n = nearest(tuple(p))
                uniq[n] = uniq.get(n, 0) + 1
            print(f"  {tag}: colours {uniq} (targets {sorted(want)})")
        print(f"{tag:10s} fs={fs:3d} {w_px:5d}x{h_px:4d}px  frame {round(w_in*72)}x{round(h_in*72)}pt  "
              f"ink->({px},{py})")
        del out, tight, arr
        gc.collect()
    json.dump(table, open(os.path.join(ASSETS, "eq015_table.json"), "w"), indent=1)
    print("WROTE " + os.path.join(ASSETS, "eq015_table.json"))


if __name__ == "__main__":
    sys.exit(main())
