#!/usr/bin/env bash
# S20c leg supervisor: re-queues this slide's unbanked ground-truth desc legs
# until each transcript exists or the deadline passes. Yield law intact —
# dispatch_desc.sh probes pgrep -c -f analyze_image.py >= 8 (exit 42 = PARK),
# so this loop never competes with cert lanes; it only re-queues.
# Usage: supervise_legs.sh SLIDE LEG [LEG...]      SLIDE=slide0NN
# Env: SUPERVISE_SECS (default 7200), PARK_SLEEP (default 240), ROUND_SLEEP (default 60)
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 3
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
SLIDE="${1:?SLIDE=slide0NN}"; shift
LEGS=("$@")
BASE="videos/machine-learning/03_ridger_regression_gradient_descent"
PRE="$BASE/recreated_pptx/qa/$SLIDE/prephase"
U="$BASE/unique_slides"
DEADLINE=$(( $(date +%s) + ${SUPERVISE_SECS:-7200} ))
round=0
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  round=$((round+1)); pending=0
  for LEG in "${LEGS[@]}"; do
    OUT="$PRE/orig_judges/desc_${LEG}.txt"
    [ -s "$OUT" ] && continue
    pending=1
    if [ "$LEG" = "full" ]; then
      IMG="$U/${SLIDE:0:5}_${SLIDE:5}.jpg"
    else
      IMG="$PRE/orig_judges/crop${SLIDE:5}_${LEG}.png"
    fi
    echo "[sup $SLIDE] r$round dispatch $LEG at $(date +%H:%M:%S) load=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0)"
    bash "$PRE/dispatch_desc.sh" "$IMG" "$PRE/prompt_${LEG}.txt" "$OUT" \
      "${SLIDE} ${LEG} ORIGINAL ground-truth description (S20c prephase supervisor r${round})"
    rc=$?
    echo "[sup $SLIDE] r$round leg $LEG rc=$rc $(date +%H:%M:%S)"
    [ "$rc" -eq 42 ] && sleep "${PARK_SLEEP:-240}"
  done
  if [ "$pending" -eq 0 ]; then echo "[sup $SLIDE] all legs banked $(date +%H:%M:%S)"; exit 0; fi
  sleep "${ROUND_SLEEP:-60}"
done
echo "[sup $SLIDE] deadline reached $(date +%H:%M:%S)"
