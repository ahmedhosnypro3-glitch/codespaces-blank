#!/usr/bin/env python3
"""Read-only PIL probe of the LIVE build/assets/plot_025_bl.png (k17g-promoted).

Locates dark text clusters, maps them to slide px via the actual addImage
placement (x83 y290 w293 h237), and template-identifies each cluster against
the four candidate label strings. Also reports where the task's anchor centers
land under BOTH transforms so the patch can pick the verified one.
Writes probe_k17r_bl.txt + probe_k17r_bl_crops.png. Never writes build files.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = os.path.join(NS, "recreated_pptx/qa/rejudge_20261027/slide025")
ASSET = os.path.join(NS, "recreated_pptx/build/assets/plot_025_bl.png")
OUT = os.path.join(RJ, "probe_k17r_bl.txt")

# actual placement from build/slide_025.js addImage: x83 y290 w293 h237 (slide px=pt)
PX, PY, PW, PH = 83.0, 290.0, 293.0, 237.0
# task-recipe transform: region x60..470 y296..527 (411x231), scale=asset_w/411
TX, TY, TW = 60.0, 296.0, 411.0

ANCHORS = [  # frame px centers, authoritative ground truth
    ("Global Maxima", 255, 311),
    ("Local Maxima", 300, 344),
    ("Local Minima", 298, 394),
    ("Global Minima", 173, 452),
]

L = []
def P(s=""):
    print(s)
    L.append(s)

img = Image.open(ASSET).convert("RGB")
W, H = img.size
a = np.asarray(img).astype(np.int32)
P("asset %s size=%dx%d" % (ASSET, W, H))
sx, sy = W / PW, H / PH
P("placement transform: slide = (%g + ax/%.4f, %g + ay/%.4f); task transform scale=%.4f"
  % (PX, sx, PY, sy, W / TW))

for name, fx, fy in ANCHORS:
    P("anchor %-14s frame(%d,%d) -> asset placement (%.1f, %.1f) | task (%.1f, %.1f)"
      % (name, fx, fy, (fx - PX) * sx, (fy - PY) * sy, (fx - TX) * (W / TW), (fy - TY) * (W / TW)))

dark = (a.max(2) < 145) & ((a.max(2) - a.min(2)) < 80)
lab, n = ndimage.label(dark, structure=np.ones((3, 3)))
comps = []
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) >= 40:
        comps.append((len(xs), xs.min(), ys.min(), xs.max(), ys.max()))
comps.sort(key=lambda c: -c[0])
P("\ndark comps area>=40: %d (top 25 by area)" % len(comps))
for c in comps[:25]:
    area, x0, y0, x1, y1 = c
    P("  area=%5d asset x%d..%d y%d..%d  slide-center=(%.0f, %.0f) size asset %dx%d"
      % (area, x0, x1, y0, y1, PX + (x0 + x1) / 2 / sx, PY + (y0 + y1) / 2 / sy,
         x1 - x0 + 1, y1 - y0 + 1))

# template identity for each candidate string, single-line, regular + bold
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CANDS = ["Global Maxima", "Local Maxima", "Local Minima", "Global Minima"]

def render(s, fontpath, fs):
    f = ImageFont.truetype(fontpath, fs)
    im = Image.new("L", (600, 160), 255)
    ImageDraw.Draw(im).text((10, 10), s, font=f, fill=0)
    ar = np.array(im)
    ys, xs = np.nonzero(ar < 128)
    return ar[ys.min():ys.max() + 1, xs.min():xs.max() + 1] < 128

def identify(win):
    dm = (win.max(2) < 145) & ((win.max(2) - win.min(2)) < 80)
    if not dm.any():
        return (-1.0, "?")
    ys, xs = np.nonzero(dm)
    crop = dm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    best = (-2.0, "?")
    for s in CANDS:
        for fp in (FONT_R, FONT_B):
            for fs in range(20, 130, 4):
                c = render(s, fp, fs)
                cr = np.array(Image.fromarray((c * 255).astype(np.uint8))
                              .resize((crop.shape[1], crop.shape[0]), Image.BILINEAR)) > 127
                inter = (cr & crop).sum()
                union = (cr | crop).sum()
                v = float(inter) / union if union else -1.0
                if v > best[0]:
                    best = (v, s)
    return best

# focus windows: generous boxes around each anchor under the PLACEMENT transform
P("\nper-anchor cluster identification (placement-transform windows, asset res):")
crops = []
for name, fx, fy in ANCHORS:
    ax = (fx - PX) * sx
    ay = (fy - PY) * sy
    wx0, wy0 = int(ax - 130), int(ay - 60)
    wx1, wy1 = int(ax + 130), int(ay + 60)
    wx0, wy0 = max(0, wx0), max(0, wy0)
    wx1, wy1 = min(W - 1, wx1), min(H - 1, wy1)
    win = a[wy0:wy1 + 1, wx0:wx1 + 1]
    dm = (win.max(2) < 145) & ((win.max(2) - win.min(2)) < 80)
    ink = int(dm.sum())
    v, got = identify(win)
    P("  %-14s anchor frame(%d,%d) asset(%.0f,%.0f) window x%d..%d y%d..%d ink=%d id='%s' IoU=%.2f"
      % (name, fx, fy, ax, ay, wx0, wx1, wy0, wy1, ink, got, v))
    if ink:
        ys, xs = np.nonzero(dm)
        P("     ink bbox in window: x%d..%d y%d..%d -> asset x%d..%d y%d..%d -> slide x%.1f..%.1f y%.1f..%.1f"
          % (xs.min(), xs.max(), ys.min(), ys.max(),
             wx0 + xs.min(), wx0 + xs.max(), wy0 + ys.min(), wy0 + ys.max(),
             PX + (wx0 + xs.min()) / sx, PX + (wx0 + xs.max()) / sx,
             PY + (wy0 + ys.min()) / sy, PY + (wy0 + ys.max()) / sy))
    crop = Image.fromarray(win.astype(np.uint8)).resize(((wx1 - wx0) * 3, (wy1 - wy0) * 3), Image.LANCZOS)
    crops.append((name, crop))

# contact sheet
cw = max(c.width for _, c in crops)
ch = sum(c.height for _, c in crops) + 10 * len(crops)
sheet = Image.new("RGB", (cw + 160, ch), (255, 255, 0))
y = 0
d = ImageDraw.Draw(sheet)
for name, c in crops:
    d.text((5, y + 5), name, fill=(255, 0, 0))
    sheet.paste(c, (160, y))
    y += c.height + 10
sheet.save(os.path.join(RJ, "probe_k17r_bl_crops.png"))
P("\ncrops sheet: probe_k17r_bl_crops.png")

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
print("wrote", OUT)
