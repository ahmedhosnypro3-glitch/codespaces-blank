#!/usr/bin/env python3
"""Render slide-050 equation PNGs (mathtext -> 600dpi transparent PNG).

mathtext in this env no longer supports \\begin{array}; the stacked column
vector is produced with \\left( \\substack{a\\\\b} \\right) which renders a
proper 2D stack inside parentheses (professional format).
"""
import os
import subprocess
import sys

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
ASSETS = os.path.join(
    ROOT,
    "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets",
)

BS = chr(92)
NB = BS + BS


def col(top, bot):
    return BS + "left( " + BS + "substack{" + str(top) + NB + str(bot) + "} " + BS + "right)"


JOBS = [
    ("eq_050_initialW.png", "Initial" + BS + " W = " + col(4, -2), 13, "000000"),
    ("eq_050_finalW.png", BS + "underline{W} = " + BS + "left( " + BS + "substack{" + "5" + NB + "-1" + NB + "-1" + "} " + BS + "right)", 13, "000000"),
    ("eq_050_Z1.png", col(0, 0), 12, "000000"),
    ("eq_050_Z2.png", col(7, 6), 12, "000000"),
    ("eq_050_Z3.png", col(3, 2), 12, "000000"),
    ("eq_050_eta.png", BS + "eta = 1", 13, "C00000"),
]

for name, latex, fs, color in JOBS:
    out = os.path.join(ASSETS, name)
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts/render_eq.py"), latex, out, str(fs), color],
        capture_output=True, text=True, cwd=ROOT,
    )
    line = r.stdout.strip()
    if r.returncode == 0:
        import json
        info = json.loads(line)
        print("OK   %-22s %dx%d px  (%.3f x %.3f in)  baseline_frac=%.3f"
              % (name, info["w_px"], info["h_px"], info["w_in"], info["h_in"], info["baseline_frac"]))
    else:
        print("FAIL %-22s %s" % (name, r.stderr.strip()[-160:]))
