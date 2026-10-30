#!/usr/bin/env python3
"""Find all circle-like colored blobs in each box of slide 33."""
from PIL import Image

img = Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_033.jpg').convert('RGB')
W, H = img.size
px = img.load()
IN = W / 13.33


def is_ink(p):
    r, g, b = p
    return (max(p) - min(p)) > 28


def find_circles(y0, y1, label):
    print(f"\n=== {label}: blobs of colored ink, size 0.20-0.60in ===")
    seen = [[False] * W for _ in range(y1 - y0)]
    for yy in range(y0, y1):
        for xx in range(W):
            if seen[yy - y0][xx] or not is_ink(px[xx, yy]):
                continue
            st = [(xx, yy)]
            seen[yy - y0][xx] = True
            pts = []
            while st:
                cx, cy = st.pop()
                pts.append((cx, cy))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = cx + dx, cy + dy
                        if y0 <= ny < y1 and 0 <= nx < W and not seen[ny - y0][nx] and is_ink(px[nx, ny]):
                            seen[ny - y0][nx] = True
                            st.append((nx, ny))
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            w_in, h_in = (max(xs) - min(xs)) / IN, (max(ys) - min(ys)) / IN
            if 0.19 <= w_in <= 0.62 and 0.19 <= h_in <= 0.62 and len(pts) > 150:
                cx, cy = sum(xs) / len(pts), sum(ys) / len(pts)
                c = px[int(cx), int(cy)]
                print(f"  center_in=({cx/IN:.2f},{cy/IN:.2f}) w={w_in:.2f} h={h_in:.2f} n={len(pts)} color={c}")


find_circles(90, 290, "BOX A (top)")
find_circles(330, 530, "BOX B (bottom)")
