#!/usr/bin/env python3
"""Glyph-level verification for slides 3 and 4.

Counts DARK GLYPH pixels inside each equation box (border excluded) so a
transparent PNG hidden under a solid fill is caught instead of being counted
as ink. Usage: verify_render_content.py
"""
import json
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
S = 2000 / 960


def px(v):
    return v * S


def dark_glyph_fraction(path, x0, y0, x1, y1):
    """Fraction of pixels inside the box that are dark ink (glyph or border)."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    reg = a[int(y0):int(y1), int(x0):int(x1)]
    lum = reg.mean(axis=2)
    return float((lum < 120).mean()), reg.shape[:2]


def report(name, path, boxes):
    print(f"=== {name} ({path.split('/')[-2]}) ===")
    for label, (x, y, w, h) in boxes.items():
        frac, size = dark_glyph_fraction(path, x, y, x + w, y + h)
        flag = "OK " if frac > 0.004 else "EMPTY"
        print(f"  [{flag}] {label}: glyph={100*frac:.2f}% region={size}")


def main():
    p3 = f"{ROOT}/recreated_pptx/qa/slide003/render-1.png"
    p4 = f"{ROOT}/recreated_pptx/qa/slide004/render-1.png"

    strip = px(405)
    report("slide 3", p3, {
        "For Layer j box (net_eq+o_eq)": (px(58) + 6, strip + 24, px(250) - 12, px(108)),
        "If Layer j is Output Layer (e_eq)": (px(740) + 6, strip + 24, px(175) - 12, px(58)),
        "diagram panel": (px(58), px(94), px(858), px(258)),
        "Node Bias strip": (px(60), px(358), px(340), px(60)),
    })
    s4 = {
        "eq1 definition box": (px(140) + 4, px(110) + 4, px(250), px(70)),
        "eq2 green f(x) box": (px(0), px(0), 0, 0),
        "derivation box 1 (eq3)": (px(140) + 6, px(250) + 4, px(490), px(66)),
        "derivation box 2 (eq4)": (px(140) + 6, px(330) + 4, px(490), px(66)),
        "derivation box 3 (eq5)": (px(140) + 6, px(410) + 4, px(490), px(66)),
        "result box (eq6)": (px(710), px(390), px(300), px(90)),
    }
    report("slide 4", p4, s4)


if __name__ == "__main__":
    main()
