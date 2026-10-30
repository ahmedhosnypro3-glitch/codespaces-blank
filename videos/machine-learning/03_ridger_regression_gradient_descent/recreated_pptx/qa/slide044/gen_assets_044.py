#!/usr/bin/env python3
"""Render slide_044 equation assets (mathtext -> 600dpi transparent PNG + sidecar).

Content: analysis/slide_044_final.json (verbatim), with the Initial W bracket
re-measured from unique_slides/slide_044.jpg (the frame's bracket shows THREE
glyph stacks: 4 / -2 / -2, y62..102 between strokes x331 and x353).
"""
import json, os, subprocess, sys

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ASSETS = f"{DECK}/recreated_pptx/build/assets/"
RENDER = "/workspaces/codespaces-blank/ai_llm_slides/scripts/render_eq.py"

EQS = {
    # centre text
    "eq_044_initw": (r"\mathrm{Initial}\; W = [4; \; -2; \; -2]", 20, "000000"),
    "eq_044_step":  (r"\mathrm{Step}\; \eta = 2",                  20, "C00000"),
    # d(x_i) rows  (spec verbatim)
    "eq_044_dx1":   (r"d(x_1) = [1 \; 1 \; 1; \; -12; \; -8] = -12", 20, "000000"),
    "eq_044_dx2":   (r"d(x_2) = [1 \; 2 \; 1; \; -10; \; -6] = -16", 20, "000000"),
    "eq_044_dx3":   (r"d(x_3) = [1 \; 1 \; 2; \; -6; \; -2] = -4",   20, "000000"),
    "eq_044_dx4":   (r"d(x_4) = [1 \; 5 \; 4; \; -4; \; 0] = -6",    20, "000000"),
    "eq_044_dx5":   (r"d(x_5) = [1 \; 6 \; 5; \; -14; \; -10] = -10",20, "000000"),
    "eq_044_dx6":   (r"d(x_6) = [1 \; 6 \; 6; \; -14; \; -4] = -4",  20, "000000"),
    # W-update rows (spec verbatim)
    "eq_044_w1":    (r"W = [4; \; -2] + 2 * [3; \; -2] = [10; \; -6]", 20, "C00000"),
    "eq_044_w2":    (r"W = [10; \; -6] + 2 * [1; \; 1] = [12; \; -4]", 20, "C00000"),
    "eq_044_w3":    (r"W = [12; \; -4] + 2 * [1; \; 0] = [14; \; -4]", 20, "C00000"),
    "eq_044_w4":    (r"W = [14; \; -4]", 20, "000000"),
    "eq_044_w5":    (r"W = [14; \; -4]", 20, "000000"),
    "eq_044_w6":    (r"W = [14; \; -4]", 20, "000000"),
}

for name, (latex, fs, color) in EQS.items():
    png = ASSETS + name + ".png"
    js = ASSETS + name + ".json"
    out = subprocess.run([sys.executable, RENDER, latex, png, str(fs), color],
                         capture_output=True, text=True)
    if out.returncode != 0:
        print("FAIL", name, out.stderr.strip()[:300]); sys.exit(1)
    info = json.loads(out.stdout)
    info["mathtext"] = latex
    info["font_size_pt"] = fs
    info["color"] = color
    json.dump(info, open(js, "w"), indent=1)
    print(f"{name}: w_in={info['w_in']} h_in={info['h_in']} bf={info['baseline_frac']}")
print("OK")
