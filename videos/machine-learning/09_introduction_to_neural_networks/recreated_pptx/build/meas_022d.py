"""Map slide_022 original: row bands, per-box fills, box edges, text ink colors."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
PX = W / 13.33  # px per inch

def near(col, tol):
    return np.abs(a - np.array(col)).sum(axis=2) < tol

peach = near((240, 224, 208), 30)
lyellow = near((240, 240, 224), 30)

print("peach n=%d  lyellow n=%d" % (peach.sum(), lyellow.sum()))

# Horizontal profile inside each row band: classify pixels
def profile(y0, y1, label):
    band = slice(y0, y1)
    print("\n=== %s  y=%d..%d ===" % (label, y0, y1))
    row = a[band].reshape(-1, 3)
    p = peach[band].sum(axis=0)
    l = lyellow[band].sum(axis=0)
    # find runs of peach / lyellow along x
    def runs(mask1d, minlen):
        out = []
        start = None
        for i, v in enumerate(mask1d):
            if v and start is None:
                start = i
            elif not v and start is not None:
                if i - start >= minlen:
                    out.append((start, i - 1))
                start = None
        if start is not None and len(mask1d) - start >= minlen:
            out.append((start, len(mask1d) - 1))
        return out
    # per-column: is this column predominantly peach or lyellow?
    pdom = p > (y1 - y0) * 0.25
    ldom = l > (y1 - y0) * 0.25
    print("  peach-dominant runs:", [r for r in runs(pdom, 8)])
    print("  lyellow-dominant runs:", [r for r in runs(ldom, 8)])

# container y 110..504 -> 4 rows. Find actual row separators by ink profile
for i, (y0, y1) in enumerate([(110, 208), (208, 306), (306, 405), (405, 504)]):
    profile(y0, y1, "row%d" % (i + 1))
