import numpy as np
from PIL import Image
ORIG = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_005.jpg"
REND = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/render_7.png"
o = np.asarray(Image.open(ORIG).convert("L")).astype(int)
r = np.asarray(Image.open(REND).convert("L")).astype(int)
SX, SY = 2001/960.0, 1125/540.0

def text_extent(arr, x0, x1, t_y0, t_y1, b_y0, b_y1, sx, sy, label, gap=1):
    X0, X1 = int(x0*sx), int(x1*sx)
    def norm(y0, y1):
        Y0, Y1 = int(y0*sy), int(y1*sy)
        return (arr[Y0:Y1+1, X0:X1+1] < 200).mean(axis=0)
    t, b = norm(t_y0, t_y1), norm(b_y0, b_y1)
    cols = np.nonzero(t > b + 0.15)[0]
    if len(cols) == 0: print(f"  {label}: none"); return
    L = (X0+cols.min())/sx; R = (X0+cols.max())/sx
    print(f"  {label}: text ink x {L:.1f}..{R:.1f} (w={R-L+1:.1f}) centre={(L+R)/2:.1f} ncols={len(cols)}")

print("=== getbest TEXT (bands normalised, threshold +0.15) ===")
text_extent(o, 180, 512, 306, 322, 289, 305, 1, 1, "ORIG")
text_extent(r, 180, 512, 306, 322, 289, 305, SX, SY, "REND")
print()
print("=== also check the pink box LEFT/right borders are where expected ===")
def vertborder(arr, x0, x1, y0, y1, sx, sy, label):
    X0,X1,Y0,Y1 = int(x0*sx),int(x1*sx),int(y0*sy),int(y1*sy)
    sub = arr[Y0:Y1+1, X0:X1+1] < 200
    cs = sub.mean(axis=0)
    cols = np.nonzero(cs > 0.9)[0]
    print(f"  {label}: full-height ink cols (frame x) = {[f'{(X0+c)/sx:.1f}' for c in cols]}")
vertborder(o, 70, 512, 292, 340, 1, 1, "ORIG")
vertborder(r, 70, 512, 292, 340, SX, SY, "REND")
