#!/usr/bin/env python3
"""Generate slide 029 equations: Net_j summation, sigmoid activation, error function."""
import json
import subprocess
import sys

DPI = 600
BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"

def run_render_eq(latex, out_name, fontsize, color="#000000"):
    out_path = f"{BUILD_DIR}/{out_name}"
    res = subprocess.run([
        sys.executable, 
        "/home/codespace/ai_llm_slides/scripts/render_eq.py", 
        latex, out_path, str(fontsize), color
    ], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED {out_name}:\n{res.stdout}\n{res.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(res.stdout.strip())

def run_render_eq_wide(latex, out_name, fontsize, color="#000000"):
    out_path = f"{BUILD_DIR}/{out_name}"
    res = subprocess.run([
        sys.executable, 
        "/home/codespace/ai_llm_slides/scripts/render_eq_wide.py", 
        latex, out_path, str(fontsize), color
    ], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED {out_name} (wide):\n{res.stdout}\n{res.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(res.stdout.strip())

manifest = {}

# Equation 1: Net_j = \sum_i (w_{ji} O_i)  — wide equation
# Per raw.json: "Net_j = \u2211_j (w_ji O_i)" — but the subscript j on sum is wrong per web search
# Web search confirms: Net_j = \sum_i w_{ji} O_i (sum over i, weight from i to j)
info = run_render_eq_wide(r"Net_j = \sum_i w_{ji} O_i", "slide_029_eq_net.png", 16)
manifest["slide_029_eq_net"] = [info]

# Equation 2: O_j = f(Net_j) = \frac{1}{1 + e^{-Net_j}}  — sigmoid
info = run_render_eq(r"O_j = f(\mathit{Net}_j) = \frac{1}{1 + e^{-\mathit{Net}_j}}", "slide_029_eq_sigmoid.png", 16)
manifest["slide_029_eq_sigmoid"] = [info]

# Equation 3: E = \frac{1}{2} \sum_j (t_j - O_j)^2  — error function
info = run_render_eq_wide(r"E = \frac{1}{2} \sum_j (t_j - O_j)^2", "slide_029_eq_error.png", 16)
manifest["slide_029_eq_error"] = [info]

# Also need: w_ji label (small)
info = run_render_eq(r"w_{ji}", "slide_029_wji.png", 12, "#0070C0")
manifest["slide_029_wji"] = [info]

# Net_j and O_j labels (red, bold italic)
info = run_render_eq(r"\mathit{Net}_j", "slide_029_netj_label.png", 12, "#FF0000")
manifest["slide_029_netj_label"] = [info]

info = run_render_eq(r"\mathit{O}_j", "slide_029_oj_label.png", 12, "#FF0000")
manifest["slide_029_oj_label"] = [info]

with open(f"{BUILD_DIR}/slide_029_equations.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(json.dumps(manifest, indent=2))