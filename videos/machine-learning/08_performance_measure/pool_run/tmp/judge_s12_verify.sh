#!/usr/bin/env bash
# judge_s12_verify.sh <K> <render_png> — original-first comparison judge for slide 12.
# 429 -> sleep 300, retry up to 8x. 400 -> stop and report (payload fix needed).
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
PY=/home/codespace/.pyenv/versions/3.15.2/bin/python3
K=$1
RENDER=$2
TR=$NS/recreated_pptx/qa/slide012/judge_verify_${K}.txt
LOG=$NS/recreated_pptx/qa/slide012/judge_verify_${K}.log
sleep 180
for i in $(seq 1 8); do
  echo "=== judge attempt ${K} round $i $(date) ==="
  out=$(timeout 540 bash scripts/16_vision_gate.sh "$PY" .agents/skills/image-analysis/scripts/analyze_image.py \
    comparison "$NS/unique_slides/slide_012.jpg" "$RENDER" \
    --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 \
    -p "$(cat $NS/pool_run/judge_prompt_template.txt)" \
    --transcript "$TR" 2>&1)
  echo "$out" | tee -a "$LOG" | tail -6
  if echo "$out" | grep -q "HTTP 400"; then echo "HTTP 400 — payload problem, stopping for payload fix"; exit 2; fi
  if [ -f "$TR" ] && grep -q "FINAL VERDICT" "$TR"; then echo "VERDICT RECORDED in $TR"; grep "FINAL VERDICT" "$TR"; exit 0; fi
  if echo "$out" | grep -q "429"; then echo "429 seen — sleeping 300s"; sleep 300; else sleep 30; fi
done
echo "EXHAUSTED 8 rounds"
exit 3
