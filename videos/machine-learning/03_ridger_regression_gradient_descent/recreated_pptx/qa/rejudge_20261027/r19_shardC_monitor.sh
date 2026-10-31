#!/usr/bin/env bash
# r19 shard C monitor — polls until every shard-C r19 target is clean (FINAL VERDICT,
# no 429) or its wrapper is gone (exhausted). Writes status lines to the monitor log.
set -u
RJ=/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027
LOG=$RJ/r19_shardC_monitor.log
: > "$LOG"
clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
SLIDES="035 036 037 038 039 040 041 042 043 044 045 046 047 048 049 050 051"
while true; do
  done_count=0; pend=""
  for N in $SLIDES; do
    D=$RJ/slide$N
    for leg in full crop; do
      if [ "$N" = "050" ] && [ "$leg" = "crop" ]; then continue; fi
      if [ "$leg" = full ]; then T=$D/judge_full_r19.txt; else T=$D/crop_dense_judge_r19.txt; fi
      if clean "$T"; then done_count=$((done_count+1)); continue; fi
      alive=$(ps -eo args | grep '[v]ision_leg.sh' | grep -c "slide$N/$(basename $T)")
      if [ "$alive" -gt 0 ]; then pend="$pend $N:$leg(alive)"; else pend="$pend $N:$leg(DEAD)"; fi
    done
  done
  echo "$(date -u +%FT%TZ) clean=$done_count/33 pending:${pend:- none}" >> "$LOG"
  [ -z "$pend" ] && break
  [ "$done_count" -eq 33 ] && break
  # if all pending are DEAD (wrappers exhausted without clean transcript), stop too
  case "$pend" in *alive*) ;; *) break ;; esac
  sleep 60
done
echo "MONITOR_DONE $(date -u +%FT%TZ)" >> "$LOG"
cat "$LOG" | tail -3
