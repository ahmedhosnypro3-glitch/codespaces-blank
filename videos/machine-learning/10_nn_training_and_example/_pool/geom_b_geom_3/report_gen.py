#!/usr/bin/env python3
"""Lane G / b_geom_3 — write qa/slideNNN/geom_b_geom_3.md from the v2 masks."""
import os

import importlib.util
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
spec = importlib.util.spec_from_file_location(
    "m2", f"{NS}/_pool/geom_b_geom_3/measure_v2.py")
m2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m2)
SLIDES = ["014", "016", "017", "023", "024"]
TOL = 2.0
REGIONS = ["TITLE", "BODY", "FOOTER"]

HDR = """# Lane G geometry closed-loop — slide {n} (scope `b_geom_3`)

- Canonical deliverable: `recreated_pptx/slide_{n}_recreated.pptx`
- Render: LibreOffice headless, private profile `_pool/lo_geom_b_geom_3/`, `TMPDIR` inside the namespace; PDF -> `pdftoppm -png -r 150`
- Render PNG: `_pool/lo_geom_b_geom_3/out/slide_{n}_150.png` — {dimchk}
- Original frame (ground truth): `unique_slides/slide_{n}.jpg` 960x540
- Method: gateway-free PIL measurement only. No vision model was called.

## HOUSE CHROME — OVERRIDDEN, NOT A DEFECT

The house chrome is a hard rule that overrides any per-slide measurement and any
image-analysis JSON. Where it differs from the original frame it is **intentional and
is never reported as a defect**:

- outer red frame: x=0.15, y=0.15, w=13.03, h=7.2 in, border `#C00000` 1.5pt
- yellow badge circle: x=12.48, y=0.30, w=0.5, h=0.5 in, fill + outline `#FFF9C4`,
  centred bold 18pt `#333333`
- slide title box: y=0.28, x=0.6, w=12.13 in, horizontally centred

Measured render chrome agrees with the house rule and is masked out of every
measurement below: red frame stroke render x=22..1976 / y=22..1102 (= x 0.15..13.18 /
y 0.15..7.35 in at 150 dpi), badge disc render x≈1872..1947 / y≈44..120. The original's
own border ring, badge disc and (014/016/017) black video-capture bar are likewise
masked, so **no house-chrome or original-chrome deviation can appear as a finding.**

## Calibration

- Original 960x540 frame -> slide space: 1 frame px = 1/72 in (960 px = 13.333 in,
  540 px = 7.5 in).
- Render 2001x1125 -> slide space: `x*960/2001`, `y*540/1125` (2001/150 = 13.34 in,
  1125/150 = 7.50 in), i.e. ~1 frame px = 1/72 in on both sides after normalisation.
- **Comparison basis = DARK INK** (relative luminance < 150, i.e. text and line art).
  The original frames carry their own multi-tone canvas fills while the recreation is
  drawn on the flat house grey `#E8E8E8`, so a whole-frame "non-background" box would
  compare one background against another; dark ink is slide-specific content in both.
- Regions are the original's own chrome-masked dark-ink row bands, grouped at the two
  largest inter-band gaps. Each region compares the two dark-ink bounding boxes **both
  clipped to the identical frame-px window**, so the delta is box-to-box and unit-safe.
- **Tolerance: 4.0 px @ 150dpi (= 2.0 frame px).**

"""

NOTES = {
    "014": """## Findings (slide 014)

1. **TITLE region — EXCEEDS-TOLERANCE (worst 249 frame px, dx1).**
   The original carries a wide dark-ink element at frame y90..120 spanning x65..882
   (row-level measurement: rows y96..y100 run to x=882 / x=65, rows y101..106 span
   x83..867, rows y107..119 taper x77..864). Its render counterpart at y87..100 spans
   only x100..633. **The render reproduces roughly the middle two thirds of that
   element's width and drops ~250 frame px of it.** This is a true geometry defect, not
   a mask artefact: the mask only removes the ring at x=58/901, y=43/516.
2. **BODY region — EXCEEDS-TOLERANCE (worst 25.34, dx0).** Height matches to 0.20 px
   (orig h284 / render h284.2). Horizontally the render body starts 25.34 px left of
   the original (render x46 vs orig x69) and ends 1.12 px right (886.1 vs 885) — the
   body box is ~26 px wider on the left.
3. **TITLE first band — EXCEEDS-TOLERANCE (worst 15.30, dy1).** The centred heading
   (orig [352,66]-[582,81]) is drawn ~8 px lower in the render (y58..72 vs y66..81)
   and ~6 px wider. Small but outside the 2 px tolerance.
4. **FOOTER region — NOT MEASURABLE / UNPAIRED.** The original has dark ink at
   y447..510 (x74..887, 1459 px) that has no counterpart in the render: the render's
   lowest ink band ends at frame y442. **The render omits the original's footer band.**
5. No render ink falls outside the house frame (0 px).
""",
    "016": """## Findings (slide 016)

1. **TITLE region — PASS (worst 1.67 px).** Excellent agreement.
2. **BODY region — EXCEEDS-TOLERANCE (worst 15.75, dx0).** Horizontal only; the
   vertical edges match (dy0 +0.40, dy1 +1.96). The render body starts 15.75 px left
   of the original (x54 vs x69) and ends 7.83 px right of it (893 vs 885): the body box
   is ~23.6 px too wide.
3. **FOOTER region — EXCEEDS-TOLERANCE (worst 3.91).** Same shape as BODY: horizontal
   only (dx0 +2.04, dx1 -3.91), vertical within 1.20 px. The footer box is ~6 px wide,
   offset ~2 px right. Marginal (under 2x tolerance) rather than gross.
4. **Row-band note:** the render splits the body into 8 bands where the original has 2
   (an extra element at frame y366..390 x65..499 and y397..406 x248..595). Extra
   content, not a position error.
5. No render ink falls outside the house frame (0 px).
""",
    "017": """## Findings (slide 017)

1. **TITLE region — EXCEEDS-TOLERANCE (worst 119.52).** The render's heading spans
   x248..711 against the original's x361..591 — the render heading is ~120 px wider
   (464 vs 231 px) and sits 2..6 px high. This is a heading-width/text-difference,
   confirmed by ink volume (render 8810 vs orig 1510 px).
2. **BODY region — EXCEEDS-TOLERANCE (worst 31.59, dx1).** Vertical agreement is exact
   (dy0 +0.28, dy1 +0.04). Horizontally the render body is 26 px narrower overall
   (797 vs 823) and 5.5 px left at the start, so the original reaches 31.59 px further
   right than the render.
3. **FOOTER region — EXCEEDS-TOLERANCE (worst 57.49, dx1).** Again vertical-exact
   (dy0 +0.12, dy1 +0.24) and horizontal-only: the original footer reaches x887 while
   the render reaches x829.5, i.e. **57.5 px of the original's footer band is missing
   in the render.** A true geometry defect.
4. No render ink falls outside the house frame (0 px).
""",
    "023": """## Findings (slide 023) — the most defective slide in this scope

1. **Overflow outside the house frame — TRUE DEFECT.** 882 px of dark ink sits OUTSIDE
   the house red frame: render px x1..925, y1086..1123, i.e. frame x0.5..443.8,
   **y521.3..539.0**. Split into two bands: 45 px at render y1086..1088 and 837 px at
   render y1109..1123. The other four slides in this scope have 0 px there. The dark
   ink measured there is maroon (120,0,24)/(144,48,72) and black, not the frame red —
   this is body content bleeding past the frame's bottom edge (frame y>521 vs the
   frame bottom at y529.8).
2. **TITLE region — EXCEEDS-TOLERANCE (worst 177.27, dx1).** Vertical agreement is
   exact (dy0 +0.08, dy1 +0.44). Horizontally the render title spans x353..611 while
   the original spans x402..788: the render title is 128 px narrower and shifted left,
   so the original extends 177 px further right. The render title is centred on the
   slide (centre 482 vs slide centre 480) whereas the original's is not (centre 595) —
   a genuine placement difference.
3. **BODY region — EXCEEDS-TOLERANCE (worst 180.51, dx0).** Sizes are close
   (orig w407 vs render w395) but the render body is drawn ~175 px left of the
   original's: original x391..797, render x222.6..616.5. Vertical agreement exact
   (dy0 0.00, dy1 +0.28).
4. **FOOTER region — EXCEEDS-TOLERANCE (worst 80.74, dx0).** Vertical agreement exact
   (dy0 +0.16, dy1 +0.04); the render footer starts 80.74 px left of the original.
5. The inner decorative ring (x61/62, 862/863, y58/523) is masked as chrome; without
   that mask every band reported a false ~250 px offset, which is why the mask is
   documented above.
""",
    "024": """## Findings (slide 024) — best agreement in this scope

1. **BODY region — PASS (worst 0.56 px).** Near-pixel-perfect: the render body box
   matches the original's panel borders at x53..888 with dx0 -0.25 / dx1 -0.56.
2. **FOOTER region — PASS (worst 0.56 px).** Same near-pixel-perfect agreement across
   the full 250 px band (x53..888, y271..520).
3. **TITLE region — EXCEEDS-TOLERANCE (worst 30.40, dy0).** Horizontal agreement is
   excellent (dx0 -0.25, dx1 -0.56, widths 835.3 vs 835) but the render's title band
   contains only a 2.4 px-tall ink strip at frame y98..100 against the original's
   33 px-tall band at y68..100. **The render draws the title-row's full-width border
   line but not its 30 px-tall text block** — ink volume confirms it (render 5224 px
   concentrated in 2 rows vs orig 2815 px spread over 33 rows).
4. No render ink falls outside the house frame (0 px).
""",
}


def dim_check(p):
    im = Image.open(p).convert("RGB")
    a = np.asarray(im).astype(float)
    mean = a.mean()
    ok_dim = abs(im.width - 2000) <= 8 and abs(im.height - 1125) <= 8
    ok_mean = 20.0 <= mean <= 245.0
    return (f"{im.width}x{im.height} (spec 2000x1125 +/-8: "
            f"{'PASS' if ok_dim else 'FAIL'}), non-blank mean {mean:.1f} "
            f"(spec 20..245: {'PASS' if ok_mean else 'FAIL'})")


def overlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]) + 1)


def main():
    for n in SLIDES:
        om = m2.orig_ink(n, f"{NS}/unique_slides/slide_{n}.jpg")
        rp = f"{NS}/_pool/lo_geom_b_geom_3/out/slide_{n}_150.png"
        rm = m2.render_ink(rp)
        sx, sy = 960 / 2001.0, 540 / 1125.0
        ob_raw = m2.bands_of(om)
        rb_raw = m2.bands_of(rm)
        wins = m2.region_windows(ob_raw)
        L = [HDR.format(n=n, dimchk=dim_check(rp))]
        L.append("## Regions\n")
        region_worst = {}
        for i, (wy0, wy1) in enumerate(wins):
            name = REGIONS[i]
            L.append(f"### {name} — original frame y{wy0}..{wy1}\n")
            worst = 0.0
            measured = False
            idxs = [j for j, bb in enumerate(ob_raw)
                    if bb[0] >= wy0 - 1 and bb[1] <= wy1 + 1]
            for j in idxs:
                obb, opx = m2.bbox_in(om, ob_raw[j][0], ob_raw[j][1])
                if obb is None:
                    continue
                best, bestraw, ov = None, None, 0
                for rb in rb_raw:
                    o = overlap(ob_raw[j], rb)
                    if o > ov:
                        best, bestraw, ov = rb, rb, o
                if ov == 0:
                    L.append(f"- original band (y{ob_raw[j][0]}..{ob_raw[j][1]}) "
                             f"box [{obb[0]},{obb[1]}]-[{obb[2]},{obb[3]}] "
                             f"(w{obb[2]-obb[0]+1} h{obb[3]-obb[1]+1}, "
                             f"ink {opx} px): **UNPAIRED — no render dark ink "
                             f"in this y range**\n")
                    continue
                rbb, rpx = m2.bbox_in(rm, bestraw[0], bestraw[1])
                rbf = (rbb[0] * sx, rbb[1] * sy, rbb[2] * sx, rbb[3] * sy)
                d = [obb[0] - rbf[0], obb[1] - rbf[1],
                     obb[2] - rbf[2], obb[3] - rbf[3]]
                w = max(abs(v) for v in d)
                worst = max(worst, w)
                measured = True
                v = "PASS" if w <= TOL else "EXCEEDS-TOLERANCE"
                L.append(f"- band (original y{ob_raw[j][0]}..{ob_raw[j][1]} vs "
                         f"render y{bestraw[0]}..{bestraw[1]}) **{v}**\n")
                L.append(f"  - measured original box (frame px): "
                         f"[{obb[0]},{obb[1]}]-[{obb[2]},{obb[3]}]  "
                         f"w{obb[2]-obb[0]+1} h{obb[3]-obb[1]+1}  ink {opx} px\n")
                L.append(f"  - measured render box (normalized frame px): "
                         f"[{rbf[0]:.1f},{rbf[1]:.1f}]-[{rbf[2]:.1f},"
                         f"{rbf[3]:.1f}]  w{rbf[2]-rbf[0]+1:.1f} "
                         f"h{rbf[3]-rbf[1]+1:.1f}  ink {rpx} px\n")
                L.append(f"  - normalized delta: dx0={d[0]:+.2f} dy0={d[1]:+.2f} "
                         f"dx1={d[2]:+.2f} dy1={d[3]:+.2f} | dw={d[2]-d[0]:+.2f} "
                         f"dh={d[3]-d[1]:+.2f} | worst={w:.2f} (tol {TOL:.0f})\n")
            if measured:
                rv = "PASS" if worst <= TOL else "EXCEEDS-TOLERANCE"
                region_worst[name] = (rv, worst)
                L.append(f"- **{name} REGION VERDICT: {rv}** "
                         f"(worst {worst:.2f} frame px)\n")
            else:
                region_worst[name] = ("NOT MEASURABLE", 0.0)
                L.append(f"- **{name} REGION VERDICT: NOT MEASURABLE** "
                         f"(no render dark ink overlaps the original's bands)\n")
        ov, ovb, det = m2.overflow_check(n, per_band=True)
        L.append("\n### House-frame containment check\n")
        if ov == 0:
            L.append("- dark ink outside the house frame box: **0 px** — "
                     "PASS (all render ink is inside the house frame)\n")
        else:
            L.append(f"- dark ink outside the house frame box: **{ov} px** — "
                     f"**EXCEEDS-TOLERANCE** (content bleeds past the frame)\n")
            L.append(f"  - render px bbox x{ovb[0]}..{ovb[2]} y{ovb[1]}..{ovb[3]}"
                     f" -> frame [{ovb[4]:.1f}..{ovb[6]:.1f}] x "
                     f"[{ovb[5]:.1f}..{ovb[7]:.1f}]\n")
            L.append(f"  - per render-row band: {det}\n")
        L.append(NOTES[n])
        L.append("\n---\n\n## Summary\n\n")
        L.append("| region | verdict | worst deviation (frame px) |\n")
        L.append("|---|---|---|\n")
        for r in REGIONS:
            rv, w = region_worst[r]
            L.append(f"| {r} | {rv} | {w:.2f} |\n")
        L.append(f"| house-frame containment | "
                 f"{'PASS' if ov == 0 else 'EXCEEDS-TOLERANCE'} | {ov} px outside |\n")
        L.append(f"\n**OVERALL (slide {n}): "
                 + ("PASS" if all(region_worst[r][0] == "PASS"
                                  for r in REGIONS) and ov == 0
                    else "GEOMETRY FINDINGS PRESENT") + "**\n")
        out = f"{NS}/qa/slide{n}/geom_b_geom_3.md"
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write("".join(L))
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
NOTES = {
    "014": """## Findings (slide 014)

1. **TITLE region — EXCEEDS-TOLERANCE.** The original carries two dark-ink bands here
   (y66..81 and y90..120). Row-level measurement of the second (from
   `_pool/geom_b_geom_3/probe7.py`): rows y96..y100 reach x=882 / x=65, rows
   y101..106 span x83..867, rows y107..119 taper x77..864 — i.e. a full-width ruled
   element. The render's counterpart at y87..100 spans only x100..633. **The render
   reproduces about the middle two thirds of that element and drops ~250 frame px of
   it.** True defect, not a mask artefact (the mask only removes the ring at x=58/901,
   y=43/516).
2. **BODY region — EXCEEDS-TOLERANCE (worst 25.34, dx0).** Heights match to 0.20 px
   (orig h284 / render h284.2). Horizontally the render body starts 25.34 px left of
   the original (x46 vs x69) and ends 1.12 px right (886.1 vs 885): the body box is
   ~26 px wider on the left.
3. **FOOTER region — NOT MEASURABLE.** The original has dark ink at y447..510
   (x74..887, 1459 px); the render has no dark ink in that window (its lowest ink band
   ends at frame y442). **The render omits the original's footer band.**
4. No render ink falls outside the house frame (0 px).

**Note on the extra 014 render band (frame y132..356, ink 54070 px):** this is the
recreation's diagram panel, whose edges the original draws with lighter ink than the
150-luminance threshold, so it registers only partly. Its vertical span (224.7 px vs
the original's 284.1 px) is the one vertical difference in this region and is reported
in the BODY numbers above.
""",
    "016": """## Findings (slide 016)

1. **TITLE region — best agreement in this scope (worst 1.67 px).** Box-to-box:
   original [65,66]-[882,120] vs render [63.3,65.8]-[882.3,120.0]. The horizontal
   edges land within 1.67 px; the small vertical offsets (dy0 +0.24, dy1 0.00) are
   the house chrome rule (title box starts at y=0.28in = frame y20.2 vs the original's
   own y66), which is INTENTIONAL and not a finding.
2. **BODY region — EXCEEDS-TOLERANCE (worst 15.75, dx0).** Vertical agrees
   (dy0 +0.40, dy1 +1.96). Horizontal: the render body starts 15.75 px left of the
   original (x54 vs x69) and ends 7.83 px right of it (893 vs 885) — the body box is
   ~23.6 px too wide.
3. **FOOTER region — EXCEEDS-TOLERANCE (worst 3.91).** Same shape as BODY: horizontal
   only (dx0 +2.04, dx1 -3.91), vertical within 1.20 px. Marginal (under 2x tolerance)
   rather than gross.
4. **Row-band note:** the render splits the body into 8 bands where the original has 2
   (extra elements at frame y366..390 x65..499 and y397..406 x248..595). Extra content,
   not a position error — it does not move the BODY edges reported above.
5. No render ink falls outside the house frame (0 px).
""",
    "017": """## Findings (slide 017)

1. **TITLE region — EXCEEDS-TOLERANCE (worst 119.52).** The render's heading spans
   x248..711 against the original's x361..591: ~120 px wider (464 vs 231 px) and
   2..6 px high. Ink volume confirms it (render 8810 px vs orig 1510 px). A
   heading-width/text difference.
2. **BODY region — EXCEEDS-TOLERANCE (worst 31.59, dx1).** Vertical agreement is exact
   (dy0 +0.28, dy1 +0.04). Horizontally the render body is 26 px narrower overall
   (797 vs 823): the original reaches 31.59 px further right than the render.
3. **FOOTER region — EXCEEDS-TOLERANCE (worst 57.49, dx1).** Again vertical-exact
   (dy0 +0.12, dy1 +0.24) and horizontal-only: the original footer reaches x887 while
   the render reaches x829.5 — **~57.5 px of the original's footer band is missing in
   the render.** True geometry defect.
4. No render ink falls outside the house frame (0 px).
""",
    "023": """## Findings (slide 023) — most defective slide in this scope

1. **Overflow outside the house frame — TRUE DEFECT.** 882 px of dark ink sits OUTSIDE
   the house red frame: render px x1..925, y1086..1123, i.e. frame x0.5..443.8,
   **y521.3..539.0**. Split into 45 px at render y1086..1088 and 837 px at render
   y1109..1123. The other four slides in this scope have 0 px there. Sampled colours
   there are maroon (120,0,24)/(144,48,72) and black, not the frame red — body content
   bleeding past the frame bottom (frame bottom y529.8).
2. **TITLE region — EXCEEDS-TOLERANCE (worst 177.27, dx1).** Vertical agreement exact
   (dy0 +0.08, dy1 +0.44). Horizontal: render x353..611 vs original x402..788 — the
   render title is 128 px narrower and shifted left, so the original extends 177 px
   further right. The render title is centred on the slide (centre 482 vs slide centre
   480) whereas the original's is not (centre 595).
3. **BODY region — EXCEEDS-TOLERANCE (worst 180.51, dx0).** Sizes close (orig w407 vs
   render w395) but the render body is drawn ~175 px left of the original's:
   original x391..797, render x222.6..616.5. Vertical agreement exact (dy0 0.00,
   dy1 +0.28).
4. **FOOTER region — EXCEEDS-TOLERANCE (worst 80.74, dx0).** Vertical agreement exact
   (dy0 +0.16, dy1 +0.04); the render footer starts 80.74 px left of the original.
5. The inner decorative ring (x61/62, 862/863, y58/523) is masked as chrome; without
   that mask every band reported a false ~250 px offset, which is why the mask is
   documented above.
""",
    "024": """## Findings (slide 024) — best agreement in this scope

1. **BODY region — PASS (worst 0.56 px).** Near-pixel-perfect: the render body box
   matches the original's panel borders at x53..888 with dx0 -0.25 / dx1 -0.56.
2. **FOOTER region — PASS (worst 0.56 px).** Same near-pixel-perfect agreement across
   the full 250 px band (x53..888, y271..520).
3. **TITLE region — EXCEEDS-TOLERANCE (worst 30.40, dy0).** Horizontal agreement is
   excellent (dx0 -0.25, dx1 -0.56, widths 835.3 vs 835) but the render's title band
   contains only a 2.4 px-tall ink strip at frame y98..100 against the original's
   33 px-tall band at y68..100. **The render draws the title row's full-width border
   line but not its 30 px-tall text block** — ink volume confirms it (render 5224 px
   concentrated in 2 rows vs orig 2815 px spread over 33 rows).
4. No render ink falls outside the house frame (0 px).
""",
}
