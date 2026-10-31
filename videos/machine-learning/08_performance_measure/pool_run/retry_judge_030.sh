#!/usr/bin/env bash
# retry_judge.sh <out_transcript> <max_tries>
# Runs the prescribed original-first comparison against the vision gate, retrying on
# transient gateway failures (429 / empty stream) until the transcript contains a verdict.
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
Q=$NS/recreated_pptx/qa/slide030
OUT=$Q/$1
MAX=${2:-8}
PROMPT="$(cat $NS/pool_run/judge_prompt_template.txt)"

for i in $(seq 1 "$MAX"); do
  TRY="$Q/$(basename "$OUT" .txt)_try$i.txt"
  timeout 900 bash scripts/16_vision_gate.sh /home/codespace/.pyenv/versions/3.15.2/bin/python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $NS/unique_slides/slide_030.jpg $Q/render_1.png \
    --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$TRY" 2>&1
  rc=$?
  echo "--- try $i rc=$rc bytes=$(wc -c < "$TRY") $(date -u +%T)" >> "$Q/retry_$(basename "$OUT" .txt).log"
  if grep -q "FINAL VERDICT" "$TRY"; then
    cp "$TRY" "$OUT"
    echo "VERDICT FOUND in $TRY -> $OUT" >> "$Q/retry_$(basename "$OUT" .txt).log"
    exit 0
  fi
  sleep 45
done
echo "NO VERDICT after $MAX tries" >> "$Q/retry_$(basename "$OUT" .txt).log"
exit 1
