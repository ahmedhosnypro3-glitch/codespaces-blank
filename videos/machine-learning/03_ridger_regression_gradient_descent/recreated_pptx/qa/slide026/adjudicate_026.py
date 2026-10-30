#!/usr/bin/env python3
"""Slide 026 adjudication (resume worker, 2026-10-21).

selfcheck_attempt_3.out FAILs every text band by 1-14 frame px. Law (building.md
closed-loop checker discipline): a checker's FAIL is a CLAIM, not a verdict —
run the SAME predicates/windows on BOTH images so JPEG-antialias bleed cancels,
then compare original-vs-render directly. If the original's own bbox (same mask)
sits within ~2 frame px of the render's, the FAIL is mask/threshold noise
(JPEG halo on the original inflating the banked targets), NOT a build defect.

All values in frame px (original is 960x540; render is 2001x1125, converted back).
"""
import numpy as np
from PIL import Image
import sys

QA = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
REN = sys.argv[1] if len(sys.argv) > 1 else QA + "/recreated_pptx/qa/slide026/render_4.png"
ORG = QA + "/unique_slides/slide_026.jpg"
print("adjudicating:", REN)

ren = np.asarray(Image.open(REN).convert("RGB")).astype(int)
org = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
HR, WR, _ = ren.shape
SY, SX = HR / 540.0, WR / 960.0
print("render %dx%d scale x %.4f y %.4f | original %dx%d" % (WR, HR, SX, SY, org.shape[1], org.shape[0]))

def masks(im, is_render):
    R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    red = (R - G > 40) & (R - B > 40)
    blue = (B - R > 40) & (B - G > 40)
    inkW = (np.abs(im - 255).max(axis=2) > 30)   # box interior is ~(254,255,253) = white in BOTH
    GRAY = np.array([233, 233, 231])
    inkG = (np.abs(im - GRAY).max(axis=2) > 25)  # title zone sits on gray/white panel
    return {"red": red, "blue": blue, "inkW": inkW, "inkG": inkG}

mr, mo = masks(ren, True), masks(org, False)

def band(mask, fy0, fy1, fx0, fx1, sx, sy):
    y0, y1 = int(fy0 * sy), int(fy1 * sy)
    x0, x1 = int(fx0 * sx), int(fx1 * sx)
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    return ((x0 + xs.min()) / sx, (x0 + xs.max()) / sx,
            (y0 + ys.min()) / sy, (y0 + ys.max()) / sy)

# identical windows as selfcheck_attempt_3; mask per row
CASES = [
    ("title",     "inkG", 56, 86, 280, 650,  (294, 639, 60, 82)),
    ("gdhdr",     "red",  105, 133, 100, 860, (109, 392, 110, 129)),
    ("rowA",      "blue", 138, 168, 140, 860, (146, 469, 143, 162)),
    ("rowB",      "blue", 172, 202, 140, 860, (146, 846, 177, 196)),
    ("rowC-bl",   "blue", 205, 236, 140, 516, (146, 512, 210, 229)),
    ("rowC-red",  "red",  205, 236, 515, 860, (518, 689, 210, 229)),
    ("rowD",      "blue", 238, 268, 140, 860, (146, 830, 243, 262)),
    ("noteshdr",  "red",  305, 328, 100, 860, (109, 159, 310, 324)),
    ("N1",        "inkW", 338, 366, 86, 860,  (91, 769, 342, 361)),
    ("N2",        "inkW", 372, 400, 100, 860, (109, 575, 376, 394)),
    ("N3",        "inkW", 437, 465, 86, 860,  (91, 836, 441, 460)),
    ("N4",        "inkW", 470, 496, 100, 860, (109, 295, 475, 494)),
]

print("\n== ADJUDICATION: identical predicates, original vs render (frame px) ==")
print("%-10s %-26s | %-26s | orig-ren | verdict" % ("band", "ORIGINAL", "RENDER_3"))
real = []
for name, mk, y0, y1, x0, x1, want in CASES:
    bo = band(mo[mk], y0, y1, x0, x1, 1.0, 1.0)
    br = band(mr[mk], y0, y1, x0, x1, SX, SY)
    if bo is None or br is None:
        print("%-10s MISSING  orig=%s ren=%s" % (name, bo, br))
        real.append((name, "missing"))
        continue
    d = [br[i] - bo[i] for i in range(4)]
    ok = all(abs(v) <= 2.0 for v in d)
    if not ok:
        real.append((name, d))
    print("%-10s x %5.1f..%5.1f y %5.1f..%5.1f | x %5.1f..%5.1f y %5.1f..%5.1f | %+5.1f %+5.1f %+5.1f %+5.1f %s"
          % (name, bo[0], bo[1], bo[2], bo[3], br[0], br[1], br[2], br[3],
             d[0], d[1], d[2], d[3], "OK" if ok else "<<< REAL DELTA"))

print("\nbands with real orig-vs-render deltas >2px: %s" % ([r[0] for r in real] or "NONE"))

# Also: what does the ORIGINAL's own band look like vs the banked 'want' values?
print("\n== original's own bbox vs banked want (mask noise check) ==")
for name, mk, y0, y1, x0, x1, want in CASES:
    bo = band(mo[mk], y0, y1, x0, x1, 1.0, 1.0)
    if bo is None:
        print("  %-10s MISSING" % name); continue
    d = [bo[i] - want[i] for i in range(4)]
    print("  %-10s orig-want %+5.1f %+5.1f %+5.1f %+5.1f" % (name, d[0], d[1], d[2], d[3]))
