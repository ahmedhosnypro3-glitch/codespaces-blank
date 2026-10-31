#!/usr/bin/env bash
# Slide 35 judge attempt 3 — self-retrying loop per founder cadence:
# random 90-150s before each call; on 429/HangError sleep 300s; up to 8 tries.
# No outer timeout wrapper; ends in wait. All inside the slide-35 namespace.
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide035
cd /home/codespace/ai_llm_slides
for i in $(seq 1 8); do
  s=$((90 + RANDOM % 61))
  echo "[loop] try $i: sleeping ${s}s before gate call" >> "$QA/judge_attempt_3_loop.log"
  sleep "$s"
  bash scripts/16_vision_gate.sh /home/codespace/.pyenv/versions/3.15.2/bin/python3 \
    .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    $NS/unique_slides/slide_035.jpg $NS/recreated_pptx/qa/slide035/render_3.png \
    --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
    -p "$(cat $NS/pool_run/judge_prompt_template.txt)" \
    > "$QA/judge_attempt_3.txt" 2>&1
  rc=$?
  echo "[loop] try $i rc=$rc bytes=$(wc -c < "$QA/judge_attempt_3.txt")" >> "$QA/judge_attempt_3_loop.log"
  if grep -q "FINAL VERDICT" "$QA/judge_attempt_3.txt"; then
    echo "[loop] try $i produced FINAL VERDICT — done" >> "$QA/judge_attempt_3_loop.log"
    break
  fi
  # bank the failed transcript, then back off
  tag="try${i}_rc${rc}"
  cp "$QA/judge_attempt_3.txt" "$QA/judge_attempt_3_${tag}.txt"
  if grep -qiE "429|HangError" "$QA/judge_attempt_3.txt"; then
    echo "[loop] try $i hit 429/HangError — 300s backoff" >> "$QA/judge_attempt_3_loop.log"
    sleep 300
  else
    echo "[loop] try $i starved/empty — no extra backoff beyond pre-sleep" >> "$QA/judge_attempt_3_loop.log"
  fi
done
wait
echo "[loop] finished" >> "$QA/judge_attempt_3_loop.log"
