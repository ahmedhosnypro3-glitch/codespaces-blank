#!/bin/bash
# Dual-judge runner for slide 32 re-fix. Usage: run_judge_32.sh <outfile_basename>
# From repo root. Random 90-150s pacing sleep before first call; on 429/empty/HangError
# sleep 300 and retry up to 8x. Original FIRST in comparison order.
cd /home/codespace/ai_llm_slides
OUT="videos/machine-learning/08_performance_measure/recreated_pptx/qa/slide032/$1"
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
NS=videos/machine-learning/08_performance_measure
RENDER="$NS/recreated_pptx/qa/slide032/render_7.png"
PROMPT="$(cat $NS/pool_run/judge_prompt_template.txt)"
sleep $((90 + RANDOM % 61))
echo "pacing sleep done at $(date)" >> "$OUT"
for i in $(seq 1 8); do
  echo "=== attempt $i at $(date) ===" >> "$OUT"
  $PY .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_032.jpg" "$RENDER" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$PROMPT" >> "$OUT" 2>&1
  rc=$?
  echo "attempt $i rc=$rc at $(date)" >> "$OUT"
  if grep -q "FINAL VERDICT" "$OUT" && ! tail -50 "$OUT" | grep -qiE "429|HangError|rate.?limit|ServiceTimeout"; then
    echo "VERDICT OBTAINED on attempt $i" >> "$OUT"
    break
  fi
  echo "retrying after 300s sleep (429/empty/HangError or no verdict)" >> "$OUT"
  sleep 300
done
echo "JOB DONE $(date)" >> "$OUT"
wait
