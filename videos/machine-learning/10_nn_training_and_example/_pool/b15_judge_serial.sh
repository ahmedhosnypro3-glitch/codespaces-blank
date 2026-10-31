#!/usr/bin/env bash
# b15: judge slide 030 (IMG1 = recreation render, IMG2 = original frame).
# Serialized: ONE vision call at a time in this namespace (concurrent heavy
# calls draw upstream 400/429 rejections). All gate slots available so the
# call is never blocked by gate contention.
# Storm clause: on HTTP 400 upstream_rejected / 429 / 502 / 504 / connection
# error / timeout, sleep 120s and retry up to 3x per attempt.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
N=030
RENDER="$NS/qa/slide${N}/b15/render-1.png"
ORIG="$NS/unique_slides/slide_${N}.jpg"
PROMPT="$(cat "$NS/judge_template.txt")"
ATT=$1
OUT="$NS/qa/slide_${N}_judge_attempt${ATT}.txt"

verdict() {
  if grep -q 'FINAL VERDICT: PASS' "$OUT" 2>/dev/null; then echo PASS; return 0; fi
  if grep -q 'FINAL VERDICT: FAIL' "$OUT" 2>/dev/null; then echo FAIL; return 1; fi
  echo INVALID; return 2
}

for try in 1 2 3; do
  echo "=== slide 030 judge attempt $ATT try $try $(date +%F\ %T) ==="
  timeout 900 env VISION_SLOTS=6 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" comparison "$RENDER" "$ORIG" \
    --view "Slide 30 recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 780 --rounds 1 --tries 1 > "$OUT.tmp" 2>&1
  rc=$?
  mv "$OUT.tmp" "$OUT"
  v=$(verdict)
  echo "slide 030 judge attempt $ATT try $try rc=$rc bytes=$(wc -c < "$OUT") verdict=$v"
  if [ "$v" != INVALID ]; then exit 0; fi
  if grep -Eiq "upstream_rejected|HTTP 400|HTTP 429|\b429\b|502|504|ServiceTimeout|ConnectionReset|Connection aborted|Connection error|EmptyStreamError|empty content|timed out|Timeout" "$OUT"; then
    if [ "$try" -lt 3 ]; then echo "storm clause — sleep 120s"; sleep 120; continue; fi
  fi
  break
done
echo "slide 030 judge attempt $ATT FINAL bytes=$(wc -c < "$OUT") verdict=$(verdict)"
exit 3
