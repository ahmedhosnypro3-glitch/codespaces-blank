#!/usr/bin/env python3
"""Self-check for slide 046 — PIL comparison of the 150dpi render against the
original frame's MEASURED ink bboxes.

Frame is 960x540 (1px = 1pt). Render is 150dpi of a 13.333x7.5in slide
(2001x1125px), so render_px = frame_px * 2001/960 = frame_px * 2.0844.

Every window below is a MEASURED frame-px ink extent from
unique_slides/slide_046.jpg (PIL, this session). For each we assert the render
has ink inside it and that its measured ink bbox stays within TOL frame px of
the original's.
"""
import sys
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
ORIG = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_046.jpg"
RENDER = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide046/render_2.png"
OUT = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide046/selfcheck_attempt_2.txt"

S = 2001 / 960
TOL = 8

WINDOWS = [
    ("top_rule_1",      68, 53, 720, 58),
    ("top_rule_2",      68, 126, 720, 132),
    ("table_header",    74, 60, 232, 76),
    ("table_row1",      74, 78, 250, 92),
    ("table_row2",      74, 94, 250, 108),
    ("table_classrow",  74, 108, 232, 126),
    ("caption",         250, 108, 455, 126),
    ("upper_mid_text",  328, 60, 445, 106),
    ("z_matrix",        590, 60, 665, 112),
    ("yellow_box",      735, 57, 832, 145),
    ("dash_sep",        66, 136, 250, 144),
    ("aug_subscript",   66, 146, 250, 176),
    ("aug_header",      74, 162, 250, 178),
    ("aug_rows",        70, 180, 246, 226),
    ("aug_classrow",    74, 228, 240, 244),
    ("aug_rule_255",    70, 250, 246, 255),
    ("iteration4_box",  84, 277, 212, 304),
    ("stop_box",        64, 331, 245, 415),
    ("plot",            312, 172, 825, 481),
    ("badge",           858, 55, 895, 92),
]
# Windows dominated by saturated red/blue class labels: measure STRONG so the
# JPEG chroma halo around a saturated glyph does not fake a wider bbox.
STRONG = {"table_classrow", "caption", "table_header", "aug_classrow"}


def ink_bbox(im, x0, y0, x1, y1, thr=205, strong=False):
    """strong=True: ink = low-luminance OR high-saturation. This keeps pure
    blue (0,0,255) and pure red (255,0,0) glyphs as ink while rejecting the
    near-white JPEG chroma halo they bleed into neighbouring pixels."""
    px = im.load()
    minx = miny = 10 ** 9
    maxx = maxy = -1
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            lum = (r + g + b) / 3
            sat = max(r, g, b) - min(r, g, b)
            hit = (lum < thr or sat > 90) if strong else (r < thr or g < thr or b < thr)
            if hit:
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    return (minx, miny, maxx, maxy) if maxx >= 0 else None


def main():
    orig = Image.open(ORIG).convert("RGB")
    rend = Image.open(RENDER).convert("RGB")
    lines = []
    fails = 0
    print(f"orig {orig.size}  render {rend.size}  scale {S:.4f}  TOL {TOL} frame px")
    lines.append(f"orig {orig.size}  render {rend.size}  scale {S:.4f}  TOL {TOL} frame px")

    for name, fx0, fy0, fx1, fy1 in WINDOWS:
        strong = name in STRONG
        o = ink_bbox(orig, fx0, fy0, fx1 + 1, fy1 + 1, strong=strong)
        if o is None:
            msg = f"{name:16s} ORIGINAL has NO ink in window -- window wrong or element absent"
            print("FAIL " + msg)
            lines.append("FAIL " + msg)
            fails += 1
            continue
        r = ink_bbox(rend, int(fx0 * S), int(fy0 * S), int(fx1 * S) + 1, int(fy1 * S) + 1, strong=strong)
        if r is None:
            msg = f"{name:16s} MISSING INK in render window"
            print("FAIL " + msg)
            lines.append("FAIL " + msg)
            fails += 1
            continue
        rf = (r[0] / S, r[1] / S, r[2] / S, r[3] / S)
        d = (rf[0] - o[0], rf[1] - o[1], rf[2] - o[2], rf[3] - o[3])
        dev = max(abs(v) for v in d)
        status = "ok  " if dev <= TOL else "FAIL"
        if dev > TOL:
            fails += 1
        msg = (f"{status} {name:16s} orig=({o[0]},{o[1]})-({o[2]},{o[3]}) "
               f"rend=({rf[0]:.1f},{rf[1]:.1f})-({rf[2]:.1f},{rf[3]:.1f}) "
               f"d=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f}) max={dev:.1f}"
               + ("  [strong]" if strong else ""))
        print(msg)
        lines.append(msg)

    print(f"\nSELFCHECK: {len(WINDOWS) - fails}/{len(WINDOWS)} windows within {TOL} frame px")
    lines.append(f"\nSELFCHECK: {len(WINDOWS) - fails}/{len(WINDOWS)} windows within {TOL} frame px")
    lines.append("VERDICT: " + ("PASS" if fails == 0 else "FAIL"))
    with open(OUT, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"banked {OUT}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
