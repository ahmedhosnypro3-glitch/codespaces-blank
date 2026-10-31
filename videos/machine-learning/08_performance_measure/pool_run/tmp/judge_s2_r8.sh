#!/usr/bin/env bash
# Slide-2 judge driver: attempt_9 then verify_9, original-first, vs render_8.png.
set -u
REPO=/home/codespace/ai_llm_slides
NS=$REPO/videos/machine-learning/08_performance_measure
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
ORIG=$NS/unique_slides/slide_002.jpg
RENDER=$NS/recreated_pptx/qa/slide002/render_8.png
PROMPT=$(cat $NS/pool_run/judge_prompt_template.txt)

run_judge() {
  local out=$1
  local try=1
  while [ $try -le 8 ]; do
    sleep $(( 90 + RANDOM % 61 ))
    cd "$REPO"
    timeout 700 "$PY" .agents/skills/image-analysis/scripts/analyze_image.py \
      comparison "$ORIG" "$RENDER" \
      --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
      -p "$PROMPT" > "$out" 2>&1
    local rc=$?
    if grep -q "FINAL VERDICT" "$out" && ! grep -qiE "HangError|429|rate.?limit" "$out"; then
      echo "OK try=$try rc=$rc -> $out"
      return 0
    fi
    echo "BAD try=$try rc=$rc -> $out (sleeping 300)"
    sleep 300
    try=$(( try + 1 ))
  done
  echo "EXHAUSTED -> $out"
  return 1
}

run_judge "$NS/recreated_pptx/qa/slide002/judge_attempt_9.txt"
echo "attempt done rc=$?"
run_judge "$NS/recreated_pptx/qa/slide002/judge_verify_9.txt"
echo "verify done rc=$?"
echo "ALL DONE"
