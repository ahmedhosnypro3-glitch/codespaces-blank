#!/usr/bin/env python3
"""Slide 009 verification, part 2: LOCATE the equation boxes and the top-band red ink
instead of trusting asserted coordinates. Ground truth = colour segmentation on both
images. Frame 960x540 (1px=1pt); render_5 150dpi scale 2.08333."""
import numpy as np
from collections import deque
from PIL import Image

Q = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
S = 2001 / 540.0

orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(np.int16)
rnd = np.asarray(Image.open(f"{Q}/render_5.png").convert("RGB")).astype(np.int16)


def near(a, rgb, tol):
    return (np.abs(a - np.array(rgb)).max(axis=2) <= tol)


def blobs(mask, min_px=200):
    """connected components (8-conn) -> list of (area, bbox)"""
    seen = np.zeros_like(mask, dtype=bool); out = []
    H, W = mask.shape
    for i in range(H):
        for j in range(W):
            if mask[i, j] and not seen[i, j]:
                q = deque([(i, j)]); seen[i, j] = True; pts = []
                while q:
                    a, b = q.popleft(); pts.append((a, b))
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            na, nb = a + da, b + db
                            if 0 <= na < H and 0 <= nb < W and mask[na, nb] and not seen[na, nb]:
                                seen[na, nb] = True; q.append((na, nb))
                if len(pts) >= min_px:
                    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                    out.append((len(pts), (min(xs), min(ys), max(xs), max(ys))))
    return sorted(out, reverse=True)


CYAN = (0xEC, 0xFD, 0xF9)
print("== pale-cyan ECFDF9 fill regions (equation boxes) ==")
print("-- render_5 (coords shown in frame px) --")
for a, bb in blobs(near(rnd, CYAN, 12), 500)[:8]:
    print(f"   area={a:7d} bbox_render={bb} frame=({bb[0]/S:.1f},{bb[1]/S:.1f},{bb[2]/S:.1f},{bb[3]/S:.1f})")
print("-- original --")
for a, bb in blobs(near(orig, CYAN, 12), 200)[:8]:
    print(f"   area={a:7d} bbox_frame={bb}")

print("\n== navy-bordered rect components near each cyan box (render) ==")
navy_r = near(rnd, (0, 0, 128), 60)
for a, bb in blobs(navy_r, 400)[:6]:
    print(f"   area={a:7d} bbox_render={bb} frame=({bb[0]/S:.1f},{bb[1]/S:.1f},{bb[2]/S:.1f},{bb[3]/S:.1f})")

print("\n== red C00000-family ink in render TOP band (frame y<40) ==")
red_r = near(rnd, (192, 0, 0), 40)
top = red_r[:150, :]
ys, xs = np.nonzero(top)
if len(xs):
    print(f"   count={len(xs)} bbox_render=({xs.min()},{ys.min()},{xs.max()},{ys.max()}) frame=({xs.min()/S:.1f},{ys.min()/S:.1f},{xs.max()/S:.1f},{ys.max()/S:.1f})")
else:
    print("   none")
print("== same band, original ==")
redo = near(orig, (192, 0, 0), 40)
t2 = redo[:40, :]
ys, xs = np.nonzero(t2)
print(f"   count={len(xs) if len(xs) else 0}")

print("\n== dark glyph ink INSIDE each located cyan box, padding vs box edges ==")


def glyph_pad(img, box_img, box_bb, scale, tag):
    x0, y0, x1, y1 = box_bb
    pad = 2
    sub = img[max(0, y0 - pad):y1 + pad + 1, max(0, x0 - pad):x1 + pad + 1]
    dark = (sub.sum(axis=2) < 420)
    # exclude the border: erode box interior check — use only pixels >=2px inside the box
    inner = dark[pad + 2:dark.shape[0] - pad - 2, pad + 2:dark.shape[1] - pad - 2]
    ys, xs = np.nonzero(inner)
    if not len(xs):
        print(f"   [{tag}] NO dark ink inside box (BLOCKER if box should hold an equation)")
        return
    gb = (xs.min() + max(0, x0 - pad) + pad + 2, ys.min() + max(0, y0 - pad) + pad + 2,
          xs.max() + max(0, x0 - pad) + pad + 2, ys.max() + max(0, y0 - pad) + pad + 2)
    pl, pr, pt, pb = gb[0] - x0, x1 - gb[2], gb[1] - y0, y1 - gb[3]
    print(f"   [{tag}] glyph bbox={gb} frame=({gb[0]/scale:.1f},{gb[1]/scale:.1f},{gb[2]/scale:.1f},{gb[3]/scale:.1f}) pad L/R/T/B={pl/scale:.1f}/{pr/scale:.1f}/{pt/scale:.1f}/{pb/scale:.1f} frame-px")


for a, bb in blobs(near(rnd, CYAN, 12), 500)[:4]:
    glyph_pad(rnd, rnd, bb, S, f"render box {bb}")
for a, bb in blobs(near(orig, CYAN, 12), 200)[:4]:
    glyph_pad(orig, orig, bb, 1.0, f"orig box {bb}")

print("\n== caption boxes (cream FBFCEC fill) locations ==")
CREAM = (0xFB, 0xFC, 0xEC)
for a, bb in blobs(near(rnd, CREAM, 8), 2000)[:4]:
    print(f"   render area={a} frame=({bb[0]/S:.1f},{bb[1]/S:.1f},{bb[2]/S:.1f},{bb[3]/S:.1f})")
for a, bb in blobs(near(orig, CREAM, 8), 2000)[:4]:
    print(f"   orig  area={a} frame={bb}")
print("VERIFY2 DONE")
