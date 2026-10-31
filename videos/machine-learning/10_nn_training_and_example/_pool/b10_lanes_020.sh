#!/usr/bin/env bash
# b10 slide 020 lanes: missing wave-2 audit, then judge attempts 6..8 against
# the current build render (render-4.png, pixel-identical to deliverable).
# Attempts 1-5 were transport/429 deaths (no verdict) — do not consume budget.
set -u
NS="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
cd "$NS" || exit 1
PROMPT="$(cat "$NS/judge_template.txt")"

# --- wave-2 audit (fresh analysis; advisory, judge does not depend on it) ---
for a in 1 2 3; do
  out="_pool/audit2/slide_020.txt"
  env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
    analysis unique_slides/slide_020.jpg \
    --timeout 900 --rounds 1 --tries 1 --max-tokens 16000 \
    -p "$(cat _pool/audit_prompt.txt)" > "$out" 2>&1
  cp "$out" "_pool/audit2/slide_020_r${a}.txt"
  b=$(wc -c < "$out")
  if grep -q '\[winner\]' "$out" && [ "$b" -ge 4000 ]; then
    echo "audit020: OK attempt $a (${b} bytes)"; break
  fi
  echo "audit020: attempt $a failed (${b} bytes) — storm sleep 120"
  [ "$a" -lt 3 ] && sleep 120
done

# --- comparison judge, attempts 6..8 ---
for a in 6 7 8; do
  out="qa/slide_020_judge_attempt${a}.txt"
  env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
    comparison qa/slide020/rejudge/render-4.png unique_slides/slide_020.jpg \
    --view "Slide 020 recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 --max-tokens 16000 > "$out" 2>&1
  b=$(wc -c < "$out")
  if grep -q 'FINAL VERDICT' "$out" && [ "$b" -ge 1000 ]; then
    v=$(grep -o 'FINAL VERDICT: [A-Z]*' "$out" | head -1)
    echo "judge020 attempt $a: $v (${b} bytes)"
    cp "$out" "qa/slide020/rejudge/last_judge_transcript.txt"
    break
  fi
  echo "judge020 attempt $a: no verdict (${b} bytes) — storm sleep 120"
  [ "$a" -lt 8 ] && sleep 120
done
echo "020 lanes done"
