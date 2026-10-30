import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide031"
K = 1125 / 540.0


def region(arr, fx0, fy0, fx1, fy1):
    x0, x1 = int(round(fx0 * K)), int(round(fx1 * K))
    y0, y1 = int(round(fy0 * K)), int(round(fy1 * K))
    sub = arr[y0:y1, x0:x1]
    return 0.299*sub[:, :, 0] + 0.587*sub[:, :, 1] + 0.114*sub[:, :, 2]


def groups(lum, thresh=170, gap=8):
    m = lum < thresh
    on = m.sum(axis=0) > 0
    out, st = [], None
    for i, v in enumerate(on):
        if v and st is None: st = i
        elif not v and st is not None: out.append((st, i-1)); st = None
    if st is not None: out.append((st, len(on)-1))
    merged = []
    for a, b in out:
        if merged and a - merged[-1][1] <= gap: merged[-1] = (merged[-1][0], b)
        else: merged.append((a, b))
    return merged, m


def summarize(tag, arr):
    print("=== %s ===" % tag)
    # equation interior
    lum = region(arr, 400, 186, 528, 210)
    g, m = groups(lum)
    xs = np.nonzero(m.sum(axis=1))[0]
    print("  eq ink: x %d..%d render px -> frame %.1f..%.1f  y %d..%d -> %.1f..%.1f  groups=%d"
          % (min(a for a,b in g), max(b for a,b in g), 400 + min(a for a,b in g)/K, 400 + max(b for a,b in g)/K,
             xs.min(), xs.max(), 186 + xs.min()/K, 186 + xs.max()/K, len(g)))
    print("  group extents (frame px rel to x400):", ["%.1f-%.1f" % (400+a/K, 400+b/K) for a, b in g])
    # title band colours
    for name, rgb, tol in [("red", (255, 0, 0), 0), ("green", (0, 128, 0), 0), ("blue", (0, 0, 255), 0)]:
        pass
    return


def lum_all(arr):
    return 0.299*arr[:, :, 0] + 0.587*arr[:, :, 1] + 0.114*arr[:, :, 2]


def colour_title(tag, arr):
    print("--- %s TITLE ink by colour (frame y55..95) ---" % tag)
    L = lum_all(arr)
    y0, y1 = int(55*K), int(95*K)
    x0, x1 = int(30*K), int(700*K)
    sl = arr[y0:y1, x0:x1]; sll = L[y0:y1, x0:x1]
    for name, mask in [
        ("red",   (sl[:,:,0] > 110) & (sl[:,:,0]-sl[:,:,1] > 40) & (sl[:,:,0]-sl[:,:,2] > 40) & (sll < 150)),
        ("green", (sl[:,:,1] > 90) & (sl[:,:,1]-sl[:,:,0] > 25) & (sl[:,:,1]-sl[:,:,2] > 25) & (sll < 150)),
        ("blue",  (sl[:,:,2] > 90) & (sl[:,:,2]-sl[:,:,0] > 25) & (sl[:,:,2]-sl[:,:,1] > 25) & (sll < 150)),
    ]:
        on = mask.sum(axis=0) > 0
        out, st = [], None
        for i, v in enumerate(on):
            if v and st is None: st = i
            elif not v and st is not None: out.append((st, i-1)); st = None
        if st is not None: out.append((st, len(on)-1))
        merged = []
        for a, b in out:
            if merged and a - merged[-1][1] <= 10: merged[-1] = (merged[-1][0], b)
            else: merged.append((a, b))
        ext = ["%.1f-%.1f" % (30+a/K, 30+b/K) for a, b in merged]
        # glyph count within the big first group
        print("   %-6s groups(%d): %s" % (name, len(merged), ext))


for tag, f in [("render_8", "render_8.png"), ("render_9", "render_9.png")]:
    a = np.asarray(Image.open(QA + "/" + f).convert("RGB")).astype(int)
    summarize(tag, a)
    colour_title(tag, a)
    print()
