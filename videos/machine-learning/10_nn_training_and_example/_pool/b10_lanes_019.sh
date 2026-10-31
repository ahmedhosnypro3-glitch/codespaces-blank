#!/usr/bin/env bash
# b10 slide 019 re-judge against the FIXED build (render-attempt3.png).
# Attempt 1 was the real FAIL on math index errors; attempt 2 was truncated
# (no max-tokens); attempts are now 3..6 with --max-tokens 16000.
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example || exit 1
PROMPT="$(cat judge_template.txt)"
RENDER="qa/slide019/rejudge/render-attempt3.png"
FRAME="unique_slides/slide_019.jpg"

for a in 3 4 5 6; do
  out="qa/slide_019_judge_attempt${a}.txt"
  env VISION_SLOTS=3 bash _pool/vision_gate.sh \
    python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
    comparison "$RENDER" "$FRAME" \
    --view "Slide 019 recreation render (post-fix) vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 --max-tokens 16000 > "$out" 2>&1
  b=$(wc -c < "$out")
  if grep -q 'FINAL VERDICT' "$out" && [ "$b" -ge 1000 ]; then
    v=$(grep -o 'FINAL VERDICT: [A-Z]*' "$out" | head -1)
    echo "judge019 attempt $a: $v (${b} bytes)"
    cp "$out" "qa/slide019/rejudge/last_judge_transcript.txt"
    break
  fi
  echo "judge019 attempt $a: no verdict (${b} bytes) — storm sleep 120"
  [ "$a" -lt 6 ] && sleep 120
done
echo "019 judge lane done"
