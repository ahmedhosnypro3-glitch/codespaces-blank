#!/usr/bin/env python3
"""Probe 20: FONT FIT for slide 009's text elements.

Rasterizes each verbatim string with PIL (Liberation Serif = Times New Roman
metrics; Liberation Sans = Arial metrics), at a range of pt sizes, and reports
the ink width + cap-height so the measured frame geometry can be matched.

MEASURED (frame px, 1px = 1pt), from probes 12/15/16/18/19:
  LCAP line1 'Overfit (try to minimize the residuals ONLY)'  ink w 311 (x109..419)
             caps y488..501 (h 14), descender to y504
             LEADING WORD 'Overfit' is RED (x108..156), rest BLACK (x165..419)
  LCAP line2 'Fails to detect the Pattern'                   ink w 171 (x179..349)
             caps y507..520 (h 14)
  RCAP line1 'Generalized (Residuals are not minimized)'     ink w 318 (x502..819)
             caps y487..501, 'Generalized' RED (x498..607) rest BLACK
  RCAP line2 'Successes to detect the Pattern'               ink w 208 (x567..774)
             caps y507..520 (h 14)
Font-fit rule: pick the size whose rendered ink width is within 2% of measured.
"""
from PIL import Image, ImageDraw, ImageFont

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

TARGETS = [
    ("LCAP1", "Overfit (try to minimize the residuals ONLY)", 311),
    ("LCAP2", "Fails to detect the Pattern", 171),
    ("RCAP1", "Generalized (Residuals are not minimized)", 318),
    ("RCAP2", "Successes to detect the Pattern", 208),
]


def ink_w(text, path, size_pt):
    """Render at 1px-per-pt scale and return (ink width, cap height)."""
    f = ImageFont.truetype(path, int(round(size_pt * 4)))  # 4x for precision
    im = Image.new("L", (10, 10), 255)
    d = ImageDraw.Draw(im)
    bb = d.textbbox((0, 0), text, font=f)
    w = (bb[2] - bb[0]) / 4.0
    # cap height: render 'H' and 'x'
    hb = d.textbbox((0, 0), "H", font=f)
    xb = d.textbbox((0, 0), "x", font=f)
    cap = (hb[3] - hb[1]) / 4.0
    xh = (xb[3] - xb[1]) / 4.0
    return w, cap, xh


for nm, text, meas in TARGETS:
    print(f"\n===== {nm}  measured ink w={meas} =====")
    print(f"  text: {text!r}")
    rows = []
    for label, path in (("SerifReg", SERIF), ("SerifBold", SERIF_B),
                        ("SansReg", SANS), ("SansBold", SANS_B)):
        for size in [x / 2 for x in range(20, 60)]:
            w, cap, xh = ink_w(text, path, size)
            rows.append((abs(w - meas), label, size, w, cap, xh))
    rows.sort()
    for diff, label, size, w, cap, xh in rows[:6]:
        pct = 100.0 * (w - meas) / meas
        print(f"  {label:9s} {size:5.1f}pt -> ink w {w:6.1f} ({pct:+5.2f}%)  capH {cap:5.1f}  xH {xh:5.1f}")
