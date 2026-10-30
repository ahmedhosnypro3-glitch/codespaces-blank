# Slide 050 L4 caption BLOCKER verification (finish worker, 2026-10-24)
# Original vs current render_4 (post-captionfix). 960x540 frame, 1px=1pt.
import numpy as np
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = Image.open(f"{DECK}/unique_slides/slide_050.jpg").convert("RGB")
REND = Image.open(f"{DECK}/recreated_pptx/qa/slide050/render_4.png").convert("RGB")
ow, oh = ORIG.size
rw, rh = REND.size
print(f"orig {ow}x{oh}  render {rw}x{rh}  scale {rw/ow:.4f} x {rh/oh:.4f}")
S = rw / ow

# Original L4 caption band (banked measurement): x240..510 y110..124
bands = {
    "L4 caption (whole)": (240, 108, 512, 126),
    "C1 word": (240, 108, 258, 126),
    "C2 word": (258, 108, 332, 126),
    "Zero word": (386, 108, 428, 126),
    "tail is unaccepted": (424, 108, 512, 126),
}

def classify(arr):
    a = arr.astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    dark = (r + g + b) < 450
    red = (r - np.maximum(g, b)) > 60
    blue = (b - np.maximum(r, g)) > 60
    green = (g - np.maximum(r, b)) > 40
    return int(dark.sum()), int(red.sum()), int(blue.sum()), int(green.sum())

for name, (x0, y0, x1, y1) in bands.items():
    oc = ORIG.crop((x0, y0, x1, y1))
    od, ored_, obl, ogr = classify(np.asarray(oc))
    # same frame region in the render, scaled
    rc = REND.crop((int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S)))
    rd, rred, rblu, rgrn = classify(np.asarray(rc))
    print(f"{name:22s} orig ink={od:5d} (red {ored_:3d} blue {obl:3d} green {ogr:3d})   "
          f"render ink={rd:5d} (red {rred:3d} blue {rblu:3d} green {rgrn:3d})")

# Full L4 band ink bbox on both
oc = np.asarray(ORIG.crop((230, 100, 540, 135)).convert("L"))
ys, xs = np.where(oc < 140)
print(f"orig L4 ink bbox: x{xs.min()+230}..{xs.max()+230} y{ys.min()+100}..{ys.max()+100} "
      f"({len(xs)} ink px)")

rg = np.asarray(REND.crop((int(230*S), int(100*S), int(540*S), int(135*S))).convert("L"))
ys2, xs2 = np.where(rg < 140)
print(f"render L4 ink bbox: x{(xs2.min()+int(230*S))/S:.0f}..{(xs2.max()+int(230*S))/S:.0f} "
      f"y{(ys2.min()+int(100*S))/S:.0f}..{(ys2.max()+int(100*S))/S:.0f} "
      f"({len(xs2)} ink px @150dpi)")

# Green ink check in original (Zero word) — banked said 183/183 green px at x394..423
ocg = np.asarray(ORIG.crop((394, 108, 424, 126)))
a = ocg.astype(int)
dark = (a.sum(axis=2) < 450)
green = (a[..., 1] - np.maximum(a[..., 0], a[..., 2])) > 40
print(f"orig 'Zero' band x394..424 y108..126: dark={int(dark.sum())} green={int((dark&green).sum())}")

# Old placeholder position (x266..466 y112..125) — confirm render_4 no longer has it?
# (render_4 was rebuilt, so instead verify caption present: count dark pixels across band)
