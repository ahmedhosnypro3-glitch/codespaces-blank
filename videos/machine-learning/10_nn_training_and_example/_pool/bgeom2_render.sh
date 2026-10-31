#!/usr/bin/env bash
# Lane G geometry: render canonical deliverable -> PDF -> 150dpi PNG.
# Private LO profile per slide under _pool/lo_geom_b_geom_2/<NNN>/.
set -u
NS="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
cd "$NS" || exit 1
OUTROOT="_pool/tmp_geom_b_geom_2"

render_one() {
  s="$1"
  prof="$NS/_pool/lo_geom_b_geom_2/$s"
  out="$NS/$OUTROOT/$s"
  mkdir -p "$prof" "$out"
  export TMPDIR="$out/tmp"
  mkdir -p "$TMPDIR"
  timeout 300 soffice --headless --norestore --invisible \
    -env:UserInstallation="file://$prof" \
    --convert-to pdf --outdir "$out" \
    "$NS/recreated_pptx/slide_${s}_recreated.pptx" > "$out/lo.log" 2>&1
  rc=$?
  pdf="$out/slide_${s}_recreated.pdf"
  if [ $rc -ne 0 ] || [ ! -f "$pdf" ]; then
    echo "$s LO-FAIL rc=$rc"; cat "$out/lo.log"; return 1
  fi
  pdftoppm -png -r 150 "$pdf" "$out/render"
  if [ ! -f "$out/render-1.png" ]; then
    echo "$s PDFTOPPM-FAIL"; return 1
  fi
  echo "$s OK $(python3 -c "
from PIL import Image
im=Image.open('$out/render-1.png'); print(im.size)")"
}

for s in 008 009 010 012 013; do
  render_one "$s" &
done
wait
echo "ALL RENDERS DONE"
