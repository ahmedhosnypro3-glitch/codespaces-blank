#!/usr/bin/env python3
"""Cut Procedure-B crop pairs from render_5 (attempt-5 build) + originals at matched
scale, and diff every dense region across render_3/render_4/render_5 to decide which
prior crop certificates remain valid (law: a crop transcript is kept only if its region
is pixel-identical across the rebuild). Frame 960x540, 1px=1pt; render scale = H/540."""
import numpy as np
from PIL import Image

Q = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide009"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"

orig = Image.open(ORIG).convert("RGB")
r3 = Image.open(f"{Q}/render_3.png").convert("RGB")
r4 = Image.open(f"{Q}/render_4.png").convert("RGB")
r5 = Image.open(f"{Q}/render_5.png").convert("RGB")
S = r5.width / 540.0
print(f"render_5 size={r5.size} scale={S:.5f}")

REGIONS = {
    "eq_left":    (208, 138, 327, 185),   # LEFT equation box x216..317 y148..175 + 8px pad
    "eq_right":   (621, 138, 744, 185),   # RIGHT equation box x631..734 y148..175 + pad
    "cap_left":   (85, 469, 444, 539),    # LEFT caption box x95..434 y479..529 + pad
    "cap_right":  (491, 469, 852, 539),   # RIGHT caption box x501..842 y479..529 + pad
    "chart_left": (85, 97, 476, 484),     # LEFT chart frame x95..466 y107..474 + pad
    "chart_right":(476, 97, 881, 484),    # RIGHT chart frame x486.5..871.5 y107..474 + pad
}

def crop_render(img, box):
    x0, y0, x1, y1 = box
    return img.crop((int(round(x0*S)), int(round(y0*S)), int(round(x1*S)), int(round(y1*S))))

def crop_orig_matched(box, rw, rh):
    x0, y0, x1, y1 = box
    c = orig.crop((x0, y0, x1, y1))
    return c.resize((rw, rh), Image.LANCZOS)

out = []
for name, box in REGIONS.items():
    rc = crop_render(r5, box)
    rw, rh = rc.size
    oc = crop_orig_matched(box, rw, rh)
    assert oc.size == rc.size, f"{name}: scale mismatch {rc.size} vs {oc.size}"
    rc.save(f"{Q}/crop_5_{name}_render.png")
    oc.save(f"{Q}/crop_5_{name}_orig.png")
    # cross-build diff at render resolution: count pixels that changed
    def arr(im):
        a = np.asarray(im).astype(np.int16)
        return a
    diffs = {}
    for tag, prev in (("r3", r3), ("r4", r4)):
        a1, a2 = arr(crop_render(prev, box)), arr(rc)
        ch = (np.abs(a1 - a2).max(axis=2) > 12)
        ys, xs = np.nonzero(ch)
        bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if len(xs) else None
        diffs[tag] = (int(ch.sum()), bbox)
    line = f"{name}: box={box} crop={rw}x{rh} (frame {box[2]-box[0]}x{box[3]-box[1]}) scale={rw/(box[2]-box[0]):.4f} diff4vs5={diffs['r4'][0]} bbox={diffs['r4'][1]} diff3vs5={diffs['r3'][0]}"
    out.append(line)
    print(line)

with open(f"{Q}/crossbuild_diff_5.txt", "w") as f:
    f.write("region diffs, render_3/render_4 vs render_5 (render px, threshold >12/255 max-channel)\n")
    f.write("a region with diff=0 in BOTH comparisons keeps its crop_3 certificate (law: pixel-identical -> kept)\n")
    for l in out:
        f.write(l + "\n")
print("wrote crossbuild_diff_5.txt + crop_5_* pairs")
