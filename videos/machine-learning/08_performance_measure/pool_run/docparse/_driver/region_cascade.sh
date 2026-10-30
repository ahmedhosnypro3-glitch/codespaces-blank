#!/bin/bash
# Targeted region cascades for the doc-parse lane.
# Each region PNG is a DIFFERENT INPUT FORM read of the dense area the
# full-frame read left under-parsed. One cascade per region, sequentially:
# each cascade already fans up to 4 parse calls against the single endpoint.
# Output dirs are derived from the PNG path so the slideNNN vs slide_NNN
# naming difference cannot bite.
SKD=/home/codespace/.agents/skills/doc-parse
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
BASE="$NS/pool_run/docparse"

while IFS= read -r PNG; do
  REGION_DIR="$(dirname "$PNG")"
  REGION="$(basename "$REGION_DIR")"
  SLIDE_DIR="$(dirname "$(dirname "$REGION_DIR")")"
  OUT="$REGION_DIR/run"
  START=$(date +%s)
  timeout 600 python3 "$SKD/scripts/crop_cascade.py" "$PNG" \
    --prompt-file "$SKD/references/prompts/crop_decision.md" \
    --out "$OUT" \
    --max-crops 16 --max-parse-calls 24 --max-depth 6 \
    --max-retries 3 --max-parallel 4 --parse-timeout 150 --chat-timeout 60 \
    > "$REGION_DIR/cascade_stdout.txt" 2> "$REGION_DIR/cascade_stderr.txt"
  EXIT=$?
  END=$(date +%s)
  echo "$(basename "$SLIDE_DIR") $REGION exit=$EXIT wall=$((END-START))s" \
    >> "$BASE/_region_cascade_records.txt"
  echo "$(basename "$SLIDE_DIR") $REGION exit=$EXIT wall=$((END-START))s"
done < "$BASE/_driver/region_list.txt"
