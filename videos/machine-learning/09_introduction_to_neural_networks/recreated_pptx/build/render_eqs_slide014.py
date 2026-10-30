#!/usr/bin/env python3
"""Render the five derivation equations for slide 014 as 2D mathtext PNGs (600 dpi)."""
import json
import subprocess
import sys

RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq_wide.py"
BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"

CASES = [
    # (name, latex, fontsize, color)
    ("eq14_sum1", r"Sum\ 1 = w_{11}x_1 + w_{12}x_2", 11, "#000000"),
    ("eq14_sum2", r"Sum\ 2 = w_{21}x_1 + w_{22}x_2", 11, "#000000"),
    ("eq14_sum3", r"Sum\ 3 = (w_{11}x_1 + w_{12}x_2)\,w_{31} + (w_{21}x_1 + w_{22}x_2)\,w_{32}", 11, "#000000"),
    ("eq14_expand", r"= (w_{11}w_{31} + w_{21}w_{32})\,x_1 + (w_{12}w_{31} + w_{22}w_{32})\,x_2", 11, "#000000"),
    ("eq14_linear", r"= w'_1x_1 + w'_2x_2", 11, "#000000"),
]

for name, latex, fs, color in CASES:
    out = f"{BUILD_DIR}/{name}.png"
    res = subprocess.run(
        [sys.executable, RENDER, latex, out, str(fs), color],
        capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FAILED {name}:\n{res.stdout}\n{res.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"{name}: {res.stdout.strip()}")
