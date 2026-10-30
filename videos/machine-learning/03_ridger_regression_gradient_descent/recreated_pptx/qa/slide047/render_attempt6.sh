#!/usr/bin/env bash
# Fresh render of the slide-047 deliverable for judge attempt 6 (worker w047-root-20261024).
# pptx -> PDF -> 150dpi PNG (2001x1125). Banked under qa/slide047/render_10.png.
set -e
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$DECK/recreated_pptx/qa/slide047"
export TMPDIR="$ROOT/scratch/tmp"
WORK="$TMPDIR/render_w047_attempt6"
rm -rf "$WORK"; mkdir -p "$WORK"

soffice --headless -env:UserInstallation=file://"$WORK/lo_profile" \
  --convert-to pdf --outdir "$WORK" "$DECK/recreated_pptx/slide_047_recreated.pptx" >/dev/null 2>&1
pdftoppm -png -r 150 "$WORK/slide_047_recreated.pdf" "$WORK/slide"
cp "$WORK/slide-1.png" "$Q/render_10.png"
python3 - "$Q/render_10.png" <<'EOF'
import sys
from PIL import Image
im = Image.open(sys.argv[1])
print("RENDER", im.size)
EOF
