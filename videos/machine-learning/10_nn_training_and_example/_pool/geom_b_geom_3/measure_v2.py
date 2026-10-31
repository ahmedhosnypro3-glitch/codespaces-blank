#!/usr/bin/env python3
"""Lane G / b_geom_3 — closed-loop geometry PIL verification.

Slides 014, 016, 017, 023, 024 (namespace 10_nn_training_and_example).

Method
------
Comparison basis is DARK INK (relative luminance < 150, i.e. text and line
art). The recreation renders on the house grey #E8E8E8 canvas while the
original frames carry their own multi-tone canvas fills, so a whole-frame
"non-background" box compares one background against another; dark ink is
slide-specific content in both images and is directly comparable.

Chrome is masked and never reported:
  render : 1px white PDF page border; house red frame @0.15in inset
           (150dpi x=22..1978, y=22..1103); yellow badge disc.
  original: the original slide's OWN border ring(s), its own badge disc, and
           (014/016/017) the black video-capture bar. 023's original carries a
           DECORATIVE DOUBLE ring (outer x=38/920 y=43/539, inner x=61..863
           y=58..523) - both strokes are masked.
Original frame is 960x540; render is 2001x1125. Render boxes are normalized
to the 960x540 frame scale (x*960/2001, y*540/1125) before comparison.

Regions are derived per slide from the ORIGINAL's own chrome-masked dark-ink
row bands, split at the two largest inter-band gaps: TITLE / BODY / FOOTER.
Tolerance: 2.0 frame px (~4px at 150dpi).
"""
import os

import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
FW, FH = 960, 540
TOL = 2.0
SLIDES = ["014", "016", "017", "023", "024"]
OUT = f"{NS}/_pool/geom_b_geom_3/final_v2_out.txt"
REND = f"{NS}/_pool/lo_geom_b_geom_3/out/slide_{{}}_150.png"

# Original-side chrome (measured, frame px).
# 014/016/017: single dark-maroon ring x=58/901, y=43/516 + black capture bar.
# 023/024:     thick maroon ring x=38/920, y=43/539; 023 adds an inner ring.
ORIG_CHROME = {
    "014": {"bar": 516, "ring": (58, 43, 901, 516), "badge": (852, 42, 900, 92),
            "inner": None},
    "016": {"bar": 516, "ring": (58, 43, 901, 516), "badge": (852, 42, 900, 92),
            "inner": None},
    "017": {"bar": 516, "ring": (58, 43, 901, 516), "badge": (852, 42, 900, 92),
            "inner": None},
    "023": {"bar": None, "ring": (38, 43, 920, 539), "badge": (868, 48, 918, 94),
            "inner": (61, 58, 863, 523)},
    "024": {"bar": None, "ring": (38, 43, 920, 539), "badge": (868, 48, 918, 94),
            "inner": None},
}
REGIONS = ["TITLE", "BODY", "FOOTER"]


def dark(a, lum_max=150):
    lum = (a[:, :, 0] * 299 + a[:, :, 1] * 587 + a[:, :, 2] * 114) / 1000.0
    return lum < lum_max


def stroke(m, x0, y0, x1, y1, band=5):
    """Mask the outline of a box (4 strokes of half-width band)."""
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
    inset, band = int(round(0.15 * 150)), 6
    ex = np.zeros_like(m)
    for t in (inset, W - 1 - inset):
        ex[:, max(0, t - band):t + band + 1] = True
    for t in (inset, H - 1 - inset):
        ex[max(0, t - band):t + band + 1, :] = True
    ex[int(0.10 * 150):int(1.00 * 150), int(12.20 * 150):int(13.20 * 150)] = True
    return m & ~ex


def orig_ink(n, p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(int)
    m = dark(a)
    ch = ORIG_CHROME[n]
    ex = np.zeros_like(m)
    if ch["bar"] is not None:
        ex[ch["bar"]:, :] = True
    x0, y0, x1, y1 = ch["ring"]
    ex |= stroke(m, x0, y0, x1, y1, band=4)
    if ch["inner"]:
        ex |= stroke(m, *ch["inner"], band=2)
    bx0, by0, bx1, by1 = ch["badge"]
    ex[by0:by1, bx0:bx1] = True
    return m & ~ex


def bbox_in(m, y0, y1, x0=0, x1=None):
    x1 = m.shape[1] - 1 if x1 is None else x1
    y0, y1 = max(0, y0), min(m.shape[0] - 1, y1)
    x0, x1 = max(0, x0), min(m.shape[1] - 1, x1)
    sub = m[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        return None, 0
    return (int(xs.min()) + x0, int(ys.min()) + y0,
            int(xs.max()) + x0, int(ys.max()) + y0), int(sub.sum())


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


def region_windows(bands):
    """Split the original's own row bands into 3 regions at the 2 largest gaps."""
    if len(bands) < 3:
        return [(bands[0][0], bands[-1][1])] if bands else []
    gaps = [(bands[i + 1][0] - bands[i][1] - 1, i) for i in range(len(bands) - 1)]
    gaps.sort(reverse=True)
    cuts = sorted(i for _, i in gaps[:2])
    wins = []
    start = 0
    for c in cuts + [len(bands) - 1]:
        wins.append((bands[start][0], bands[c][1]))
        start = c + 1
    return wins


def overflow_check(n, count=True, per_band=False):
    """Dark ink that sits OUTSIDE the house frame box (x<22 / x>1978 /
    y<22 / y>1103 at 150dpi), excluding the frame stroke and badge disc.
    Returns (total_px, bbox_frame or None, per_top-level-band breakdown)."""
    a = np.asarray(Image.open(REND.format(n)).convert("RGB")).astype(int)
    m = dark(a)
    m[0, :] = m[-1, :] = m[:, 0] = m[:, -1] = False
    H, W = m.shape
    inset, band = 22, 6
    ex = np.zeros_like(m)
    for t in (inset, W - 1 - inset):
        ex[:, max(0, t - band):t + band + 1] = True
    for t in (inset, H - 1 - inset):
        ex[max(0, t - band):t + band + 1, :] = True
    ex[int(0.10 * 150):int(1.00 * 150), int(12.20 * 150):int(13.20 * 150)] = True
    m = m & ~ex
    out = np.zeros_like(m)
    out[:inset, :] = True
    out[H - 1 - inset + 1:, :] = True
    out[:, :inset] = True
    out[:, W - inset + 1:] = True
    om = m & out
    ys, xs = np.nonzero(om)
    if len(xs) == 0:
        return 0, None, {}
    fx, fy = FW / W, FH / H
    det = {}
    if per_band:
        for i, (y0, y1) in enumerate(bands_of(om)):
            det[(y0, y1)] = int(om[y0:y1 + 1, :].sum())
    return int(om.sum()), (int(xs.min()), int(ys.min()),
                           int(xs.max()), int(ys.max()),
                           xs.min() * fx, ys.min() * fy,
                           xs.max() * fx, ys.max() * fy), det


def main():
    L = []
    for n in SLIDES:
        om = orig_ink(n, f"{NS}/unique_slides/slide_{n}.jpg")
        rm = render_ink(REND.format(n))
        bands = bands_of(om)
        wins = region_windows(bands)
        L.append(f"\n## slide {n}\n\n")
        L.append(f"- original chrome-masked dark-ink fraction: {om.mean():.4f}\n")
        L.append(f"- original dark-ink row bands (frame px): {bands}\n")
        L.append(f"- regions (frame px): "
                 + " | ".join(f"{REGIONS[i]}={w[0]}..{w[1]}"
                              for i, w in enumerate(wins)) + "\n")
        ov, ovb, det = overflow_check(n, per_band=True)
        L.append(f"- dark ink OUTSIDE the house frame: {ov} px")
        if ovb:
            L.append(f" at render px x{ovb[0]}..{ovb[2]} y{ovb[1]}..{ovb[3]}"
                     f" -> frame [{ovb[4]:.1f}..{ovb[6]:.1f}] x"
                     f" [{ovb[5]:.1f}..{ovb[7]:.1f}]"
                     + (f" (per band {det})" if det else "") + "\n")
        else:
            L.append(" (none — all render ink is inside the house frame)\n")
        for i, (y0, y1) in enumerate(wins):
            ob, on = bbox_in(om, y0, y1)
            rb, rn = bbox_in(rm, int(y0 / 540 * 1125), int(y1 / 540 * 1125))
            if ob is None or rb is None:
                L.append(f"\n- {REGIONS[i]} (y{y0}..{y1}): NOT MEASURABLE "
                         f"orig_ink={ob} render_ink={rb}\n")
                continue
            sx, sy = FW / 2001.0, FH / 1125.0
            rbf = (rb[0] * sx, rb[1] * sy, rb[2] * sx, rb[3] * sy)
            d = [ob[0] - rbf[0], ob[1] - rbf[1], ob[2] - rbf[2], ob[3] - rbf[3]]
            worst = max(abs(v) for v in d)
            v = "PASS" if worst <= TOL else "EXCEEDS-TOLERANCE"
            L.append(f"\n- **{REGIONS[i]}** (y{y0}..{y1}) **{v}**\n")
            L.append(f"  - original box (frame px): [{ob[0]},{ob[1]}]-"
                     f"[{ob[2]},{ob[3]}]  w{ob[2]-ob[0]+1} h{ob[3]-ob[1]+1}"
                     f"  dark_ink_px={on}\n")
            L.append(f"  - render box (normalized frame px): [{rbf[0]:.1f},"
                     f"{rbf[1]:.1f}]-[{rbf[2]:.1f},{rbf[3]:.1f}]  "
                     f"w{rbf[2]-rbf[0]+1:.1f} h{rbf[3]-rbf[1]+1:.1f}"
                     f"  dark_ink_px={rn}\n")
            L.append(f"  - normalized delta: dx0={d[0]:+.2f} dy0={d[1]:+.2f} "
                     f"dx1={d[2]:+.2f} dy1={d[3]:+.2f} | dw={d[2]-d[0]:+.2f} "
                     f"dh={d[3]-d[1]:+.2f} | worst={worst:.2f} (tol "
                     f"{TOL:.0f})\n")
    txt = "".join(L)
    open(OUT, "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
