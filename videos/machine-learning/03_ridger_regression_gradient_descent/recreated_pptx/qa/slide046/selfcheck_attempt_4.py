#!/usr/bin/env python3
"""Self-check for slide 046 attempt 4 — PIL comparison of the 150dpi render
(render_4.png) against ink bboxes measured FRESH from unique_slides/slide_046.jpg.

Frame is 960x540 (1px = 1pt). Render is 150dpi of a 13.333x7.5in slide
(2001x1125px) -> scale 1125/540 = 2.08333 render-px per frame-px.

Every window below is a MEASURED frame-px ink extent from the original frame
(PIL, this session). For each we assert the render has ink inside it and that
its measured ink bbox stays within TOL frame px of the original's.

Windows correct the attempt-2/3 list, which was transcribed against the ROW
layout. Attempt 4 rebuilds the top matrix and the augmented box as
PARENTHESISED COLUMN VECTORS, so the windows now cover the column bands.
"""
import sys
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
DECK = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{DECK}/unique_slides/slide_046.jpg"
RENDER = f"{DECK}/recreated_pptx/qa/slide046/render_4.png"
OUT = f"{DECK}/recreated_pptx/qa/slide046/selfcheck_attempt_4.txt"

S = 1125 / 540
TOL = 8

WINDOWS = [
    # top-left box: header row, the 6 paren column pair band, class row, caption
    ("top_header",        86,  58, 216,  76),
    ("top_colpairs",      86,  76, 216, 108),
    ("top_classrow",      86, 108, 216, 128),
    ("caption",          244, 106, 512, 126),
    ("top_box_left",      66,  52,  74, 132),
    ("top_box_right",    714,  52, 722, 132),
    # Initial W vector + red Step eta line
    ("initial_vec",      328,  56, 374, 110),
    ("step_eta",         368,  62, 456,  84),
    ("check_classes",    496,  74, 582,  92),
    # Z matrix
    ("z_header",         594,  60, 660,  76),
    ("z_colpairs",       594,  76, 660, 110),
    # final-weight box
    ("yellow_box",       736,  56, 832, 146),
    ("yellow_vec",       780,  64, 826, 136),
    # augmented box
    ("aug_title",         80, 142, 238, 162),
    ("a_header",          88, 160, 214, 180),
    ("a_colpairs",        86, 176, 214, 228),
    ("a_classrow",        88, 228, 214, 246),
    ("aug_box_left",      66, 138,  74, 258),
    ("aug_box_right",    240, 138, 250, 258),
    # callouts
    ("iteration4_box",    82, 276, 214, 306),
    ("stop_box",          62, 329, 247, 417),
    ("stop_text1",        76, 344, 230, 374),
    ("stop_text2",        76, 372, 230, 396),
    # plot
    ("plot",             310, 171, 827, 484),
    ("plot_dec_line",    535, 180, 552, 446),
    # house chrome
    ("badge",            856,  53, 898,  95),
]
# Windows dominated by saturated red/blue glyphs: measure STRONG so the JPEG
# chroma halo around a saturated glyph does not fake a wider bbox.
STRONG = {"top_classrow", "caption", "a_classrow"}


def ink_bbox(im, x0, y0, x1, y1, thr=205, strong=False):
    """strong=True: ink = low-luminance OR high-saturation."""
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
    head = f"orig {orig.size}  render {rend.size}  scale {S:.5f}  TOL {TOL} frame px"
    print(head)
    lines.append(head)

    for name, fx0, fy0, fx1, fy1 in WINDOWS:
        strong = name in STRONG
        o = ink_bbox(orig, fx0, fy0, fx1 + 1, fy1 + 1, strong=strong)
        if o is None:
            msg = f"FAIL {name:16s} ORIGINAL has NO ink in window"
            print(msg)
            lines.append(msg)
            fails += 1
            continue
        r = ink_bbox(rend, int(fx0 * S), int(fy0 * S), int(fx1 * S) + 1, int(fy1 * S) + 1, strong=strong)
        if r is None:
            msg = f"FAIL {name:16s} MISSING INK in render window"
            print(msg)
            lines.append(msg)
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
