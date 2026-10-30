#!/usr/bin/env python3
"""Procedure B crop-pairs for slide_004 render_2, at matched effective scale."""
from PIL import Image

QA = ('/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/'
      '03_ridger_regression_gradient_descent/recreated_pptx/qa/slide004')
ORIG = ('/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/'
        '03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg')

render = Image.open(QA + '/render_2.png').convert('RGB')
orig = Image.open(ORIG).convert('RGB')
RH = render.size[1]
S = RH / 540.0
print(f'render {render.size}  scale {S:.4f}')

REGIONS = {
    # densest regions: the 2D vector equation stack + label boxes,
    # and the bottom Define+Formula band.
    'label_boxes': (70, 90, 750, 230,
                    'Original Labels box (left) and Predicted Labels box (right) with their 2D column-vector equations'),
    'bottom': (70, 380, 495, 530,
               'Objective box, Error box, Define box and Formula box (the two densest full-width bands)'),
}

for name, (x0, y0, x1, y1, desc) in REGIONS.items():
    fw, fh = x1 - x0, y1 - y0
    rw, rh = int(round(fw * S)), int(round(fh * S))
    rx, ry = int(round(x0 * S)), int(round(y0 * S))
    rc = render.crop((rx, ry, rx + rw, ry + rh))
    oc = orig.crop((x0, y0, x1, y1))
    oc_up = oc.resize((rw, rh), Image.LANCZOS)
    rc.save(f'{QA}/crop_2_{name}_render.png')
    oc_up.save(f'{QA}/crop_2_{name}_orig.png')
    print(f'{name}: render {rc.size} | orig upscaled {oc_up.size} (frame {fw}x{fh}) | {desc}')
