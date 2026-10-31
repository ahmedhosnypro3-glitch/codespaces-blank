#!/usr/bin/env python3
"""Lane G / b_geom_3 — write qa/slideNNN/geom_b_geom_3.md (v2 generator).

Per region: the original's dark-ink box and the render's dark-ink box, both clipped
to the SAME frame-px window, so the comparison is box-to-box and unit-safe.
Bands earlier paired raw render-px y-ranges against frame-px y-ranges (different
scales) which produced garbage deltas; that approach is discarded.
"""
import os
import sys

import importlib.util
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_gen import HDR, NOTES  # noqa: E402
spec = importlib.util.spec_from_file_location(
    "m2", f"{NS}/_pool/geom_b_geom_3/measure_v2.py")
m2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m2)
SLIDES = ["014", "016", "017", "023", "024"]
TOL = 2.0
REGIONS = ["TITLE", "BODY", "FOOTER"]
REGION_NAMES = ["title block", "body / equation / diagram / table region",
                "footer region"]


def obox_in(b):
    """(x0,y0,x1,y1) frame px -> slide-inch box string."""
    if b is None:
        return "none"
    return (f"x {b[0]/72:.2f}..{b[2]/72:.2f} in, y {b[1]/72:.2f}.."
            f"{b[3]/72:.2f} in")


def dim_check(p):
    im = Image.open(p).convert("RGB")
    a = np.asarray(im).astype(float)
    mean = a.mean()
    ok_dim = abs(im.width - 2000) <= 8 and abs(im.height - 1125) <= 8
    ok_mean = 20.0 <= mean <= 245.0
    return (f"{im.width}x{im.height} (spec 2000x1125 +/-8: "
            f"{'PASS' if ok_dim else 'FAIL'}), non-blank mean {mean:.1f} "
            f"(spec 20..245: {'PASS' if ok_mean else 'FAIL'})")


def region_box(mask, y0, y1, unit):
    """Dark-ink bbox clipped to frame-px y window [y0,y1]. unit='f' if mask rows
    are already frame px, 'r' if mask rows are render px."""
    if unit == "r":
        ry0, ry1 = round(y0 * 1125 / 540), round(y1 * 1125 / 540)
    else:
        ry0, ry1 = y0, y1
    return m2.bbox_in(mask, ry0, ry1)


def main():
    for n in SLIDES:
        om = m2.orig_ink(n, f"{NS}/unique_slides/slide_{n}.jpg")
        rp = f"{NS}/_pool/lo_geom_b_geom_3/out/slide_{n}_150.png"
        rm = m2.render_ink(rp)
        sx, sy = 960 / 2001.0, 540 / 1125.0
        wins = m2.region_windows(m2.bands_of(om))
        L = [HDR.format(n=n, dimchk=dim_check(rp))]
        L.append("## Regions\n")
        L.append("Each region compares the dark-ink bounding box of the original and the "
                 "render **clipped to the identical frame-px y window** (unit-safe). "
                 "Boxes are given in slide inches (1 frame px = 1/72 in).\n")
        region_worst = {}
        for i, (y0, y1) in enumerate(wins):
            name = REGION_NAMES[i]
            ob, opx = region_box(om, y0, y1, "f")
            rb, rpx = region_box(rm, y0, y1, "r")
            L.append(f"\n### {name} (slide y {y0/72:.2f}..{y1/72:.2f} in)\n")
            if ob is None or rb is None:
                L.append(f"### {name} (slide y {y0/72:.2f}..{y1/72:.2f} in)\n")
                L.append(f"- Measured original box: {obox_in(ob)} (ink {opx} px)\n")
                L.append("- Measured render box: none\n")
                L.append("- Normalized delta: not computable (a region is empty on one "
                         "side)\n")
                L.append(f"- **EXCEEDS-TOLERANCE**\n")
                L.append("- Note: region empty on one side only — the render has no dark "
                         "ink in this window\n")
                region_worst[name] = ("EXCEEDS-TOLERANCE", 0.0)
                continue
            rbf = (rb[0] * sx, rb[1] * sy, rb[2] * sx, rb[3] * sy)
            d = [ob[0] - rbf[0], ob[1] - rbf[1], ob[2] - rbf[2], ob[3] - rbf[3]]
            w = max(abs(v) for v in d)
            v = "PASS" if w <= TOL else "EXCEEDS-TOLERANCE"
            region_worst[name] = (v, w)
            # deltas expressed @150dpi (render - original), 1 frame px = 2.083 render px
            d150 = [-x * 2.0833 for x in d]
            w150 = max(abs(x) for x in d150)
            L.append(f"### {name} (slide y {y0/72:.2f}..{y1/72:.2f} in)\n")
            L.append(f"- Measured render box: {obox_in(rbf)} (ink {rpx} px)\n")
            L.append(f"- Measured original box: {obox_in(ob)} (ink {opx} px)\n")
            L.append(f"- Normalized delta (px @ 150dpi, render - original): left "
                     f"{d150[0]:+.1f}, top {d150[1]:+.1f}, right {d150[2]:+.1f}, "
                     f"bottom {d150[3]:+.1f}\n")
            L.append(f"- Worst |delta|: **{w150:.1f} px @ 150dpi** "
                     f"(tolerance 4.0 px)\n")
            L.append(f"- **{v}**\n")
            L.append(f"- Frame-px detail: dx0={d[0]:+.2f} dy0={d[1]:+.2f} "
                     f"dx1={d[2]:+.2f} dy1={d[3]:+.2f} | dw={d[2]-d[0]:+.2f} "
                     f"dh={d[3]-d[1]:+.2f}\n")
        ov, ovb, det = m2.overflow_check(n, per_band=True)
        L.append("\n### House-frame containment check\n")
        if ov == 0:
            L.append("- dark ink outside the house frame box: **0 px** — PASS "
                     "(all render ink is inside the house frame)\n")
        else:
            L.append(f"- dark ink outside the house frame box: **{ov} px** — "
                     "**EXCEEDS-TOLERANCE** (content bleeds past the frame)\n")
            L.append(f"  - render px bbox x{ovb[0]}..{ovb[2]} y{ovb[1]}..{ovb[3]}"
                     f" -> frame [{ovb[4]:.1f}..{ovb[6]:.1f}] x "
                     f"[{ovb[5]:.1f}..{ovb[7]:.1f}]\n")
            L.append(f"  - per render-row band: {det}\n")
        L.append(NOTES[n])
        L.append("\n---\n\n## Verdict\n\n")
        for i, rid in enumerate(REGIONS):
            rv, w = region_worst[REGION_NAMES[i]]
            L.append(f"- {REGION_NAMES[i]}: **{rv}**"
                     + (f" (worst {w * 2.0833:.1f} px @ 150dpi)"
                        if rv != "NOT MEASURABLE" else "")
                     + ("\n"))
        if ov != 0:
            L.append(f"- house-frame containment: **EXCEEDS-TOLERANCE** "
                     f"({ov} px of content ink outside the house red frame)\n")

        L.append("\n## Content geometry findings (chrome excluded)\n\n")
        for i, rid in enumerate(REGIONS):
            rv, w = region_worst[REGION_NAMES[i]]
            if rv == "NOT MEASURABLE":
                L.append(f"- {REGION_NAMES[i]}: the render has no dark ink in this "
                         f"window while the original does (missing element)\n")
            else:
                L.append(f"- **{REGION_NAMES[i]}**: worst {w * 2.0833:.1f} px "
                         f"@ 150dpi\n")
        if ov != 0:
            L.append(f"- **frame overflow**: {ov} px of content ink outside the "
                     f"house red frame ({ovb[4]:.1f}..{ovb[6]:.1f} x "
                     f"{ovb[5]:.1f}..{ovb[7]:.1f} frame px)\n")
        L.append("\nA region that exceeds tolerance is an input to adjudication, not "
                 "an automatic\nrebuild. Deviations explained by the house chrome "
                 "(outer red rectangle\nx=0.15/y=0.15/w=13.03/h=7.2 border #C00000 "
                 "1.5pt, yellow badge circle x=12.48/y=0.30/w=0.5/h=0.5\nfill+outline "
                 "#FFF9C4 bold 18pt #333333, title box y=0.28/x=0.6/w=12.13 centred) "
                 "are listed above\nfor context and are NOT findings. PIL measurement "
                 "is ground truth; judge prose is not.\n")
        out = f"{NS}/qa/slide{n}/geom_b_geom_3.md"
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write("".join(L))
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
