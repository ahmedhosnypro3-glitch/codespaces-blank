#!/usr/bin/env bash
# Retry slide-013 reanalysis after the main sequential lane (pid 46316) exits,
# then once more if it 429s. Background task, no subagent.
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
LOG=$NS/pool_run/reanalysis_013_retry.log
for i in $(seq 1 40); do
  if [ -f "$NS/analysis/reanalysis/slide_013_raw.json" ]; then echo "[$(date '+%F %T')] slide_013 raw exists, done" >>"$LOG"; exit 0; fi
  if ! kill -0 46316 2>/dev/null; then
    echo "[$(date '+%F %T')] main lane exited; running slide-013 retry (iter $i)" >>"$LOG"
    cd /home/codespace/ai_llm_slides && VISION_SLOTS=2 bash scripts/16_vision_gate.sh /home/codespace/.pyenv/versions/3.15.2/bin/python3 scripts/12_analyze_slides.py videos/machine-learning/08_performance_measure/unique_slides videos/machine-learning/08_performance_measure/analysis/reanalysis --from 13 --to 13 --slides 37 >>"$LOG" 2>&1
    [ -f "$NS/analysis/reanalysis/slide_013_raw.json" ] && { echo "[$(date '+%F %T')] slide_013 OK" >>"$LOG"; exit 0; }
  fi
  sleep 60
done
echo "[$(date '+%F %T')] retry loop exhausted" >>"$LOG"
