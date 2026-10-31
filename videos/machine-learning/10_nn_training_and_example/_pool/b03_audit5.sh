#!/usr/bin/env bash
# b03 wave-2 fresh audit for slide_005 (storm-resilient, max 3 tries + 120s sleeps).
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
TOOL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
cd "$NS" || exit 9
OUT=_pool/audit2/slide_005.txt
ok() { [ -f "$OUT" ] && [ "$(wc -c <"$OUT")" -ge 4000 ] && grep -qa "\[winner\]" "$OUT"; }
for r in 1 2 3; do
  echo "$(date '+%F %T') b03 audit5 try $r start"
  env VISION_SLOTS=3 bash _pool/vision_gate.sh python3 "$TOOL" analysis \
    unique_slides/slide_005.jpg --timeout 900 --rounds 1 --tries 1 \
    -p "$(cat _pool/audit_prompt.txt)" > "$OUT" 2>&1
  rc=$?
  if ok; then
    echo "$(date '+%F %T') b03 audit5 OK try $r rc=$rc bytes=$(wc -c <"$OUT")"
    exit 0
  fi
  echo "$(date '+%F %T') b03 audit5 try $r failed rc=$rc bytes=$(wc -c <"$OUT")"
  if [ -f "$OUT" ]; then cp "$OUT" "qa/slide005/rejudge/b03/audit2_slide005_try${r}_failed.txt"; fi
  if [ "$r" -lt 3 ]; then sleep 120; fi
done
echo "$(date '+%F %T') b03 audit5 EXHAUSTED"
exit 1
