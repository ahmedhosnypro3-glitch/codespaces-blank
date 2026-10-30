#!/bin/bash
# Crop-cascade driver for the doc-parse lane.
# Usage: cascade.sh <slide_number> ...
# Each slide runs ONE cascade at a time: the cascade's internal pool already
# fans up to 4 parse calls against the single endpoint (bounded parallel fan).
SKD=/home/codespace/.agents/skills/doc-parse
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
BASE="$NS/pool_run/docparse"

for N in "$@"; do
  S=$(printf "%03d" "$N")
  IMG="$NS/unique_slides/slide_${S}.jpg"
  OUT="$BASE/slide${S}"
  if [ ! -f "$IMG" ]; then echo "slide${S}: MISSING IMAGE"; continue; fi
  START=$(date +%s)
  timeout 600 python3 "$SKD/scripts/crop_cascade.py" "$IMG" \
    --prompt-file "$SKD/references/prompts/crop_decision.md" \
    --out "$OUT" \
    --max-crops 16 --max-parse-calls 24 --max-depth 6 \
    --max-retries 3 --max-parallel 4 --parse-timeout 150 --chat-timeout 60 \
    > "$OUT/cascade_stdout.txt" 2> "$OUT/cascade_stderr.txt"
  EXIT=$?
  END=$(date +%s)
  echo "slide${S} cascade exit=$EXIT wall=$((END-START))s" >> "$BASE/_cascade_records.txt"
  echo "slide${S} cascade exit=$EXIT wall=$((END-START))s"
done
