#!/usr/bin/env bash
# render_slide.sh <NN> — LO headless -> pdftoppm 150dpi PNG into qa/slideNNN/render_K.txt-less
set -eu
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
N=$(printf '%s' "${1#0}")
PPTX="$NS/recreated_pptx/slide_$(printf '%03d' "$N")_recreated.pptx"
OUT="$NS/recreated_pptx/qa/slide$(printf '%03d' "$N")"
K=${2:-1}
mkdir -p "$OUT"
cd "$NS/recreated_pptx"
rm -f /tmp/lo_slide_$N.pdf
timeout 300 libreoffice --headless --norestore --convert-to pdf --outdir /tmp "slide_$(printf '%03d' "$N")_recreated.pptx" >/dev/null 2>&1
mv "/tmp/slide_$(printf '%03d' "$N")_recreated.pdf" /tmp/lo_slide_$N.pdf
pdftoppm -png -r 150 /tmp/lo_slide_$N.pdf "$OUT/render_${N}"
LATEST=$(ls -1 "$OUT/render_${N}"-*.png | tail -1)
cp "$LATEST" "$OUT/render_${K}.png"
echo "rendered: $OUT/render_${K}.png"
