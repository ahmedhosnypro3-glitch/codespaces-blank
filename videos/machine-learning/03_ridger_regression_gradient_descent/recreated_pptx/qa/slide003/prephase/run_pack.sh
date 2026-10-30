#!/usr/bin/env bash
# S20a pre-phase pack runner: runs this slide's ground-truth legs sequentially.
# One vision call at a time; before each dispatch, yield to cert lanes while
# pgrep -c -f analyze_image.py >= 8 (12 x 120s max, else PARK that leg).
# Legs whose transcript already exists (non-empty) are skipped (idempotent).
# Usage: run_pack.sh <legs...>   e.g. run_pack.sh full topbox matrix sideboxes bottomright
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 3
SLIDE="${SLIDE:?export SLIDE=slide00N}"
BASE="videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$BASE/recreated_pptx/qa/$SLIDE/prephase/orig_judges"
U="$BASE/unique_slides"
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp

for LEG in "$@"; do
  if [ "$LEG" = "full" ]; then
    IMG="$U/${SLIDE:0:5}_${SLIDE:5}.jpg"
  else
    IMG="$Q/orig_${LEG}.png"
  fi
  PROMPT="$Q/prompt_${LEG}.txt"
  OUT="$Q/desc_${LEG}.txt"
  if [ -s "$OUT" ]; then echo "[pack $SLIDE] skip $LEG (banked transcript)"; continue; fi
  n=0
  while [ "$(pgrep -c -f analyze_image.py)" -ge 8 ]; do
    n=$((n+1))
    if [ "$n" -gt 12 ]; then echo "[pack $SLIDE] PROBE-WALL leg $LEG: load >= 8 after 12 checks; PARK leg"; continue 2; fi
    sleep 120
  done
  echo "[pack $SLIDE] dispatch $LEG at $(date +%H:%M:%S) (load $(pgrep -c -f analyze_image.py))"
  bash "$Q/../dispatch_desc.sh" "$IMG" "$PROMPT" "$OUT" \
    "${SLIDE} ${LEG} ORIGINAL ground-truth description (S20a prephase)" \
    && echo "[pack $SLIDE] leg $LEG done" || echo "[pack $SLIDE] leg $LEG FAILED rc=$?"
done
echo "[pack $SLIDE] pack complete"
wait
