#!/usr/bin/env python3
"""Closed-loop PIL comparison: render vs original frame for slides 3 and 4."""
from PIL import Image, ImageChops
import numpy as np

def load(path):
    return Image.open(path).convert("RGB")

def compare_regions(orig, render, scale_factor, regions, label):
    """Compare specific regions between original and render."""
    orig_arr = np.asarray(orig)
    render_arr = np.asarray(render.resize(orig.size, Image.LANCZOS))
    
    print(f"\n=== {label} ===")
    for name, (x0, y0, x1, y1) in regions.items():
        orig_crop = orig_arr[y0:y1, x0:x1]
        render_crop = render_arr[y0:y1, x0:x1]
        diff = np.abs(orig_crop.astype(int) - render_crop.astype(int))
        max_diff = diff.max()
        mean_diff = diff.mean()
        # ink pixel count (non-background)
        bg = np.array([240, 240, 240])  # approximate gray bg
        orig_ink = np.abs(orig_crop - bg).mean(axis=2) > 20
        render_ink = np.abs(render_crop - bg).mean(axis=2) > 20
        ink_match = (orig_ink == render_ink).mean()
        print(f"  {name}: max_diff={max_diff:.1f}, mean_diff={mean_diff:.1f}, ink_match={ink_match*100:.1f}%")

# Load images
orig3 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_003.jpg")
render3 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/qa/slide003/render-1.png")

orig4 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_004.jpg")
render4 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/qa/slide004/render-1.png")

print(f"Original 3: {orig3.size}, Render 3: {render3.size}")
print(f"Original 4: {orig4.size}, Render 4: {render4.size}")

# Scale factor: original is 960px, render at 150dpi of 13.33in = 2000px
scale = 2000/960
print(f"Scale factor: {scale}")

# Resize render to original size for comparison
render3_resized = render3.resize(orig3.size, Image.LANCZOS)
render4_resized = render4.resize(orig4.size, Image.LANCZOS)

# Full frame diff
diff3 = np.abs(np.asarray(orig3).astype(int) - np.asarray(render3_resized).astype(int))
diff4 = np.abs(np.asarray(orig4).astype(int) - np.asarray(render4_resized).astype(int))

print(f"\nSlide 3 full frame: max_diff={diff3.max():.1f}, mean_diff={diff3.mean():.1f}")
print(f"Slide 4 full frame: max_diff={diff4.max():.1f}, mean_diff={diff4.mean():.1f}")

# Define regions to check (x0,y0,x1,y1 in original 960x540 coordinates)
regions3 = {
    "title": (70, 40, 300, 90),
    "badge": (860, 55, 895, 90),
    "diagram_area": (70, 100, 880, 400),
    "error_bar": (800, 100, 850, 400),
    "class_boxes": (850, 100, 920, 400),
    "bottom_annotations": (70, 400, 880, 500),
    "frame_top": (40, 40, 920, 60),
    "frame_left": (40, 40, 60, 500),
    "frame_right": (900, 40, 920, 500),
    "bottom_bar": (0, 500, 960, 540),
}

regions4 = {
    "title": (320, 200, 650, 250),
    "badge": (860, 55, 895, 90),
    "top_row_boxes": (70, 100, 880, 200),
    "sigmoid_graph": (600, 80, 920, 200),
    "derivation_middle": (70, 200, 880, 400),
    "bottom_row": (70, 400, 880, 500),
    "frame_top": (40, 40, 920, 60),
    "frame_left": (40, 40, 60, 500),
    "frame_right": (900, 40, 920, 500),
    "bottom_bar": (0, 500, 960, 540),
}

compare_regions(orig3, render3_resized, scale, regions3, "Slide 3 Regions")
compare_regions(orig4, render4_resized, scale, regions4, "Slide 4 Regions")

# Also check for specific elements
print("\n=== Checking house chrome (red frame, yellow badge) ===")

# Slide 3 - check red frame
frame_area3 = render3_resized.crop((40, 40, 920, 500))
frame_arr3 = np.asarray(frame_area3)
is_red3 = (frame_arr3[:,:,0] > 150) & (frame_arr3[:,:,0] - frame_arr3[:,:,1] > 50) & (frame_arr3[:,:,0] - frame_arr3[:,:,2] > 50)
print(f"Slide 3 frame area red pixels: {is_red3.mean()*100:.1f}%")

# Slide 3 - check yellow badge
badge_area3 = render3_resized.crop((860, 55, 895, 90))
badge_arr3 = np.asarray(badge_area3)
is_yellow3 = (badge_arr3[:,:,0] > 200) & (badge_arr3[:,:,1] > 200) & (badge_arr3[:,:,2] < 180)
print(f"Slide 3 badge area yellow pixels: {is_yellow3.mean()*100:.1f}%")

# Slide 4 - check red frame
frame_area4 = render4_resized.crop((40, 40, 920, 500))
frame_arr4 = np.asarray(frame_area4)
is_red4 = (frame_arr4[:,:,0] > 150) & (frame_arr4[:,:,0] - frame_arr4[:,:,1] > 50) & (frame_arr4[:,:,0] - frame_arr4[:,:,2] > 50)
print(f"Slide 4 frame area red pixels: {is_red4.mean()*100:.1f}%")

# Slide 4 - check yellow badge
badge_area4 = render4_resized.crop((860, 55, 895, 90))
badge_arr4 = np.asarray(badge_area4)
is_yellow4 = (badge_arr4[:,:,0] > 200) & (badge_arr4[:,:,1] > 200) & (badge_arr4[:,:,2] < 180)
print(f"Slide 4 badge area yellow pixels: {is_yellow4.mean()*100:.1f}%")

# Check beige background for slide 3
diag_area3 = render3_resized.crop((70, 100, 880, 400))
diag_arr3 = np.asarray(diag_area3)
is_beige3 = (diag_arr3[:,:,0] > 200) & (diag_arr3[:,:,1] > 200) & (diag_arr3[:,:,2] > 180) & (diag_arr3[:,:,2] < 240)
print(f"Slide 3 diagram area beige pixels: {is_beige3.mean()*100:.1f}%")

# Check gray background for slide 4
bg_area4 = render4_resized.crop((40, 40, 920, 500))
bg_arr4 = np.asarray(bg_area4)
is_gray4 = (np.abs(bg_arr4[:,:,0] - bg_arr4[:,:,1]) < 20) & (np.abs(bg_arr4[:,:,1] - bg_arr4[:,:,2]) < 20) & (bg_arr4[:,:,0] > 200) & (bg_arr4[:,:,0] < 240)
print(f"Slide 4 background gray pixels: {is_gray4.mean()*100:.1f}%")