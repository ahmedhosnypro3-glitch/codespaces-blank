#!/usr/bin/env python3
"""Build assets_k17r/plot_025_bl.png: patch ONLY the BL plot label texts.

- Source: live build/assets/plot_025_bl.png (md5-verified before run).
- Whiten: dark ink (text glyphs + leader-line segments) inside the label
  regions only. Red X markers / red rectangle / jet surface are untouched
  (whitening is restricted to the dark mask, and regions avoid red ink).
- Draw: 2-line labels (word1 above word2), DejaVuSans regular, black,
  centered on the authoritative frame anchors, line ink height = 6 frame px,
  band pitch = 10 frame px (measured from the original frame, probe5).
- Transform: the ACTUAL addImage placement x83 y290 w293 h237
  (asset 1220x987 -> sx=1220/293, sy=987/237). Verified by probe_k17r_bl:
  the asset's existing label clusters map onto the ground-truth anchors
  under this transform.
- Verify: diff vs source confined to the whiten regions (<5% outside,
  expect 0%); red mask identical; writes patch_k17r_bl_verify.txt.
"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = os.path.join(NS, "recreated_pptx/qa/rejudge_20261027/slide025")
SRC = os.path.join(NS, "recreated_pptx/build/assets/plot_025_bl.png")
OUTDIR = os.path.join(RJ, "assets_k17r")
OUT = os.path.join(OUTDIR, "plot_025_bl.png")
VERIFY = os.path.join(RJ, "patch_k17r_bl_verify.txt")

PX, PY, PW, PH = 83.0, 290.0, 293.0, 237.0  # addImage placement, slide px

# authoritative labels: (text, anchor frame cx, cy)
LABELS = [
    ("Global Maxima", 255, 311),
    ("Local Maxima",  300, 344),
    ("Local Minima",  298, 394),
    ("Global Minima", 173, 452),
]
# whiten regions in frame px (x0,y0,x1,y1) — the 4 label boxes + the extra
# lower-right label found in the live asset (probe4 low-R cluster)
REGIONS = [
    (225, 295, 290, 335),   # top
    (270, 325, 350, 375),   # mid-up
    (265, 370, 350, 425),   # mid-low
    (130, 425, 220, 485),   # low-L
    (285, 430, 360, 480),   # low-R extra label removal
]
REMOVE_LOW_R = os.environ.get("K17R_KEEP_LOW_R", "0") == "1"  # default: remove

LINE_H_FRAME = 6.0    # measured line ink height in the original frame
PITCH_FRAME = 10.0    # measured band pitch in the original frame

L = []
def P(s=""):
    print(s)
    L.append(s)

import hashlib
h = hashlib.md5(open(SRC, "rb").read()).hexdigest()
P("source md5=%s (expect 7a8e7210f118b728245d268552a7d32d)" % h)
if h != "7a8e7210f118b728245d268552a7d32d":
    P("CLOBBER: source asset md5 mismatch — aborting")
    sys.exit(2)

img = Image.open(SRC).convert("RGB")
W, H = img.size
sx, sy = W / PW, H / PH
P("asset %dx%d  sx=%.4f sy=%.4f" % (W, H, sx, sy))

a = np.asarray(img).astype(np.int32)
dark = (a.max(2) < 170) & ((a.max(2) - a.min(2)) < 90)
red = (a[:, :, 0] > 110) & (a[:, :, 0] - a[:, :, 1] > 50) & (a[:, :, 0] - a[:, :, 2] > 50)

def f2a(fx, fy):
    return (fx - PX) * sx, (fy - PY) * sy

# whiten regions (dark ink only)
whiten_mask = np.zeros((H, W), bool)
for (fx0, fy0, fx1, fy1) in REGIONS:
    if (fx0, fy0, fx1, fy1) == (285, 430, 360, 480) and REMOVE_LOW_R:
        pass  # still whiten; removal is the default
    ax0, ay0 = f2a(fx0, fy0)
    ax1, ay1 = f2a(fx1, fy1)
    x0, y0 = int(round(ax0)), int(round(ay0))
    x1, y1 = int(round(ax1)), int(round(ay1))
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W - 1, x1), min(H - 1, y1)
    whiten_mask[y0:y1 + 1, x0:x1 + 1] = True

# verify red ink is not inside whiten mask (markers must survive untouched)
red_in_white = int((red & whiten_mask).sum())
P("red px inside whiten mask: %d (markers/rect must be 0; if >0 those px are NOT whitened because whitening uses the dark mask only)" % red_in_white)

erase = dark & whiten_mask
P("whitening %d dark px inside label regions" % int(erase.sum()))
a[erase] = 255
img = Image.fromarray(a.astype(np.uint8))
d = ImageDraw.Draw(img)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def fit_fs(text, target_h):
    lo, hi = 8, 200
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        f = ImageFont.truetype(FONT, mid)
        im = Image.new("L", (800, 300), 0)
        ImageDraw.Draw(im).text((10, 10), text, font=f, fill=255)
        ar = np.array(im)
        ys, xs = np.nonzero(ar > 127)
        hh = ys.max() - ys.min() + 1 if len(ys) else 0
        if best is None or abs(hh - target_h) < best[0]:
            best = (abs(hh - target_h), mid, hh)
        if hh < target_h:
            lo = mid + 1
        elif hh > target_h:
            hi = mid - 1
        else:
            break
    return best[1], best[2]

line_h = LINE_H_FRAME * sy
pitch = PITCH_FRAME * sy
P("line ink height target=%.1f asset px, pitch=%.1f asset px" % (line_h, pitch))

for text, fcx, fcy in LABELS:
    ax, ay = f2a(fcx, fcy)
    words = text.split(" ", 1)
    for i, w in enumerate(words):
        fs, hh = fit_fs(w, int(round(line_h)))
        f = ImageFont.truetype(FONT, fs)
        bb = d.textbbox((0, 0), w, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        cy = ay + (i - (len(words) - 1) / 2.0) * pitch
        d.text((ax - tw / 2.0 - bb[0], cy - th / 2.0 - bb[1]), w, font=f, fill=(0, 0, 0))
        P("drew '%s' fs=%d ink_h=%d at asset (%.1f, %.1f) center (frame %.1f, %.1f)"
          % (w, fs, hh, ax - tw / 2.0, cy - th / 2.0, fcx, fcy))

os.makedirs(OUTDIR, exist_ok=True)
img.save(OUT)
P("wrote %s md5=%s" % (OUT, hashlib.md5(open(OUT, "rb").read()).hexdigest()))

# ---- verify ----
new = np.asarray(Image.open(OUT).convert("RGB")).astype(np.int32)
old = np.asarray(Image.open(SRC).convert("RGB")).astype(np.int32)
diff = (np.abs(new - old).sum(2) > 12)
outside = diff & ~whiten_mask
P("verify: changed px=%d, outside whiten regions=%d (%.4f%% of asset) -> %s"
  % (int(diff.sum()), int(outside.sum()), 100.0 * outside.sum() / diff.size,
     "PASS" if outside.sum() / max(1, diff.size) < 0.05 else "FAIL"))
red_old = (old[:, :, 0] > 110) & (old[:, :, 0] - old[:, :, 1] > 50) & (old[:, :, 0] - old[:, :, 2] > 50)
red_new = (new[:, :, 0] > 110) & (new[:, :, 0] - new[:, :, 1] > 50) & (new[:, :, 0] - new[:, :, 2] > 50)
P("red mask: old=%d new=%d symmetric-diff=%d -> %s"
  % (int(red_old.sum()), int(red_new.sum()), int((red_old ^ red_new).sum()),
     "PASS" if (red_old ^ red_new).sum() == 0 else "FAIL"))

with open(VERIFY, "w") as f:
    f.write("\n".join(L) + "\n")
print("wrote", VERIFY)
