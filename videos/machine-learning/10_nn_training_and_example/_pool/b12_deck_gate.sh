#!/usr/bin/env bash
# End-to-end proof: render the merged final deck and pixel-compare pages
# 23 and 24 against the certified source renders.
# Evidence dir: qa/slide023/ + qa/slide024/ are NOT modified.
set -eu
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
Q="$NS/_pool/b12_deck_gate"
mkdir -p "$Q" "$NS/_pool/lo_b12_gate"
TMPDIR="$NS/_pool" soffice --headless \
  -env:UserInstallation=file://$NS/_pool/lo_b12_gate \
  --convert-to pdf --outdir "$Q" "$NS/10_nn_training_and_example_final.pptx" >/dev/null 2>&1
pdftoppm -png -r 150 "$Q/10_nn_training_and_example_final.pdf" "$Q/deck"
python3 - "$Q" <<'PY'
import sys, glob, os
from PIL import Image, ImageChops
import numpy as np
q = sys.argv[1]
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
pages = sorted(glob.glob(q + "/deck-*.png"))
print("deck pages rendered:", len(pages))
srcs = {
    23: NS + "/qa/slide023/rejudge/render-1.png",
    24: NS + "/qa/slide024/attempt4/render-1.png",
}
for n, sp in srcs.items():
    dp = [p for p in pages if int(os.path.basename(p).split("-")[-1].split(".")[0]) == n]
    if not dp:
        print("page", n, "NOT RENDERED")
        continue
    a = Image.open(dp[0]).convert("RGB")
    b = Image.open(sp).convert("RGB")
    w = min(a.size[0], b.size[0]); h = min(a.size[1], b.size[1])
    ca, cb = a.crop((0, 0, w, h)), b.crop((0, 0, w, h))
    d = np.array(ImageChops.difference(ca, cb))
    diff = int((d.sum(axis=2) > 0).sum())
    print("page %d deck=%s src=%s overlap=%dx%d differing_px=%d (%.4f%%) maxdelta=%d"
          % (n, a.size, b.size, w, h, diff, 100.0 * diff / (w * h), int(d.max())))
PY
