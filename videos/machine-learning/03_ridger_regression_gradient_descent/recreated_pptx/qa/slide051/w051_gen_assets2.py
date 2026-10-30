#!/usr/bin/env python3
"""Slide 051 att3 asset generation (attempt 3 design).

Row-level mathtext PNGs (mission mechanism, 600dpi, embed w=px/600):
  dzlabel_1/2/3  d(Z_i)=          fs 12.3  black   ink-left 283, ink-top 160/230/296
  rowvec_1/2/3   (1 ;; 0 ;; 0)    fs 15.56 #0F0087 rp-apex 378.5, ink-top 149/218/284
  step           Step , eta ,=, 1 fs 13.2  #A1232A ink-left 365, ink-top 67

Bezier tall parens (gen_parens049 certified pattern, S=1.5 D=1.0):
  sample51 inkH 28 black   lp apex [89,111,133,156,179,201]  rp [102,124,147,170,192,214] ink-top 78
  z51      inkH 29 black   lp [597,621,643]                  rp [612,634,656]            ink-top 81
  aug51    inkH 44 black   lp [93,114,137,159,182,204]       rp [107,128,151,173,195,218] ink-top 180

wcol green (5;-1;-1) via render_wcol_049p.py fs 12 gap 25 #659969
  -> ink-left 381, ink-top 148/218/284
initw (4;-2;-2): REUSES 049's eq_initial_w_col_paren.png (25.2x46.3pt)
  -> ink-left 329, ink-top 59

Writes consolidated sidecar w051_assets2.json with placement-ready numbers.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ASSETS = f"{BASE}/recreated_pptx/build/assets"
QA = f"{BASE}/recreated_pptx/qa/slide051"
P51 = f"{ASSETS}/parens051"
os.makedirs(P51, exist_ok=True)
os.environ["TMPDIR"] = "/home/ahmed/Projects/ai_llm_slides/scratch/tmp"
sys.path.insert(0, "/home/ahmed/Projects/ai_llm_slides/scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("render_eq", "/home/ahmed/Projects/ai_llm_slides/scripts/render_eq.py")
rq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rq)

PPP = 72.0 / 600.0  # pt per asset px

def ink_metrics(path, thr=30):
    a = np.array(Image.open(path))
    alpha = a[:, :, 3] if a.shape[2] == 4 else (255 - a[:, :, 0])
    ys, xs = np.nonzero(alpha > thr)
    return {"ink_left_px": int(xs.min()), "ink_right_px": int(xs.max()),
            "ink_top_px": int(ys.min()), "ink_bot_px": int(ys.max())}

out = {}

# ---------- 1. mathtext row-level PNGs ----------
MT = [
    ("dzlabel_1", "d(Z_1)=", 12.3, "#000000"),
    ("dzlabel_2", "d(Z_2)=", 12.3, "#000000"),
    ("dzlabel_3", "d(Z_3)=", 12.3, "#000000"),
    ("rowvec_1", "(1\\;\\,0\\;\\,0)", 15.56, "#0F0087"),
    ("rowvec_2", "(1\\;\\,7\\;\\,6)", 15.56, "#0F0087"),
    ("rowvec_3", "(1\\;\\,3\\;\\,2)", 15.56, "#0F0087"),
    ("step", "Step\\,\\eta\\,=\\,1", 13.2, "#A1232A"),
]
for name, latex, fs, color in MT:
    p = f"{ASSETS}/eq_051_{name}.png"
    info = rq.render(latex, p, fs, color)
    info.update(ink_metrics(p))
    info["mathtext"] = latex
    out[name] = info
    print(f"{name}: w {info['w_in']*72:.1f}pt h {info['h_in']*72:.1f}pt ink L{info['ink_left_px']} T{info['ink_top_px']} R{info['ink_right_px']}")

# ---------- 2. bezier tall parens ----------
def bezier_x(t, x_tip, x_ctrl):
    return (1 - t) ** 2 * x_tip + 2 * (1 - t) * t * x_ctrl + t ** 2 * x_tip

def render_paren(name, S, inkH, D, color):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    PAD = 0.5
    W = S + D + 2 * PAD
    H = inkH + 2 * PAD
    res = {}
    for side in ("lp", "rp"):
        if side == "lp":
            x_bulge = PAD + S / 2.0
            x_tip = x_bulge + D
        else:
            x_bulge = W - PAD - S / 2.0
            x_tip = x_bulge - D
        x_ctrl = 2 * x_bulge - x_tip
        t = np.linspace(0.0, 1.0, 400)
        xs = bezier_x(t, x_tip, x_ctrl)
        ys = np.linspace(PAD + S / 2.0, H - PAD - S / 2.0, 400)
        fig = plt.figure(figsize=(W / 72.0, H / 72.0))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
        ax.plot(xs, ys, lw=S, color="#" + color, solid_capstyle="round",
                solid_joinstyle="round")
        p = f"{P51}/paren_{name}_{side}.png"
        fig.savefig(p, dpi=600, transparent=True)
        plt.close(fig)
        m = ink_metrics(p)
        m.update({"px_w": Image.open(p).width, "px_h": Image.open(p).height,
                  "w_in": Image.open(p).width / 600, "h_in": Image.open(p).height / 600,
                  "S_pt": S, "D_pt": D, "inkH_pt": inkH, "color": color, "side": side})
        res[side] = m
    out[f"paren_{name}"] = res
    print(f"paren_{name}: lp ink L{res['lp']['ink_left_px']} T{res['lp']['ink_top_px']}  "
          f"rp ink R{res['rp']['ink_right_px']} T{res['rp']['ink_top_px']}")

render_paren("sample51", 1.5, 28.0, 1.0, "000000")
render_paren("z51", 1.5, 29.0, 1.0, "000000")
render_paren("aug51", 1.5, 44.0, 1.0, "000000")

# ---------- 3. green wcol full column ----------
wp = f"{ASSETS}/eq_051_wcol_green.png"
r = subprocess.run([sys.executable, f"{ASSETS}/render_wcol_049p.py", wp,
                    "12", "659969", "25", "5", "-1", "-1"],
                   capture_output=True, text=True)
if r.returncode != 0:
    sys.exit(f"wcol green FAILED: {r.stderr}")
info = json.loads(r.stdout)
info.update(ink_metrics(wp))
info["rows"] = ["5", "-1", "-1"]
out["wcol_green"] = info
print(f"wcol_green: w {info['w_in']*72:.1f}pt h {info['h_in']*72:.1f}pt ink L{info['ink_left_px']} T{info['ink_top_px']} R{info['ink_right_px']}")

# ---------- 4. initw (reuse 049 asset) ----------
iw049 = json.load(open(f"{ASSETS}/eq_slide049_wcol_paren.json"))["iw"]
ip = f"{ASSETS}/eq_initial_w_col_paren.png"
info = dict(iw049)
info.update(ink_metrics(ip))
info["path_abs"] = ip
out["initw_reuse"] = info
print(f"initw_reuse: w {info['w_in']*72:.1f}pt h {info['h_in']*72:.1f}pt ink L{info['ink_left_px']} T{info['ink_top_px']}")

# ---------- 5. placement table (frame px targets) ----------
PLACE = {
    "dzlabel_1": {"ax": 283, "ay": 160}, "dzlabel_2": {"ax": 283, "ay": 230},
    "dzlabel_3": {"ax": 283, "ay": 296},
    "rowvec_1": {"rx": 378.5, "ay": 149}, "rowvec_2": {"rx": 378.5, "ay": 218},
    "rowvec_3": {"rx": 378.5, "ay": 284},
    "step": {"ax": 365, "ay": 67},
    "wcol_green": {"ax": 381, "ays": [148, 218, 284]},
    "initw_reuse": {"ax": 329, "ay": 59},
    "paren_sample51": {"lp_x": [89, 111, 133, 156, 179, 201],
                       "rp_x": [102, 124, 147, 170, 192, 214], "ay": 78},
    "paren_z51": {"lp_x": [597, 621, 643], "rp_x": [612, 634, 656], "ay": 81},
    "paren_aug51": {"lp_x": [93, 114, 137, 159, 182, 204],
                    "rp_x": [107, 128, 151, 173, 195, 218], "ay": 180},
}
out["_placement"] = PLACE
json.dump(out, open(f"{QA}/w051_assets2.json", "w"), indent=1)
print("WROTE", f"{QA}/w051_assets2.json")
