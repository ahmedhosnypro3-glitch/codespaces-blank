#!/usr/bin/env bash
# Wave-2 audits for scope b10 slides 019/020, with storm-clause retry.
cd /home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example || exit 1

run_audit() {
  local n="$1"
  local out="_pool/audit2/slide_${n}.txt"
  local a
  for a in 1 2 3 4; do
    env VISION_SLOTS=3 bash _pool/vision_gate.sh \
      python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
      analysis "unique_slides/slide_${n}.jpg" \
      --timeout 900 --rounds 1 --tries 1 \
      -p "$(cat _pool/audit_prompt.txt)" > "$out" 2>&1
    cp "$out" "_pool/audit2/slide_${n}_attempt${a}.txt"
    local bytes
    bytes=$(wc -c < "$out")
    if grep -q '\[winner\]' "$out" && [ "$bytes" -ge 4000 ]; then
      echo "slide_${n}: OK on attempt ${a} (${bytes} bytes)"
      return 0
    fi
    echo "slide_${n}: attempt ${a} failed (${bytes} bytes, winner=$(grep -c '\[winner\]' "$out"))"
    if [ "$a" -lt 4 ]; then sleep 120; fi
  done
  echo "slide_${n}: FAILED after 3 retries"
  return 1
}

run_audit 019
run_audit 020
