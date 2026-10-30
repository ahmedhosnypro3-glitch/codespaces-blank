#!/usr/bin/env python3
"""Closed-loop PIL comparison for slide 23: render vs original frame."""
from PIL import Image, ImageChops
import numpy as np

def load(path):
    return Image.open(path).convert("RGB")

orig = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_023.jpg")
render = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/qa/slide023/render-1.png")

print(f"Original: {orig.size}, Render: {render.size}")

# Resize render to original size for comparison
render_resized = render.resize(orig.size, Image.LANCZOS)

# Full frame diff
diff = np.abs(np.asarray(orig).astype(int) - np.asarray(render_resized).astype(int))
print(f"\nFull frame: max_diff={diff.max():.1f}, mean_diff={diff.mean():.1f}")

# Check specific regions in original coordinates (960x540)
regions = {
    "badge_area": (860, 55, 895, 90),
    "top_area": (100, 100, 860, 150),
    "init_box": (250, 180, 710, 230),  # Initialization box
    "pick_box": (250, 240, 710, 290),   # Pick box
    "forward_box": (250, 300, 710, 350), # Forward box
    "backward_box": (250, 360, 710, 410), # Backward box
    "last_sample_diamond": (300, 420, 660, 480),
    "stop_criteria_diamond": (300, 500, 660, 560),
}

print("\n=== Slide 23 Regions ===")
for name, (x0, y0, x1, y1) in regions.items():
    orig_crop = np.asarray(orig.crop((x0, y0, x1, y1)))
    render_crop = np.asarray(render_resized.crop((x0, y0, x1, y1)))
    d = np.abs(orig_crop.astype(int) - render_crop.astype(int))
    max_d = d.max()
    mean_d = d.mean()
    # ink pixel count (non-background)
    bg_orig = np.array([255, 255, 255])  # white background in original
    bg_render = np.array([232, 232, 232])  # E8E8E8 gray in render
    orig_ink = np.abs(orig_crop - bg_orig).mean(axis=2) > 20
    render_ink = np.abs(render_crop - bg_render).mean(axis=2) > 20
    ink_match = (orig_ink == render_ink).mean()
    print(f"  {name}: max_diff={max_d:.1f}, mean_diff={mean_d:.1f}, ink_match={ink_match*100:.1f}%")

# Also check for key colored elements in render (CORRECTED for actual colors)
print("\n=== Checking key colored elements in render (ACTUAL COLORS) ===")
# Check for pale purple (Initialization) - F7BBF9 = (247,187,249)
init_area = render_resized.crop((250, 180, 710, 230))
init_arr = np.asarray(init_area)
is_pale_purple = (init_arr[:,:,0] > 220) & (init_arr[:,:,2] > 220) & (init_arr[:,:,1] < 210)
print(f"Initialization box pale purple pixels: {is_pale_purple.mean()*100:.1f}%")

# Check for pale cream (Pick) - FCFFF0 = (252,255,240)
pick_area = render_resized.crop((250, 240, 710, 290))
pick_arr = np.asarray(pick_area)
is_pale_cream = (pick_arr[:,:,0] > 240) & (pick_arr[:,:,1] > 240) & (pick_arr[:,:,2] > 220)
print(f"Pick box pale cream pixels: {is_pale_cream.mean()*100:.1f}%")

# Check for pale cream (Forward)
forward_area = render_resized.crop((250, 300, 710, 350))
forward_arr = np.asarray(forward_area)
is_pale_cream_f = (forward_arr[:,:,0] > 240) & (forward_arr[:,:,1] > 240) & (forward_arr[:,:,2] > 220)
print(f"Forward box pale cream pixels: {is_pale_cream_f.mean()*100:.1f}%")

# Check for pale cream (Last Sample diamond)
diamond_area = render_resized.crop((300, 420, 660, 480))
diamond_arr = np.asarray(diamond_area)
is_pale_cream_d = (diamond_arr[:,:,0] > 240) & (diamond_arr[:,:,1] > 240) & (diamond_arr[:,:,2] > 220)
print(f"Last Sample diamond pale cream pixels: {is_pale_cream_d.mean()*100:.1f}%")

# Check for red frame in render (should be at ~0.15in = 10.8pt = ~22px at 150dpi = ~10px at original scale)
frame_check = render_resized.crop((5, 5, 955, 535))
frame_arr = np.asarray(frame_check)
is_red_frame = (frame_arr[:,:,0] > 150) & (frame_arr[:,:,0] - frame_arr[:,:,1] > 50) & (frame_arr[:,:,0] - frame_arr[:,:,2] > 50)
print(f"Red frame border pixels: {is_red_frame.mean()*100:.1f}%")

# Check badge (pale yellow FFFFA2 = 255,255,162)
badge_area = render_resized.crop((860, 55, 895, 90))
badge_arr = np.asarray(badge_area)
is_pale_yellow_badge = (badge_arr[:,:,0] > 240) & (badge_arr[:,:,1] > 240) & (badge_arr[:,:,2] < 200)
print(f"Badge pale yellow pixels: {is_pale_yellow_badge.mean()*100:.1f}%")

# Check badge actual color
print(f"Badge mean color: {badge_arr.mean(axis=(0,1))}")