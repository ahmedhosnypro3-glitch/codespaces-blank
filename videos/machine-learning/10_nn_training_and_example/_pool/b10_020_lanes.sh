#!/usr/bin/env bash
# Slide 020: wave-2 audit (storm clause) then comparison judge, attempts 3..6.
# IMG1 = recreation render, IMG2 = original frame.
set -u
NS="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
cd "$NS" || exit 1
PROMPT="$(cat "$NS/judge_template.txt")"

for a in 1 2 3 4; do
  out="_pool/audit2/slide_020.txt"
  env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
    analysis unique_slides/slide_020.jpg \
    --timeout 900 --rounds 1 --tries 1 \
    -p "$(cat _pool/audit_prompt.txt)" > "$out" 2>&1
  cp "$out" "_pool/audit2/slide_020_r$a.txt"
  b=$(wc -c < "$out")
  if grep -q '\[winner\]' "$out" && [ "$b" -ge 4000 ]; then
    echo "audit020: OK attempt $a (${b} bytes)"; break
  fi
  echo "audit020: attempt $a failed (${b} bytes)"
  [ "$a" -lt 4 ] && sleep 120
done

for a in 3 4 5 6; do
  out="qa/slide_020_judge_attempt${a}.txt"
  env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
    comparison qa/slide020/rejudge/render-4.png unique_slides/slide_020.jpg \
    --view "Slide 020 recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$out" 2>&1
  b=$(wc -c < "$out")
  if grep -q 'FINAL VERDICT' "$out" && [ "$b" -ge 1000 ]; then
    v=$(grep -o 'FINAL VERDICT: [A-Z]*' "$out" | head -1)
    echo "judge020 attempt $a: $v (${b} bytes)"
    cp "$out" "qa/slide020/rejudge/last_judge_transcript.txt"
    break
  fi
  echo "judge020 attempt $a: no verdict (${b} bytes)"
  [ "$a" -lt 6 ] && sleep 120
done
echo "020 lanes done"
