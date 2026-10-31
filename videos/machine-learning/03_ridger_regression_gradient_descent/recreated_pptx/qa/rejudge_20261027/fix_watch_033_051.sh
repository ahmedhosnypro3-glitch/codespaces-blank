#!/usr/bin/env bash
# Read-only watcher: polls the post-fix legs for slides 033 and 051 until each
# has a clean (FINAL VERDICT, no 429) judge_full_fix.txt and crop_dense_judge_fix.txt,
# then writes a READY marker per slide. Never launches legs, never edits evidence.
set -u
RJ=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/fix_watch_033_051.log
: > "$LOG"
clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verd() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" 2>/dev/null | tail -1 | grep -oE 'PASS|FAIL'; }
for i in $(seq 1 240); do
  ts=$(date -u +%FT%TZ)
  line=""
  for N in 033 051; do
    D=$RJ/slide$N
    F=$D/judge_full_fix.txt; C=$D/crop_dense_judge_fix.txt
    fs="none"; cs="none"; fv=""; cv=""
    if clean "$F"; then fs=clean; fv=$(verd "$F"); fi
    if clean "$C"; then cs=clean; cv=$(verd "$C"); fi
    line="$line | $N full:$fs/$fv crop:$cs/$cv"
    if [ "$fs" = clean ] && [ "$cs" = clean ] && [ "$fv" = PASS ] && [ "$cv" = PASS ]; then
      if [ ! -f "$RJ/READY_$N" ]; then
        echo "$ts READY slide$N full=$fv crop=$cv" >> "$LOG"
        : > "$RJ/READY_$N"
      fi
    fi
  done
  echo "$ts$line" >> "$LOG"
  if [ -f "$RJ/READY_033" ] && [ -f "$RJ/READY_051" ]; then
    echo "$ts ALL_READY" >> "$LOG"
    exit 0
  fi
  sleep 60
done
echo "$(date -u +%FT%TZ) WATCH_TIMEOUT" >> "$LOG"
exit 1
