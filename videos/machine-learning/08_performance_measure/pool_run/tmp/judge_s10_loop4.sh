#!/usr/bin/env bash
# Slide 010 judge loop4 (light probe): attempts 25-32 on render_8.png, original-first,
# SAME judge prompt but capped generation (--max-tokens 24000, --thinking high kept)
# and shorter per-request timeout (--timeout 240 -> HangError abort at 270s) so each
# internal retry cycle is ~4.5min and the HARD_RETRY_CAP=3 ladder fits in ~15min.
# Outer timeout 1200s, 480s spacing between attempts.
cd /home/codespace/ai_llm_slides
NS=videos/machine-learning/08_performance_measure
OUT=$NS/recreated_pptx/qa/slide010
for i in 25 26 27 28 29 30 31 32; do
  sleep 480
  echo "=== attempt_$i start $(date -u +%FT%TZ) ==="
  timeout 1200 bash scripts/16_vision_gate.sh /home/codespace/.pyenv/versions/3.15.2/bin/python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison $NS/unique_slides/slide_010.jpg /home/codespace/ai_llm_slides/$NS/recreated_pptx/qa/slide010/render_8.png --view "Slide 10 recreation — judge vs original lecture frame" --capture "IMG1=original lecture video frame (ground truth, read first); IMG2=150dpi PNG render of the recreation (read second)" --thinking high --max-tokens 24000 --timeout 240 --rounds 1 --tries 1 -p "$(cat $NS/pool_run/judge_prompt_template.txt)" > $OUT/judge_attempt_$i.txt 2>&1
  echo "exit=$? bytes=$(wc -c < $OUT/judge_attempt_$i.txt)"
  if grep -q "FINAL VERDICT" $OUT/judge_attempt_$i.txt; then echo "VERDICT FOUND in attempt_$i"; break; fi
done
echo "loop4 done $(date -u +%FT%TZ)"
