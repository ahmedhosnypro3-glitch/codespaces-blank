#!/usr/bin/env bash
set -eu
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
PROF="$NS/_pool/lo_b10_gate"; TMPD="$NS/_pool/tmp_b10"; OUT="$NS/_pool/b10_gate"
mkdir -p "$PROF" "$TMPD" "$OUT"
TMPDIR="$TMPD" soffice --headless -env:UserInstallation=file://$PROF \
  --convert-to pdf --outdir "$OUT" "$NS/10_nn_training_and_example_final.pptx" >/dev/null 2>&1
pdftoppm -png -r 150 -f 19 -l 20 "$OUT/10_nn_training_and_example_final.pdf" "$OUT/page"
python3 - "$OUT" <<'PY'
import sys, glob
from PIL import Image, ImageChops
import numpy as np
out = sys.argv[1]
pairs = [(19, out + "/page-19.png", out + "/../qa/slide019/rejudge/render-final-1.png"),
         (20, out + "/page-20.png", out + "/../qa/slide020/rejudge/render-4.png")]
for n, deck_png, src_png in pairs:
    a = Image.open(deck_png).convert('RGB'); b = Image.open(src_png).convert('RGB')
    if a.size != b.size:
        print(f'page {n}: SIZE MISMATCH {a.size} vs {b.size}'); continue
    d = np.asarray(ImageChops.difference(a, b)).sum(axis=2)
    diff = int((d > 0).sum())
    print(f'page {n}: {diff} differing px of {a.size[0]*a.size[1]}  ({diff/(a.size[0]*a.size[1])*100:.4f}%)')
PY
