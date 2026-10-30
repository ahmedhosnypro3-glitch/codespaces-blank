#!/usr/bin/env python3
"""Self-check attempt 1 for slide 022 (pre-judge, mandatory).

Runs the SAME red-ink predicates on the 150dpi render and the original frame
(identical windows on BOTH images — JPEG/AA halo cancels), then compares the
render's title bands against the frame-measured targets:
  L1 '[3] Inverse of High Dimension' ink x 189..726, y 235..274 (center 457.5,254.5)
  L2 '(non-singular) Matrix'        ink x 274..652, y 325..364 (center 463.0,344.5)
Also: full-render ink census (only badge+L1+L2 may exist), frame containment
(no ink outside panel edges / no wrap spill below L2 / one band per element),
and text core color.
Render: 2001x1125 -> frame px via / (2001/960) on x, / (1125/540) on y.
"""
import sys
import numpy as np
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide022/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_022.jpg"

ren = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
ori = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
RH, RW = ren.shape[:2]
SX, SY = RW / 960.0, RH / 540.0  # render px per frame px
print(f"render {RW}x{RH}  scale x={SX:.4f} y={SY:.4f}")

TARGETS = {  # frame px, measured from the original (inclusive halo bboxes)
    "L1": {"x0": 189, "x1": 726, "y0": 235, "y1": 274},
    "L2": {"x0": 274, "x1": 652, "y0": 325, "y1": 364},
}

def red_mask(img, title_zone=True):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
    z = np.zeros_like(red)
    # frame-px title zone x 70..895, y 60..500 (excludes chrome strokes+badge)
    z[int(60 * (img.shape[0] / 540)):int(500 * (img.shape[0] / 540)),
      int(70 * (img.shape[1] / 960)):int(895 * (img.shape[1] / 960))] = True
    return red & z

def band_of(mask):
    rows = np.where(mask.sum(axis=1) > 2)[0]
    if not len(rows):
        return None
    y0, y1 = rows.min(), rows.max()
    xs = np.where(mask.any(axis=0))[0]
    return {"x0": xs.min(), "x1": xs.max(), "y0": y0, "y1": y1}

fails = []

# original bands (re-derive with THIS script's own windows; must reproduce the
# build-header targets)
omask = red_mask(ori)
obands = {}
rows = np.where(omask.sum(axis=1) > 2)[0]
groups = np.split(rows, np.where(np.diff(rows) > 6)[0] + 1) if len(rows) else []
for i, gr in enumerate(groups):
    b = band_of(omask[gr.min():gr.max() + 1])
    b["y0"], b["y1"] = gr.min(), gr.max()
    obands[f"orig_band_{i}"] = b
    print(f"orig band {i}: y {b['y0']}..{b['y1']}, x {b['x0']}..{b['x1']} (w {b['x1']-b['x0']+1})")

# render bands -> frame px
rmask = red_mask(ren)
rbands = {}
rows = np.where(rmask.sum(axis=1) > 2)[0]
groups = np.split(rows, np.where(np.diff(rows) > 6)[0] + 1) if len(rows) else []
if len(groups) != 2:
    fails.append(f"render has {len(groups)} red title bands (expected 2)")
for i, gr in enumerate(groups):
    b = band_of(rmask[gr.min():gr.max() + 1])
    b["y0"], b["y1"] = gr.min(), gr.max()
    rbands[f"render_band_{i}"] = b
    f = {k: (v / (SX if k[0] == "x" else SY)) for k, v in b.items()}
    print(f"render band {i}: y {b['y0']}..{b['y1']}, x {b['x0']}..{b['x1']} "
          f"=> frame px y {f['y0']:.1f}..{f['y1']:.1f}, x {f['x0']:.1f}..{f['x1']:.1f} "
          f"(w {f['x1']-f['x0']:.1f})")

TOL = 4  # render px at 150dpi per pipeline standard; report frame-px residuals too
for name, tgt in TARGETS.items():
    i = 0 if name == "L1" else 1
    rb = rbands.get(f"render_band_{i}")
    if rb is None:
        fails.append(f"{name}: no render band")
        continue
    f = {k: v / (SX if k[0] == "x" else SY) for k, v in rb.items()}
    for edge in ("x0", "x1", "y0", "y1"):
        resid = f[edge] - tgt[edge]
        status = "OK" if abs(resid) <= 2.0 else "FIX"
        print(f"{name} {edge}: frame {f[edge]:.1f} vs target {tgt[edge]} -> residual {resid:+.1f} frame px  [{status}]")
        if abs(resid) > 2.0:
            fails.append(f"{name} {edge} residual {resid:+.1f} frame px")
    cx = (f["x0"] + f["x1"]) / 2
    cy = (f["y0"] + f["y1"]) / 2
    print(f"{name} center ({cx:.1f},{cy:.1f}); pitch check next")
cys = []
for i in (0, 1):
    rb = rbands.get(f"render_band_{i}")
    if rb:
        cys.append((rb["y0"] + rb["y1"]) / 2 / SY)
if len(cys) == 2:
    pitch = cys[1] - cys[0]
    print(f"band pitch: {pitch:.1f} frame px (target 90.0)")
    if abs(pitch - 90) > 2:
        fails.append(f"pitch {pitch:.1f} vs 90")

# containment: NO red ink anywhere in the title zone outside the two bands, and
# no ink (any color) below y=380 frame px inside the panel, none between bands
gap = rmask[int(285 * SY):int(320 * SY), :]
if gap.sum() > 0:
    fails.append(f"red ink between title bands ({gap.sum()} px) — unexpected element")
below = rmask[int(380 * SY):int(520 * SY), :]
if below.sum() > 0:
    fails.append(f"red ink below L2 band ({below.sum()} px) — wrap spill / stray element")
above = rmask[int(60 * SY):int(228 * SY), :]
if above.sum() > 0:
    fails.append(f"red ink above L1 band ({above.sum()} px) — unexpected element")

# non-red ink census inside the panel (should be ONLY the badge cluster ~y54..94)
BG = np.array([233, 233, 231])
panel = ren[int(50 * SY):int(530 * SY), int(66 * SX):int(894 * SX)]
d = np.abs(panel - BG).max(axis=2)
nonred = (d > 18) & ~((panel[:, :, 0] > 90) & ((panel[:, :, 0] - panel[:, :, 1]) > 40) & ((panel[:, :, 0] - panel[:, :, 2]) > 10))
if nonred.sum():
    ys, xs = np.where(nonred)
    print(f"non-red panel ink: {nonred.sum()} px, x {66+xs.min()/SX:.0f}..{66+xs.max()/SX:.0f}, y {50+ys.min()/SY:.0f}..{50+ys.max()/SY:.0f} (frame px)")
else:
    print("non-red panel ink: 0 px")

# core color of rendered text
core = ren[rmask]
if len(core):
    dk = core[core.sum(axis=1).argmin()]
    print(f"render title core color: darkest {tuple(dk)}, median strong {tuple(np.median(core[core[:,0]>150],axis=0).astype(int))}")

print()
if fails:
    print("SELFCHECK: FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELFCHECK: PASS — all band edges within 2.0 frame px, census/containment clean")
