from PIL import Image
import numpy as np

ORIG = ('/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/'
        '03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg')
orig = np.asarray(Image.open(ORIG).convert('RGB')).astype(int)


def bands(y0, y1, x0, x1, thr=200, minh=2, minpx=3):
    sub = orig[y0:y1, x0:x1]
    m = sub.min(axis=2) < thr
    rows = m.sum(axis=1)
    runs = []
    s = None
    for i, v in enumerate(rows):
        if v >= minpx and s is None:
            s = i
        elif v < minpx and s is not None:
            if i - s >= minh:
                runs.append((y0 + s, y0 + i - 1))
            s = None
    if s is not None and (y1 - s) >= minh:
        runs.append((y0 + s, y1 - 1))
    return runs


AREAS = {
    'WHERE (x498..880, y235..369)':    (235, 369, 498, 880),
    'REMEMBER (x786..878, y101..151)': (101, 151, 786, 878),
    'OBJECTIVE (x82..297, y245..299)': (245, 299, 82, 297),
    'FORMULA (x82..482, y466..520)':   (466, 520, 82, 482),
    'BOX1 (x84..391, y102..219)':      (102, 219, 84, 391),
    'BOX2 (x431..741, y102..219)':     (102, 219, 431, 741),
    'DEFINE (x82..651, y389..446)':    (389, 446, 82, 651),
}
for name, (y0, y1, x0, x1) in AREAS.items():
    print(name)
    for a, b in bands(y0, y1, x0, x1):
        print(f'   y {a}..{b}  (h={b-a+1})')
    print()
