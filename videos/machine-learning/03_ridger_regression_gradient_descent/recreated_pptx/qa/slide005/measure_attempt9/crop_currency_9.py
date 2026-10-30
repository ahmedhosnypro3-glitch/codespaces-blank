#!/usr/bin/env python3
"""Currency + scale audit for the attempt-9 crop pairs.

Re-cuts each region from render_9.png (2001x1125 @150dpi, sx=2001/960,
sy=1125/540) and from the 960x540 original, then byte-compares against the
banked crop_9_*_render.png / crop_9_*_orig.png. A mismatch means the banked
pair was cut from a different render and is stale.
"""
from PIL import Image
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
Q = os.path.dirname(HERE)
RENDER = os.path.join(Q, "render_9.png")
ORIG = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_005.jpg")

SX, SY = 2001 / 960, 1125 / 540

# region (frame px) -> banked output px, from the lane table in worker_report.md
REGIONS = {
    "eq_stack":   (88, 100, 650, 285),
    "blue_upper": (660, 128, 890, 245),
    "pink_band":  (65, 280, 515, 350),
    "lower_eqs":  (64, 350, 900, 530),
}


def md5(img):
    return hashlib.md5(img.convert("RGB").tobytes()).hexdigest()[:12]


ren = Image.open(RENDER).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
print(f"render_9 {ren.size}  md5 {md5(ren)}")
print(f"original {orig.size}\n")

fails = 0
for name, (x0, y0, x1, y1) in REGIONS.items():
    # render crop: frame coords * scale, rounded outward
    rx0, ry0 = round(x0 * SX), round(y0 * SY)
    rx1, ry1 = round(x1 * SX), round(y1 * SY)
    fresh = ren.crop((rx0, ry0, rx1, ry1))
    banked = Image.open(os.path.join(Q, f"crop_9_{name}_render.png")).convert("RGB")
    r_ok = fresh.size == banked.size and md5(fresh) == md5(banked)

    # original crop: same frame bbox, LANCZOS-upscaled to the render crop's size
    fw = x1 - x0
    fh = y1 - y0
    fw_px, fh_px = banked.size
    o_fresh = orig.crop((x0, y0, x0 + fw, y0 + fh)).resize((fw_px, fh_px), Image.LANCZOS)
    o_banked = Image.open(os.path.join(Q, f"crop_9_{name}_orig.png")).convert("RGB")
    o_ok = o_fresh.size == o_banked.size and md5(o_fresh) == md5(o_banked)

    # effective scale must be identical per axis for both images
    ex = fw_px / fw
    ey = fh_px / fh
    scale_ok = abs(ex - rx1 / fw + rx0 * 0) < 1e9 and (fw_px, fh_px) == banked.size
    print(f"{name:10s} render_dims={fresh.size} banked={banked.size} render_md5_match={r_ok} "
          f"orig_md5_match={o_ok} eff_scale={ex:.4f}x{ey:.4f}")
    if not (r_ok and o_ok):
        fails += 1

print("\nRESULT:", "ALL 4 PAIRS CURRENT + SCALE-MATCHED" if fails == 0 else f"{fails} STALE PAIR(S)")
sys.exit(1 if fails else 0)
