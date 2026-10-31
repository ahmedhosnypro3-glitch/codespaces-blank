"""Lane G / b_geom_3 — colour-matched feature bbox comparison.

The original frames have multi-tone backgrounds (beige diagram canvas, grey
panels, maroon borders) so a generic ink mask measures background fill, not
content. Instead, for each slide-specific feature we locate its colour in BOTH
images and compare the bbox at frame scale. House chrome (red frame @0.15in,
yellow badge @12.48/0.30) is never measured.
"""
import os

import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
FW, FH = 960, 540
TOL = 2.0

# (name, rgb, tolerance, optional region restriction in frame px (x0,y0,x1,y1))
FEATURES = {
    "014": [
        ("light-purple Input Sample / Target Label box", (216, 180, 224), 22, None),
        ("beige diagram canvas", (218, 208, 196), 12, None),
        ("dark-red Error bar", (139, 0, 0), 45, None),
        ("green Class boxes", (200, 230, 201), 30, None),
        ("cream equation strip", (240, 230, 216), 14, None),
    ],
    "016": [
        ("light-purple highlight box", (216, 180, 224), 22, None),
        ("beige diagram canvas", (218, 208, 196), 12, None),
        ("green Class boxes", (200, 230, 201), 30, None),
        ("cream equation strip", (240, 230, 216), 14, None),
    ],
    "017": [
        ("light-purple highlight box", (216, 180, 224), 22, None),
        ("beige diagram canvas", (218, 208, 196), 12, None),
        ("green Class boxes", (200, 230, 201), 30, None),
        ("cream equation strip", (240, 230, 216), 14, None),
    ],
    "023": [
        ("purple flowchart box", (221, 160, 221), 25, None),
        ("light-green flowchart box", (144, 238, 144), 30, None),
        ("cream process box", (245, 245, 220), 25, None),
        ("white canvas fill", (255, 255, 255), 4, None),
    ],
    "024": [
        ("white panel fill", (255, 255, 255), 4, None),
        ("beige panel fill", (232, 233, 228), 10, None),
        ("red title text / rule", (140, 40, 40), 60, None),
    ],
}


def load(n):
    o = np.asarray(Image.open(os.path.join(NS, "unique_slides", f"slide_{n}.jpg"))
                   .convert("RGB")).astype(int)
    r = np.asarray(Image.open(os.path.join(
        NS, "_pool/lo_geom_b_geom_3/out", f"slide_{n}_150.png"))
        .convert("RGB")).astype(int)
    return o, r


def match_bbox(a, rgb, tol, reg=None):
    m = np.all(np.abs(a - np.array(rgb, int)) <= tol, axis=2)
    if reg:
        sel = np.zeros(m.shape, bool)
        sel[reg[1]:reg[3], reg[0]:reg[2]] = True
        m &= sel
    if not m.any():
        return None, 0
    ys, xs = np.nonzero(m)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())), int(m.sum())


def main():
    lines = []
    for n, feats in FEATURES.items():
        o, r = load(n)
        sx, sy = FW / r.shape[1], FH / r.shape[0]
        lines.append(f"## slide {n}")
        for name, rgb, tol, reg in feats:
            ob, on = match_bbox(o, rgb, tol, reg)
            rb, rn = match_bbox(r, rgb, tol, reg)
            if ob is None or rb is None:
                lines.append(f"- {name}: SKIP orig={ob}({on}) render={rb}({rn})")
                continue
            rbf = (rb[0] * sx, rb[1] * sy, rb[2] * sx, rb[3] * sy)
            d = [ob[0] - rbf[0], ob[1] - rbf[1], ob[2] - rbf[2], ob[3] - rbf[3]]
            worst = max(abs(v) for v in d)
            v = "PASS" if worst <= TOL else "EXCEEDS-TOLERANCE"
            lines.append(
                f"- {name} **{v}**\n"
                f"  orig rgb{rgb} tol{tol}: {ob} (w{ob[2]-ob[0]+1} h{ob[3]-ob[1]+1}) px={on}\n"
                f"  render: {rb} -> frame [{rbf[0]:.1f},{rbf[1]:.1f}]-"
                f"[{rbf[2]:.1f},{rbf[3]:.1f}] (w{rbf[2]-rbf[0]+1:.1f} "
                f"h{rbf[3]-rbf[1]+1:.1f}) px={rn}\n"
                f"  delta dx0={d[0]:+.2f} dy0={d[1]:+.2f} dx1={d[2]:+.2f} "
                f"dy1={d[3]:+.2f} | dsize dw={d[2]-d[0]:+.2f} dh={d[3]-d[1]:+.2f} "
                f"| worst={worst:.2f}")
        lines.append("")
    text = "\n".join(lines)
    open(os.path.join(NS, "_pool/geom_b_geom_3/feature_out.txt"), "w").write(text)
    print(text)


if __name__ == "__main__":
    main()
