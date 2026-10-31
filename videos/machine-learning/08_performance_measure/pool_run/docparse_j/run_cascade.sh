#!/bin/bash
# Crop-cascade lane for dense slides 020-028 -> pool_run/docparse_j/cascade_slideNNN
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
OUT=$NS/pool_run/docparse_j
CASCADE=/home/codespace/.agents/skills/doc-parse/scripts/crop_cascade.py
PROMPT=/home/codespace/.agents/skills/doc-parse/references/prompts/crop_decision.md
mkdir -p "$OUT"

cascade_one() {
  local num=$1 img=$2
  local dir=$OUT/cascade_slide$num
  mkdir -p "$dir"
  echo "cascade slide$num start $(date -u +%FT%TZ)"
  python3 "$CASCADE" "$img" --prompt-file "$PROMPT" --out "$dir" \
    --parse-timeout 300 > "$dir/run.log.console" 2>&1
  local rc=$?
  echo "cascade slide$num rc=$rc $(date -u +%FT%TZ)"
  return $rc
}

# 028's image file is slide_028-.jpg
cascade_one 020 "$NS/unique_slides/slide_020.jpg" &
cascade_one 021 "$NS/unique_slides/slide_021.jpg" &
cascade_one 022 "$NS/unique_slides/slide_022.jpg" &
cascade_one 023 "$NS/unique_slides/slide_023.jpg" &
wait
cascade_one 024 "$NS/unique_slides/slide_024.jpg" &
cascade_one 025 "$NS/unique_slides/slide_025.jpg" &
cascade_one 026 "$NS/unique_slides/slide_026.jpg" &
cascade_one 027 "$NS/unique_slides/slide_027.jpg" &
wait
cascade_one 028 "$NS/unique_slides/slide_028-.jpg" &
wait
echo "ALL_CASCADE_DONE" >> "$OUT/cascade_done.marker"
