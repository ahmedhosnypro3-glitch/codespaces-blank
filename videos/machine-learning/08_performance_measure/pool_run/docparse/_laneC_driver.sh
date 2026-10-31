#!/bin/bash
# Lane C driver: doc-parse crop cascade over slides 20-28 of 08_performance_measure.
# One cascade at a time, 60-90s pacing between slides, <=2 concurrent parse calls
# (script-internal pool), wrapper retries up to 6x with 120-300s sleeps on failure.
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
SKILL=~/.agents/skills/doc-parse
OUT=$NS/pool_run/docparse
LOG=$OUT/_laneC_run.log
cd "$NS"

run_one() {
  local src="$1" name="$2" dir="$3"
  local attempt=1 rc
  while [ $attempt -le 6 ]; do
    echo "$(date '+%F %T') START $name attempt=$attempt -> $OUT/$dir" >> "$LOG"
    python3 "$SKILL/scripts/crop_cascade.py" "unique_slides/$src" \
      --prompt-file "$SKILL/references/prompts/crop_decision.md" \
      --out "$OUT/$dir" \
      --max-crops 16 --max-parse-calls 24 --max-depth 6 \
      --max-retries 6 --max-parallel 2 \
      --parse-timeout 150 --chat-timeout 60 >> "$OUT/$dir.cascade.log" 2>&1
    rc=$?
    echo "$(date '+%F %T') END $name attempt=$attempt exit=$rc" >> "$LOG"
    if [ $rc -eq 0 ] || [ $rc -eq 6 ]; then
      echo "$(date '+%F %T') ACCEPT $name exit=$rc (0=complete, 6=partial with banked gap)" >> "$LOG"
      return $rc
    fi
    if [ $attempt -lt 6 ]; then
      local s=$((120 + RANDOM % 181))
      echo "$(date '+%F %T') RETRY-WAIT $name exit=$rc sleeping ${s}s" >> "$LOG"
      sleep $s
    fi
    attempt=$((attempt + 1))
  done
  echo "$(date '+%F %T') GAVE-UP $name after 6 attempts" >> "$LOG"
  return 99
}

for n in 020 021 022 023 024 025 026 027 028-; do
  name="slide${n%-}"
  run_one "slide_$n.jpg" "$name" "$name"
  if [ "$n" != "028-" ]; then
    ps=$((60 + RANDOM % 31))
    echo "$(date '+%F %T') PACE sleeping ${ps}s before next slide" >> "$LOG"
    sleep $ps
  fi
done
echo "$(date '+%F %T') LANE-C-DONE" >> "$LOG"
