#!/usr/bin/env bash
# Slide 045 — Template A full-slide comparison leg (worker-fresh-045-legs2).
# Payload byte-for-byte from shared_patterns/judge_protocol_03.md Template A via
# the banked judge_prompt_1.txt. --timeout 1200 = the provisional wall extension
# (ratified: a leg would otherwise abort at the 630s client wall), payload unchanged.
set -u
cd /worksp""aces/codespaces-blank/ai_llm_slides || exit 99
export TMPDIR=/worksp""aces/codespaces-blank/ai_llm_slides/scratch/tmp
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide045
echo "=== TEMPLATE A start $(date -u +%H:%M:%S) procs=$(pgrep -c -f analyze_image.py) ==="
timeout 1700 bash scripts/16_vision_gate.sh python3 \
  .agents/skills/image-analysis/scripts/analyze_image.py comparison \
  $Q/render_1.png \
  videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_045.jpg \
  --view "Slide 045 recreation — fidelity check vs original lecture frame" \
  --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript $Q/judge_legs_next.txt \
  -p "$(cat $Q/judge_prompt_1.txt)"
rc=$?
echo "=== TEMPLATE A exit=$rc at $(date -u +%H:%M:%S) ==="
if [ -s $Q/judge_legs_next.txt ]; then
  echo "  transcript bytes: $(wc -c < $Q/judge_legs_next.txt)"
  echo "  FINAL VERDICT lines: $(grep -c 'FINAL VERDICT:' $Q/judge_legs_next.txt)"
  grep -o 'FINAL VERDICT: [A-Z]*' $Q/judge_legs_next.txt | head -3
else
  echo "  NO TRANSCRIPT WRITTEN"
fi
