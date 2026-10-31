#!/usr/bin/env python3
"""Lane G (b_geom_4): sample colours at corresponding points in original vs
render (both on the 960x540 frame grid) to build element masks."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"

SAMPLES = {
    "025": [(60, 170), (60, 245), (845, 140), (100, 330), (60, 350), (380, 380),
            (150, 130), (60, 90)],
    "026": [(480, 240), (480, 300), (480, 355), (890, 65)],
    "027": [(200, 120), (60, 300), (700, 300), (60, 470), (200, 60)],
    "029": [(150, 210), (175, 250), (670, 260), (480, 300)],
    "032": [(110, 95), (350, 130), (110, 335), (600, 400)],
}


def main():
    for n, pts in SAMPLES.items():
        o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
        r = np.asarray(Image.open(f"{TMP}/png_{n}/render-1.png").convert("RGB")).astype(int)
        rf = np.asarray(Image.fromarray(r.astype("uint8")).resize((960, 540), Image.BOX)).astype(int)
        print(f"##### slide {n}")
        for (x, y) in pts:
            print(f"  ({x:4d},{y:4d}) ORIG {o[y, x].tolist()}  REND {rf[y, x].tolist()}")


if __name__ == "__main__":
    main()
