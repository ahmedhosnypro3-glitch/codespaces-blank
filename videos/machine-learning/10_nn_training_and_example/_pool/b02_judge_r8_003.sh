#!/usr/bin/env bash
# b02 judge runner r8 — SERIAL (one vision call at a time, VISION_SLOTS=2), no
# outer timeout wrapper (the script's own wall governs, §10.2). Slide 3 only.
#
# Judge target: CURRENT slide-3 build bytes (render md5 a8c5dd2a, r5 chain).
# Prior attempt history for slide 3 on these bytes was banked to
# qa/slide_003_judge_attempt{1..12}.txt; attempt 4 is the documented next number
# in the r5 render sub-chain, so the new transcript goes to
# qa/slide003/rejudge/r5/judge_attempt_4.txt (nothing banked there yet).
# Attempts 1-3 in that sub-chain were 429/0-byte stubs; attempt 7 on the OLD r4
# render truncated at the token budget = NO-RESULT (not FAIL).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
PROMPT="$(cat judge_template.txt)"
RENDER="qa/slide003/rejudge/r5/render-1.png"
OUT="qa/slide003/rejudge/r5/judge_attempt_4.txt"
LOG=_pool/b02_judge_r8.out
: > "$LOG"

echo "r5 render md5: $(md5sum "$RENDER" | cut -d' ' -f1)" >> "$LOG"
[ -f "$OUT" ] && [ -s "$OUT" ] && cp -p "$OUT" \
  "qa/slide003/rejudge/r5/prior_attempts/judge_attempt_4_$(date +%H%M%S).txt"

for k in 1 2 3; do
  echo "slide 003 attempt ${k} START $(date -u +%T) render=$(md5sum "$RENDER" | cut -c1-8)" >> "$LOG"
  env VISION_SLOTS=2 bash _pool/vision_gate.sh \
    python3 -u /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
    comparison "$RENDER" "unique_slides/slide_003.jpg" \
    --view "Slide 003: image 1 = recreation render, image 2 = original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 780 --rounds 1 --tries 1 --max-tokens 24000 \
    > "$OUT" 2>&1
  rc=$?
  echo "slide 003 attempt ${k} rc=${rc} $(date -u +%T) bytes=$(wc -c < "$OUT")" >> "$LOG"
  if grep -q 'FINAL VERDICT' "$OUT"; then
    echo "slide 003 VERDICT: $(grep 'FINAL VERDICT' "$OUT" | tail -1)" >> "$LOG"
    echo "r8 done PASS $(date -u +%T)" >> "$LOG"
    exit 0
  fi
  if grep -qE 'HTTP 429|HTTP 502|HTTP 504|upstream_rate_limited|HangError|EmptyStreamError|Connection reset|Connection aborted|every model failed' "$OUT"; then
    echo "slide 003 STORM-sleep180" >> "$LOG"
    sleep 180
    continue
  fi
  echo "slide 003 NO-VERDICT-NO-STORM (candidate NO-RESULT: truncated or wall)" >> "$LOG"
  exit 1
done
echo "slide 003 exhausted 3 attempts without verdict" >> "$LOG"
exit 1
