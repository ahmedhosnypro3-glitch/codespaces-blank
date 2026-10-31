#!/usr/bin/env bash
# b02 judge runner r5 — judge the CURRENT build bytes (first judged attempt).
# IMG1 = recreation render, IMG2 = original frame (frozen judge_template.txt order).
# Storm clause: 429/502/504/timeout/connection error -> sleep 120s, retry (max 3).
# Max 6 CONTENT attempts per slide (1 used: the stale-render FAIL); storm failures
# are transport retries and do not consume a content attempt.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS"
PROMPT="$(cat judge_template.txt)"
LOG=_pool/b02_judge_r5.out
: > "$LOG"

run_one() {
  local n="$1" render="$2" first="$3" last="$4"
  for k in $(seq "$first" "$last"); do
    local out="qa/slide_${n}_judge_attempt${k}.txt"
    echo "slide ${n} attempt ${k} START $(date -u +%T)" >> "$LOG"
    env VISION_SLOTS=3 timeout 480 bash _pool/vision_gate.sh \
      python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
      comparison "$render" "unique_slides/slide_${n}.jpg" \
      --view "Slide ${n}: image 1 = recreation render, image 2 = original lecture frame" \
      --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
      -p "$PROMPT" --timeout 240 --rounds 1 --tries 1 > "$out" 2>&1
    local rc=$?
    echo "slide ${n} attempt ${k} rc=${rc} $(date -u +%T) bytes=$(wc -c < "$out")" >> "$LOG"
    if grep -q 'FINAL VERDICT' "$out"; then
      echo "slide ${n} attempt ${k} VERDICT: $(grep 'FINAL VERDICT' "$out" | tail -1)" >> "$LOG"
      return 0
    fi
    if grep -qE 'HTTP 429|HTTP 502|HTTP 504|upstream_rate_limited|HangError|EmptyStreamError|timed out|Connection reset|Connection aborted|every model failed' "$out"; then
      echo "slide ${n} attempt ${k} STORM-sleep120" >> "$LOG"
      sleep 120
      continue
    fi
    echo "slide ${n} attempt ${k} NONSTORM-FAIL (no verdict, no storm signature)" >> "$LOG"
    return 1
  done
  echo "slide ${n} exhausted attempts ${first}..${last}" >> "$LOG"
  return 1
}

run_one 003 qa/slide003/rejudge/r4/render-1.png 7 9 &
P1=$!
sleep 15
run_one 004 qa/slide004/rejudge/r3/render-1.png 5 7 &
P2=$!
wait $P1 $P2
echo "both runners done $(date -u +%T)" >> "$LOG"
