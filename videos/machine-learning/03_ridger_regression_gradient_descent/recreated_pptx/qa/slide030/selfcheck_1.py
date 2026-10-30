"""Self-check 1 — slide 030: label glyph comparison render vs original.
Render: render_1.png 2001x1125 (150dpi). Original: unique_slides/slide_030.jpg 960x540.
Scale: sx=2001/960, sy=1125/540."""
import numpy as np
from PIL import Image

DECK = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent'
ren = np.asarray(Image.open(DECK + '/recreated_pptx/qa/slide030/render_1.png').convert('RGB')).astype(int)
orig = np.asarray(Image.open(DECK + '/unique_slides/slide_030.jpg').convert('RGB')).astype(int)
SX, SY = 2001/960, 1125/540
print(f"render {ren.shape}, orig {orig.shape}, scale x={SX:.4f} y={SY:.4f}")

def ascii_render(name, fx0, fx1, fy0, fy1):
    x0, x1 = int(round(fx0*SX)), int(round(fx1*SX))
    y0, y1 = int(round(fy0*SY)), int(round(fy1*SY))
    sub = ren[y0:y1, x0:x1]
    ink = sub.sum(axis=2) < 600
    print(f"== RENDER {name} frame x{fx0}..{fx1} y{fy0}..{fy1} ==")
    for r in ink:
        print("   " + ''.join('#' if v else '.' for v in r))

def ascii_orig(name, fx0, fx1, fy0, fy1):
    sub = orig[fy0:fy1, fx0:fx1]
    ink = sub.sum(axis=2) < 600
    print(f"== ORIG {name} frame x{fx0}..{fx1} y{fy0}..{fy1} ==")
    for r in ink:
        print("   " + ''.join('#' if v else '.' for v in r))

# downsample render to frame-px scale for shape comparison? No - print render at 1 char per 2 render px
def ascii_render_half(name, fx0, fx1, fy0, fy1):
    x0, x1 = int(round(fx0*SX)), int(round(fx1*SX))
    y0, y1 = int(round(fy0*SY)), int(round(fy1*SY))
    sub = ren[y0:y1, x0:x1]
    ink = (sub.sum(axis=2) < 600)
    print(f"== RENDER(half-res) {name} frame x{fx0}..{fx1} y{fy0}..{fy1} ==")
    for r in ink[::2]:
        print("   " + ''.join('#' if v else '.' for v in r[::2]))

ascii_render_half("(7,7)-label", 716, 768, 134, 160)
ascii_render_half("(5,1)-label", 694, 734, 240, 262)
ascii_render_half("(2,10)-label", 626, 670, 144, 172)
