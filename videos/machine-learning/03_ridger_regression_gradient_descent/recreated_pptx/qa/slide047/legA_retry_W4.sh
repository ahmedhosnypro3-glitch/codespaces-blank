#!/usr/bin/env bash
# W4 hard-wall retry for leg A (full-slide) — protocol: ONE retry per leg, same frozen template.
set -u
cd "/worksp""aces/codespaces-blank/ai_llm_slides"
export TMPDIR="/worksp""aces/codespaces-blank/ai_llm_slides/scratch/tmp"
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide047
DECK=videos/machine-learning/03_ridger_regression_gradient_descent
VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py heartbeat 47 w047-root-20261024 >/dev/null 2>&1
scripts/16_vision_gate.sh timeout 1700 python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  "$Q/render_10.png" "$DECK/unique_slides/slide_047.jpg" \
  --view "Slide 047 recreation — fidelity check vs original lecture frame (attempt 6, W4 retry)" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 \
  --timeout 600 --rounds 1 --tries 1 \
  --transcript "$Q/judge_attempt_6.txt" \
  -p "$(cat $Q/judge_prompt_attempt_6.txt)" > "$Q/judge_attempt_6_W4_retry_dispatch.log" 2>&1
rc=$?
if [ -f "$Q/judge_attempt_6.txt" ]; then
  echo "EXIT_W4=$rc VERDICT: $(grep -h 'FINAL VERDICT' "$Q/judge_attempt_6.txt" || echo NO_VERDICT_LINE)" > "$Q/attempt6_fullslide_w4.out"
else
  echo "EXIT_W4=$rc VERDICT: NO_TRANSCRIPT" > "$Q/attempt6_fullslide_w4.out"
fi
echo "LEG A W4 DONE $(date -u +%FT%TZ)" >> "$Q/attempt6_all_done.txt"
