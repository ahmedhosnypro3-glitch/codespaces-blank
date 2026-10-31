#!/usr/bin/env bash
# Re-render the candidate certified pptx files and compare md5 with the banked judge renders.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SRC="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
cd "$NS" || exit 9

verify() { # $1=slide $2=src pptx $3=banked render png
  local N="$1" PPTX="$2" BANK="$3"
  local T="_pool/b03_ver_${N}"
  rm -rf "$T"; mkdir -p "$T"
  cp "$PPTX" "$T/slide_${N}_recreated.pptx"
  TMPDIR="$NS/_pool" timeout 300 soffice --headless \
    -env:UserInstallation=file://$NS/_pool/lo_b03_v3 \
    --convert-to pdf --outdir "$T" "$T/slide_${N}_recreated.pptx" > /dev/null 2>&1
  if [ ! -f "$T/slide_${N}_recreated.pdf" ]; then echo "slide ${N}: PDF CONVERT FAILED"; return 1; fi
  pdftoppm -png -r 150 "$T/slide_${N}_recreated.pdf" "$T/render"
  local NEW="$T/render-1.png"
  if [ ! -f "$NEW" ]; then echo "slide ${N}: PNG FAILED"; return 1; fi
  local A B
  A=$(md5sum "$NEW" | cut -d' ' -f1)
  B=$(md5sum "$BANK" | cut -d' ' -f1)
  if [ "$A" = "$B" ]; then
    echo "slide ${N}: RENDER MATCH (md5 $A) -> PASS transcript covers these bytes"
  else
    echo "slide ${N}: RENDER MISMATCH new=$A banked=$B"
  fi
}

verify 5 "$SRC/recreated_pptx/build/slide_005_recreated.pptx" "$SRC/qa/slide005/rejudge/b03/render_b03-1.png"
verify 6 "$SRC/recreated_pptx/build/slide_006_v3.pptx" "$SRC/qa/slide006/rejudge/b03/render_v3-1.png"
