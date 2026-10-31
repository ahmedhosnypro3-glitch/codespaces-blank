#!/usr/bin/env bash
# dual judge for slide 21; args: K
set -u
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
K=$1
RENDER=$(ls -1 $NS/recreated_pptx/qa/slide021/render_*.png | sort -V | tail -1)
echo "render=$RENDER" 
for i in $(seq 1 8); do
  sleep $((90 + RANDOM % 61))
  bash scripts/16_vision_gate.sh /home/codespace/.pyenv/versions/3.15.2/bin/python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison $NS/unique_slides/slide_021.jpg "$RENDER" --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 -p "$(cat $NS/pool_run/judge_prompt_template.txt)" > $NS/recreated_pptx/qa/slide021/judge_${2}_${K}.txt 2>&1
  rc=$?
  echo "try $i rc=$rc" >> $NS/recreated_pptx/qa/slide021/judge_${2}_${K}.log
  if [ $rc -eq 0 ] && grep -q "FINAL VERDICT" $NS/recreated_pptx/qa/slide021/judge_${2}_${K}.txt; then
    grep -E "FINAL VERDICT" $NS/recreated_pptx/qa/slide021/judge_${2}_${K}.txt | tail -1
    exit 0
  fi
  sleep 300
done
echo "ALL TRIES FAILED"
exit 1
