#!/usr/bin/env bash
# b15: judge ONE slide (IMG1 = recreation render, IMG2 = original frame),
# per _pool/REJUDGE_PROTOCOL.md. Storm clause: on Connection error / 429 / 502 /
# 504 / empty stream / timeout, sleep 120s and retry up to 3x per attempt group.
# Max 6 judge attempts total, then bank failure and stop.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
SKILL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis
N=$(printf '%03d' "$((10#$1))")
RENDER="$NS/qa/slide${N}/b15/render-1.png"
ORIG="$NS/unique_slides/slide_${N}.jpg"
PROMPT="$(cat "$NS/judge_template.txt")"
OUT="$NS/qa/slide_${N}_judge_attempt$(($2)).txt"

verdict() { grep -q 'FINAL VERDICT: PASS' "$OUT" 2>/dev/null && echo PASS && return 0; grep -q 'FINAL VERDICT: FAIL' "$OUT" 2>/dev/null && echo FAIL && return 1; echo INVALID; return 2; }

for try in 1 2 3; do
  echo "=== slide $N judge attempt $2 try $try $(date +%F\ %T) ==="
  timeout 540 env VISION_SLOTS=3 bash "$NS/_pool/vision_gate.sh" \
    python3 "$SKILL/scripts/analyze_image.py" comparison "$RENDER" "$ORIG" \
    --view "Slide ${N#0} recreation render vs original lecture frame" \
    --capture "13.33x7.5in slide, 150dpi render (2001x1125px) vs 960x540px original frame" \
    -p "$PROMPT" --timeout 420 --rounds 1 --tries 1 > "$OUT.tmp" 2>&1
  rc=$?
  mv "$OUT.tmp" "$OUT"
  v=$(verdict)
  echo "slide $N judge attempt $2 try $try rc=$rc bytes=$(wc -c < "$OUT") verdict=$v"
  if [ "$v" != INVALID ]; then exit 0; fi
  if grep -Eiq "Connection error|ConnectionReset|Connection aborted|HTTP 429|\b429\b|502|504|ServiceTimeout|EmptyStreamError|empty content|timed out|Timeout" "$OUT"; then
    if [ "$try" -lt 3 ]; then echo "slide $N: provider storm on try $try — sleep 120s"; sleep 120; continue; fi
  fi
  break
done
echo "slide $N judge attempt $2 FINAL bytes=$(wc -c < "$OUT") verdict=$(verdict)"
exit 3
