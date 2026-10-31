"""Lane G / b_geom_3 final geometry measurement (v2) — dark-ink geometry.

Why dark ink: the ORIGINAL frames are mostly a large light-beige/grey canvas
fill, while the RECREATION renders the same content on the house grey #E8E8E8
background. A whole-frame "non-background" bbox therefore compares a canvas
against a background and is not meaningful. TEXT and LINE ART (dark ink) are
slide-specific content in both images and are directly comparable.

Chrome is masked and NEVER reported:
  render   : 1px white PDF page border; house red frame stroke @0.15in inset
             (150dpi x=22..1978, y=22..1103); yellow badge disc.
  original : 014/016/017 -> black video-capture bar (y>=516) and its own border
             ring at x=40..919 / y=42..516; 023/024 -> the original slide's own
             thick maroon border ring; each original's own badge disc.

Regions come from the ORIGINAL's own dark-ink band structure, then the same
bands are applied to the render.
"""
import os

import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
FW, FH = 960, 540
TOL = 2.0
SLIDES = ["014", "016", "017", "023", "024"]

# original-side chrome to mask, measured in frame px.
# 014/016/017: the original slide's own dark-maroon border ring at
#   x=58 (left), x=901 (right), y=43 (top), y=516 (bottom) + black capture bar.
# 023/024: the original slide's own thick maroon ring at x=38/920, y=43/538.
ORIG_CHROME = {
    "014": {"black_bar_y": 516, "ring": (58, 43, 901, 516), "badge": (852, 42, 900, 92)},
    "016": {"black_bar_y": 516, "ring": (58, 43, 901, 516), "badge": (852, 42, 900, 92)},
    "017": {"black_bar_y": 516, "ring": (58, 43, 901, 516), "badge": (852, 42, 900, 92)},
    "023": {"black_bar_y": None, "ring": (38, 43, 920, 538), "badge": (868, 48, 918, 94)},
    "024": {"black_bar_y": None, "ring": (38, 43, 920, 538), "badge": (868, 48, 918, 94)},
}


def dark_mask(a, lum_max=150):
    """Text / line-art ink: dark pixels only (colour-agnostic)."""
    lum = (a[:, :, 0] * 299 + a[:, :, 1] * 587 + a[:, :, 2] * 114) / 1000.0
    return lum < lum_max


def render_ink(p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(int)
    m = dark_mask(a)
    m[0, :] = m[-1, :] = m[:, 0] = m[:, -1] = False
    H, W = m.shape
    ex = np.zeros_like(m)
    inset, band = int(round(0.15 * 150)), 6
    for t in (inset, W - 1 - inset):
        ex[:, max(0, t - band):t + band + 1] = True
    for t in (inset, H - 1 - inset):
        ex[max(0, t - band):t + band + 1, :] = True
    ex[int(0.10 * 150):int(1.00 * 150), int(12.20 * 150):int(13.20 * 150)] = True
    return m & ~ex


def orig_ink(n, p):
    a = np.asarray(Image.open(p).convert("RGB")).astype(int)
    m = dark_mask(a)
    H, W = m.shape
    ex = np.zeros_like(m)
    ch = ORIG_CHROME[n]
    if ch["black_bar_y"] is not None:
        ex[ch["black_bar_y"]:, :] = True
    x0, y0, x1, y1 = ch["ring"]
    band = 5
    ex[max(0, y0 - band):y0 + band + 1, :] = True
    ex[max(0, y1 - band):y1 + band + 1, :] = True
    ex[:, max(0, x0 - band):x0 + band + 1] = True
    ex[:, max(0, x1 - band):x1 + band + 1] = True
    bx0, by0, bx1, by1 = ch["badge"]
    ex[by0:by1, bx0:bx1] = True
    return m & ~ex


def bbox_in(m, y0, y1, x0, x1):
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


def main():
    lines = []
    for n in SLIDES:
        om = orig_ink(n, os.path.join(NS, "unique_slides", f"slide_{n}.jpg"))
        rm = render_ink(os.path.join(NS, "_pool/lo_geom_b_geom_3/out",
                                     f"slide_{n}_150.png"))
        sx, sy = FW / 2001.0, FH / 1125.0
        bands = bands_of(om)
        lines.append(f"## slide {n}\n\n")
        lines.append(f"dark-ink fraction (chrome-masked): orig={om.mean():.4f} "
                     f"render={rm.mean():.4f}\n\n")
        lines.append(f"original dark-ink bands (frame px): {bands}\n\n")
        for i, (y0, y1) in enumerate(bands):
            ob, on = bbox_in(om, y0, y1, 0, FW - 1)
            rb, rn = bbox_in(rm, round(y0 / sy), round(y1 / sy), 0, 2000)
            if ob is None or rb is None:
                lines.append(f"- band{i} y{y0}-{y1}: SKIP (no dark ink one side) "
                             f"orig={ob} render={rb}\n\n")
                continue
            rbf = (rb[0] * sx, rb[1] * sy, rb[2] * sx, rb[3] * sy)
            d = [ob[0] - rbf[0], ob[1] - rbf[1], ob[2] - rbf[2], ob[3] - rbf[3]]
            worst = max(abs(v) for v in d)
            v = "PASS" if worst <= TOL else "EXCEEDS-TOLERANCE"
            lines.append(
                f"- band{i} y{y0}-{y1} **{v}**\n"
                f"  orig   [{ob[0]},{ob[1]}]-[{ob[2]},{ob[3]}] "
                f"(w{ob[2]-ob[0]+1} h{ob[3]-ob[1]+1}) dark_ink_px={on}\n"
                f"  render {rb} -> frame [{rbf[0]:.1f},{rbf[1]:.1f}]-"
                f"[{rbf[2]:.1f},{rbf[3]:.1f}] (w{rbf[2]-rbf[0]+1:.1f} "
                f"h{rbf[3]-rbf[1]+1:.1f}) dark_ink_px={rn}\n"
                f"  delta  dx0={d[0]:+.2f} dy0={d[1]:+.2f} dx1={d[2]:+.2f} "
                f"dy1={d[3]:+.2f} | dsize dw={d[2]-d[0]:+.2f} "
                f"dh={d[3]-d[1]:+.2f} | worst={worst:.2f} (tol {TOL})\n\n")
    text = "".join(lines)
    open(os.path.join(NS, "_pool/geom_b_geom_3/final_out.txt"), "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
