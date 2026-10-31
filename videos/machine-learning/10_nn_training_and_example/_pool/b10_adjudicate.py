#!/usr/bin/env python3
"""PIL adjudication for b10 slides 019/020: crop the flagged panel from both
the recreation render and the original frame at matched effective scale, and
report ink density + bounding box of the equation block."""
import sys
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"


def ink(img):
    a = np.asarray(img.convert("L"))
    mask = a < 128
    if not mask.any():
        return 0, (0, 0, 0, 0)
    ys, xs = np.where(mask)
    return float(mask.mean()), (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def panel(slide, x0, y0, x1, y1, out):
    render = Image.open(f"{NS}/qa/slide{slide}/rejudge/render-4.png")
    orig = Image.open(f"{NS}/unique_slides/slide_{slide}.jpg")
    # original is 960x540; render is 2001x1125 -> scale factor ~2.084
    sx = render.width / orig.width
    sy = render.height / orig.height
    ox0, oy0, ox1, oy1 = int(x0 * sx), int(y0 * sy), int(x1 * sx), int(y1 * sy)
    rc = render.crop((ox0, oy0, ox1, oy1))
    oc = orig.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    rc.save(out)
    ri, rb = ink(rc)
    oi, ob = ink(oc)
    print(f"{out} size={rc.size} render_ink={ri:.4f} bbox={rb}")
    print(f"{out}          orig_ink={oi:.4f} bbox={ob}")


if __name__ == "__main__":
    slide = sys.argv[1]
    x0, y0, x1, y1 = (int(v) for v in sys.argv[2:6])
    panel(slide, x0, y0, x1, y1, sys.argv[6])
