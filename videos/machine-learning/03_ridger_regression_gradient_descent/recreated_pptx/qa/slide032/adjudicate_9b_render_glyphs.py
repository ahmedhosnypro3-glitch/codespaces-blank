#!/usr/bin/env python3
"""Adjudicate_9b — render-side glyph reading at 1:1 for the RIGHT label.

The render is 2001x1125 = 2.0833 render px per frame px, so every glyph must be
read at native render resolution (1 char = 1 render px), not subsampled.
"""
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
REND = V + "/recreated_pptx/qa/slide032/render_9.png"
ORIG = V + "/unique_slides/slide_032.jpg"

r = np.asarray(Image.open(REND).convert("L")).astype(int)
o = np.asarray(Image.open(ORIG).convert("L")).astype(int)
S = r.shape[0] / 540.0
print(f"REND {r.shape[1]}x{r.shape[0]}  S={S:.4f}\n")


def rmap(x0, y0, x1, y1, tag):
    sub = r[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    print(f"--- {tag}: render px x{int(x0*S)}..{int(x1*S)} "
          f"y{int(y0*S)}..{int(y1*S)}  (frame x{x0}..{x1} y{y0}..{y1}) ---")
    for ry in range(sub.shape[0]):
        ROW = "".join("#" if v < 120 else ("+" if v < 175 else ("." if v < 225 else " "))
                      for v in sub[ry, :])
        print(f"  y{int(y0*S)+ry:>4} {ROW}")
    print()


# RIGHT label: build draws "(7, 7)" at x724 w30 y140 h13 -> frame x724..754, y140..153
# native render px: 1509..1571, 291..319
rmap(718, 138, 762, 158, "REND9 RIGHT label — full run")
# LEFT label: build draws "(2, 10)" at x619 w40 y149 h14 -> frame x619..659, y149..163
rmap(614, 145, 666, 166, "REND9 LEFT label '(2, 10)'")
# VERTEX label: build draws "(5, 1)" at x694 w36 y244 h14
rmap(690, 240, 742, 260, "REND9 VERTEX label '(5, 1)'")

# ORIG at native 1px: the same right-label run for the reference "7" and "(" shapes
sub = o[138:158, 716:762]
print("--- ORIG right-label window x716..762 y138..158 (1 char = 1 frame px) ---")
for ry in range(sub.shape[0]):
    ROW = "".join("#" if v < 120 else ("+" if v < 175 else ("." if v < 225 else " "))
                  for v in sub[ry, :])
    print(f"  y{138 + ry:>3} {ROW}")
