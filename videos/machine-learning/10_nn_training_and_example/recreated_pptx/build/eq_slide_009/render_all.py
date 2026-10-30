#!/usr/bin/env python3
"""Render slide_009 equations: 600dpi mathtext PNGs, multi-part (red eta/Delta) composed on one baseline."""
import json, os, subprocess
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS = os.path.join(HERE, "parts")
os.makedirs(PARTS, exist_ok=True)
RENDER = "/home/codespace/.agents/skills/slide-recreation/scripts/render_eq.py"
FS = "14"
GAP = 4  # px between composed parts

EQS = [
    ("eq1", [(r"W_{ji}^{Updated} = W_{ji}^{old} -", "#000000"), (r"\eta", "#FF0000"),
             (r"\frac{\partial E}{\partial W_{ji}}", "#000000")]),
    ("eq2", [(r"W_{ji}^{Updated} = W_{ji}^{old} +", "#000000"), (r"\Delta_{ji}", "#FF0000")]),
    ("eq3", [(r"\Delta_{ji}", "#FF0000"), (r" = -", "#000000"), (r"\eta", "#FF0000"),
             (r"\frac{\partial E}{\partial W_{ji}}", "#000000")]),
    ("eq4", [(r"E = \frac{1}{2} \sum_j (t_j - O_j)^2", "#000000")]),
    ("eq5", [(r"O_j = f(Net_j) = \frac{1}{1+e^{-Net_j}}", "#000000")]),
    ("eq6", [(r"Net_j = \sum_i (w_{ji} O_i)", "#000000")]),
    ("eq7", [(r"\frac{\partial E}{\partial O_j} = -(t_j - O_j)", "#000000")]),
    ("eq8", [(r"\frac{\partial O_j}{\partial Net_j} = O_j(1-O_j)", "#000000")]),
    ("eq9", [(r"\frac{\partial Net_j}{\partial W_{ji}} = O_i", "#000000")]),
    ("eq10", [(r"\frac{\partial E}{\partial W_{ji}} = \frac{\partial E}{\partial O_j} * "
               r"\frac{\partial O_j}{\partial Net_j} * \frac{\partial Net_j}{\partial W_{ji}}", "#000000")]),
    ("eq11", [(r"= -(t_j - O_j) * O_j(1-O_j) * O_i", "#000000")]),
    ("eq12", [(r"\frac{\partial E}{\partial O_j} = -(t_j - O_j)", "#000000")]),
    ("eq13", [(r"\frac{\partial O_j}{\partial Net_j} = O_j(1-O_j)", "#000000")]),
    ("eq14", [(r"\frac{\partial Net_j}{\partial W_{ji}} = O_i", "#000000")]),
]


def render_part(latex, color, tag):
    png = os.path.join(PARTS, f"{tag}.png")
    r = subprocess.run(["python3", RENDER, latex, png, FS, color], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"render failed {latex!r}: {r.stderr[-400:]}")
    info = json.loads(r.stdout)
    im = Image.open(png).convert("RGBA")
    arr = np.asarray(im)[:, :, 3]
    rows = np.where(arr.any(axis=1))[0]
    cols = np.where(arr.any(axis=0))[0]
    y0, y1, x0, x1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
    cropped = im.crop((x0, y0, x1, y1))
    meta = {"w_px": int(x1 - x0), "h_px": int(y1 - y0),
            "baseline_px": int(info["baseline_px"] - y0),
            "latex": latex, "color": color}
    return cropped, meta


for name, parts in EQS:
    metas = []
    for i, (latex, color) in enumerate(parts):
        metas.append(render_part(latex, color, f"{name}_{i}"))
    base = max(m["baseline_px"] for _, m in metas)
    height = max(base + (m["h_px"] - m["baseline_px"]) for _, m in metas)
    width = sum(m["w_px"] for _, m in metas) + GAP * (len(metas) - 1)
    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = 0
    for im, m in metas:
        canvas.alpha_composite(im, (x, base - m["baseline_px"]))
        x += m["w_px"] + GAP
    out = os.path.join(HERE, name + ".png")
    canvas.save(out)
    h, w = canvas.height, canvas.width
    info = {"path": out, "w_px": int(w), "h_px": int(h), "w_in": round(w / 600, 5),
            "h_in": round(h / 600, 5), "baseline_px": int(base), "baseline_frac": round(base / h, 5),
            "dpi": 600, "fontsize_pt": float(FS), "color": "#000000",
            "latex": " ".join(p[0] for p in parts),
            "parts": [[p[0], p[1]] for p in parts]}
    with open(os.path.join(HERE, name + ".json"), "w") as f:
        json.dump(info, f, indent=2)
    print(f"{name}: {info['w_in']}x{info['h_in']}in base_frac={info['baseline_frac']}")
