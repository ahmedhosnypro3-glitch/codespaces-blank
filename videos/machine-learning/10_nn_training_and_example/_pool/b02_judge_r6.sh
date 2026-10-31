#!/usr/bin/env bash
# b02 judge runner r6 — judge CURRENT build bytes for slides 3 (rebuild) and 4.
# fix vs r5: --max-tokens 24000 (analyzer default 8192 truncated attempt 7 at
# 30,760 chars mid-body) and longer per-request/outer walls for the saturated
# gateway. IMG1 = recreation render, IMG2 = original frame (frozen template).
# Storm clause: 429/502/504/HangError/timeout/reset -> sleep 120s, retry (max 3).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
PROMPT="$(cat judge_template.txt)"
MAXTOK="${MAXTOK:-24000}"
LOG=_pool/b02_judge_r6.out
: > "$LOG"

run_one() {
  local n="$1" render="$2" first="$3" last="$4"
  for k in $(seq "$first" "$last"); do
    local out="qa/slide_${n}_judge_attempt${k}.txt"
    echo "slide ${n} attempt ${k} START $(date -u +%T) render=$(md5sum "$render" | cut -c1-8)" >> "$LOG"
    env VISION_SLOTS=2 timeout 900 bash _pool/vision_gate.sh \
      python3 /home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py \
      comparison "$render" "unique_slides/slide_${n}.jpg" \
      --view "Slide ${n}: image 1 = recreation render, image 2 = original lecture frame" \
      --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
      -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 --max-tokens "$MAXTOK" \
      > "$out" 2>&1
    local rc=$?
    echo "slide ${n} attempt ${k} rc=${rc} $(date -u +%T) bytes=$(wc -c < "$out")" >> "$LOG"
    if grep -q 'FINAL VERDICT' "$out"; then
      echo "slide ${n} attempt ${k} VERDICT: $(grep 'FINAL VERDICT' "$out" | tail -1)" >> "$LOG"
      return 0
    fi
    if grep -qE 'HTTP 429|HTTP 502|HTTP 504|upstream_rate_limited|HangError|EmptyStreamError|timed out|Connection reset|Connection aborted|every model failed|No such file' "$out"; then
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

run_one 003 qa/slide003/rejudge/r5/render-1.png 8 10 &
P1=$!
sleep 20
run_one 004 qa/slide004/rejudge/r3/render-1.png 6 8 &
P2=$!
wait $P1 $P2
echo "both runners done $(date -u +%T)" >> "$LOG"
