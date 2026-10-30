#!/usr/bin/env bash
# STORM-RESILIENCE: probe-gated validation retry for slides 12-13.
# cheap 8-token text probe (75s cap) -> real call only on probe body
# -> sleep 120 between cycles -> max 3 attempts/phase
cd /home/codespace/ai_llm_slides
LOG=videos/machine-learning/10_nn_training_and_example/_pool/validate_a7.log
ANALYSIS=videos/machine-learning/10_nn_training_and_example/analysis
KEY=$(cat .analyze-image-key)

for cycle in 1 2 3; do
  for slide in 12 13; do
    out="$ANALYSIS/slide_$(printf '%03d' "$slide")_final.json"
    if [ -f "$out" ]; then
      echo "[cycle $cycle] slide $slide already validated" >> "$LOG"
      continue
    fi
    body=$(timeout 75 curl -s -X POST http://localhost:17844/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $KEY" \
      -d '{"model":"validate_slides","messages":[{"role":"user","content":"Say OK"}],"max_tokens":8,"stream":true}' 2>/dev/null)
    if [ -z "$body" ] || ! printf '%s' "$body" | grep -q 'data:'; then
      echo "[cycle $cycle] slide $slide PROBE FAILED — skip real call" >> "$LOG"
      continue
    fi
    echo "[cycle $cycle] slide $slide probe OK — real call" >> "$LOG"
    timeout 900 python3 scripts/13_validate_slides.py "$ANALYSIS" \
      --from "$slide" --to "$slide" >> "$LOG" 2>&1
    if [ -f "$out" ]; then
      echo "[cycle $cycle] slide $slide VALIDATED" >> "$LOG"
    else
      echo "[cycle $cycle] slide $slide validation did not produce final" >> "$LOG"
    fi
    sleep 120
  done
done
echo "STORM LOOP DONE" >> "$LOG"
