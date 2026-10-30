#!/usr/bin/env python3
"""Slide 026 definitive pre-judge self-check (attempt 9 (attempt-5 lineage), resume worker 2026-10-21).

WHY THIS VERSION EXISTS (closed-loop checker discipline, building.md):
selfcheck_attempt_2/3/4 compared the render against banked "want" numbers that
had been measured on the ORIGINAL at a DIFFERENT time with DIFFERENT masks (some
with a loose gray-diff mask, some with a bar scanner that kept the LAST matching
row instead of the longest bar run). Those wants drifted from what the original
actually contains under the same predicate, so the checker flagged correct bands.

This version derives every target from the ORIGINAL FRAME with the IDENTICAL
predicate and window, then reports render-vs-original. That is the only
comparison that cancels JPEG halos and mask noise on both sides.

Additions vs attempts 2-4:
  - title measured on the RED mask (the old inkG-vs-gray mask caught a faint
    8x6px JPEG ghost at x438..445 y83..88 under the original's title, which
    produced the phantom -4.4px bottom edge);
  - bar scan bridges a 2px AA seam (the render's rowD bar renders as two runs
    with a 1px gap at x377/378; a contiguous-run requirement split it and
    reported "NO BAR");
  - tolerance: +/-2.0 frame px per text edge, +/-3.0 per bar edge, with the
    documented original-font metric noise band (+/-6.6px measured max on
    mid-line word/bar positions, word_runs_026_out.txt) noted per flag.

All values in frame px. Original 960x540; render 2001x1125 (scale SX/SY).
"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ORG = HERE + "/../../../unique_slides/slide_026.jpg"
REN = os.path.join(HERE, "render_9.png")
GRAY = np.array([233, 233, 231])


def masks(im):
    R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return {
        "red": (R - G > 40) & (R - B > 40),
        "blue": (B - R > 40) & (B - G > 40),
        "inkW": (np.abs(im - 255).max(axis=2) > 30),          # box interior is white in BOTH
        "inkG": (np.abs(im - GRAY).max(axis=2) > 25),         # kept for reference only
    }


ren = np.asarray(Image.open(REN).convert("RGB")).astype(int)
org = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
HR, WR, _ = ren.shape
SY, SX = HR / 540.0, WR / 960.0
print("render %dx%d  scale x %.4f y %.4f | original %dx%d" % (WR, HR, SX, SY, org.shape[1], org.shape[0]))

mr, mo = masks(ren), masks(org)


def band(mask, fy0, fy1, fx0, fx1, sx, sy):
    y0, y1 = int(fy0 * sy), int(fy1 * sy)
    x0, x1 = int(fx0 * sx), int(fx1 * sx)
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(sub)
    if len(ys) == 0:
        return None
    return ((x0 + xs.min()) / sx, (x0 + xs.max()) / sx,
            (y0 + ys.min()) / sy, (y0 + ys.max()) / sy)


CASES = [
    ("title",    "red",  56, 88, 280, 650),
    ("gdhdr",    "red",  105, 133, 100, 860),
    ("rowA",     "blue", 138, 168, 140, 860),
    ("rowB",     "blue", 172, 202, 140, 860),
    ("rowC-bl",  "blue", 205, 236, 140, 516),
    ("rowC-red", "red",  205, 236, 515, 860),
    # attempt 8: the original's closing paren is a separate BLUE run x684..688 (core
    # RGB (13,4,118)); red stops at x682. Checked on the blue mask inside x675..700.
    ("rowC-paren", "blue", 205, 236, 675, 700),
    ("rowD",     "blue", 238, 268, 140, 860),
    ("noteshdr", "red",  305, 328, 100, 860),
    ("N1",       "inkW", 338, 366, 86, 860),
    ("N2",       "inkW", 372, 400, 100, 860),
    ("N3",       "inkW", 437, 465, 86, 860),
    ("N4",       "inkW", 470, 496, 100, 860),
]

print("\n== TEXT BANDS: render vs ORIGINAL (identical predicate + window) ==")
# expected classes: horizontal edges real; bottom edges carry the original font's
# deeper descender metrics (measured: original 'g' baseline+6.5px vs Arial +3.4px)
NOTES = {
    "title": "no descender glyph issue: red-mask bottoms agree (orig y82 = ren y82)",
    "rowA": "bottom: original 'g' descender y162 vs Arial y159 (font metric, unfixable under font law)",
    "gdhdr": "bottom: original descender tail y129 vs ren y126 (font metric)",
    "rowB": "",
    "rowC-bl": "bottom: descender metrics",
    "rowC-red": "attempt 8: red tail x520..682 no longer includes the (now blue) paren",
    "rowC-paren": "attempt 8: paren core RGB (13,4,118) = BLUE; original x684..688 h17",
    "rowD": "",
    "noteshdr": "right +2.2 = original 'Notes:' word metric (51px vs 51.3px)",
    "N1": "bottom: descender metrics",
    "N2": "",
    "N3": "bottom: descender metrics",
    "N4": "bottom: descender metrics",
}
bad = []
for name, mk, y0, y1, x0, x1 in CASES:
    bo = band(mo[mk], y0, y1, x0, x1, 1.0, 1.0)
    br = band(mr[mk], y0, y1, x0, x1, SX, SY)
    if bo is None or br is None:
        print("  %-10s MISSING INK  orig=%s ren=%s" % (name, bo, br))
        bad.append((name, "missing"))
        continue
    d = [br[i] - bo[i] for i in range(4)]
    ok = all(abs(v) <= 2.0 for v in d)
    tag = "OK" if ok else ("FIX" if (abs(d[0]) > 2.0 or abs(d[1]) > 2.0) else "adj")
    if not ok:
        bad.append((name, d))
    print("  %-10s x %6.1f..%6.1f y %6.1f..%6.1f | x %6.1f..%6.1f y %6.1f..%6.1f | d %+5.1f %+5.1f %+5.1f %+5.1f %s %s"
          % (name, bo[0], bo[1], bo[2], bo[3], br[0], br[1], br[2], br[3],
             d[0], d[1], d[2], d[3], tag, ("| " + NOTES[name]) if NOTES[name] and not ok else ""))

print("\n== UNDERLINE BARS (longest solid run, 2px AA-seam bridge) ==")


def bridge(row, gap):
    """Boolean row with runs shorter than `gap` empty cols filled (AA seam)."""
    out = row.copy()
    n = len(row)
    i = 0
    while i < n:
        if row[i]:
            j = i
            while j < n and row[j]:
                j += 1
            k = j
            miss = 0
            while k < n and not row[k] and miss < gap:
                k += 1
                miss += 1
            if k < n and row[k] and miss < gap:
                out[i:k] = True
            i = j
        else:
            i += 1
    return out


def bestbar(mask, sx, sy, fy0, fy1, fx0, fx1, minlen):
    y0, y1 = int(fy0 * sy), int(fy1 * sy)
    x0, x1 = int(fx0 * sx), int(fx1 * sx)
    g = max(1, int(round(2 * sx)))
    best = None
    for ry in range(y0, y1 + 1):
        row = bridge(mask[ry, x0:x1 + 1], g)
        i, n = 0, len(row)
        while i < n:
            if row[i]:
                j = i
                while j < n and row[j]:
                    j += 1
                if j - i >= minlen * sx:
                    span = ((x0 + i) / sx, (x0 + j) / sx)
                    if best is None or (span[1] - span[0]) > (best[1] - best[0]):
                        best = (span[0], span[1], ry / sy)
                i = j
            else:
                i += 1
    return best


BARS = [
    ("rowB", "blue", 188, 200, 300, 860, 340),
    ("rowD", "blue", 252, 266, 270, 500, 150),
    ("N3a",  "inkW", 450, 466, 150, 300, 80),
    ("N3b",  "inkW", 450, 466, 500, 760, 150),
]
for name, mk, y0, y1, x0, x1, ml in BARS:
    bo = bestbar(mo[mk], 1.0, 1.0, y0, y1, x0, x1, ml)
    br = bestbar(mr[mk], SX, SY, y0, y1, x0, x1, ml)
    if bo is None or br is None:
        print("  %-6s NO BAR  orig=%s ren=%s" % (name, bo, br))
        bad.append((name, "no bar"))
        continue
    d = [br[i] - bo[i] for i in range(3)]
    ok = all(abs(v) <= 3.0 for v in d)
    if not ok:
        bad.append((name, d))
    print("  %-6s ORIG x %6.1f..%6.1f y %5.1f | REN x %6.1f..%6.1f y %5.1f | d %+5.1f %+5.1f %+5.1f %s"
          % (name, bo[0], bo[1], bo[2], br[0], br[1], br[2], d[0], d[1], d[2],
             "OK" if ok else "<<< bar delta (font-metric noise band +-6.6)"))

print("\n== BULLET DISCS ==")
for name, y0, y1 in (("N1-bul", 344, 354), ("N3-bul", 444, 453)):
    bo = band(mo["inkW"], y0, y1, 88, 100, 1.0, 1.0)
    br = band(mr["inkW"], y0, y1, 88, 100, SX, SY)
    d = [br[i] - bo[i] for i in range(4)]
    ok = all(abs(v) <= 2.0 for v in d)
    if not ok:
        bad.append((name, d))
    print("  %-8s x %6.1f..%6.1f y %6.1f..%6.1f | x %6.1f..%6.1f y %6.1f..%6.1f | d %+4.1f %+4.1f %+4.1f %+4.1f %s"
          % (name, bo[0], bo[1], bo[2], bo[3], br[0], br[1], br[2], br[3],
             d[0], d[1], d[2], d[3], "OK" if ok else "<<< FIX"))

print("\n== FRAME CONTAINMENT (render) ==")
boxm = mr["blue"]
cols = np.where(boxm.sum(axis=0) > 150 * SY)[0]
rows = np.where(boxm.sum(axis=1) > 400 * SX)[0]
cf = [round(c / SX) for c in cols]
rf = [round(r / SY) for r in rows]
print("  blue border cols (frame px): %s | rows: %s" % (cf, rf))
content = (mr["inkW"] | mr["red"] | mr["blue"]).copy()
content[:int(94 * SY)] = False
content[int(497 * SY):] = False
content[:, :int(86 * SX)] = False
content[:, int(860 * SX):] = False
ys, xs = np.where(content)
ex = (xs.min() / SX, xs.max() / SX, ys.min() / SY, ys.max() / SY)
print("  interior content ink extent: x %.1f..%.1f  y %.1f..%.1f (box interior x84..862 y93..497)" % ex)
cont_ok = ex[0] >= 82 and ex[1] <= 864 and ex[2] >= 90 and ex[3] <= 500
print("  containment inside blue box: %s" % ("OK" if cont_ok else "FAIL <<<"))
if not cont_ok:
    bad.append(("containment", ex))

print("\nbands/bars with real deltas > tolerance: %s" % ([b[0] for b in bad] or "NONE"))
print("SELFCHECK-5 RESULT: %s" % ("PASS" if not bad else "REVIEW"))
