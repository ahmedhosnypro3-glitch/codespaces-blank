#!/usr/bin/env python3
"""Arrow bbox + coarse ASCII glyph read of the equation row (both images)."""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_036.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide036/render_5.png"

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
r = np.array(Image.open(REND).convert("RGB")).astype(int)
s = r.shape[0] / 540.0

def bbox(img, x0, x1, y0, y1, thr=175, sc=1.0):
    a = img[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)]
    lum = a.mean(axis=2)
    m = lum < thr
    if not m.any(): return None
    ys, xs = np.where(m)
    return (round(x0+xs.min()/sc,1), round(x0+xs.max()/sc,1),
            round(y0+ys.min()/sc,1), round(y0+ys.max()/sc,1))

print("ARROW REGION bbox (x375..420):")
print("  ORIG:", bbox(o, 375, 420, 372, 400))
print("  REND:", bbox(r, 375, 420, 372, 400, sc=s))
print("ARROW REGION bbox, tighter window x384..415:")
print("  ORIG:", bbox(o, 384, 415, 372, 400))
print("  REND:", bbox(r, 384, 415, 372, 400, sc=s))

# coarse ASCII: 1 char per 2 frame px, x295..530, y366..400
def ascii_read(img, tag, sc=1.0):
    print(f"\n=== {tag}  (1 char = 2 frame px; x295..530, y366..400) ===")
    X0, X1, Y0, Y1 = 295, 530, 366, 400
    sub = img[int(Y0*sc):int(Y1*sc), int(X0*sc):int(X1*sc)]
    lum = sub.mean(axis=2)
    # pool 2x2 frame px -> one char
    rows_out = []
    for fy in range(Y0, Y1):
        line = []
        for fx in range(X0, X1, 2):
            y_a0, y_a1 = int((fy-Y0)*sc), int((fy+1-Y0)*sc)
            x_a0, x_a1 = int((fx-X0)*sc), int((fx+2-X0)*sc)
            blk = lum[y_a0:y_a1, x_a0:x_a1]
            v = blk.min() if blk.size else 255
            line.append('#' if v < 120 else ('+' if v < 190 else '.'))
        rows_out.append((fy, "".join(line)))
    hdr = "".join(str((X0+i)//10 % 10) if (X0+i) % 10 == 0 else " " for i in range(0, X1-X0, 2))
    print("        " + hdr)
    for fy, l in rows_out:
        print(f"  y{fy:3d}  {l}")

ascii_read(o, "ORIGINAL slide_036.jpg")
ascii_read(r, "RENDER_5", sc=s)
