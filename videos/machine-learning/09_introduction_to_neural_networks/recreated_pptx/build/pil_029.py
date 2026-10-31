from PIL import Image
import sys

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"

def report(p, label):
    try:
        im = Image.open(p).convert("RGB")
    except Exception as e:
        print(f"{label}: FAILED {e}")
        return
    print(f"{label}: {p}")
    print(f"  size={im.size} mode=RGB")
    small = im.resize((160, 90))
    px = list(small.getdata())
    n = len(px)
    mean = tuple(round(sum(c[i] for c in px) / n, 1) for i in range(3))
    print(f"  mean(160x90)={mean}")
    # histogram-ish: count of near-white and near-black
    white = sum(1 for c in px if min(c) > 235)
    black = sum(1 for c in px if max(c) < 30)
    print(f"  near-white={white}/{n} ({100*white/n:.1f}%) near-black={black}/{n} ({100*black/n:.1f}%)")
    # sample some pixels
    w, h = im.size
    for name, fx, fy in [
        ("bg_topleft", 0.02, 0.02), ("bg_center", 0.5, 0.5),
        ("title_area", 0.5, 0.12), ("badge_area", 0.915, 0.13),
        ("panel_left", 0.10, 0.45), ("diagram", 0.30, 0.45),
        ("errbar", 0.59, 0.45), ("legend", 0.80, 0.32),
        ("bottom_formula", 0.20, 0.87), ("bottom_bar_orig", 0.5, 0.985),
    ]:
        print(f"    px[{name}]={im.getpixel((int(fx*w), int(fy*h)))}")
    print()

for p, lab in [
    (f"{V}/unique_slides/slide_029.jpg", "ORIGINAL"),
    (f"{V}/recreated_pptx/build/slide_029_recreated.pptx", "SOURCE PPTX"),
    (f"{V}/recreated_pptx/build/slide_029_rendered-1.png", "PREV RENDER (build)"),
    (f"{V}/recreated_pptx/qa/slide029/render_1.png", "PREV RENDER (qa)"),
]:
    report(p, lab)
