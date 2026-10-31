#!/bin/bash
# verify-wing poll for slide 026: detect judge_attempt_K.txt with FINAL VERDICT: PASS
# while no judge_verify_*.txt PASS exists. Writes trigger flag on detection.
NS=/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure
QA=$NS/recreated_pptx/qa/slide026
FLAG=$NS/pool_run/tmp/verify_wing_26_trigger.txt
rm -f "$FLAG"
i=0
while [ $i -lt 320 ]; do
  i=$((i+1))
  pass_attempt=$(grep -l "FINAL VERDICT: PASS" "$QA"/judge_attempt_*.txt 2>/dev/null | sort -V | tail -1)
  pass_verify=$(grep -l "FINAL VERDICT: PASS" "$QA"/judge_verify_*.txt 2>/dev/null | sort -V | tail -1)
  if [ -n "$pass_verify" ]; then
    echo "$(date -Is) verify PASS already exists: $pass_verify — wing stands down" > "$FLAG"
    echo "STANDDOWN $pass_verify"
    exit 0
  fi
  if [ -n "$pass_attempt" ]; then
    newest_render=$(ls -t "$QA"/render_*.png | head -1)
    echo "$(date -Is) TRIGGER attempt=$pass_attempt render=$newest_render" > "$FLAG"
    echo "TRIGGER $pass_attempt $newest_render"
    exit 0
  fi
  sleep 90
done
echo "$(date -Is) poll exhausted without PASS" > "$FLAG"
echo "EXHAUSTED"
exit 1
