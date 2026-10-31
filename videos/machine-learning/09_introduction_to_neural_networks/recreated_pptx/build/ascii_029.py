from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB")
w, h = im.size
SW, SH = 13.33, 7.5

# Panel: x 0.94-7.55 in, y 1.93-5.36 in
x0, y0, x1, y1 = 0.94, 1.93, 7.55, 5.36
px0, py0 = int(x0 / SW * w), int(y0 / SH * h)
px1, py1 = int(x1 / SW * w), int(y1 / SH * h)
crop = im.crop((px0, py0, px1, py1))
print(f"crop {crop.size}")
CW, CH = 78, 26
small = crop.resize((CW, CH), Image.BOX)

# Column header: x in inches at each char
print("x-axis (in):", "".join("|" if int((i + 0.5) / CW * (x1 - x0) + x0) % 1 < 1.0 / CW * (x1 - x0) else " " for i in range(CW)))
labels = "".join(
    (f"{(i+0.5)/CW*(x1-x0)+x0:.0f}" if i % 10 == 0 else " ")
    for i in range(CW)
)
print("        ", labels)

for j in range(CH):
    row = []
    for i in range(CW):
        r, g, b = small.getpixel((i, j))
        if max(r, g, b) < 60:
            ch = "#"           # black text/outline
        elif r > 150 and r - g > 70 and r - b > 70:
            ch = "R"           # red
        elif b > 150 and b - r > 50 and b - g > 30:
            ch = "B"           # blue
        elif g > 120 and g - r > 40 and g - b > 40:
            ch = "G"           # green
        elif r > 190 and g > 150 and g < 200 and b > 190 and b < 235:
            ch = "M"           # magenta
        elif min(r, g, b) > 240:
            ch = "."           # white
        elif r - b > 18 and r > 195 and g > 180:
            ch = "p"           # beige panel
        else:
            ch = " "           # gray/other
        row.append(ch)
    print(f"{y0 + j / CH * (y1 - y0):5.2f}in |" + "".join(row))
