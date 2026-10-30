#!/usr/bin/env bash
# Persistent resume loop: re-run resume_wave.sh until all 37 transcripts are
# complete (done predicate inside resume_wave.sh: >5000 bytes + VERDICT).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
OUT="$NS/pool_run/image_analysis"
LOG="$OUT/resume_loop.log"
count_ok(){
  local ok=0 f b
  for f in "$OUT"/*_analysis.txt; do
    b=$(wc -c < "$f" 2>/dev/null || echo 0)
    if [ "$b" -gt 5000 ] && grep -qi verdict "$f" 2>/dev/null; then ok=$((ok+1)); fi
  done
  echo "$ok"
}
i=0
while [ "$i" -lt 40 ]; do
  i=$((i+1))
  ok=$(count_ok)
  echo "[$(date '+%F %T')] loop iter $i: complete=$ok/37" >> "$LOG"
  [ "$ok" -ge 37 ] && { echo "[$(date '+%F %T')] ALL 37 COMPLETE" >> "$LOG"; exit 0; }
  bash "$NS/pool_run/image_analysis/resume_wave.sh" >> "$LOG" 2>&1
  sleep 20
done
echo "[$(date '+%F %T')] loop exhausted iters, complete=$(count_ok)/37" >> "$LOG"
