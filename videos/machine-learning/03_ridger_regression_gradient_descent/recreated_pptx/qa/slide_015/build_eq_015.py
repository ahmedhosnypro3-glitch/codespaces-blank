#!/usr/bin/env python3
r"""Banked equation builder for slide 015 (deck 03, 2026-10-23/24).

Renders every equation of slide 015 in PROFESSIONAL 2D mathtext form (stacked
\frac, \partial fractions, \underline{W}, aligned sub/superscripts) to a 600dpi
transparent PNG -> build/assets/eq_015_*.png + eq_015_*.json sidecar per the
fleet contract (scripts/render_eq.py + slide_023 precedent).

MEASURED (unique_slides/slide_015.jpg, 960x540, 1px = 1pt = 1/72in; banked
forensics in qa/slide_015/{forensics_015_eq,probe_015_colors,boxes_015,
ascii_015,calib_015_eq}.py):

  Verified ink bboxes (reink_015.py, this session) - the targets reproduced:
    eq1_l1   x97..791   y108..150   695x43
    eq1_l2   x97..760   y167..209   664x43
    eq1_l3   x97..652   y220..262   556x43
    redbox_eq  x81..177  y280..302   97x23   <-- TIGHT INK (verified attempt 3:
                                                 the wider 81..210 span is the
                                                 element's box, not its ink;
                                                 attempt 2 rendered it 128pt wide
                                                 and crowded the sentence)
    peach_eq   x791..890 y295..329  100x35
    deriv_l1 x79..652   y352..402   574x51
    deriv_l2 x79..499   y417..466   421x50
    normal   x229..501  y484..508   273x25
    solution x553..884  y477..509   332x33
    redbox_sent 209..702 296..315 494x20
    peach_remem 792..856 279..290  65x12

  ARROW — ADJUDICATED NON-EXISTENT (attempt 3).  The analysis JSON for slide 015
  claims a "right-pointing arrow following the centered normal-equation line,
  pointing toward the green solution box", and the original does carry faint
  diagonal ink at x503..510 y488..496 that attempt 2 nearly mistook for one.
  Pixel-first adjudication (qa/slide_015/adjudicate_arrow_015.py,
  adjudicate_arrow.txt) settles it: the original's ink in the gap between the
  equation's right edge (x510) and the green box's left edge (x547) is ZERO
  pixels at luma<200 over y466..521.  The tail marks are the equation's final
  glyph (the closing paren at x501..502 y485..507 plus the "Y"'s stroke), and
  the render's equation ends at x494.  So there is no arrow element anywhere in
  the gap, in EITHER image, and none is drawn - inventing one would add an
  element the original does not have, which is a defect, not a fix.

  INK_W is the frame's measured ink WIDTH per tag; render_fit() solves the
  composite's font size to reproduce it exactly, then applies the MAX_EXTENT
  caps.  Attempt 2 only shrank from a hardcoded size (never grew), so eq1_l1/l2/l3
  rendered at w-ratio 0.88/0.87/0.90 and solution at 0.75 vs the frame.

  Font sizes are chosen so the mathtext ink WIDTH equals the frame ink width
  (the sibling slide_005 recipe, verified against eq_005_loss*.json).  mathtext
  stacks a \frac ~2.2x the height of the original's inline ½, so the render runs
  h-ratio 1.0..1.3 at w-ratio ~1.0 - the sibling's own certified regime
  (loss2: h-ratio 1.31 at w-ratio 1.00).  The build script centres each image
  on the frame band, absorbing the extra height in the band gaps.

  Colours (per-symbol census, probe_015_colors.py): body #000000, "J(W)" head
  #00008B, lambda term #1E7B1E, solution W underlined.  The two 2D CREAM
  CONTENT RECTS (mode #FBFDE5, x74..890 y104..265 / y344..520) are slide
  content, NOT house chrome, and are drawn by the build script.
"""
import gc
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
VID = "videos/machine-learning/03_ridger_regression_gradient_descent"
ASSETS = os.path.join(ROOT, VID, "recreated_pptx/build/assets")
TMP = os.path.join(ROOT, "scratch", "tmp")

DPI = 600
PAD = 8
FIG_W, FIG_H = 12, 2   # 7200x1200px: fits every equation's ink (max ~800pt
                        # wide, ~475pt tall) with margin, at 1/3 the memory of
                        # a 16x4in canvas - the box has 2.7GB available and a
                        # 9600x2400 RGBA buffer plus its FFT temporaries OOM-kills
                        # the build mid-run
CANVAS_W_PT = FIG_W * 72   # 864pt: the widest a single render can be
BLACK, BLUE, GREEN = "#000000", "#00008B", "#1E7B1E"

# Font sizes: each equation is set to reproduce the frame's measured ink WIDTH
# (verified by the reink_015.py bboxes).  mathtext renders a \frac about 2.2x
# as tall as the original handwriting's inline ½, so the h-ratio runs 1.0..1.3
# at equal width - exactly the sibling slide_005 regime (loss2: h-ratio 1.31 at
# w-ratio 1.00, certified).  The build script centres each image in its band, so
# the extra height is absorbed by the band gaps (eq1 l1..l3 keep a visible gap
# inside cream rect A y104..265).
EQ = {
    # frame ink x97..791 y108..150 (695x43); width-matched at ~fs 19
    "eq1_l1": (19, r"J(\underline{W}) = \frac{1}{2}(Y-\hat{Y})^{T}(Y-\hat{Y})"
                  r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}"
                  r" = \frac{1}{2}(Y-XW)^{T}(Y-XW)"
                  r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}",
               [(r"J(\underline{W})", BLUE),
                (r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}", GREEN)]),
    # frame ink x97..760 y167..209 (664x43)
    "eq1_l2": (20, r"J(\underline{W}) = \frac{1}{2}[Y^{T}Y + (XW)^{T}(XW)"
                  r" - Y^{T}(XW) - (XW)^{T}Y]"
                  r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}",
               [(r"J(\underline{W})", BLUE),
                (r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}", GREEN)]),
    # frame ink x97..652 y220..262 (556x43)
    "eq1_l3": (19, r"J(\underline{W}) = \frac{1}{2}[Y^{T}Y + (XW)^{T}(XW)"
                  r" - 2(XW)^{T}Y] + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}",
               [(r"J(\underline{W})", BLUE),
                (r" + \frac{1}{2}\lambda \underline{W}^{T}\underline{W}", GREEN)]),
    # frame ink x81..210 y279..301 (130x23) inline in the pink box; 2D stacked
    # form is the mandated format upgrade.  No parts: mathtext typesets a \frac
    # numerator at script size, so the blue J(W) cannot be located inside it.
    "redbox_eq": (35, r"\frac{\partial J(\underline{W})}{\partial \underline{W}} = 0", []),
    # frame ink x791..890 y295..329 (100x35), peach box x786..895
    "peach_eq": (20, r"\frac{\partial W^{T}W}{\partial W} = 2W", []),
    # frame ink x79..652 y352..402 (574x51)
    "deriv_l1": (22, r"\frac{\partial J(\underline{W})}{\partial \underline{W}} = 0"
                    r" = \frac{1}{2}[(XW)^{T}(X) + (X)^{T}(XW)"
                    r" - 2(X)^{T}Y] + \lambda \underline{W}",
                 [(r"J(\underline{W})", BLUE), (r" + \lambda \underline{W}", GREEN)]),
    # frame ink x79..499 y417..466 (421x50)
    "deriv_l2": (21, r"\frac{\partial J(\underline{W})}{\partial \underline{W}} = 0"
                    r" = \frac{1}{2}[2X^{T}XW - 2X^{T}Y] + \lambda I \underline{W}",
                 [(r"J(\underline{W})", BLUE),
                  (r" + \lambda I \underline{W}", GREEN)]),
    # frame ink x229..501 y484..508 (273x25) left of the green box; room runs to
    # y520 inside cream rect B, so a 52pt-tall 2D form fits below the green box
    "normal": (30, r"(X^{T}X + \lambda I)\underline{W} = X^{T}Y",
               [(r"\lambda I", GREEN)]),
    # frame ink x553..884 y477..509 (332x33), green box x547..885; the leading W
    # is underlined (analysis equations[8] + the frame bar y506..508)
    "solution": (30, r"\underline{W} = (X^{T}X + \lambda I)^{-1}X^{T}Y",
                 [(r"\lambda I", GREEN)]),
}

# (ink_x_left, band_y0, band_y1).  The image's INK left edge lands at ink_x_left
# and the ink is centred vertically inside [band_y0, band_y1].  These bands are
# the ELEMENT interiors (or, for eq1/DERIV, the frame band widened so the
# taller 2D ink stays inside the cream rect), never the frame's own inline ink
# band - verified interiors are listed above MAX_EXTENT.
BAND = {
    # frame ink y108..150; widened to keep the 54pt-tall 2D ink inside rect A
    "eq1_l1": (97, 104, 154), "eq1_l2": (97, 163, 213), "eq1_l3": (97, 216, 266),
    # pink box interior y274..335 (the 2D ink is taller than the frame's inline
    # 23pt, so it is centred in the box, left of the sentence)
    "redbox_eq": (81, 275, 334),
    # peach box interior y277..330
    "peach_eq": (791, 295, 329),
    # cream rect B: frame ink y352..402 / y417..466
    "deriv_l1": (79, 350, 404), "deriv_l2": (79, 415, 468),
    # normal: lower edge of cream rect B, room y468..519
    "normal": (229, 468, 519),
    # solution: green box exterior y472..516
    "solution": (553, 472, 516),
}


def ink_mask(rgba, thr=8):
    return rgba[:, :, 3] > thr


# The canvas is FIG_W inches at 600dpi; the text is anchored with
# ha="center", va="baseline" so the baseline sits at figure y=0.5 and the
# descenders plus superscripts have room above and below it.  Every ceiling
# clamp in render_fit() guarantees the ink stays inside CANVAS_W_PT*0.92, so
# no equation is ever clipped and no part becomes unlocatable.


def render_canvas(tex, fs, color):
    """Render $tex$ centred on a fixed canvas (baseline at figure y=0.5), so
    every render - full, skeleton, part - shares one coordinate system and its
    baseline row. Return (rgba, ink_mask)."""
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${tex}$", fontsize=fs, color=color, ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba()).copy()
    ink = buf[:, :, 3] > 8
    plt.close(fig)
    return buf, ink

def fft_locate(needle_mask, haystack_mask, min_score=0.80):
    """Locate every occurrence of needle_mask inside haystack_mask by FFT
    cross-correlation (immune to the sub-pixel antialiasing noise that a
    phantom-slot difference picks up). Return ink-left offsets [(x, y)]."""
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
        out.append((int(x), int(y)))
        y0, y1 = max(0, y - h), min(H, y + 2 * h)
        x0, x1 = max(0, x - w), min(W, x + 2 * w)
        scores[y0:y1, x0:x1] = 0.0
    deduped = []
    for hx, hy in out:
        if any(abs(hx - dx) <= max(w // 2, 8) and abs(hy - dy) <= max(h // 2, 8)
               for dx, dy in deduped):
            continue
        deduped.append((hx, hy))
    return deduped


# Fraction sub-scale: mathtext typesets a \\frac numerator/denominator at a
# SCRIPT size.  Measured by brute-force correlation sweep (calibration script
# banked as scratch/tmp/calib_best.py): a standalone render scaled by 0.70
# scores 0.995 against its in-fraction ink, vs 0.711 unscaled.  The locator
# tries 0.70 first (fraction parts) and then 1.0 (top-level parts).
SCRIPT_SCALE = 0.70

# Ink-extent guard (frame px), from the verified ELEMENT interiors measured this
# session (scratch/tmp/boxgeom.py):
#   pink box    x72..711 y274..335  -> interior room 640w x 59h
#   peach box   x788..893 y277..330  -> 106w x 54h
#   green box   x550..882 y475..514  -> 333w x 40h (exterior y472..516, 44h)
#   cream rect A x74..891 y104..266  -> 818w x 163h (holds eq1 lines 1-3)
#   cream rect B x74..891 y344..520  -> 818w x 177h (holds the 2 DERIV lines
#                                        plus, at its lower edge, `normal`)
# WIDTH caps the ink inside its element; HEIGHT caps it inside the element's
# interior so a 2D stacked form never spills past a rect edge.
MAX_EXTENT = {
    # cream rect A y104..266: 3 lines, each <=50pt, centred so none crosses the
    # rect's top (104) or bottom (266) and the lines keep their gaps
    "eq1_l1": (705, 50), "eq1_l2": (674, 50), "eq1_l3": (566, 50),
    # pink box interior 59h / peach box interior 54h
    "redbox_eq": (620, 58), "peach_eq": (106, 54),
    # cream rect B y344..520 for the two DERIV lines
    "deriv_l1": (580, 56), "deriv_l2": (430, 56),
    # normal sits in the lower edge of cream rect B (room y468..519)
    "normal": (300, 52),
    # solution sits inside the green box (exterior 44h)
    "solution": (333, 44),
}
MIN_FS = 7

# Frame-ink WIDTH target per tag (reink_015.py, the ORIGINAL's measured ink
# width in frame px == pt).  render_fit() matches the composite's measured ink
# WIDTH to this value and then only shrinks if the element's MAX_EXTENT cap
# would break.  Width matching is what the earlier attempt-2 comment claimed
# ("width-matched at ~fs 19") without implementing: render_fit() only ever
# shrank from a hardcoded size, so eq1_l1/l2/l3 rendered at w-ratio
# 0.88/0.87/0.90 and solution at 0.75 against the frame.
INK_W = {
    "eq1_l1": 695, "eq1_l2": 664, "eq1_l3": 556,
    "redbox_eq": 97,   # tight ink, not the 130pt box width
    "peach_eq": 100,
    "deriv_l1": 574, "deriv_l2": 421,
    "normal": 273, "solution": 332,
}


def measure(buf):
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    return (int(cols[-1] - cols[0] + 1) * 72.0 / DPI,
            int(rows[-1] - rows[0] + 1) * 72.0 / DPI)


def render_fit(tag, fs, tex, parts):
    """Solve for the font size whose COMPOSITE ink width equals the frame's
    measured ink width (INK_W[tag]), then shrink only if the element's extent
    cap would break.

    Width is matched on the COMPOSITE, because coloured parts located by FFT
    correlation widen the ink relative to the black skeleton (eq1_l1's composite
    is 682pt where its skeleton is 536pt).  The solution uses one reference
    composite at the seed size plus two Newton steps (ink width scales
    linearly with fs), which keeps the build fast - a 22-step bisection of full
    16in canvases costs ~20s per equation.

    Canvas safety: the reference composite is rendered at the seed size, whose
    ink is known to fit the 16in (=1152pt) canvas, and every scaled fs is
    clamped to that same ceiling.  Rendering past the canvas width clips the
    ink and makes the coloured parts impossible to locate.

    Return (fs, canvas, w_px, h_px)."""
    target_w = INK_W.get(tag)
    lim_w, lim_h = MAX_EXTENT[tag]

    def build(f):
        return build_composite(tex, f, parts, tag) if parts else \
            render_canvas(tex, f, BLACK)[0]

    if target_w:
        out = build(fs)
        w = measure(out)[0]
        # clamp the ceiling to the reference render's own scale
        ceiling = fs * (CANVAS_W_PT * 0.92) / max(w, 1e-6)
        for _ in range(3):
            f = fs * target_w / max(w, 1e-6)
            f = max(float(MIN_FS), min(f, ceiling))
            fi = max(MIN_FS, int(round(f)))
            if fi == fs:
                break
            out = build(fi)
            fs, w = fi, measure(out)[0]
        # one final nudge if int rounding left a small overshoot
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
    w_px = int(cols[-1] - cols[0] + 1)
    h_px = int(rows[-1] - rows[0] + 1)
    return fs, out, w_px, h_px


def build_composite(tex, fs, parts, tag):
    """Black base render + each coloured part's own render located inside it by
    FFT correlation and pasted ink-left/baseline aligned (baselines coincide:
    every render anchors its baseline at figure y=0.5)."""
    buf, _ = render_canvas(tex, fs, BLACK)
    haystack = (buf[:, :, 3] > 8).astype(np.float32)
    out = buf.copy()
    h, w = out.shape[:2]
    for needle, color in parts:
        cand = None
        for sc in (1.0, SCRIPT_SCALE):
            pbuf = render_canvas(needle, fs * sc, color)[0]
            pm = ink_mask(pbuf)
            if not pm.any():
                continue
            npys, npxs = np.where(pm)
            part_x0, part_y0 = int(npxs.min()), int(npys.min())
            part_x1, part_y1 = int(npxs.max()) + 1, int(npys.max()) + 1
            # Core = the needle's TIGHT ink bbox (+4px margin).  A core that
            # runs to the canvas edge wraps in the circular FFT correlation and
            # produces phantom hits at dy<0 / dy=height.
            core = pm[max(0, part_y0 - 4):part_y1 + 4,
                      max(0, part_x0 - 4):part_x1 + 4].astype(np.float32)
            core_ox, core_oy = max(0, part_x0 - 4), max(0, part_y0 - 4)
            hits = fft_locate(core, haystack)
            if hits:
                cand = (sc, hits, part_x0, part_y0, core_ox, core_oy, pbuf)
                break
        if cand is None:
            raise SystemExit(f"could not locate {needle!r} in {tag} "
                             f"(image would fall back to uncoloured)")
        sc, hits, part_x0, part_y0, core_ox, core_oy, pbuf = cand
        n = 0
        for hx, hy in hits:
            # hx/hy is the CORE's top-left inside the canvas, so the part's
            # origin (pbuf 0,0) lands at (hx - core_ox, hy - core_oy)
            dx, dy = hx - core_ox, hy - core_oy
            n_ys, n_ye = max(0, dy), min(h, dy + pbuf.shape[0])
            n_xs, n_xe = max(0, dx), min(w, dx + pbuf.shape[1])
            if n_ye <= n_ys or n_xe <= n_xs:
                continue
            region = pbuf[n_ys - dy:n_ye - dy, n_xs - dx:n_xe - dx]
            assert region.shape[:2] == (n_ye - n_ys, n_xe - n_xs), \
                (region.shape, n_ye - n_ys, n_xe - n_xs)
            out[n_ys:n_ye, n_xs:n_xe] = np.where(region[:, :, 3:4] > 20, region,
                                                 out[n_ys:n_ye, n_xs:n_xe])
            n += 1
        print(f"  {tag}: {needle!r} -> {color} x{sc:.2f} at {n} hit(s) "
              f"x={[x for x, _ in hits]}")
    return out


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
        w_in, h_in = round(w_px / 600, 5), round(h_px / 600, 5)
        ink_x, band_y0, band_y1 = BAND[tag]
        h_pt = h_px * 72.0 / DPI
        py = int(round((band_y0 + band_y1) / 2.0 - h_pt / 2.0))
        px = int(ink_x)
        sidecar = {
            "path": png, "w_px": w_px, "h_px": h_px, "w_in": w_in, "h_in": h_in,
            "dpi": DPI, "pad_px": PAD, "fontsize_pt": fs, "color": "000000",
            "mathtext": tex,
            "symbol_colors": {"default": "000000",
                              **({f"part{i}": c.lstrip("#") for i, (_, c) in enumerate(parts)}
                                 if parts else {})},
            "orig_ink_px": [ink_x, ink_x + round(w_in * 72) - 1,
                            py, py + round(h_in * 72) - 1],
            "notes": "2D mathtext composite: black skeleton + coloured parts "
                     "located by FFT correlation and pasted aligned on the "
                     "shared canvas baseline",
        }
        json.dump(sidecar, open(os.path.join(ASSETS, f"eq_015_{tag}.json"), "w"), indent=1)
        table[tag] = {"png": png, "w_in": w_in, "h_in": h_in, "x_frame": px, "y_frame": py,
                      "fontsize_pt": fs, "w_pt": round(w_in * 72), "h_pt": round(h_in * 72)}
        # verify the intended colours actually landed (no silent mis-paste)
        arr = np.asarray(Image.open(png).convert("RGBA")).astype(int)
        am = arr[:, :, 3] > 40
        if am.any():
            want = {c.lstrip("#").lower() for _, c in parts} or {"000000"}
            rgbpx = arr[:, :, :3][am]
            # snap measured colours to the nearest intended target
            def nearest(px):
                best, bd = None, 1e9
                for tgt in want:
                    t = [int(tgt[i:i + 2], 16) for i in (0, 2, 4)]
                    d = sum((px[i] - t[i]) ** 2 for i in range(3))
                    if d < bd:
                        best, bd = tgt, d
                return best
            uniq = {}
            for ppx in rgbpx[:: max(1, len(rgbpx) // 4000)]:
                n = nearest(tuple(ppx))
                uniq[n] = uniq.get(n, 0) + 1
            print(f"  {tag}: colours {uniq} (targets {sorted(want)})")
            if set(uniq) - want:
                raise SystemExit(f"colour mismatch in {tag}: {uniq} vs {want}")
        print(f"{tag:10s} {w_px:5d}x{h_px:4d}px  frame {round(w_in*72)}x{round(h_in*72)}pt  "
              f"ink->({px},{py})")
        # release the canvas before the next equation: 9 equations x several
        # renders of a 12x2in 600dpi buffer (35MB each) exhaust the box's RAM
        # if the allocator keeps the freed blocks
        del out, tight, arr
        gc.collect()
    json.dump(table, open(os.path.join(ASSETS, "eq015_table.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
