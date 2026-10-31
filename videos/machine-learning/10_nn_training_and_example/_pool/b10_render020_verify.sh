#!/usr/bin/env bash
set -eu
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
PROF="$NS/_pool/lo_b10_020_final"; TMPD="$NS/_pool/tmp_b10"; OUT="$NS/qa/slide020/rejudge"
mkdir -p "$PROF" "$TMPD"
TMPDIR="$TMPD" soffice --headless -env:UserInstallation=file://$PROF \
  --convert-to pdf --outdir "$TMPD" "$NS/recreated_pptx/slide_020_recreated.pptx" >/dev/null 2>&1
mv "$TMPD/slide_020_recreated.pdf" "$OUT/slide_020_recreated.pdf"
pdftoppm -png -r 150 "$OUT/slide_020_recreated.pdf" "$OUT/render-verify"
python3 - "$OUT" <<'PY'
import sys, glob
from PIL import Image, ImageChops
import numpy as np
out = sys.argv[1]
vp = sorted(glob.glob(out + "/render-verify-*.png"))[0]
a = Image.open(vp).convert('RGB'); b = Image.open(out + "/render-4.png").convert('RGB')
print('verify render', a.size, 'vs judged render-4', b.size)
if a.size == b.size:
    d = np.asarray(ImageChops.difference(a, b)).sum(axis=2)
    print('differing px:', int((d > 0).sum()))
PY
