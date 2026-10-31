#!/usr/bin/env bash
# Sequential judge attempts for slide 24 until one returns a FINAL VERDICT (max 6).
cd /home/codespace/ai_llm_slides
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide024
for K in 1 2 3 4 5 6; do
  timeout 540 bash scripts/16_vision_gate.sh /home/codespace/.pyenv/versions/3.15.2/bin/python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison $NS/unique_slides/slide_024.jpg $QA/render_1.png --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 -p "$(cat $NS/pool_run/judge_prompt_template.txt)" > $QA/judge_attempt_$K.txt 2>&1
  rc=$?
  echo "attempt $K rc=$rc bytes=$(wc -c < $QA/judge_attempt_$K.txt) $(grep -o 'FINAL VERDICT: [A-Z]*' $QA/judge_attempt_$K.txt | tail -1)" >> $QA/judge_loop.log
  if grep -q "FINAL VERDICT" $QA/judge_attempt_$K.txt; then echo "DONE K=$K" >> $QA/judge_loop.log; break; fi
  sleep 20
done
echo "LOOP END" >> $QA/judge_loop.log
