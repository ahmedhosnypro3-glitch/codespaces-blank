#!/usr/bin/env python3
"""Generate 600-dpi mathtext PNGs for slide 008 rebuild (wave 3).

Equations come ONLY from qa/reanalysis2/slide_008_analysis.txt section 8.
Assets land in build/eq_008/ as <name>.png + <name>.json sidecars + manifest.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EQDIR = os.path.join(HERE, "eq_008")
RENDER = os.path.join(HERE, "render_math.py")

INK = "1A1A1A"

# name, render_math.py --row value, maxw_in, maxh_in, base size pt
ASSETS = [
    # objective "0.5x^2+3x+4y", box [0.188,0.203,0.325,0.248]
    ("obj", r"#%s:0.5x^{2}+3x+4y" % INK, (0.325 - 0.188) * 13.33, (0.248 - 0.203) * 7.5, 26.0),
    # quadratic form 1/2[x^T P x] + q^T x, box [0.765,0.293,0.917,0.372]
    ("qform",
     r"#00A650:\frac{1}{2}||#C00060:[||#0033CC:x^{T}Px||#C00060:]\ +\ q^{T}||#0033CC:x",
     (0.917 - 0.765) * 13.33, (0.372 - 0.293) * 7.5, 30.0),
    # "Gx <= h" bold red, box [0.413,0.545,0.500,0.590]
    ("gxh", r"#C00000:\mathbf{Gx} \leq \mathbf{h}",
     (0.500 - 0.413) * 13.33, (0.590 - 0.545) * 7.5, 30.0),
    # constraint stack, boxes from spec section 8; oversize so the glyph fills
    # the box height (widths are the binding constraint for c1/c2)
    ("c1", r"#%s:x \geq 0" % INK, (0.126 - 0.085) * 13.33, (0.648 - 0.611) * 7.5, 26.0),
    ("c2", r"#%s:y \geq 0" % INK, (0.126 - 0.085) * 13.33, (0.689 - 0.653) * 7.5, 26.0),
    ("c3", r"#%s:x + 3y \geq 15" % INK, (0.185 - 0.085) * 13.33, (0.731 - 0.694) * 7.5, 26.0),
    ("c4", r"#%s:2x + 5y \leq 100" % INK, (0.201 - 0.085) * 13.33, (0.772 - 0.735) * 7.5, 26.0),
    ("c5", r"#%s:3x + 4y \leq 80" % INK, (0.194 - 0.085) * 13.33, (0.813 - 0.777) * 7.5, 26.0),
]


def main():
    os.makedirs(EQDIR, exist_ok=True)
    manifest = {}
    env = dict(os.environ, MATHTEXT_FONTSET="stix")
    for name, row, maxw, maxh, size in ASSETS:
        out = os.path.join(EQDIR, name + ".png")
        js = os.path.join(EQDIR, name + ".json")
        subprocess.run([
            sys.executable, RENDER,
            "--out", out, "--size", str(size),
            "--maxw", str(maxw), "--maxh", str(maxh),
            "--row", row, "--out-json", js,
        ], check=True, cwd=HERE, env=env)
        with open(js) as fh:
            info = json.load(fh)
        manifest[name] = {
            "image": name + ".png",
            "w_in": info["w_in"], "h_in": info["h_in"],
            "pt": info["fontsize_pt"][0],
        }
        print(name, info["w_in"], "x", info["h_in"], "in @", round(info["fontsize_pt"][0], 2), "pt")
    with open(os.path.join(EQDIR, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)


if __name__ == "__main__":
    main()
