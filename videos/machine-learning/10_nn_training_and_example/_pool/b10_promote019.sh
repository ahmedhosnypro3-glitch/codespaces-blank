#!/usr/bin/env bash
set -eu
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
PPTX="$NS/recreated_pptx/slide_019_recreated.pptx"
PROF="$NS/_pool/lo_b10_019_final"
TMPD="$NS/_pool/tmp_b10"
OUTDIR="$NS/qa/slide019/rejudge"
mkdir -p "$PROF" "$TMPD"
TMPDIR="$TMPD" soffice --headless \
  -env:UserInstallation=file://$PROF \
  --convert-to pdf --outdir "$TMPD" "$PPTX" >/dev/null 2>&1
mv "$TMPD/slide_019_recreated.pdf" "$OUTDIR/slide_019_recreated.pdf"
pdftoppm -png -r 150 "$OUTDIR/slide_019_recreated.pdf" "$OUTDIR/render-final"
python3 - "$OUTDIR" <<'PY'
import sys, glob
from PIL import Image
import numpy as np
for p in sorted(glob.glob(sys.argv[1] + "/render-final-*.png")):
    im = Image.open(p)
    a = np.asarray(im.convert("RGB")).astype(int)
    nz = (a < 245).any(axis=2)
    print(f"{p}: {im.size} mean={a.mean():.1f} ink_frac={nz.mean():.4f}")
PY
