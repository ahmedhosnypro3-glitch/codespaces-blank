#!/usr/bin/env bash
# scope_r4 step-3: re-render the CURRENT deliverable bytes for slides 11,12,13
# Private LO profile is suffixed _r4 to avoid collisions with other rejudge scopes.
set -u
VID="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
ST="/Home/codespace/ai_llm_slides"
LOG="$VID/_pool/r4_render.log"
export TMPDIR="$VID/_pool"
mkdir -p "$VID/_pool/tmp_r4"
say() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

for N in 011 012 013; do
  mkdir -p "$VID/qa/slide${N#0}/rejudge"
  SRC="$VID/recreated_pptx/build/slide_${N}_recreated.pptx"
  cp "$SRC" "$VID/_pool/tmp_r4/slide_${N}_recreated.pptx"
  say "slide_$N: source md5 $(md5sum "$SRC" | cut -d' ' -f1) size $(stat -c%s "$SRC")"
  say "slide_$N: soffice convert"
  timeout 600 soffice --headless \
    -env:UserInstallation=file://$VID/_pool/lo_rejudge_r4 \
    --convert-to pdf --outdir "$VID/qa/slide${N#0}/rejudge" \
    "$VID/_pool/tmp_r4/slide_${N}_recreated.pptx" >> "$LOG" 2>&1
  say "slide_$N: pdftoppm 150dpi"
  timeout 300 pdftoppm -png -r 150 \
    "$VID/qa/slide${N#0}/rejudge/slide_${N}_recreated.pdf" \
    "$VID/qa/slide${N#0}/rejudge/render" >> "$LOG" 2>&1
  ls -la "$VID/qa/slide${N#0}/rejudge/"
  say "slide_$N: render done"
done
say "=== r4 render complete ==="
