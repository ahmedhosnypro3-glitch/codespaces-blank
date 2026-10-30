#!/usr/bin/env python3
"""Closed-loop PIL comparison: render vs original frame."""
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
orig5 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_005.jpg")
render5 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/qa/slide005/render-1.png")

orig6 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_006.jpg")
render6 = load("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/qa/slide006/render-1.png")

print(f"Original 5: {orig5.size}, Render 5: {render5.size}")
print(f"Original 6: {orig6.size}, Render 6: {render6.size}")

# Scale factor: 1px = 1pt, 960px = 13.33in = 960pt, so render at 150dpi = 2000px
# Actually original is 960px, render at 150dpi of 13.33in = 2000px
# scale factor = 2000/960 = 2.083
scale = 2000/960
print(f"Scale factor: {scale}")

# Resize render to original size for comparison
render5_resized = render5.resize(orig5.size, Image.LANCZOS)
render6_resized = render6.resize(orig6.size, Image.LANCZOS)

# Full frame diff
diff5 = np.abs(np.asarray(orig5).astype(int) - np.asarray(render5_resized).astype(int))
diff6 = np.abs(np.asarray(orig6).astype(int) - np.asarray(render6_resized).astype(int))

print(f"\nSlide 5 full frame: max_diff={diff5.max():.1f}, mean_diff={diff5.mean():.1f}")
print(f"Slide 6 full frame: max_diff={diff6.max():.1f}, mean_diff={diff6.mean():.1f}")

# Define regions to check (x0,y0,x1,y1 in original 960x540 coordinates)
regions5 = {
    "title": (70, 40, 300, 90),
    "badge": (860, 55, 895, 90),
    "box1_top": (70, 100, 880, 180),
    "box1_mid": (70, 180, 840, 350),
    "box2_top": (70, 250, 880, 320),
    "box2_mid": (70, 320, 880, 450),
    "box3_top": (70, 360, 840, 440),
    "box3_bottom": (70, 470, 840, 500),
}

regions6 = {
    "title_line1": (320, 200, 650, 250),
    "title_line2": (370, 270, 610, 310),
    "subtitle": (210, 320, 770, 350),
    "badge": (860, 55, 895, 90),
    "frame_top": (40, 40, 920, 60),
    "frame_left": (40, 40, 60, 500),
    "frame_right": (900, 40, 920, 500),
    "bottom_bar": (0, 500, 960, 540),
}

compare_regions(orig5, render5_resized, scale, regions5, "Slide 5 Regions")
compare_regions(orig6, render6_resized, scale, regions6, "Slide 6 Regions")

# Also check for specific elements
# Check if highlight boxes exist in render
print("\n=== Checking highlight box backgrounds ===")
# Box 1 light blue region
box1_area = render5_resized.crop((70, 100, 880, 350))
box1_arr = np.asarray(box1_area)
# Check for light blue tint
blue_channel = box1_arr[:,:,2]
green_channel = box1_arr[:,:,1]
red_channel = box1_arr[:,:,0]
is_blue = (blue_channel > red_channel + 30) & (blue_channel > green_channel + 30)
print(f"Slide 5 box1 area blue pixels: {is_blue.mean()*100:.1f}%")

# Box 2 light yellow
box2_area = render5_resized.crop((70, 250, 880, 450))
box2_arr = np.asarray(box2_area)
is_yellow = (box2_arr[:,:,0] > 200) & (box2_arr[:,:,1] > 200) & (box2_arr[:,:,2] < 180)
print(f"Slide 5 box2 area yellow pixels: {is_yellow.mean()*100:.1f}%")

# Box 3 light green
box3_area = render5_resized.crop((70, 360, 840, 500))
box3_arr = np.asarray(box3_area)
is_green = (box3_arr[:,:,1] > box3_arr[:,:,0] + 30) & (box3_arr[:,:,1] > box3_arr[:,:,2] + 30)
print(f"Slide 5 box3 area green pixels: {is_green.mean()*100:.1f}%")

# Slide 6 - check frame
frame_area = render6_resized.crop((40, 40, 920, 500))
frame_arr = np.asarray(frame_area)
# Check for red frame border
is_red = (frame_arr[:,:,0] > 150) & (frame_arr[:,:,0] - frame_arr[:,:,1] > 50) & (frame_arr[:,:,0] - frame_arr[:,:,2] > 50)
print(f"Slide 6 frame area red pixels: {is_red.mean()*100:.1f}%")