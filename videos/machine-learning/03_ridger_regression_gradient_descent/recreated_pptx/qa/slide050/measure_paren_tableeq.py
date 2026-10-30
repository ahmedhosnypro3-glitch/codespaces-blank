from PIL import Image
import numpy as np

DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{DECK}/recreated_pptx/qa/slide050"
ren = np.asarray(Image.open(f"{QA}/render_18.png").convert("L")).astype(int)
org = np.asarray(Image.open(f"{DECK}/unique_slides/slide_050.jpg").convert("L")).astype(int)
SR = ren.shape[1] / 960.0

def prof(a, scale, x0, y0, x1, y1, thr):
    sub = a[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    return (sub < thr).mean(axis=0)

def report(title, a, scale, cols, band, thr=150):
    print(f"== {title} band y{band[0]}..{band[1]}")
    for cx0, cx1 in cols:
        f = prof(a, scale, cx0 - 4, band[0], cx1 + 4, band[1], thr)
        w = len(f)
        edges = []
        for i, v in enumerate(f):
            if v > 0.55:
                fx = cx0 - 4 + i / (w - 1) * (cx1 - cx0 + 8)
                edges.append(round(fx, 1))
        print(f"  col {cx0}..{cx1}: maxfrac={f.max():.2f} tallink@x={edges}")

TOP_COLS = [(88, 110), (110, 132), (132, 155), (155, 178), (178, 203), (203, 225)]
CAP_COLS = [(89, 111), (111, 132), (133, 154), (155, 177), (178, 200), (201, 222)]
report("TOP TABLE ORIG ", org, 1.0, TOP_COLS, (74, 110))
report("TOP TABLE REN18", ren, SR, TOP_COLS, (74, 110))
report("CAPTION ORIG   ", org, 1.0, CAP_COLS, (174, 228))
report("CAPTION REN18  ", ren, SR, CAP_COLS, (174, 228))
