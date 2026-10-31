# Local helper: pixel measurements for slide 026 rejudge. Read-only diagnostics.
import sys
from PIL import Image

p = sys.argv[1]
im = Image.open(p).convert("RGB")
w, h = im.size
print(f"file={p} size={w}x{h} aspect={w/h:.4f}")
px = im.load()

def samp(x_in, y_in, tag):
    x = int(x_in / 13.33 * w)
    y = int(y_in / 7.5 * h)
    print(f"{tag}: x={x} y={y} rgb={px[x, y]}")

# house frame border at 0.15in
samp(0.15, 0.15, "frame_tl_border")
samp(0.15, 7.35, "frame_bl_border")
samp(13.18, 7.35, "frame_br_border")
samp(13.18, 0.15, "frame_tr_border")
# badge
samp(12.73, 0.55, "badge_center")
# title text band
samp(6.6, 0.55, "title_band")
# background between frame and content
samp(6.6, 7.3, "bg_bottom_center")
# footer box
samp(6.6, 6.6, "footer_box")
