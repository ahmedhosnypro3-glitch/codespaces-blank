#!/usr/bin/env bash
# Render the slide-014 deliverable at 150dpi (pptx -> PDF -> PNG, 2001x1125) to a
# scratch name so it can be diffed against the banked render_2.png before any
# attempt-numbering decision.
set -e
ROOT="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$DECK/recreated_pptx/qa/slide014"
export TMPDIR="$ROOT/scratch/tmp"
WORK="$TMPDIR/w014_render_verify"
rm -rf "$WORK"; mkdir -p "$WORK"

soffice --headless -env:UserInstallation=file://"$WORK/lo_profile" \
  --convert-to pdf --outdir "$WORK" "$DECK/recreated_pptx/slide_014_recreated.pptx" >/dev/null 2>&1
pdftoppm -png -r 150 "$WORK/slide_014_recreated.pdf" "$WORK/slide"
cp "$WORK/slide-1.png" "$Q/render_verify_rebuild.png"
python3 - "$Q/render_verify_rebuild.png" <<'EOF'
import sys
from PIL import Image
im = Image.open(sys.argv[1])
print("RENDER", im.size, im.mode)
EOF
