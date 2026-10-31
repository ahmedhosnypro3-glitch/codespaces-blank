#!/usr/bin/env bash
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
OUT=$NS/recreated_pptx/qa/slide010
for i in 15 16 17 18 19 20; do
  sleep 420
  echo "=== attempt_$i start $(date -u +%FT%TZ) ==="
  timeout 800 bash scripts/16_vision_gate.sh /home/codespace/.pyenv/versions/3.15.2/bin/python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison $NS/unique_slides/slide_010.jpg /home/codespace/ai_llm_slides/$NS/recreated_pptx/qa/slide010/render_8.png --view "Slide 10 recreation — judge vs original lecture frame" --capture "IMG1=original lecture video frame (ground truth, read first); IMG2=150dpi PNG render of the recreation (read second)" --thinking high --max-tokens 65536 --timeout 420 --rounds 1 --tries 1 -p "$(cat $NS/pool_run/judge_prompt_template.txt)" > $OUT/judge_attempt_$i.txt 2>&1
  echo "exit=$?"
  if grep -q "FINAL VERDICT" $OUT/judge_attempt_$i.txt; then echo "VERDICT FOUND in attempt_$i"; break; fi
done
echo "loop2 done $(date -u +%FT%TZ)"
