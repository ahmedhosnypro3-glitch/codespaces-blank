import numpy as np
from PIL import Image

FRAME = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_025.jpg"
im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[..., 0], a[..., 1], a[..., 2]
mx = a.max(axis=2); mn = a.min(axis=2)
# jet / rainbow saturation: notable chroma
sat = (mx - mn) > 45
panel = (np.abs(R - 233) < 12) & (np.abs(G - 233) < 12) & (np.abs(B - 231) < 12)
print("saturated px: %d   panel px: %d" % (sat.sum(), panel.sum()))

# exclude the house chrome badge + title red
sat[:110, :] = False
sat[50:100, 840:910] = False

QUADS = {
    "TL": (54, 45, 470, 300),
    "TR": (470, 45, 903, 300),
    "BL": (54, 300, 470, 540),
    "BR": (470, 300, 903, 540),
}
for name, (x0, y0, x1, y1) in QUADS.items():
    sub = np.zeros_like(sat); sub[y0:y1, x0:x1] = True
    m = sat & sub
    ys, xs = np.where(m)
    if len(ys):
        # histogram of x to find the dense core
        hx = np.bincount(xs, minlength=W)
        core = np.where(hx > 20)[0]
        hy = np.bincount(ys, minlength=H)
        corey = np.where(hy > 20)[0]
        print("%s SAT bbox x %d..%d (w %d) y %d..%d (h %d) px %d | x-core %d..%d y-core %d..%d"
              % (name, xs.min(), xs.max(), xs.max()-xs.min()+1,
                 ys.min(), ys.max(), ys.max()-ys.min()+1, m.sum(),
                 core.min(), core.max(), corey.min(), corey.max()))
    else:
        print(name, "none")

# Red reference lines: strict red, thin horizontal runs
red = (R > 150) & (R - G > 70) & (R - B > 70)
red[:110, :] = False
print("\nred px total (body): %d" % red.sum())
for name, (x0, y0, x1, y1) in QUADS.items():
    sub = np.zeros_like(red); sub[y0:y1, x0:x1] = True
    m = red & sub
    ys, xs = np.where(m)
    if len(ys):
        print("  %s red bbox x %d..%d y %d..%d px %d" % (name, xs.min(), xs.max(), ys.min(), ys.max(), m.sum()))
