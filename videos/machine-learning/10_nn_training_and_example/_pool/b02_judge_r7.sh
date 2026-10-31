#!/usr/bin/env bash
# b02 judge runner r7 — patient retry under sustained upstream 429 storm.
# r6 outcome: attempts 8/6 = HTTP 429 upstream_rate_limited; 9/7 killed by the
# 900s task cap before the gate freed a slot. r7 raises backoff to 240s,
# continues attempt numbering (003: 10..12, 004: 8..10), same renders.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
cd "$NS" || exit 1
PROMPT="$(cat judge_template.txt)"
MAXTOK=24000
LOG=_pool/b02_judge_r7.out
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
      echo "slide ${n} attempt ${k} STORM-sleep240" >> "$LOG"
      sleep 240
      continue
    fi
    echo "slide ${n} attempt ${k} NONSTORM-FAIL (no verdict, no storm signature)" >> "$LOG"
    return 1
  done
  echo "slide ${n} exhausted attempts ${first}..${last}" >> "$LOG"
  return 1
}

run_one 003 qa/slide003/rejudge/r5/render-1.png 10 12 &
P1=$!
sleep 20
run_one 004 qa/slide004/rejudge/r3/render-1.png 8 10 &
P2=$!
wait $P1 $P2
echo "both runners done $(date -u +%T)" >> "$LOG"
