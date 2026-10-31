#!/usr/bin/env bash
# Fill missing reanalysis outputs (slides 13, 25, 26, 27, 36) with heavy pacing
# to avoid the shared-gateway 429 storm. Background task, no subagent.
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
ROOT=/home/codespace/ai_llm_slides
LOG=$NS/pool_run/reanalysis_gapfill.log
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
for n in 13 25 26 27 36; do
  f=$NS/analysis/reanalysis/slide_0${n}_raw.json
  for i in $(seq 1 60); do
    if [ -s "$f" ]; then echo "[$(date '+%F %T')] slide_$n already present" >>"$LOG"; break; fi
    echo "[$(date '+%F %T')] slide_$n attempt $i" >>"$LOG"
    cd $ROOT && VISION_SLOTS=1 bash scripts/16_vision_gate.sh $PY scripts/12_analyze_slides.py videos/machine-learning/08_performance_measure/unique_slides videos/machine-learning/08_performance_measure/analysis/reanalysis --from $n --to $n --slides 37 >>"$LOG" 2>&1
    if [ -s "$f" ]; then echo "[$(date '+%F %T')] slide_$n OK" >>"$LOG"; break; fi
    echo "[$(date '+%F %T')] slide_$n failed (likely 429), sleeping 180s" >>"$LOG"
    sleep 180
  done
  # long settle between slides so the gateway recovers
  sleep 120
done
echo "[$(date '+%F %T')] gapfill done" >>"$LOG"
