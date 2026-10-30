#!/usr/bin/env python3
"""Create crop pairs for dense regions of slide 014."""
import numpy as np
from PIL import Image

# Render is 150dpi, 13.333x7.5in = 2000x1125 px (close to 2001x1125)
# Original is 960x540
# Scale factor = 2001/960 ≈ 2.084

render = Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/render_1.png")
orig = Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg")

print(f"Render: {render.size}, Orig: {orig.size}")

# Scale factor
H_render = render.height  # 1125
H_orig = orig.height      # 540
scale = H_render / H_orig  # ~2.083
print(f"Scale: {scale}")

# Dense regions (slide-space bbox in frame px, x0,y0,x1,y1 with 8px padding)
# 1. Vector boxes (y 95..240, x 50..900)
# 2. Ridge/Objective bands (y 248..340)
# 3. Define Loss band (y 390..410)
# 4. Loss/Reg term boxes (y 460..525)
# 5. Final band (y 510..525)

regions = [
    ("vector_boxes", 50, 95, 900, 240),
    ("ridge_objective", 50, 248, 900, 340),
    ("define_loss", 50, 390, 900, 410),
    ("loss_reg_terms", 50, 460, 900, 525),
    ("final_band", 50, 510, 900, 525),
]

for name, x0, y0, x1, y1 in regions:
    # Crop render (already at 150dpi)
    rx0, ry0 = int(x0 * scale), int(y0 * scale)
    rx1, ry1 = int(x1 * scale), int(y1 * scale)
    render_crop = render.crop((rx0, ry0, rx1, ry1))
    
    # Crop original and upscale to match render's effective scale
    orig_crop = orig.crop((x0, y0, x1, y1))
    # Upscale by LANCZOS
    orig_up = orig_crop.resize((rx1 - rx0, ry1 - ry0), Image.LANCZOS)
    
    out_dir = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/"
    render_crop.save(f"{out_dir}crop_1_{name}_render.png")
    orig_up.save(f"{out_dir}crop_1_{name}_orig.png")
    print(f"{name}: render crop {render_crop.size}, orig up {orig_up.size}")

print("Crop pairs created.")