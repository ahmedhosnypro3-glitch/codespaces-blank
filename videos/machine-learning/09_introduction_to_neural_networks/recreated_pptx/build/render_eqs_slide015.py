#!/usr/bin/env python3
"""Render the XOR truth table and callout text for slide 015 as 2D mathtext PNGs (600 dpi)."""
import json
import subprocess
import sys

RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq_wide.py"
BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"

CASES = [
    # (name, latex, fontsize, color)
    ("eq15_xor_title", r"\text{Adding Non-Linearity}", 14, "#0000FF"),
    ("eq15_xor_sub1", r"\text{Solves the}", 14, "#000000"),
    ("eq15_xor_sub2", r"\text{XOR Problem}", 14, "#FF0000"),
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