#!/usr/bin/env python3
"""PIL verification of slide 045 straight delimiter bars + re-laid triplet digits.
Expected geometry from locked measurements (frame px, render scale 2.0833 at 150dpi).
Runs on the NEW render; prints per-check PASS/FAIL, exits 1 on any FAIL."""
import sys
from PIL import Image

RENDER = sys.argv[1] if len(sys.argv) > 1 else "scratch/tmp/delimchk/r045_new.png"
S = 2.0833                      # frame px -> 150dpi render px
BANDS = [140, 207, 272, 338, 404, 470]
DCY_OFF = 13.2                  # digit line cy = band_top + 13.2
CX = [334.7, 352.6, 370.7]      # measured digit centroids
BAR_L, BAR_R = 329.0, 375.0     # rect x of ( and ) bars
TOL = 5.0                       # render px

im = Image.open(RENDER).convert("RGB")
W, H = im.size
pix = im.load()

def ink_rows(x0, x1, y0, y1, thresh=220):
    ys = [y for y in range(max(0, int(y0)), min(H, int(y1) + 1))
          if any(sum(pix[x, y]) / 3 < thresh for x in range(int(x0), int(x1) + 1))]
    return (min(ys), max(ys)) if ys else None

def blue_centroid(x0, x1, y0, y1):
    pts = [(x, y) for y in range(max(0, int(y0)), min(H, int(y1) + 1))
           for x in range(max(0, int(x0)), min(W, int(x1) + 1))
           if (lambda p: p[2] > p[0] + 30 and p[2] > p[1] + 30 and sum(p) / 3 < 230)(pix[x, y])]
    if not pts:
        return None
    n = len(pts)
    return (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n, n)

fails = 0
for b in BANDS:
    for tag, bx, y_off, hh in (("(", BAR_L, 7, 13), (")", BAR_R, 8, 12)):
        m = ink_rows((bx - 1.5) * S, (bx + 2.5) * S, (b + y_off - 6) * S, (b + y_off + hh + 6) * S)
        exp_c = (b + y_off + hh / 2.0) * S
        if m is None:
            print(f"FAIL b={b} {tag}: NO INK"); fails += 1
        else:
            mc = (m[0] + m[1]) / 2.0
            ok = abs(mc - exp_c) <= TOL
            print(f"{'PASS' if ok else 'FAIL'} b={b} {tag}: ink y {m[0]}..{m[1]} center {mc:.1f} vs exp {exp_c:.1f}")
            fails += 0 if ok else 1
    dcy = (b + DCY_OFF) * S
    for k, cx in enumerate(CX):
        c = blue_centroid((cx - 8) * S, (cx + 8) * S, dcy - 9 * S, dcy + 9 * S)
        if c is None:
            print(f"FAIL b={b} digit{k}: NO BLUE INK"); fails += 1
        else:
            ok = abs(c[0] - cx * S) <= TOL and abs(c[1] - dcy) <= TOL
            print(f"{'PASS' if ok else 'FAIL'} b={b} digit{k}: centroid ({c[0]:.1f},{c[1]:.1f}) n={c[2]} vs exp ({cx*S:.1f},{dcy:.1f})")
            fails += 0 if ok else 1
    # old text-line position must now be empty (x 340..370, y b+22..b+36: below the
    # new digits' bottoms b+21, above/around the old line center b+27)
    m = ink_rows(340 * S, 370 * S, (b + 22) * S, (b + 36) * S)
    if m is not None:
        print(f"FAIL b={b}: residual ink at old text line y {m[0]}..{m[1]}"); fails += 1
    else:
        print(f"PASS b={b}: old text-line position clear")
print("EXIT " + ("FAIL" if fails else "PASS") + f" ({fails} failures)")
sys.exit(1 if fails else 0)
