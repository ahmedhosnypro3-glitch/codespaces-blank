#!/usr/bin/env python3
"""Adjudication of the gateway full-slide FAIL (attempt 5 rootw009):
finding 1 — LEFT-panel highlighted marker size (original: small red dot; render: large disc)
finding 2 — nested/double chart frame in the render.
Ground truth = PIL measurement on BOTH images, frame px (1px=1pt)."""
import numpy as np
from collections import deque
from PIL import Image

Q = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(np.int16)
rnd = np.asarray(Image.open(f"{Q}/render_5.png").convert("RGB")).astype(np.int16)
SX = rnd.shape[1] / 960.0; SY = rnd.shape[0] / 540.0


def near(a, rgb, tol):
    return (np.abs(a - np.array(rgb)).max(axis=2) <= tol)


def blob_bbox(mask, min_px=20):
    ys, xs = np.nonzero(mask)
    if len(xs) < min_px:
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(xs))


# The highlighted marker lives on the blue fit line near (233,241) frame px, LEFT chart.
# Red family (C00000 and its desaturated kin: R>=120, G<=110, B<=110, R-G>=60).
def redfam(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r - g > 50) & (r > 110) & (g < 120) & (b < 120)


# orange family for dot-size reference
def orangefam(a):
    return near(a, (255, 165, 0), 60)


def measure(img, sx, sy, tag, disc_center):
    cx, cy = disc_center
    x0, y0, x1, y1 = int((cx - 60) * sx), int((cy - 60) * sy), int((cx + 60) * sx), int((cy + 60) * sy)
    red = redfam(img)[y0:y1, x0:x1]
    # largest red blob in the window = the highlighted marker
    seen = np.zeros_like(red, bool); best = None
    H, W = red.shape
    for i in range(H):
        for j in range(W):
            if red[i, j] and not seen[i, j]:
                q = deque([(i, j)]); seen[i, j] = True; pts = []
                while q:
                    a, b = q.popleft(); pts.append((a, b))
                    for da in (-1, 0, 1):
                        for db in (-1, 0, 1):
                            na, nb = a + da, b + db
                            if 0 <= na < H and 0 <= nb < W and red[na, nb] and not seen[na, nb]:
                                seen[na, nb] = True; q.append((na, nb))
                if len(pts) >= 30 and (best is None or len(pts) > best[0]):
                    xs = [p[1] for p in pts]; ys = [p[0] for p in pts]
                    best = (len(pts), (min(xs) + x0, min(ys) + y0, max(xs) + x0, max(ys) + y0))
    # an orange dot in the same window (reference scale)
    orn = orangefam(img)[y0:y1, x0:x1]
    ob = blob_bbox(orn, 30)
    if best:
        n, bb = best
        w = (bb[2] - bb[0] + 1) / sx; h = (bb[3] - bb[1] + 1) / sy
        ow = (ob[2] - ob[0] + 1) / sx if ob else None
        oh = (ob[3] - ob[1] + 1) / sy if ob else None
        print(f"[{tag}] marker blob: n={n} bbox={bb} frame-size {w:.1f}x{h:.1f} (diam ~{(w+h)/2:.1f}) ; "
              f"orange dot frame-size {ow:.1f}x{oh:.1f} (diam ~{((ow+oh)/2):.1f})" if ob else f"[{tag}] marker {w:.1f}x{h:.1f}, no orange dot in window")
    else:
        print(f"[{tag}] NO red marker blob found in window")


print("== highlighted marker near the dimension foot (LEFT chart, frame ~(233,241)) ==")
measure(orig, 1.0, 1.0, "original", (233, 241))
measure(rnd, SX, SY, "render_5", (233, 241))
print("== reference: an isolated orange dot, LEFT chart upper area (frame ~(197,144)) ==")
measure(orig, 1.0, 1.0, "orig-orange", (197, 144))
measure(rnd, SX, SY, "rnd-orange", (197, 144))

print("\n== chart frame border counting (nested frame check) ==")
# LEFT chart border expected at frame x95..466, y107..474. Scan a vertical strip at x=93..97
# (just left of the border) and the border column; count navy stroke groups.
navy_o = near(orig, (0, 0, 128), 90)
navy_r = near(rnd, (0, 0, 128), 90)


def border_cols(img, sx, sy, y0f, y1f, x0f, x1f, tag):
    sub = img[int(y0f*sy):int(y1f*sy), int(x0f*sx):int(x1f*sx)]
    navy = near(sub, (0, 0, 128), 90)
    colhas = navy.sum(axis=0)
    # count contiguous groups of columns carrying navy
    groups = 0; inb = False
    for c in colhas:
        if c > 3 and not inb:
            groups += 1; inb = True
        elif c <= 3:
            inb = False
    print(f"[{tag}] vertical stroke groups in x{x0f}..{x1f}: {groups} "
          f"(col profile: " + ",".join(f"{x0f + i/sx:.1f}:{int(c)}" for i, c in enumerate(colhas) if c > 3) + ")")


border_cols(orig, 1.0, 1.0, 110, 470, 90, 100, "original LEFT border")
border_cols(rnd, SX, SY, 110, 470, 90, 100, "render LEFT border")
print("== same for the RIGHT chart (expected border x486..872) ==")
border_cols(orig, 1.0, 1.0, 110, 470, 481, 491, "original RIGHT border")
border_cols(rnd, SX, SY, 110, 470, 481, 491, "render RIGHT border")
