import numpy as np
from PIL import Image

DECK = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(DECK + "/unique_slides/slide_025.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(DECK + "/recreated_pptx/qa/slide_025/render_3.png")
               .convert("RGB").resize((960, 540), Image.BOX)).astype(int)

def jet(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    # saturated, non-red (exclude the C00000 reference lines/borders)
    sat = (a.max(axis=2) - a.min(axis=2)) > 45
    redl = (R > 120) & (R - G > 45) & (R - B > 45)
    return sat & ~redl

jo, jr = jet(o), jet(r)

# figure interior boxes (measured from the original, excluding the red border)
BOX = {
    "TL": (90, 122, 261, 283),
    "TR": (621, 122, 872, 311),
    "BL": (88, 295, 371, 522),
    "BR": (619, 350, 874, 527),
}
for name, (x0, y0, x1, y1) in BOX.items():
    sub = np.zeros_like(jo); sub[y0:y1+1, x0:x1+1] = True
    for tag, j in (("orig", jo), ("rend", jr)):
        m = j & sub
        ys, xs = np.where(m)
        bw, bh = x1-x0+1, y1-y0+1
        if len(xs):
            w, h = xs.max()-xs.min()+1, ys.max()-ys.min()+1
            print("%-3s %-5s jet bbox x%d..%d y%d..%d  (w%d h%d)  box %dx%d  fill %.0f%%x%.0f%%  px %d"
                  % (name, tag, xs.min(), xs.max(), ys.min(), ys.max(), w, h, bw, bh,
                     100.0*w/bw, 100.0*h/bh, m.sum()))
        else:
            print("%-3s %-5s no jet" % (name, tag))
