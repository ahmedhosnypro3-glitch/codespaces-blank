#!/usr/bin/env python3
"""Render full piecewise equations at exact final display size for slide 017."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
DPI = 600

# Target display size on slide (inches)
TARGET_W_IN = 1.25
TARGET_H_IN = 0.42

TARGET_W_PX = int(TARGET_W_IN * DPI)  # 750
TARGET_H_PX = int(TARGET_H_IN * DPI)  # 252

def render_piecewise(cases, out_path, fontsize_val=7, fontsize_cond=5, brace_size=22):
    """cases = list of (value, condition) tuples, e.g. [("0", "x<0"), ("1", "x>=0")]"""
    n = len(cases)
    # Use a canvas sized to the target, leave small margins
    fig = plt.figure(figsize=(TARGET_W_IN, TARGET_H_IN), dpi=DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    # Place cases from top to bottom
    for i, (val, cond) in enumerate(cases):
        y = 0.82 - i * (0.82 / (n + 0.3))
        ax.text(0.35, y, val, fontsize=fontsize_val, color="#000000", ha='center', va='center')
        ax.text(0.42, y, f"for {cond}", fontsize=fontsize_cond, color="#000000", ha='left', va='center')
    
    # Large curly brace on the left spanning all cases
    brace_y = 0.82 - (n - 1) * (0.82 / (n + 0.3)) / 2
    ax.text(0.16, brace_y, "{", fontsize=brace_size, color="#000000", ha='center', va='center')
    
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    
    if len(rows) == 0:
        plt.close(fig)
        return None
    
    y0, y1 = max(rows[0]-4, 0), min(rows[-1]+4, buf.shape[0])
    x0, x1 = max(cols[0]-4, 0), min(cols[-1]+4, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out_path)
    plt.close(fig)
    
    h = y1 - y0
    return {
        "path": out_path, "w_px": int(x1-x0), "h_px": int(h),
        "w_in": round(float(x1-x0)/DPI, 5), "h_in": round(float(h)/DPI, 5),
        "dpi": DPI, "fontsize_pt": fontsize_val, "color": "#000000"
    }

manifest = {}

# Uni-polar: { 0 for x<0 ; 1 for x>=0 }
info = render_piecewise([("0", "x<0"), ("1", "x>=0")], f"{BUILD_DIR}/eq_unipolar_full.png")
manifest["eq_unipolar_full"] = [info]

# Bi-polar: { -1 for x<0 ; 1 for x>=0 }
info = render_piecewise([("-1", "x<0"), ("1", "x>=0")], f"{BUILD_DIR}/eq_bipolar_full.png")
manifest["eq_bipolar_full"] = [info]

# Linear: F(x) = x - use render_eq_wide at correct size
import subprocess, sys
res = subprocess.run([sys.executable, "/home/codespace/ai_llm_slides/scripts/render_eq_wide.py", r"F(x) = x", f"{BUILD_DIR}/eq_linear.png", "7", "#000000"], capture_output=True, text=True)
if res.returncode != 0:
    print(f"FAILED linear:\n{res.stdout}\n{res.stderr}", file=sys.stderr)
    sys.exit(1)
manifest["eq_linear"] = [json.loads(res.stdout.strip())]

with open(f"{BUILD_DIR}/eq_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(json.dumps(manifest, indent=2))