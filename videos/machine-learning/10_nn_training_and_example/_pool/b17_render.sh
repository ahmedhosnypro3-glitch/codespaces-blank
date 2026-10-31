#!/usr/bin/env bash
# b17 render+measure helper: $1=slide number, $2=pptx path (optional)
set -eu
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
N="$1"
Q="$NS/qa/slide0$N/rejudge"
mkdir -p "$Q" "$NS/_pool/lo_b17_$N"
PPTX="${2:-$NS/recreated_pptx/build/slide_0${N}_recreated.pptx}"
cp "$PPTX" "$NS/_pool/b17_r${N}.pptx"
rm -f "$Q"/render-*.png "$Q"/slide_0${N}_recreated.pdf
TMPDIR="$NS/_pool" soffice --headless \
  -env:UserInstallation=file://$NS/_pool/lo_b17_$N \
  --convert-to pdf --outdir "$Q" "$NS/_pool/b17_r${N}.pptx" >/dev/null 2>&1
mv "$Q/b17_r${N}.pdf" "$Q/slide_0${N}_recreated.pdf" 2>/dev/null || true
pdftoppm -png -r 150 "$Q/slide_0${N}_recreated.pdf" "$Q/render"
python3 - "$Q" <<'PY'
import sys, glob
from PIL import Image
import numpy as np
q = sys.argv[1]
for p in sorted(glob.glob(q + "/render-*.png")):
    im = Image.open(p)
    a = np.asarray(im.convert("RGB")).astype(int)
    nz = (a < 245).any(axis=2)
    print(f"{p}: {im.size} mean={a.mean():.1f} ink_frac={nz.mean():.4f}")
PY
