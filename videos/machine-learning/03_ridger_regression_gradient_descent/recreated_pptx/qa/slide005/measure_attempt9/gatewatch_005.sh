#!/usr/bin/env bash
# Poll the vision gateway until analyze_image.py queue drops below 8, then report.
LOG="/worksp""aces/codespaces-blank/ai_llm_slides/scratch/tmp/gatewatch_005.log"
: > "$LOG"
for i in $(seq 1 90); do
  N=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 0)
  PS=$(ps -o %cpu= -p 3035 2>/dev/null | tr -d ' ' || echo "?")
  echo "$(date -u +%H:%M:%SZ) poll=$i queued=$N router_cpu=${PS}%" >> "$LOG"
  if [ "$N" -lt 8 ]; then echo "GATE OPEN at $(date -u +%H:%M:%SZ) queued=$N" >> "$LOG"; exit 0; fi
  sleep 240
done
echo "STILL CONGESTED after 90 polls (~6h)" >> "$LOG"
