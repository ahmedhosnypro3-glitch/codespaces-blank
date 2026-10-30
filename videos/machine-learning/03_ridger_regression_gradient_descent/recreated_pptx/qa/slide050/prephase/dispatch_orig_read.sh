#!/bin/bash
# S20e prephase ground-truth read dispatcher (description legs, NOT certification judges).
# Usage: bash dispatch_orig_read.sh <leg>
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 3
DECK=videos/machine-learning/03_ridger_regression_gradient_descent
n="${SLIDE_N:?SLIDE_N must be set (e.g. 048)}"
D="$DECK/recreated_pptx/qa/slide$n/prephase"
LEG="${1:?leg required}"
P="$D/desc_prompt.txt"
case "$LEG" in
  full) IMG="$DECK/unique_slides/slide_$n.jpg"
    VIEW="Slide $n ORIGINAL frame — FULL 960x540 ground-truth extraction read"
    CAP="single 960x540 JPEG lecture-video frame of the ORIGINAL slide; 1 image px = 1 slide pt; no second image" ;;
  *) IMG="$D/crops/crop_${n}_${LEG}_orig.png"
    VIEW="Slide $n ORIGINAL frame — zoomed crop '${LEG}' ground-truth extraction read"
    CAP="2x LANCZOS upscale of a crop from the 960x540 original lecture-video JPEG frame; crop slide-space box recorded in prephase/crops/README (1 original px = 1 slide pt); no second image" ;;
esac
LOAD=$(pgrep -c -f "[a]nalyze_image.py" || true)
echo "[$n/$LEG] $(date -u +%H:%M:%S) analyzer procs=$LOAD"
if [ "${LOAD:-0}" -ge 8 ]; then echo "GATE BUSY (>=8) — yield to cert lanes; retry later"; exit 75; fi
exec scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py analysis \
  "$IMG" \
  --view "$VIEW" \
  --capture "$CAP" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript "$D/orig_judges/orig_$LEG.txt" \
  -p "$(cat "$P")"
