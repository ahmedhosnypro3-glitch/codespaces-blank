#!/bin/bash
# docparse_i cascade runner: dense/thin slides, sequential, per-cascade logs.
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
SK=/home/codespace/.agents/skills/doc-parse/scripts/crop_cascade.py
PF=/home/codespace/.agents/skills/doc-parse/references/prompts/crop_decision.md
OUT=$NS/pool_run/docparse_i

for n in 010 013 014 015 016 018 019; do
  log=$OUT/cascade_slide${n}.log
  echo "start $(date -u +%FT%TZ) cascade slide_${n}" > "$log"
  python3 "$SK" "$NS/unique_slides/slide_${n}.jpg" \
    --prompt-file "$PF" \
    --out "$OUT/cascade_slide${n}" \
    --parse-timeout 300 >> "$log" 2>&1
  echo "exit=$? end $(date -u +%FT%TZ)" >> "$log"
done
echo "ALL_CASCADES_DONE $(date -u +%FT%TZ)"
