#!/usr/bin/env bash
# Reproduce render_6 from the CURRENT pptx to prove the banked render is current.
set -e
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$DECK/recreated_pptx/qa/slide005"
export TMPDIR="$ROOT/scratch/tmp"
WORK="$TMPDIR/render_w005_verify"
rm -rf "$WORK"; mkdir -p "$WORK"

soffice --headless -env:UserInstallation=file://"$WORK/lo_profile" \
  --convert-to pdf --outdir "$WORK" "$DECK/recreated_pptx/slide_005_recreated.pptx" >/dev/null 2>&1
pdftoppm -png -r 150 "$WORK/slide_005_recreated.pdf" "$WORK/slide"
ls -la "$WORK"/slide-1.png
python3 - "$WORK/slide-1.png" "$Q/render_6.png" "$WORK/slide-1.png.verify" <<'PY'
import sys
from PIL import Image
import hashlib
new = Image.open(sys.argv[1]).convert("RGB")
bank = Image.open(sys.argv[2]).convert("RGB")
print("new size:", new.size, " bank size:", bank.size)
if new.size != bank.size:
    print("FATAL size mismatch"); sys.exit(1)
import numpy as np
a = np.asarray(new, dtype=np.int16); b = np.asarray(bank, dtype=np.int16)
d = np.abs(a - b)
print("max abs diff:", int(d.max()), " mean abs diff:", round(float(d.mean()), 6))
print("pixels differing >0:", int((d.sum(axis=2) > 0).sum()))
h = hashlib.md5(open(sys.argv[1], 'rb').read()).hexdigest()
h2 = hashlib.md5(open(sys.argv[2], 'rb').read()).hexdigest()
print("md5 new :", h)
print("md5 bank:", h2)
print("IDENTICAL:", h == h2)
PY
cp "$WORK/slide-1.png" "$Q/render_7.png"
echo "banked render_7.png"
md5sum "$Q/render_7.png"
