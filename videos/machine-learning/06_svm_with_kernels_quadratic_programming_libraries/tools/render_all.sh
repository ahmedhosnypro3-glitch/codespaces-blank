#!/bin/bash
# Render every rebuilt slide to PDF + 150dpi PNG.
# Usage: render_all.sh [slide_number ...]   (no args = all slides)
set -u

BASE="/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
OUT="$BASE/recreated_pptx/renders"
mkdir -p "$OUT"

render_one() {
  local i="$1"
  local ss
  ss=$(printf "%03d" "$i")
  local pptx="$BASE/recreated_pptx/slide_${ss}_recreated.pptx"
  local pdf="$OUT/slide_${ss}_recreated.pdf"
  local png="$OUT/slide_${ss}_recreated-1.png"
  local profile="$HOME/.lo_profile_slide_${ss}"

  [ -f "$pptx" ] || { echo "MISSING pptx: $ss"; return 1; }
  rm -rf "$profile"; mkdir -p "$profile"
  rm -f "$pdf" "$png"

  soffice --headless --convert-to pdf --outdir "$OUT" \
    "-env:UserInstallation=file://$profile" "$pptx" >/dev/null 2>&1
  rm -rf "$profile"

  [ -f "$pdf" ] || { echo "RENDER FAIL (pdf): $ss"; return 1; }
  pdftoppm -png -r 150 "$pdf" "$OUT/slide_${ss}_recreated" >/dev/null 2>&1
  [ -f "$png" ] || { echo "RENDER FAIL (png): $ss"; return 1; }

  local dims
  dims=$(python3 -c "from PIL import Image;im=Image.open('$png');print(im.size[0],im.size[1])" 2>/dev/null)
  echo "OK $ss ${dims:-unknown}"
  return 0
}
export -f render_one
export BASE OUT

if [ "$#" -gt 0 ]; then
  SLIDES="$*"
else
  SLIDES=$(seq 1 55)
fi

printf '%s\n' $SLIDES | xargs -P 4 -I{} bash -c 'render_one {}'
echo "=== render_all done ==="
