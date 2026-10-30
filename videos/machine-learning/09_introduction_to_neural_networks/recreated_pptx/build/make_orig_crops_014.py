from PIL import Image, ImageDraw

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_014.jpg").convert("RGB")
tiles = [
    ("A", (560, 95, 780, 300), 3),    # threshold legend + O/P area
    ("B", (55, 88, 470, 300), 2),     # diagram left: inputs + input weights
    ("C", (380, 88, 700, 300), 3),    # diagram right: neurons, step box, O/P
    ("D", (50, 278, 700, 512), 2),    # equation block
    ("E", (680, 265, 960, 512), 3),   # inset single-perceptron box
]
crops = []
for name, box, scale in tiles:
    c = im.crop(box).resize(((box[2]-box[0])*scale, (box[3]-box[1])*scale), Image.LANCZOS)
    d = ImageDraw.Draw(c)
    d.rectangle([0, 0, 22, 22], fill=(255, 255, 0))
    d.text((6, 5), name, fill=(0, 0, 0))
    crops.append(c)

W = max(c.width for c in crops)
H = sum(c.height for c in crops) + 12*(len(crops)-1)
out = Image.new("RGB", (W, H), (255, 255, 255))
y = 0
for c in crops:
    out.paste(c, (0, y)); y += c.height + 12
p = f"{V}/recreated_pptx/qa/slide014/orig_crops_composite.png"
out.save(p)
print(p, out.size)
