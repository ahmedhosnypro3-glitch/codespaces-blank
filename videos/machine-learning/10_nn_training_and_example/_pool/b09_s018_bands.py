#!/usr/bin/env python3
"""b09 s018: row-band ink extents orig vs render + eq PNG symbol check."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"

def load(p):
    im = Image.open(NS + p).convert("RGB")
    if im.size != (960, 540):
        im = im.resize((960, 540), Image.LANCZOS)
    a = np.asarray(im).astype(np.int16)
    return a, a.sum(2)

o, oe = load("unique_slides/slide_018.jpg")
r, re = load("qa/slide018/rejudge/attempt2/render-1.png")

print("== row-band ink extents (dark ink, thr 560) ==")
print(f"{'band':16s} {'orig x-range':16s} {'rnd x-range':16s} {'dx0':>4s} {'dx1':>4s}")
BANDS = [(55, 72), (72, 88), (88, 104), (104, 120), (120, 136), (136, 152),
         (152, 168), (168, 184), (184, 200), (200, 212)]
for y0, y1 in BANDS:
    ox = oe[y0:y1, 360:910] < 560
    rx = re[y0:y1, 360:910] < 560
    oxs, oxe = (360 + np.nonzero(ox.any(0))[0][0], 360 + np.nonzero(ox.any(0))[0][-1]) if ox.any() else None
    rxs, rxe = (360 + np.nonzero(rx.any(0))[0][0], 360 + np.nonzero(rx.any(0))[0][-1]) if rx.any() else None
    d0 = (oxs - rxs) if (oxs is not None and rxs is not None) else None
    d1 = (oxe - rxe) if (oxe is not None and rxe is not None) else None
    print(f"y{y0}-{y1:<10d} {str((oxs, oxe)):16s} {str((rxs, rxe)):16s} {str(d0):>4s} {str(d1):>4s}")

print("\n== column-band ink extents (dark ink, thr 560) ==")
print(f"{'band':16s} {'orig y-range':16s} {'rnd y-range':16s} {'dy0':>4s} {'dy1':>4s}")
CBANDS = [(360, 400), (400, 440), (440, 480), (480, 520), (520, 560), (560, 600),
          (600, 640), (640, 680), (680, 720), (720, 760), (760, 800), (800, 845),
          (845, 890)]
for x0, x1 in CBANDS:
    oc = oe[50:215, x0:x1] < 560
    rc = re[50:215, x0:x1] < 560
    oys, oye = (50 + np.nonzero(oc.any(1))[0][0], 50 + np.nonzero(oc.any(1))[0][-1]) if oc.any() else None
    rys, rye = (50 + np.nonzero(rc.any(1))[0][0], 50 + np.nonzero(rc.any(1))[0][-1]) if rc.any() else None
    print(f"x{x0}-{x1:<10d} {str((oys, oye)):16s} {str((rys, rye)):16s}")

print("\n== eq_s18b.png symbol check (downsample to 60 wide) ==")
eq = Image.open(NS + "recreated_pptx/build/eq_s18b.png").convert("RGBA")
eq = eq.resize((60, int(60 * eq.size[1] / eq.size[0])), Image.LANCZOS)
a = np.asarray(eq).astype(np.int16)
ink = (a[:, :, :3].sum(2) < 560) & (a[:, :, 3] > 60)
for row in ink:
    print("".join("#" if v else "." for v in row))
