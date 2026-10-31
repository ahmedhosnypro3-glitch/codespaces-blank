#!/bin/bash
# Slide-4 verify leg: ONE fresh original-first corroboration judge vs newest render.
# Gateway storm protocol: random 90-150s pre-sleep; on 429/HangError sleep 300s, retry up to 8x.
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/08_performance_measure
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
OUT=$NS/recreated_pptx/qa/slide004/judge_verify_13.txt
TMP=$(mktemp)
cd "$ROOT"
sleep $((90 + RANDOM % 61))
for i in $(seq 1 8); do
  echo "=== corroboration attempt $i start $(date -u +%FT%TZ) ===" >> "$OUT"
  bash scripts/16_vision_gate.sh "$PY" .agents/skills/image-analysis/scripts/analyze_image.py \
    comparison "$NS/unique_slides/slide_004.jpg" "$NS/recreated_pptx/qa/slide004/render_10.png" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$(cat "$NS/pool_run/judge_prompt_template.txt")" > "$TMP" 2>&1
  rc=$?
  cat "$TMP" >> "$OUT"
  echo "=== corroboration attempt $i rc=$rc end $(date -u +%FT%TZ) ===" >> "$OUT"
  if [ $i -lt 8 ] && grep -aqiE '429|HangError|rate.?limit|Too Many Requests' "$TMP"; then
    echo "=== storm detected on attempt $i; sleeping 300s before retry ===" >> "$OUT"
    sleep 300
    continue
  fi
  break
done
rm -f "$TMP"
echo "=== slide-4 verify leg done $(date -u +%FT%TZ) ===" >> "$OUT"
wait
