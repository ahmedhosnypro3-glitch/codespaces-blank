#!/usr/bin/env python3
"""Lane G / b_geom_3 — closed-loop geometry PIL verification (v3).

Slides 014, 016, 017, 023, 024 (namespace 10_nn_training_and_example).

COMPARISON BASIS
  Dark ink: relative luminance < 150 (text + line art).  The recreation draws
  on the house grey #E8E8E8 canvas; the original frames carry their own
  multi-tone canvas fills, so a whole-frame "non-background" box compares one
  background against another.  Dark ink is slide-specific content in both.

SLIDE-AREA NORMALIZATION (the decisive step)
  Every original frame is a VIDEO CAPTURE: the 16:9 slide sits inside the
  960x540 frame with letterbox bars.  Measured from the original's own border
  ring, which is exactly 16:9 and horizontally symmetric:
      014/016/017  slide rect  x 58..901  y 43..516   (843 x 473)
      023/024      slide rect  x 38..920  y 43..539   (882 x 496)
  Both sides are mapped into ONE common space — the 960x540 slide space:
      original px -> (px - Ox0) * 960/OW, (py - Oy0) * 540/OH
      render   px -> px * 960/2001, py * 540/1125
  Without this the original's letterboxed rows are compared against the
  render's full-bleed rows and every region reports a false offset.

CHROME — masked, never reported
  render   : 1px white PDF page border; house red frame @0.15in inset
             (150dpi x=22..1978, y=22..1103); house badge disc.
  original : the original's own border ring(s), its own badge disc, and
             (014/016/017) the black video-capture bar.  023/024 originals
             carry a DECORATIVE DOUBLE border (outer x=38/920 y=43/539, inner
             x=61..863 y=58..523) - both strokes are masked.

REGIONS
  The original's own chrome-masked dark-ink row bands are normalized, then
  paired 1:1 with the render band that overlaps them most in y.  The original
  bands are grouped into TITLE / BODY / FOOTER; a region's verdict is the
  worst verdict among its pairs.

TOLERANCE: 2.0 slide px (~4px at 150dpi).
"""
import os

import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
FW, FH = 960, 540
TOL = 2.0
SLIDES = ["014", "016", "017", "023", "024"]
OUT = f"{NS}/_pool/geom_b_geom_3/final_v3_out.txt"
REND = f"{NS}/_pool/lo_geom_b_geom_3/out/slide_{{}}_150.png"

# Per slide: slide rect (ring stroke centres) + chrome to mask.
GEO = {
    "014": {"rect": (58, 43, 901, 516), "bar": 516, "badge": (852, 42, 900, 92),
            "inner": None, "ring_band": 4},
    "016": {"rect": (58, 43, 901, 516), "bar": 516, "badge": (852, 42, 900, 92),
            "inner": None, "ring_band": 4},
    "017": {"rect": (58, 43, 901, 516), "bar": 516, "badge": (852, 42, 900, 92),
            "inner": None, "ring_band": 4},
    "023": {"rect": (38, 43, 920, 539), "bar": None, "badge": (868, 48, 918, 94),
            "inner": (60, 64, 860, 865), "inner_rows": (56, 60, 521, 525),
            "ring_band": 4},
    "024": {"rect": (38, 43, 920, 539), "bar": None, "badge": (868, 48, 918, 94),
            "inner": None, "ring_band": 4},
}
REGIONS = ["TITLE", "BODY", "FOOTER"]


def dark(a, lum_max=150):
    lum = (a[:, :, 0] * 299 + a[:, :, 1] * 587 + a[:, :, 2] * 114) / 1000.0
    return lum < lum_max


def stroke(m, x0, y0, x1, y1, band=5):
    ex = np.zeros_like(m)
    for t in (y0, y1):
        ex[max(0, t - band):t + band + 1, max(0, x0 - band):x1 + band + 1] = True
    for t in (x0, x1):
        ex[max(0, y0 - band):y1 + band + 1, max(0, t - band):t + band + 1] = True
    return ex


def render_ink(p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(int)
    m = dark(a)
    m[0, :] = m[-1, :] = m[:, 0] = m[:, -1] = False
    H, W = m.shape
    inset, band = 22, 6
    ex = np.zeros_like(m)
    for t in (inset, W - 1 - inset):
        ex[:, max(0, t - band):t + band + 1] = True
    for t in (inset, H - 1 - inset):
        ex[max(0, t - band):t + band + 1, :] = True
    ex[15:150, 1830:1975] = True
    return m & ~ex


def orig_ink(n, p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(int)
    m = dark(a)
    g = GEO[n]
    ex = np.zeros_like(m)
    if g["bar"] is not None:
        ex[g["bar"]:, :] = True
    x0, y0, x1, y1 = g["rect"]
    ex |= stroke(m, x0, y0, x1, y1, band=g["ring_band"])
    if g["inner"]:
        ix0, ix1 = g["inner"][0], g["inner"][2]
        ex[:, ix0:ix1 + 1] = True
        a0, a1, b0, b1 = g["inner_rows"]
        ex[a0:a1 + 1, :] = True
        ex[b0:b1 + 1, :] = True
    bx0, by0, bx1, by1 = g["badge"]
    ex[by0:by1, bx0:bx1] = True
    return m & ~ex


def bands_of(m, min_gap=6, min_ink=4):
    on = m.sum(1) > min_ink
    out, s = [], None
    for y, v in enumerate(on):
        if v and s is None:
            s = y
        elif not v and s is not None:
            out.append((s, y - 1))
            s = None
    if s is not None:
        out.append((s, m.shape[0] - 1))
    merged = []
    for b in out:
        if merged and b[0] - merged[-1][1] - 1 < min_gap:
            merged[-1] = (merged[-1][0], b[1])
        else:
            merged.append(b)
    return merged


def bbox_rows(m, y0, y1):
    sub = m[y0:y1 + 1, :]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        return None, 0
    return (int(xs.min()), int(ys.min()) + y0,
            int(xs.max()), int(ys.max()) + y0), int(sub.sum())


def make_maps(n):
    """Return (ox_map, oy_map, rx_map, ry_map): arrays mapping source index ->
    slide-space coordinate."""
    ox0, oy0, ox1, oy1 = GEO[n]["rect"]
    ow, oh = ox1 - ox0, oy1 - oy0
    oxm = lambda i: (i - ox0) * FW / ow
    oym = lambda i: (i - oy0) * FH / oh
    rxm = lambda i: i * FW / 2001.0
    rym = lambda i: i * FH / 1125.0
    return oxm, oym, rxm, rym


def overlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]) + 1)


def pair_bands(ob, rb, ob_raw, rb_raw):
    """Pair each original band with the render band it overlaps most in y.
    Returns (normalized band, raw orig band, raw render band, overlap)."""
    pairs = []
    for k, b in enumerate(ob):
        best, bestraw, ov = None, None, 0
        for j, c in enumerate(rb):
            o = overlap(b, c)
            if o > ov:
                best, bestraw, ov = c, rb_raw[j], o
        pairs.append((b, ob_raw[k], bestraw, ov))
    return pairs


def region_windows(obands):
    """Group normalized original bands into 3 regions at the 2 largest gaps."""
    if len(obands) < 3:
        return [(0, len(obands) - 1)] if obands else []
    gaps = sorted(((obands[i + 1][0] - obands[i][1] - 1, i)
                   for i in range(len(obands) - 1)), reverse=True)
    cuts = sorted(i for _, i in gaps[:2])
    wins, start = [], 0
    for c in cuts + [len(obands) - 1]:
        wins.append((start, c))
        start = c + 1
    return wins


def main():
    L = []
    for n in SLIDES:
        om = orig_ink(n, f"{NS}/unique_slides/slide_{n}.jpg")
        rm = render_ink(REND.format(n))
        oxm, oym, rxm, rym = make_maps(n)
        ob_raw = bands_of(om)
        ob = [(oym(a), oym(b)) for a, b in ob_raw]
        rb_raw = bands_of(rm)
        rb = [(rym(a), rym(b)) for a, b in rb_raw]
        pairs = pair_bands(ob, rb, ob_raw, rb_raw)
        wins = region_windows(ob)
        L.append(f"\n## slide {n}\n\n")
        L.append(f"- slide rect (orig px): {GEO[n]['rect']}  "
                 f"w={GEO[n]['rect'][2]-GEO[n]['rect'][0]} "
                 f"h={GEO[n]['rect'][3]-GEO[n]['rect'][1]}\n")
        L.append(f"- original chrome-masked dark-ink fraction: {om.mean():.4f}; "
                 f"render (house-chrome-masked): {rm.mean():.4f}\n")
        L.append(f"- original dark-ink bands (slide px): "
                 + ", ".join(f"{a:.0f}..{b:.0f}" for a, b in ob) + "\n")
        L.append(f"- render dark-ink bands (slide px): "
                 + ", ".join(f"{a:.0f}..{b:.0f}" for a, b in rb) + "\n")
        for i, (s, e) in enumerate(wins):
            name = REGIONS[i]
            L.append(f"\n- **region {name}** (orig bands {s}..{e}, "
                     f"slide y {ob[s][0]:.0f}..{ob[e][1]:.0f})\n")
            worst_all, any_pair = 0.0, False
            for j in range(s, e + 1):
                oband, oraw, rraw, ov = pairs[j]
                obox, opx = bbox_rows(om, oraw[0], oraw[1])
                if obox is None:
                    L.append(f"  - band{j}: original has no dark ink; skipped\n")
                    continue
                # map original box into slide space
                obn = (oxm(obox[0]), oym(obox[1]), oxm(obox[2]), oym(obox[3]))
                if rraw is None or ov == 0:
                    L.append(f"  - band{j} (orig {obn[0]:.0f},{obn[1]:.0f}-"
                             f"{obn[2]:.0f},{obn[3]:.0f}) **UNPAIRED** — no "
                             f"render dark ink overlaps this band\n")
                    continue
                rbox, rpx = bbox_rows(rm, rraw[0], rraw[1])
                rbn = (rxm(rbox[0]), rym(rbox[1]), rxm(rbox[2]), rym(rbox[3]))
                d = [obn[0] - rbn[0], obn[1] - rbn[1],
                     obn[2] - rbn[2], obn[3] - rbn[3]]
                worst = max(abs(v) for v in d)
                any_pair = True
                worst_all = max(worst_all, worst)
                v = "PASS" if worst <= TOL else "EXCEEDS-TOLERANCE"
                L.append(f"  - band{j} y{oband[0]:.0f}..{oband[1]:.0f} "
                         f"**{v}**\n")
                L.append(f"    - original [{obn[0]:.1f},{obn[1]:.1f}]-"
                         f"[{obn[2]:.1f},{obn[3]:.1f}] w{obn[2]-obn[0]+1:.1f} "
                         f"h{obn[3]-obn[1]+1:.1f} ink={opx}\n")
                L.append(f"    - render   [{rbn[0]:.1f},{rbn[1]:.1f}]-"
                         f"[{rbn[2]:.1f},{rbn[3]:.1f}] w{rbn[2]-rbn[0]+1:.1f} "
                         f"h{rbn[3]-rbn[1]+1:.1f} ink={rpx}\n")
                L.append(f"    - delta dx0={d[0]:+.2f} dy0={d[1]:+.2f} "
                         f"dx1={d[2]:+.2f} dy1={d[3]:+.2f} | "
                         f"dw={d[2]-d[0]:+.2f} dh={d[3]-d[1]:+.2f} | "
                         f"worst={worst:.2f} (tol {TOL:.0f})\n")
            if not any_pair:
                L.append(f"  - region verdict: NOT MEASURABLE\n")
            else:
                L.append(f"  - **region {name} verdict: "
                         f"{'PASS' if worst_all <= TOL else 'EXCEEDS-TOLERANCE'}"
                         f"** (worst {worst_all:.2f})\n")
    txt = "".join(L)
    open(OUT, "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
