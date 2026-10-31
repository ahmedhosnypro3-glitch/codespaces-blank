#!/usr/bin/env python3
"""Generate the six real scatter plots for slide 040 from the SIPU/UEF
clustering benchmark datasets (gagolews/clustering-data-v0, downloaded to
/tmp/ds040). One transparent PNG per panel at 600 dpi, sized exactly to the
spec's plot region in inches, so addImage can place it at w=px/600, h=px/600.
Colors per spec section 4, mapped to ground-truth labels in order (cycled
when the spec lists fewer colors than clusters).
"""
import gzip
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

DATA = "/tmp/ds040"
OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"

DPI = 600
# spec VISUAL_ELEMENTS plot regions [x0,y0,x1,y1] normalized -> inches
PANELS = {
    "Aggregation": ([0.11, 0.26, 0.31, 0.52], ["0000FF", "FF0000", "00FFFF", "FFFF00", "FF00FF", "000000"]),
    "Compound":    ([0.39, 0.26, 0.58, 0.52], ["000000", "FF00FF", "0000FF", "00FF00", "FF0000"]),
    "Spiral":      ([0.67, 0.26, 0.86, 0.52], ["0000FF", "FF0000", "000000"]),
    "Pathbased":   ([0.11, 0.62, 0.31, 0.88], ["FF0000", "0000FF", "000000"]),
    "Flame":       ([0.39, 0.62, 0.58, 0.88], ["FF0000", "0000FF"]),
    "Jain":        ([0.67, 0.62, 0.86, 0.88], ["0000FF", "FF0000"]),
}
SRC = {"Aggregation": "Aggregation", "Compound": "Compound", "Spiral": "spiral",
       "Pathbased": "pathbased", "Flame": "flame", "Jain": "jain"}

def load(name):
    with gzip.open(f"{DATA}/{name}.data.gz", "rt") as f:
        xy = np.loadtxt(f)
    with gzip.open(f"{DATA}/{name}.labels.gz", "rt") as f:
        lab = np.loadtxt(f, dtype=int)
    return xy, lab

for panel, (reg, colors) in PANELS.items():
    x0, y0, x1, y1 = reg
    w_in, h_in = (x1 - x0) * 13.33, (y1 - y0) * 7.5
    xy, lab = load(SRC[panel])
    fig = plt.figure(figsize=(w_in, h_in), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(xy[:, 0].min(), xy[:, 0].max())
    ax.set_ylim(xy[:, 1].min(), xy[:, 1].max())
    ax.axis("off")
    for cls in sorted(set(lab)):
        m = lab == cls
        ax.scatter(xy[m, 0], xy[m, 1], s=10, linewidths=0,
                   c="#" + colors[(cls - 1) % len(colors)])
    path = f"{OUT}/slide_040_graph_{panel}.png"
    fig.savefig(path, dpi=DPI, transparent=True)
    plt.close(fig)
    im = Image.open(path)
    print(panel, im.size, "expect", round(w_in * DPI), round(h_in * DPI),
          f"w_in={im.size[0]/DPI:.4f} h_in={im.size[1]/DPI:.4f}")
