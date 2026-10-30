#!/usr/bin/env bash
# S20a persistent leg supervisor: retries every unbanked leg until its transcript
# exists or the deadline passes. Yield law intact — dispatch_desc.sh itself refuses
# to dispatch while pgrep -c -f analyze_image.py >= 8 (probe loop, exit 42 on park),
# so this loop never competes with cert lanes; it only re-queues.
# Usage: supervise_legs.sh SLIDE LEG [LEG...]      SLIDE=slide00N
# Env: SUPERVISE_SECS (default 21600), PARK_SLEEP (default 300), PROBE_MAX (default 4)
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 3
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
SLIDE="$1"; shift
BASE="videos/machine-learning/03_ridger_regression_gradient_descent"
Q="$BASE/recreated_pptx/qa/$SLIDE/prephase/orig_judges"
U="$BASE/unique_slides"
DEADLINE=$(( $(date +%s) + ${SUPERVISE_SECS:-21600} ))
round=0
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  round=$((round+1)); pending=0
  for LEG in "$@"; do
    OUT="$Q/desc_${LEG}.txt"
    [ -s "$OUT" ] && continue
    pending=1
    if [ "$LEG" = "full" ]; then IMG="$U/${SLIDE:0:5}_${SLIDE:5}.jpg"; else IMG="$Q/orig_${LEG}.png"; fi
    PROBE_MAX="${PROBE_MAX:-4}" bash "$Q/../dispatch_desc.sh" "$IMG" "$Q/prompt_${LEG}.txt" "$OUT" \
      "${SLIDE} ${LEG} ORIGINAL ground-truth description (S20a prephase supervisor r${round})"
    rc=$?
    echo "[sup $SLIDE] leg $LEG round $round rc=$rc $(date +%H:%M:%S)"
    if [ $rc -eq 42 ]; then sleep "${PARK_SLEEP:-300}"; fi
  done
  if [ $pending -eq 0 ]; then echo "[sup $SLIDE] all legs banked $(date +%H:%M:%S)"; exit 0; fi
  sleep 60
done
echo "[sup $SLIDE] deadline reached, legs unbanked: $(cd "$Q" && ls desc_*.txt 2>/dev/null | tr '\n' ' ')"
exit 42
