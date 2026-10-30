import os
from PIL import Image
NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
im = Image.open(os.path.join(NS, "unique_slides", "slide_032.jpg")).convert("RGB")
px = im.load()
print("ASCII map x344..380 y315..356")
print("legend: # dark crimson | + crimson | o pinkish | . white | ' ' panel-gray")
print("      " + "".join(str((x // 10) % 10) for x in range(344, 380)))
print("      " + "".join(str(x % 10) for x in range(344, 380)))
for y in range(315, 356):
    row = ""
    for x in range(344, 380):
        r, g, b = px[x, y]
        s = r + g + b
        if s < 330:
            row += "#"
        elif s < 560:
            row += "+"
        elif r > 230 and g > 185 and b > 190 and s > 560:
            row += "o"
        elif r > 240 and g > 240 and b > 240:
            row += "."
        elif abs(r - 233) < 16 and abs(g - 233) < 16 and abs(b - 231) < 18:
            row += " "
        else:
            row += "o"
    print("y=%3d %s" % (y, row))

# also the box3 bottom edge and the y309 red line, per-row ink counts
print()
print("box3 paint counts per row (x340..620, non-panel non-white):")
for y in range(286, 330):
    n = 0
    for x in range(340, 620):
        r, g, b = px[x, y]
        if r > 240 and g > 240 and b > 240:
            continue
        if abs(r - 233) < 16 and abs(g - 233) < 16 and abs(b - 231) < 18:
            continue
        n += 1
    print("  y=%3d n=%d" % (y, n))
