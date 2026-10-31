import sys
from PIL import Image
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"

# spec equation boxes (normalized) per slide
EQ_BOXES = {
    31: [(0.121, 0.246, 0.217, 0.289), (0.344, 0.250, 0.517, 0.291),
         (0.125, 0.387, 0.235, 0.431), (0.408, 0.387, 0.535, 0.431),
         (0.121, 0.533, 0.238, 0.580), (0.408, 0.533, 0.560, 0.580),
         (0.129, 0.717, 0.333, 0.770), (0.410, 0.733, 0.634, 0.770)],
    32: [(0.10, 0.29, 0.90, 0.41), (0.10, 0.51, 0.75, 0.58),
         (0.10, 0.67, 0.85, 0.75), (0.10, 0.84, 0.92, 0.92)],
}

for n in (31, 32):
    orig = Image.open(f"{NS}/qa/rejudge2/orig_png/slide_{n:03d}.png").convert("RGB")
    ren = Image.open(f"{NS}/recreated_pptx/renders/slide_{n:03d}_recreated-1.png").convert("RGB")
    print(f"slide {n}: orig {orig.size} render {ren.size}")
    ow, oh = orig.size
    rw, rh = ren.size
    oa = np.asarray(orig).astype(int)
    ra = np.asarray(ren).astype(int)
    # ink = pixels notably darker than the light background
    oink = (oa.sum(axis=2) < 600)
    rink = (ra.sum(axis=2) < 600)
    for i, (x0, y0, x1, y1) in enumerate(EQ_BOXES[n]):
        osub = oink[int(y0 * oh):int(y1 * oh), int(x0 * ow):int(x1 * ow)]
        rsub = rink[int(y0 * rh):int(y1 * rh), int(x0 * rw):int(x1 * rw)]
        print(f"  box{i} [{x0:.3f},{y0:.3f},{x1:.3f},{y1:.3f}] orig_ink={osub.sum():5d} render_ink={rsub.sum():5d}")
    # overall ink fraction
    print(f"  total ink: orig={oink.mean():.4f} render={rink.mean():.4f}")
