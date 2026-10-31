#!/usr/bin/env python3
"""Emit qa/slideNNN/geom_b_geom_2.md from _pool/bgeom2_measurements.json."""
import json
import os

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
RES = f"{NS}/_pool/bgeom2_measurements.json"
REG_LABEL = {"title": "title block", "body": "body / equation / diagram / table region",
             "footer": "footer region"}
REG_SPAN = {"title": "slide y 0.15..1.10 in", "body": "slide y 1.10..6.90 in",
            "footer": "slide y 6.90..7.50 in"}


def fmtbox(b):
    if b is None:
        return "none"
    return (f"x {b['left']:.2f}..{b['right']:.2f} in, y {b['top']:.2f}..{b['bottom']:.2f} in "
            f"(ink px {b['ink_px']})")


def emit(rec, notes):
    sl = rec["slide"]
    L = []
    A = L.append
    A(f"# Lane G geometry closed-loop — slide {sl} (scope `b_geom_2`)")
    A("")
    A(f"- Canonical deliverable: `recreated_pptx/slide_{sl}_recreated.pptx`")
    A(f"- Render: LibreOffice headless, private profile `_pool/lo_geom_b_geom_2/{sl}/`, "
      f"`TMPDIR` inside the namespace; PDF -> `pdftoppm -png -r 150`")
    A(f"- Render PNG: `_pool/tmp_geom_b_geom_2/{sl}/render-1.png` — "
      f"{rec['render_dim'][0]}x{rec['render_dim'][1]} px "
      f"({'PASS' if rec['dim_ok'] else 'FAIL'}, target 2000x1125 +/-8)")
    A(f"- Render mean luminance: {rec['render_mean']} "
      f"({'PASS' if rec['blank_ok'] else 'FAIL'}, non-blank band 20..245)")
    A(f"- Original frame (ground truth): `unique_slides/slide_{sl}.jpg` 960x540")
    A("")
    A("## Calibration")
    A("")
    A("The original 960x540 file is a **video frame that letterboxes the slide** (white band")
    A("above the slide, black band below it), and it is anisotropic, so a naive proportional")
    A("normalisation is wrong by ~10%. Both images are therefore mapped into slide-inch")
    A("coordinates through the house chrome fiducial (the outer red rectangle at")
    A("x=0.15, y=0.15, w=13.03, h=7.2 in):")
    A("")
    A("| image | red-rect line centres | scale (px/in) |")
    A("|---|---|---|")
    A("| render 2001x1125 | x 22.0 / 1976.0, y 22.0 / 1102.0 | 150.00 x, 150.00 y |")
    A(f"| original 960x540 | x 58.45 / 901.07, y 42.95 / 516.66 | "
      f"{rec['calib']['orig_ppin_x']} x, {rec['calib']['orig_ppin_y']} y |")
    A("")
    A("Cross-check: the original's yellow badge maps to slide x 12.78 in, y 0.56 in under")
    A("this mapping (house badge centre = 12.73 / 0.55) — a 0.05 in residual, versus")
    A("0.16 in if the red rectangle were instead read as the slide edge. The house-fiducial")
    A("mapping is the one adopted.")
    A("")
    A("Content ink = luminance < 170 OR chroma > 45, morphological opening to drop JPEG")
    A("speckle. The outer red rectangle, the yellow badge and everything outside the slide")
    A("area are masked out of **both** images, so no house-chrome deviation can appear as a")
    A("finding.")
    A("")
    A("## Regions")
    A("")
    for name in ("title", "body", "footer"):
        r = rec["regions"][name]
        A(f"### {REG_LABEL[name]} ({REG_SPAN[name]})")
        A("")
        A(f"- Measured render box: {fmtbox(r['render'])}")
        A(f"- Measured original box: {fmtbox(r['orig'])}")
        if r.get("deltas"):
            d = r["deltas"]
            A(f"- Normalized delta (px @ 150dpi, render - original): "
              f"left {d['left']:+.1f}, top {d['top']:+.1f}, right {d['right']:+.1f}, "
              f"bottom {d['bottom']:+.1f}")
            A(f"- Worst |delta|: **{r['worst_px150']} px @ 150dpi** (tolerance 4.0 px)")
        else:
            A("- Normalized delta: not computable (a region is empty on one side)")
        A(f"- **{r['status']}**")
        if r.get("note"):
            A(f"- Note: {r['note']}")
        note = notes.get((sl, name))
        if note:
            for ln in note:
                A(f"- {ln}")
        A("")
    A("## Verdict")
    A("")
    for name in ("title", "body", "footer"):
        A(f"- {REG_LABEL[name]}: **{rec['regions'][name]['status']}**")
    A("")
    return "\n".join(L) + "\n"


def findings(rec, notes):
    """Content geometry findings only - chrome-attributable deviations excluded."""
    out = []
    sl, cls = rec["slide"], notes.CLASS
    for name in ("title", "body", "footer"):
        r = rec["regions"][name]
        if cls.get((sl, name)) == "chrome":
            continue
        if r["status"] != "EXCEEDS-TOLERANCE":
            continue
        if r.get("deltas"):
            if cls.get((sl, name)) == "mixed":
                out.append(f"- **{name}** (MIXED - chrome edge excluded): "
                           f"{notes.MIXED_CONTENT[(sl, name)]}")
                continue
            d = r["deltas"]
            out.append(f"- **{name}**: worst {r['worst_px150']} px @150dpi "
                       f"(left {d['left']:+.1f}, top {d['top']:+.1f}, "
                       f"right {d['right']:+.1f}, bottom {d['bottom']:+.1f})")
        else:
            out.append(f"- **{name}**: {r['note']} (render={r['render']}, orig={r['orig']})")
    return out


def main():
    import importlib.util
    spec = importlib.util.spec_from_file_location("n", f"{NS}/_pool/bgeom2_notes.py")
    n = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(n)
    recs = json.load(open(RES))
    for rec in recs:
        sl = rec["slide"]
        os.makedirs(f"{NS}/qa/slide{sl}", exist_ok=True)
        md = emit(rec, n.NOTES)
        f = findings(rec, n)
        md += "## Content geometry findings (chrome excluded)\n\n"
        if f:
            md += "\n".join(f) + "\n"
        else:
            md += "- none in this slide's regions\n"
        md += ("\nA region that exceeds tolerance is an input to adjudication, not an automatic\n"
               "rebuild. Deviations explained by the house chrome (outer red rectangle, yellow\n"
               "badge, title box at x=0.6/y=0.28/w=12.13 centred) are listed above for context\n"
               "and are NOT findings.\n")
        path = f"{NS}/qa/slide{sl}/geom_b_geom_2.md"
        with open(path, "w") as fh:
            fh.write(md)
        print("wrote", path, len(md.splitlines()), "lines")


if __name__ == "__main__":
    main()
