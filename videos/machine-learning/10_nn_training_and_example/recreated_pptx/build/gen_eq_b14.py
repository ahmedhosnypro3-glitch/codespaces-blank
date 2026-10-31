#!/usr/bin/env python3
"""Generate 2D mathtext equation PNGs (+sidecars) for slides 27 and 28 of
10_nn_training_and_example. Run from this directory."""
import json
import subprocess
import sys

RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq.py"

EQ27 = [
    ("eq27_o3", r"O_3 = \dfrac{1}{1+e^{-2.2}} = 0.9", 13, "#000000"),
    ("eq27_o4", r"O_4 = \dfrac{1}{1+e^{-2.8}} = 0.943", 13, "#000000"),
    ("eq27_o5", r"O_5 = \dfrac{1}{1+e^{-3.4}} = 0.968", 13, "#000000"),
    ("eq27_o6", r"O_6 = \dfrac{1}{1+e^{-1.3312}} = 0.791", 13, "#000000"),
    ("eq27_o7", r"O_7 = \dfrac{1}{1+e^{-1.3312}} = 0.791", 13, "#000000"),
]

EQ28 = [
    ("eq28_delta_j", r"\delta_j = O_j(1-O_j)(t_j-O_j)", 13, "#000000"),
    ("eq28_delta_w",
     r"\Delta_{ji} = \eta \cdot O_i \cdot O_j(1-O_j)(t_j-O_j) = \eta \cdot O_i \cdot \delta_j",
     13, "#000000"),
    ("eq28_delta6", r"\delta_6 = 0.791(1-0.791)(0-0.791) = -0.131", 13, "#C00000"),
    ("eq28_delta7", r"\delta_7 = 0.791(1-0.791)(1-0.791) = 0.035", 13, "#C00000"),
    ("eq28_o3", r"O_3 = \dfrac{1}{1+e^{-2.2}} = 0.9", 11, "#000000"),
    ("eq28_o4", r"O_4 = \dfrac{1}{1+e^{-2.8}} = 0.943", 11, "#000000"),
    ("eq28_o5", r"O_5 = \dfrac{1}{1+e^{-3.4}} = 0.968", 11, "#000000"),
    ("eq28_o6", r"O_6 = \dfrac{1}{1+e^{-1.3312}} = 0.791", 11, "#000000"),
    ("eq28_o7", r"O_7 = \dfrac{1}{1+e^{-1.3312}} = 0.791", 11, "#000000"),
]


def run(items):
    out = {}
    for (name, latex, pt, color) in items:
        png = f"assets/{name}.png"
        js = subprocess.run(
            ["python3", RENDER, latex, png, str(pt), color],
            capture_output=True, text=True, check=True)
        info = json.loads(js.stdout.strip().splitlines()[-1])
        with open(f"assets/{name}.json", "w") as fh:
            json.dump({"name": name, "mathtext": latex, "fontsize_pt": pt,
                       "color": color, **info}, fh, indent=1)
        out[name] = info
        print(f"{name}: {info['w_in']} x {info['h_in']} in  baseline_frac="
              f"{info.get('baseline_frac')}")
    return out


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "27"):
        run(EQ27)
    if which in ("all", "28"):
        run(EQ28)
