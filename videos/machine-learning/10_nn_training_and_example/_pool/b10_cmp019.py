"""Build matched-scale region comparison images for slide 019 adjudication.

Original frame is 960x540 (=72.03 px/in); render is 2001x1125 (=150.08 px/in).
Scale = 2001/960 = 2.0844. Each output PNG stacks ORIGINAL (upscaled to render
scale) above RENDER so a judge/vision sees the same region at matched scale.
"""
import sys
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SCALE = 2001.0 / 960.0

# region name -> bbox in ORIGINAL pixel coords (x0,y0,x1,y1)
REGIONS = {
    "eqbox":   (30, 190, 660, 300),
    "diagram": (395, 60, 930, 400),
    "cyan":    (30, 55, 420, 300),
    "right":   (650, 300, 960, 520),
    "legend":  (395, 330, 930, 420),
    "lhs":     (20, 190, 200, 290),
    "tail":    (520, 190, 700, 300),
    "full":    (0, 0, 960, 540),
}


def build(name, orig_path, render_path, out_path):
    x0, y0, x1, y1 = REGIONS[name]
    o = Image.open(orig_path).convert("RGB").crop((x0, y0, x1, y1))
    r = Image.open(render_path).convert("RGB").crop(
        (int(x0 * SCALE), int(y0 * SCALE), int(x1 * SCALE), int(y1 * SCALE)))
    w = max(o.width, r.width)
    o = o.resize((w, int(o.height * w / o.width)), Image.LANCZOS)
    r = r.resize((w, int(r.height * w / r.width)), Image.LANCZOS)
    canvas = Image.new("RGB", (w, o.height + r.height + 6), (255, 0, 255))
    canvas.paste(o, (0, 0))
    canvas.paste(r, (0, o.height + 6))
    canvas.save(out_path)
    print(name, "orig crop", (x0, y0, x1, y1), "->", out_path, canvas.size)


if __name__ == "__main__":
    name = sys.argv[1]
    orig = sys.argv[2] if len(sys.argv) > 2 else f"{NS}/unique_slides/slide_019.jpg"
    render = sys.argv[3] if len(sys.argv) > 3 else f"{NS}/qa/slide019/rejudge/render-4.png"
    out = sys.argv[4] if len(sys.argv) > 4 else f"{NS}/qa/slide019/rejudge/crops019/cmp_{name}.png"
    build(name, orig, render, out)
