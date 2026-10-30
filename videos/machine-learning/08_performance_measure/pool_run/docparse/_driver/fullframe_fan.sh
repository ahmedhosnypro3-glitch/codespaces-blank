#!/bin/bash
# Full-frame parse fan for the doc-parse lane (bounded: <=4 in flight).
# Usage: fullframe_fan.sh <slide_number> ...
# Each slide gets its own fresh call dir; nothing is overwritten.
SKD=/home/codespace/.agents/skills/doc-parse
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
BASE="$NS/pool_run/docparse"

for N in "$@"; do
  S=$(printf "%03d" "$N")
  IMG="$NS/unique_slides/slide_${S}.jpg"
  OUT="$BASE/slide${S}/full_frame"
  if [ ! -f "$IMG" ]; then echo "slide${S}: MISSING IMAGE" >> "$BASE/_ff_fan.log"; continue; fi
  mkdir -p "$OUT"
  (
    START=$(date +%s)
    timeout 200 python3 "$SKD/scripts/parse_document.py" "$IMG" -o "$OUT" --timeout 150 \
      > "$OUT/stdout.txt" 2> "$OUT/stderr.txt"
    EXIT=$?
    END=$(date +%s)
    echo "slide${S} exit=$EXIT wall=$((END-START))s" >> "$OUT/call_record.txt"
  ) &
  while [ "$(jobs -rp | wc -l)" -ge 4 ]; do sleep 2; done
done
wait
echo "fan complete"
