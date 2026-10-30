#!/usr/bin/env bash
P="/workspace""s/codespace-blank/ai_llm_slides"
QA="$P/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide049"
export TMPDIR="$P/scratch/tmp"; mkdir -p "$TMPDIR"
LOG="$QA/worker_report_progress.log"
say(){ echo "[$(date -u +%H:%M:%S)] $*" >> "$LOG"; }
FIRED=0
for round in $(seq 1 400); do
  L=$(pgrep -c -f analyze_image.py 2>/dev/null || echo 99)
  if [ "${L:-99}" -ge 8 ]; then sleep 240; continue; fi
  say "round $round: slot open load=$L - firing Template A"
  rm -f "$QA/judge_attempt_6.txt"
  timeout 1700 bash "$P/scripts/16_vision_gate.sh" python3 \
    "$P/.agents/skills/image-analysis/analyze_image.py" comparison \
    "$QA/render_6.png" "$P/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_049.jpg" \
    --view "Slide 049 recreation - fidelity check vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    --transcript "$QA/judge_attempt_6.txt" -p "$(cat "$QA/judge_prompt_6.txt")" \
    > "$QA/judge_6_dispatch.log" 2>&1
  say "Template A exited rc=$?"
  if [ -s "$QA/judge_attempt_6.txt" ] && grep -q "FINAL VERDICT" "$QA/judge_attempt_6.txt"; then
    say "BANKED VERDICT: $(grep -o 'FINAL VERDICT: [A-Z]*' "$QA/judge_attempt_6.txt" | tail -1)"
    FIRED=1; break
  fi
  say "no usable transcript"
  tail -2 "$QA/judge_6_dispatch.log" 2>&1 | while read -r l; do say "    $l"; done
  sleep 60
done
say "dispatcher finished FIRED=$FIRED"
