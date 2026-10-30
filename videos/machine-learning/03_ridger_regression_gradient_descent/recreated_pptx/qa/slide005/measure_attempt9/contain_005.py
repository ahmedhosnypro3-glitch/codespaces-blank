import numpy as np
from PIL import Image
ORIG = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_005.jpg"
REND = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide005/render_7.png"
o = np.asarray(Image.open(ORIG).convert("L")).astype(int)
r = np.asarray(Image.open(REND).convert("L")).astype(int)
SX, SY = 2001/960.0, 1125/540.0

BOXES = {
 "cream_upper":  (72, 102, 892, 277),
 "blue_upper":   (676, 134, 882, 238),
 "pink":         (73, 288, 506, 343),
 "cream_lower":  (72, 358, 892, 522),
 "blue_lower":   (656, 372, 872, 422),
 "green_outline":(688, 464, 879, 498),
}
# element -> (enclosing box, x0,x1,y0,y1 window in frame px)
EL = {
 "eq1":      ("cream_upper",  90,  552, 105, 154),
 "eq2":      ("cream_upper",  90,  637, 168, 218),
 "eq3":      ("cream_upper",  90,  530, 225, 275),
 "pinkfrac": ("pink",          75,  172, 290, 341),
 "getbest":  ("pink",         180, 516, 293, 341),
 "rememberU":("blue_upper",   678,  760, 135, 153),
 "bodyX1":   ("blue_upper",   678,  878, 156, 174),
 "bodyX2":   ("blue_upper",   678,  796, 176, 194),
 "rem1eq":   ("blue_upper",   678,  872, 210, 240),
 "eq4":      ("cream_lower",  90,  600, 371, 421),
 "eq5":      ("cream_lower",  90,  645, 456, 506),
 "rememberL":("blue_lower",   658,  732, 373, 391),
 "rem2eq":   ("blue_lower",   658,  872, 393, 423),
 "green":    ("green_outline",686, 884, 461, 501),
}

def borders(arr, box, sx, sy, frac=0.85):
    """Detect the box's border rows/cols (frame px) as near-continuous ink lines."""
    x0,y0,x1,y1 = box
    X0,X1,Y0,Y1 = int(x0*sx),int(x1*sx),int(y0*sy),int(y1*sy)
    sub = arr[Y0-4:Y1+5, X0-4:X1+5] < 200
    rows = np.nonzero(sub.mean(axis=1) > frac)[0]
    cols = np.nonzero(sub.mean(axis=0) > frac)[0]
    return [(Y0-4+int(v))/sy for v in rows], [(X0-4+int(v))/sx for v in cols]

def elink(arr, win, sx, sy, maskrows, maskcols):
    x0,x1,y0,y1 = win
    X0,X1,Y0,Y1 = int(x0*sx),int(x1*sx),int(y0*sy),int(y1*sy)
    sub = arr[Y0-6:Y1+7, X0-6:X1+7] < 200
    ry = [(Y0-6+i)/sy for i in range(sub.shape[0])]
    rx = [(X0-6+j)/sx for j in range(sub.shape[1])]
    keep = np.array([[not (any(abs(ry[i]-c) <= 3.0 for c in maskrows)
                           or any(abs(rx[j]-c) <= 3.0 for c in maskcols))
                      for j in range(sub.shape[1])] for i in range(sub.shape[0])])
    m = sub & keep
    if not m.any(): return None
    ys, xs = np.nonzero(m)
    return ((X0-6+xs.min())/sx, (Y0-6+ys.min())/sy, (X0-6+xs.max())/sx, (Y0-6+ys.max())/sy)

for name, (box, wx0, wx1, wy0, wy1) in EL.items():
    b = BOXES[box]
    res = {}
    for tag, arr, sx, sy in (("ORIG", o, 1, 1), ("REND", r, SX, SY)):
        br, bc = borders(arr, b, sx, sy)
        bb = elink(arr, (wx0,wx1,wy0,wy1), sx, sy, br, bc)
        res[tag] = (bb, br, bc)
    bb_o, br_o, bc_o = res["ORIG"]; bb_r, br_r, bc_r = res["REND"]
    bx0, by0, bx1, by1 = b
    def inside(bb):
        if bb is None: return None
        return (bb[0] > bx0+1.5, bb[1] > by0+1.5, bb[2] < bx1-1.5, bb[3] < by1-1.5)
    io, ir = inside(bb_o), inside(bb_r)
    so = "n/a" if bb_o is None else f"x{bb_o[0]:.1f}..{bb_o[2]:.1f} y{bb_o[1]:.1f}..{bb_o[3]:.1f}"
    sr = "n/a" if bb_r is None else f"x{bb_r[0]:.1f}..{bb_r[2]:.1f} y{bb_r[1]:.1f}..{bb_r[3]:.1f}"
    flag = ""
    if ir is not None and not all(ir): flag = "  <<< RENDER OVERFLOWS BOX"
    if bb_r is not None and bb_o is not None:
        dr = max(abs(bb_r[0]-bb_o[0]), abs(bb_r[2]-bb_o[2])) 
        if dr > 3.0 and not flag: flag = f"  (h ext differs {dr:.1f}px)"
    print(f"{name:10s} box x{bx0}..{bx1} y{by0}..{by1}")
    print(f"   ORIG ink {so}")
    print(f"   REND ink {sr}   inside={ir}{flag}")
