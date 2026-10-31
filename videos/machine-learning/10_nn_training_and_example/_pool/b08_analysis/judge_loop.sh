#!/usr/bin/env bash
# b08 judge retry loop — storm clause: 429/hang -> sleep 120, retry (max 3 attempts/slide).
# Each attempt is banked to its OWN file (never overwrites a prior transcript).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
cd "$NS"
PROMPT="$(cat judge_template.txt)"
judge() { # $1 slide num, $2 attempt, $3 render dir
  local n="$1" a="$2" dir="$3"
  local out="qa/slide${n}/judge/judge_attempt_${a}.txt"
  echo "--- slide $n attempt $a start $(date +%T)"
  VISION_SLOTS=4 timeout 560 ./_pool/vg_spin.sh \
    python3 "$SKILL/scripts/analyze_image.py" comparison \
    "$dir/render-1.png" "unique_slides/slide_${n}.jpg" \
    --view "Slide ${n} recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$out" 2>&1
  local rc=$?
  echo "slide $n attempt $a rc=$rc bytes=$(wc -c < "$out") $(date +%T)"
  grep -q 'FINAL VERDICT' "$out" && return 0
  return 1
}
for round in 3 4 5; do
  ok15=1; ok16=1
  judge 015 "$round" qa/slide015/r2 || ok15=0
  judge 016 "$round" qa/slide016/r2 || ok16=0
  [ "$ok15" = 1 ] && [ "$ok16" = 1 ] && { echo "BOTH PASSED round $round"; break; }
  echo "storm: sleep 120 before next round $(date +%T)"
  sleep 120
done
echo "=== b08 judge loop done $(date +%T)"
