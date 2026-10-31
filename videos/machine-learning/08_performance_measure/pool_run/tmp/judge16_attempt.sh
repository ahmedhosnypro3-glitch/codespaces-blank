#!/usr/bin/env bash
# Slide 16 judge attempt (original FIRST) — uncapped, retry on 429/empty/HangError
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
OUT="$NS/recreated_pptx/qa/slide016/judge_attempt_4.txt"
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
sleep $((90 + RANDOM % 61))
for i in $(seq 1 8); do
  "$PY" .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_016.jpg" \
    "$NS/recreated_pptx/qa/slide016/render_4.png" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$(cat "$NS/pool_run/judge_prompt_template.txt")" > "$OUT" 2>&1
  rc=$?
  if grep -q "FINAL VERDICT" "$OUT" && ! grep -qiE "429|HangError|ServiceTimeout" "$OUT"; then
    echo "attempt $i rc=$rc $(grep 'FINAL VERDICT' "$OUT" | tail -1)" > "$OUT.meta"
    break
  fi
  echo "attempt $i rc=$rc retrying after 300s" >> "$OUT.meta"
  sleep 300
done
wait
