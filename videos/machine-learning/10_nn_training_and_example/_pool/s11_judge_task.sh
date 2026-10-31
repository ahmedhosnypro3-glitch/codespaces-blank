#!/usr/bin/env bash
# Slide 011 judge: one call away from b06 completion.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
OUT="qa/slide011/rejudge/judge_attempt_15.txt"
RENDER="qa/slide011/rejudge/_attempt2/render-1.png"
ORIG="unique_slides/slide_011.jpg"
echo "=== s011 judge start $(date +%F\ %T) ==="
for i in 1 2 3 4 5 6; do
  echo "--- attempt $i $(date +%T) ---"
  env VISION_SLOTS=1 bash _pool/vision_gate.sh \
    python3 -u /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$RENDER" "$ORIG" \
    --max-tokens 24000 --timeout 780 --rounds 1 --tries 1 \
    --view "Slide 011 Recreation render vs original lecture frame" \
    --capture "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
    -p "$(cat judge_template.txt)" > "$OUT" 2>&1
  rc=$?
  sz=$(wc -c < "$OUT")
  echo "rc=$rc bytes=$sz winners=$(grep -c '\[winner\]' "$OUT")"
  if grep -q 'FINAL VERDICT: PASS' "$OUT"; then echo "VERDICT PASS attempt $i"; break; fi
  if grep -q 'FINAL VERDICT: FAIL' "$OUT"; then echo "VERDICT FAIL attempt $i"; break; fi
  cp -p "$OUT" "${OUT}.storm_$i"
  if [ $i -lt 6 ]; then echo "storm sleep 120 ($(date +%T))"; sleep 120; fi
done
echo "=== s011 judge end $(date +%F\ %T) ==="
tail -5 "$OUT"
