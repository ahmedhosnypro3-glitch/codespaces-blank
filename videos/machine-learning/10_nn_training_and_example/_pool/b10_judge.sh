#!/usr/bin/env bash
# Judge dispatch for scope b10 slides 019/020 (rejudge protocol Step 4 shape).
# IMG1 = recreation render, IMG2 = original frame. Records attempts in qa/.
# Storm clause only for connection/429/timeout: sleep 120s, retry, max 6 tries.
# A real FAIL verdict stops the loop (needs adjudication + fix), no blind re-roll.
set -u
NS="/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
cd "$NS" || exit 1
PROMPT="$(cat "$NS/judge_template.txt")"
VIEW="Recreation render vs original lecture frame"
CAP="13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame"

for spec in 019 020; do
  render="qa/slide${spec}/rejudge/render-4.png"
  frame="unique_slides/slide_${spec}.jpg"
  verdict="NONE"
  for a in 1 2 3 4 5 6; do
    out="qa/slide_${spec}_judge_attempt${a}.txt"
    env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
      python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
      comparison "$render" "$frame" \
      --view "Slide ${spec} ${VIEW}" --capture "$CAP" \
      -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$out" 2>&1
    bytes=$(wc -c < "$out")
    if grep -q 'FINAL VERDICT' "$out" && [ "$bytes" -ge 1000 ]; then
      verdict=$(grep -o 'FINAL VERDICT: [A-Z]*' "$out" | head -1)
      echo "slide_${spec} attempt ${a}: ${verdict} (${bytes} bytes) -> ${out}"
      [ "$verdict" = "FINAL VERDICT: PASS" ] && break
      echo "slide_${spec} attempt ${a} VERDICT FAIL — stop, adjudicate + fix needed"
      break
    else
      echo "slide_${spec} attempt ${a}: no verdict (${bytes} bytes) — storm clause sleep 120"
      [ "$a" -lt 6 ] && sleep 120
    fi
  done
  cp "qa/slide_${spec}_judge_attempt${a}.txt" "qa/slide${spec}/rejudge/last_judge_transcript.txt" 2>/dev/null
  echo "slide_${spec} FINAL: ${verdict} (attempt ${a})"
done
