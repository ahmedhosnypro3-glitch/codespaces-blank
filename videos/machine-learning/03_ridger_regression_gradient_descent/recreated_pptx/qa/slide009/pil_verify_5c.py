#!/usr/bin/env python3
"""Slide 009 verification, part 3 (corrected scales) + crop re-cut.
SX = render_w/960 = 2.084375, SY = render_h/540 = 2.083333 (16:9 frame).
Crops follow the protocol: render crop = frame coords x scale; original crop
LANCZOS-resized to the render crop's exact size (matched effective scale by construction)."""
import numpy as np
from collections import deque
from PIL import Image

Q = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"

orig_im = Image.open(ORIG).convert("RGB")
orig = np.asarray(orig_im).astype(np.int16)
r3_im = Image.open(f"{Q}/render_3.png").convert("RGB")
r4_im = Image.open(f"{Q}/render_4.png").convert("RGB")
r5_im = Image.open(f"{Q}/render_5.png").convert("RGB")
rnd = np.asarray(r5_im).astype(np.int16)
SX = r5_im.width / 960.0
SY = r5_im.height / 540.0
print(f"SX={SX:.6f} SY={SY:.6f} render={r5_im.size}")


def near(a, rgb, tol):
    return (np.abs(a - np.array(rgb)).max(axis=2) <= tol)


def blobs(mask, min_px):
    seen = np.zeros_like(mask, dtype=bool); out = []
    H, W = mask.shape
    for i in range(H):
        for j in range(W):
            if mask[i, j] and not seen[i, j]:
                q = deque([(i, j)]); seen[i, j] = True; n = 0
                x0 = y0 = 10**9; x1 = y1 = -1
                while q:
                    a, b = q.popleft(); n += 1
                    x0 = min(x0, b); y0 = min(y0, a); x1 = max(x1, b); y1 = max(y1, a)
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            na, nb = a + da, b + db
                            if 0 <= na < H and 0 <= nb < W and mask[na, nb] and not seen[na, nb]:
                                seen[na, nb] = True; q.append((na, nb))
                if n >= min_px:
                    out.append((n, (x0, y0, x1, y1)))
    return sorted(out, reverse=True)


# ---- 1. chart frames: navy borders, expect frame x95..466 / x486..872, y107..474 ----
navy_r = near(rnd, (0, 0, 128), 70)
print("== render navy components (frame px) ==")
for a, bb in blobs(navy_r, 3000)[:4]:
    print(f"   area={a:7d} frame=({bb[0]/SX:.1f},{bb[1]/SY:.1f},{bb[2]/SX:.1f},{bb[3]/SY:.1f})")

# ---- 2. equation boxes: pale-cyan fill, frame y148..175, x216..317 / x631..734 ----
CYAN = (0xEC, 0xFD, 0xF9)
print("== render pale-cyan components (frame px) ==")
cyan_render = []
for a, bb in blobs(near(rnd, CYAN, 10), 2000):
    f = (bb[0]/SX, bb[1]/SY, bb[2]/SX, bb[3]/SY)
    if 140 < f[1] < 185:  # the equation-box row
        cyan_render.append((a, bb, f))
        print(f"   area={a:7d} render={bb} frame=({f[0]:.1f},{f[1]:.1f},{f[2]:.1f},{f[3]:.1f})")
print("== original pale-cyan components (frame px) ==")
cyan_orig = []
for a, bb in blobs(near(orig, CYAN, 10), 800):
    f = (float(bb[0]), float(bb[1]), float(bb[2]), float(bb[3]))
    if 140 < f[1] < 185 and f[2]-f[0] < 130:
        cyan_orig.append((a, bb, f))
        print(f"   area={a:7d} frame=({f[0]:.1f},{f[1]:.1f},{f[2]:.1f},{f[3]:.1f})")

# glyph ink inside each equation box (dark mask, interior only)
def glyphs_in(img_arr, box, sx, sy, tag):
    x0, y0, x1, y1 = box
    ix0, iy0, ix1, iy1 = int(round(x0*sx)), int(round(y0*sy)), int(round(x1*sx)), int(round(y1*sy))
    sub = img_arr[iy0:iy1+1, ix0:ix1+1]
    dark = (sub.sum(axis=2) < 420)
    p = 2
    inner = dark[p:dark.shape[0]-p, p:dark.shape[1]-p]
    ys, xs = np.nonzero(inner)
    if not len(xs):
        print(f"   [{tag}] NO dark ink inside box -> BLOCKER"); return None
    gb = ((xs.min()+p+ix0)/sx, (ys.min()+p+iy0)/sy, (xs.max()+p+ix0)/sx, (ys.max()+p+iy0)/sy)
    pads = (gb[0]-x0, x1-gb[2], gb[1]-y0, y1-gb[3])
    print(f"   [{tag}] glyph bbox frame=({gb[0]:.1f},{gb[1]:.1f},{gb[2]:.1f},{gb[3]:.1f}) "
          f"pad L/R/T/B={pads[0]:.1f}/{pads[1]:.1f}/{pads[2]:.1f}/{pads[3]:.1f}  "
          f"{'OK all>0' if min(pads) > 0 else 'TOUCH!'}")
    return gb

print("== glyph containment in equation boxes ==")
for a, bb, f in cyan_render:
    glyphs_in(rnd, f, SX, SY, f"render {f[0]:.0f}")
for a, bb, f in cyan_orig:
    glyphs_in(orig, bb, 1.0, 1.0, f"orig x{bb[0]}")

# ---- 3. caption boxes: cream FBFCEC, frame y479..529, x95..434 / x501..842 ----
CREAM = (0xFB, 0xFC, 0xEC)
print("== render cream components (frame px) ==")
for a, bb in blobs(near(rnd, CREAM, 6), 3000)[:5]:
    print(f"   area={a:7d} frame=({bb[0]/SX:.1f},{bb[1]/SY:.1f},{bb[2]/SX:.1f},{bb[3]/SY:.1f})")
print("== original cream components (frame px) ==")
for a, bb in blobs(near(orig, CREAM, 6), 1000)[:5]:
    print(f"   area={a:7d} frame=({bb[0]:.1f},{bb[1]:.1f},{bb[2]:.1f},{bb[3]:.1f})")

# ---- 4. frame containment: no content ink outside house panel x54..903 y45..540 ----
ink_r = rnd.sum(axis=2) < 680
ink_r[:, :int(54*SX)] = False; ink_r[:, int(903*SX):] = False; ink_r[:int(45*SY), :] = False
print(f"[containment] content ink outside house panel = {int(ink_r.sum())} px (must be 0)")

# ---- 5. re-cut crop pairs at CORRECT scale; redo cross-build diffs ----
REGIONS = {
    "eq_left":    (208, 138, 327, 185),
    "eq_right":   (623, 138, 744, 185),
    "cap_left":   (85, 469, 444, 539),
    "cap_right":  (491, 469, 852, 539),
    "chart_left": (85, 97, 476, 484),
    "chart_right":(476, 97, 881, 484),
}


def rcrop(im, box):
    x0, y0, x1, y1 = box
    return im.crop((int(round(x0*SX)), int(round(y0*SY)), int(round(x1*SX)), int(round(y1*SY))))


print("\n== crop re-cut (correct scale) + cross-build diffs ==")
lines = []
for name, box in REGIONS.items():
    rc = rcrop(r5_im, box)
    oc = orig_im.crop(box).resize(rc.size, Image.LANCZOS)
    rc.save(f"{Q}/crop_5_{name}_render.png")
    oc.save(f"{Q}/crop_5_{name}_orig.png")
    a1 = np.asarray(rcrop(r3_im, box)).astype(np.int16)
    a2 = np.asarray(rcrop(r4_im, box)).astype(np.int16)
    a3 = np.asarray(rc).astype(np.int16)
    d34 = int((np.abs(a1-a3).max(axis=2) > 12).sum())
    d45 = int((np.abs(a2-a3).max(axis=2) > 12).sum())
    l = (f"{name}: box={box} render_crop={rc.size} orig_crop={oc.size} "
         f"eff_scale={oc.size[0]/(box[2]-box[0]):.4f}/{oc.size[1]/(box[3]-box[1]):.4f} "
         f"diff r3->r5={d34} r4->r5={d45}")
    lines.append(l); print("   " + l)
with open(f"{Q}/crossbuild_diff_5.txt", "w") as f:
    f.write("region diffs (correct scales), threshold >12/255 max-channel, render px\n")
    f.write("a region with diff 0 in BOTH comparisons keeps its crop_3 certificate\n")
    for l in lines:
        f.write(l + "\n")
print("VERIFY3 DONE")
