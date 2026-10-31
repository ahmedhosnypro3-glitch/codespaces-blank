#!/usr/bin/env bash
# b09: render slide 018 pptx to a 150dpi PNG in a private LO profile.
# Usage: b09_s018_render.sh <pptx-abs-path> <out-dir>
set -eu
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
PPTX="$1"; OUTDIR="$2"
PROF="$NS/_pool/lo_b09"
TMPD="$NS/_pool/tmp_b09_s018"
rm -rf "$PROF" "$TMPD"
mkdir -p "$OUTDIR" "$PROF" "$TMPD"
TMPDIR="$TMPD" soffice --headless \
  -env:UserInstallation=file://$PROF \
  --convert-to pdf --outdir "$TMPD" "$PPTX" >/dev/null 2>&1
BASE="$(basename "${PPTX%.*}")"
mv "$TMPD/$BASE.pdf" "$OUTDIR/slide_018.pdf"
pdftoppm -png -r 150 "$OUTDIR/slide_018.pdf" "$OUTDIR/render"
ls -la "$OUTDIR"
python3 - "$OUTDIR" <<'PY'
import sys, glob
from PIL import Image
import numpy as np
for p in sorted(glob.glob(sys.argv[1] + "/render-*.png")):
    im = Image.open(p)
    a = np.asarray(im.convert("RGB")).astype(int)
    nz = (a < 245).any(axis=2)
    print(f"{p}: {im.size} mean={a.mean():.1f} ink_frac={nz.mean():.4f}")
PY
