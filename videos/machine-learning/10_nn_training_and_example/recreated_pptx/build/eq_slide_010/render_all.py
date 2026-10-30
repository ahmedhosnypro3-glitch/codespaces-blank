#!/usr/bin/env python3
"""Render all slide_010 equations with sidecar JSON output."""
import json, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = "/home/codespace/.agents/skills/slide-recreation/scripts/render_eq.py"

EQS = [
    ("eq1", r'W_{ji}^{updated} = W_{ji}^{old} - \eta \frac{\partial E}{\partial W_{ji}}'),
    ("eq2", r'W_{ji}^{updated} = W_{ji}^{old} + \Delta_{ji}'),
    ("eq3", r'\Delta_{ji} = -\eta \frac{\partial E}{\partial W_{ji}}'),
    ("eq4", r'E = \frac{1}{2} \sum_j (t_j - O_j)^2'),
    ("eq5", r'O_j = f(Net_j) = \frac{1}{1+e^{-Net_j}}'),
    ("eq6", r'Net_j = \sum_i (w_{ji} O_i)'),
    ("eq7", r'\frac{\partial E}{\partial O_j} = -(t_j - O_j)'),
    ("eq8", r'\frac{\partial O_j}{\partial Net_j} = O_j(1-O_j)'),
    ("eq9", r'\frac{\partial Net_j}{\partial W_{ji}} = O_i'),
    ("eq10", r'\frac{\partial E}{\partial W_{ji}} = \frac{\partial E}{\partial O_j} \cdot \frac{\partial O_j}{\partial Net_j} \cdot \frac{\partial Net_j}{\partial W_{ji}}'),
    ("eq11", r'= \frac{\partial E}{\partial Net_j} \cdot \frac{\partial Net_j}{\partial W_{ji}}'),
    ("eq12", r'= -(t_j - O_j) \cdot O_j(1-O_j) \cdot O_i = -\delta_j \cdot O_i'),
    ("eq13", r'\delta_j = -\frac{\partial E}{\partial Net_j} = (t_j - O_j) \cdot O_j(1-O_j)'),
    ("eq14", r'\Delta_{ji} = -\eta \frac{\partial E}{\partial W_{ji}} = \eta \delta_j \cdot O_i'),
]

for name, latex in EQS:
    png = os.path.join(HERE, name + ".png")
    side = os.path.join(HERE, name + ".json")
    r = subprocess.run(["python3", RENDER, latex, png, "14", "000000"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"{name}: FAILED {r.stderr.strip()[:120]}")
        continue
    info = json.loads(r.stdout)
    info["latex"] = latex
    info["rel_path"] = f"./eq_slide_010/{name}.png"
    with open(side, "w") as f:
        json.dump(info, f, indent=2)
    print(f"{name}: {info['w_in']}x{info['h_in']}in baseline_frac={info['baseline_frac']}")