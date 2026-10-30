import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(DECK + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)

RED = lambda c: c[0] > 90 and c[0]-c[1] > 40 and c[0]-c[2] > 40
GRID = lambda c: abs(c[0]-204) < 25 and abs(c[1]-204) < 25 and abs(c[2]-204) < 25
BLACK = lambda c: max(c) < 100
GREEN = lambda c: c[1] > c[0]+30 and c[1] > c[2]+30

print("=== ORIGINAL col x=573 : classify each pixel y 60..310 ===")
prev = None
for y in range(60, 311):
    c = o[y, 573]
    k = "RED" if RED(c) else ("GRID" if GRID(c) else ("BLACK" if BLACK(c) else ("GREEN" if GREEN(c) else "other")))
    if k != prev:
        print("  y=%3d -> %s %s" % (y, k, tuple(c)))
        prev = k
print()
print("=== ORIGINAL col x=809 : classify each pixel y 60..310 ===")
prev = None
for y in range(60, 311):
    c = o[y, 809]
    k = "RED" if RED(c) else ("GRID" if GRID(c) else ("BLACK" if BLACK(c) else ("GREEN" if GREEN(c) else "other")))
    if k != prev:
        print("  y=%3d -> %s %s" % (y, k, tuple(c)))
        prev = k
print()
print("=== ORIGINAL row y=266 / y=267 / y=268 : colour runs (x 570..815) ===")
for yy in [265, 266, 267, 268, 299, 300, 301]:
    prev = None; runlen = 0
    print(" -- y=%d" % yy)
    for x in range(570, 816):
        c = o[yy, x]
        k = "RED" if RED(c) else ("GRID" if GRID(c) else ("BLACK" if BLACK(c) else ("GREEN" if GREEN(c) else "other")))
        if k != prev:
            if runlen: print("    x %d..%d %s %s" % (x-runlen, x-1, prev, tuple(o[yy, x-1])))
            prev = k; runlen = 1
        else:
            runlen += 1
    print("    x %d..%d %s %s" % (816-runlen, 815, prev, tuple(o[yy, 815])))
