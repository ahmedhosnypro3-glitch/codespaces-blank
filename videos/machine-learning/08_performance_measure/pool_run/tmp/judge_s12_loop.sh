#!/usr/bin/env bash
# judge_s12_loop.sh <K> <render_png> — long-running judge loop for slide 12.
# Rounds spaced 200s (within the 150-240s vision-call spacing rule).
# 429 -> extra 300s sleep. 400 -> stop (payload fix). Max 8 rounds per invocation.
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
K=$1
RENDER=$2
case "$RENDER" in /*) ;; *) RENDER=$NS/$RENDER;; esac
TR=$NS/recreated_pptx/qa/slide012/judge_attempt_${K}.txt
LOG=$NS/recreated_pptx/qa/slide012/judge_attempt_${K}.log
[ -f "$TR" ] && grep -q "FINAL VERDICT" "$TR" && { echo "attempt $K already has a verdict"; exit 0; }
for i in $(seq 1 8); do
  echo "=== attempt ${K} round $i $(date) ==="
  out=$(timeout 540 bash scripts/16_vision_gate.sh "$PY" .agents/skills/image-analysis/scripts/analyze_image.py \
    comparison "$NS/unique_slides/slide_012.jpg" "$RENDER" \
    --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
    -p "$(cat $NS/pool_run/judge_prompt_template.txt)" \
    --transcript "$TR" 2>&1)
  echo "$out" | tee -a "$LOG" | tail -4
  if echo "$out" | grep -q "HTTP 400"; then echo "HTTP 400 — payload problem, stopping"; exit 2; fi
  if [ -f "$TR" ] && grep -q "FINAL VERDICT" "$TR"; then echo "VERDICT RECORDED in $TR"; grep "FINAL VERDICT" "$TR"; exit 0; fi
  if echo "$out" | grep -q "429"; then echo "429 — sleeping 300s"; sleep 300; else echo "no verdict — spacing 200s"; sleep 200; fi
done
echo "LOOP EXHAUSTED 8 rounds at $(date)"
exit 3
