#!/usr/bin/env python3
"""Render all slide_010 v2 equations (mathtext 600dpi PNG + sidecar JSON)."""
import json, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = "/home/codespace/.agents/skills/slide-recreation/scripts/render_eq.py"

BLK, RED = "000000", "C00000"
EQS = [
    ("eq1",  r'W_{ji}^{updated} = W_{ji}^{old} - \eta \frac{\partial E}{\partial W_{ji}}', BLK),
    ("eq2",  r'W_{ji}^{updated} = W_{ji}^{old} + \Delta_{ji}', BLK),
    ("eq3",  r'\Delta_{ji} = -\eta \frac{\partial E}{\partial W_{ji}}', BLK),
    ("eq4",  r'E = \frac{1}{2} \sum_j (t_j - O_j)^2', BLK),
    ("eq5",  r'O_j = f(Net_j) = \frac{1}{1+e^{-Net_j}}', BLK),
    ("eq6",  r'Net_j = \sum_i (w_{ji} O_i)', BLK),
    ("eq7",  r'\frac{\partial E}{\partial O_j} = -(t_j - O_j)', BLK),
    ("eq8",  r'\frac{\partial O_j}{\partial Net_j} = O_j(1-O_j)', BLK),
    ("eq9",  r'\frac{\partial Net_j}{\partial W_{ji}} = O_i', BLK),
    ("eq10", r'\frac{\partial E}{\partial W_{ji}} = \frac{\partial E}{\partial O_j} \cdot \frac{\partial O_j}{\partial Net_j} \cdot \frac{\partial Net_j}{\partial W_{ji}} = \frac{\partial E}{\partial Net_j} \cdot \frac{\partial Net_j}{\partial W_{ji}}', BLK),
    ("eq11", r'= -(t_j - O_j) \cdot O_j(1-O_j) \cdot O_i = -\delta_j \cdot O_i', BLK),
    ("eq12", r'\delta_j = -\frac{\partial E}{\partial Net_j} = (t_j - O_j) \cdot O_j(1-O_j) \quad (\delta_j \mathrm{\ depends\ on\ } j \mathrm{\ ONLY})', BLK),
    ("eq13", r'\Delta_{ji} = -\eta \frac{\partial E}{\partial W_{ji}} = \eta \delta_j \cdot O_i', RED),
    ("eq14", r'\delta_j = (t_j - O_j) \cdot O_j(1-O_j) \ \mathrm{for\ output\ Layer}', RED),
]

for name, latex, color in EQS:
    png = os.path.join(HERE, name + ".png")
    side = os.path.join(HERE, name + ".json")
    r = subprocess.run(["python3", RENDER, latex, png, "14", color],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"{name}: FAILED {r.stderr.strip()[:150]}")
        continue
    info = json.loads(r.stdout)
    info["latex"] = latex
    info["rel_path"] = f"./eq_slide_010b/{name}.png"
    with open(side, "w") as f:
        json.dump(info, f, indent=2)
    print(f"{name}: {info['w_in']:.3f}x{info['h_in']:.3f}in color={color}")
