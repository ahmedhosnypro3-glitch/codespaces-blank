from PIL import Image
import numpy as np

Q = ('/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/'
     '03_ridger_regression_gradient_descent/recreated_pptx/qa/slide004/')
render = np.asarray(Image.open(Q + 'render_2.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(
    '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/'
    '03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg'
).convert('RGB')).astype(int)
S = render.shape[0] / 540.0


def lines(sub, sc, y0, thr=200, mingap=3):
    m = sub.min(axis=2) < thr
    rows = m.sum(axis=1)
    runs = []
    s = None
    for i, v in enumerate(rows):
        if v > 0 and s is None:
            s = i
        elif v == 0 and s is not None:
            if i - s >= mingap:
                runs.append((round(y0 + s / sc, 1), round(y0 + (i - 1) / sc, 1)))
            s = None
    if s is not None:
        runs.append((round(y0 + s / sc, 1), round(y0 + sub.shape[0] / sc, 1)))
    return runs


REGIONS = {
    'Where box':   (498, 880, 236, 367),
    'Objective':   (82, 297, 246, 298),
    'Error':       (82, 482, 310, 361),
    'Box1 labels': (84, 390, 150, 220),
    'Box2 labels': (431, 741, 158, 220),
    'Remember':    (786, 878, 100, 152),
    'Formula eq':  (82, 482, 466, 520),
}
for name, (x0, x1, y0, y1) in REGIONS.items():
    rr = render[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    oo = orig[y0:y1, x0:x1]
    lr = lines(rr, S, y0)
    lo = lines(oo, 1.0, y0)
    print(f'{name:12s} render {len(lr)} lines: {lr}')
    print(f'{"":12s} orig   {len(lo)} lines: {lo}')
    print()
