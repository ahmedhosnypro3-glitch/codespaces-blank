import numpy as np
from PIL import Image
D = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/"
a = np.asarray(Image.open(D + "render_7_attempt6b.png").convert("RGB")).astype(int)
b = np.asarray(Image.open(D + "render_9.png").convert("RGB")).astype(int)
d = np.abs(a - b).sum(axis=2)
ys, xs = np.nonzero(d > 0)
print("attempt-6 render vs attempt-9 render: differing px =", len(ys))
if len(ys):
    print("changed region (render px): x %d..%d y %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    print("  = frame px x %.1f..%.1f y %.1f..%.1f" % (xs.min()/2.084375, xs.max()/2.084375, ys.min()/2.083333, ys.max()/2.083333))
    print("  reference: getbest text band is frame x185..505 y302..328; pink box y288..343")
    # confirm no change outside the pink band
    outside = int(((ys < 280*2.083333) | (ys > 350*2.083333)).sum())
    print("  changed px outside the pink band (frame y<280 or y>350):", outside)
