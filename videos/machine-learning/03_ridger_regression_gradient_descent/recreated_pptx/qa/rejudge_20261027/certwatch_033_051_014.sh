#!/usr/bin/env bash
# Read-only status watcher for the fix legs of slides 033/051/014.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verd() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" 2>/dev/null | tail -1 | grep -oE 'PASS|FAIL'; }
for N in 033 051 014; do
  D=$RJ/slide$N
  echo "=== slide$N $(date -u +%H:%M:%SZ) ==="
  for f in "$D"/judge_full_fix*.txt "$D"/crop_dense_judge_fix*.txt; do
    [ -f "$f" ] || continue
    if clean "$f"; then st="CLEAN/$(verd "$f")"; else st="dirty-or-429"; fi
    echo "  $(basename "$f") sz=$(stat -c %s "$f") mtime=$(stat -c %y "$f" | cut -c12-19) $st"
  done
  # live wrappers on fix targets
  ps -eo pid,etime,args | grep '[v]ision_leg.sh' | grep "slide0*$N/" | grep -oE 'slide0*[0-9]+/[a-z0-9_]+\.txt' | sort -u | sed 's/^/  live: /'
done
