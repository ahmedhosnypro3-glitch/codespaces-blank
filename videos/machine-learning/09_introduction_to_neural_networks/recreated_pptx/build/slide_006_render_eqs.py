#!/usr/bin/env python3
"""
Generate equation PNGs for slide 006.

Three equations for multi-class single-layer perceptron:
1. d_1(X) = W_1^T X = w_{11}x_1 + w_{12}x_2 + ... + w_{1n}x_n + b_1 * 1
2. d_2(X) = W_2^T X = w_{21}x_1 + w_{22}x_2 + ... + w_{2n}x_n + b_2 * 1
3. d_m(X) = W_m^T X = w_{m1}x_1 + w_{m2}x_2 + ... + w_{mn}x_n + b_m * 1
"""

import subprocess
import json
from pathlib import Path

BUILD_DIR = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build")
RENDER_SCRIPT = "/home/codespace/ai_llm_slides/scripts/render_eq.py"

# Equations in mathtext format (WITHOUT $ delimiters - render_eq.py adds them)
equations = [
    ("eq_s006_d1", r"d_1(X) = W_1^T X = w_{11}x_1 + w_{12}x_2 + ... + w_{1n}x_n + b_1 \cdot 1"),
    ("eq_s006_d2", r"d_2(X) = W_2^T X = w_{21}x_1 + w_{22}x_2 + ... + w_{2n}x_n + b_2 \cdot 1"),
    ("eq_s006_dm", r"d_m(X) = W_m^T X = w_{m1}x_1 + w_{m2}x_2 + ... + w_{mn}x_n + b_m \cdot 1"),
]

results = []
for name, mathtext in equations:
    out_png = BUILD_DIR / f"{name}.png"
    # Render at 18pt, black color
    cmd = [
        "python3", RENDER_SCRIPT,
        mathtext, str(out_png), "18", "#000000"
    ]
    print(f"Rendering {name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR rendering {name}:")
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(1)
    
    print(result.stdout.strip())
    
    # Load sidecar JSON for dimensions
    try:
        sidecar = json.loads(result.stdout)
        results.append({
            "name": name,
            "mathtext": mathtext,
            "png": str(out_png),
            "sidecar": sidecar,
        })
    except json.JSONDecodeError:
        # If stdout has extra lines, try to find JSON
        lines = result.stdout.strip().split('\n')
        for line in lines:
            try:
                sidecar = json.loads(line)
                results.append({
                    "name": name,
                    "mathtext": mathtext,
                    "png": str(out_png),
                    "sidecar": sidecar,
                })
                break
            except json.JSONDecodeError:
                continue

# Save combined manifest
manifest_path = BUILD_DIR / "slide_006_equations.json"
with open(manifest_path, "w") as f:
    json.dump({
        "slide": "006",
        "equations": [
            {
                "name": r["name"],
                "mathtext": r["mathtext"],
                "image": f"{r['name']}.png",
                "font_size_pt": 18.0,
                "color": "#000000",
                "sidecar": r["sidecar"],
            }
            for r in results
        ]
    }, f, indent=2)

print(f"\nManifest saved to {manifest_path}")
print("\nEquation PNGs and manifest complete.")