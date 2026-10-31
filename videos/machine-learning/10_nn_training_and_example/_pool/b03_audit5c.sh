#!/usr/bin/env bash
# b03 slide_005 fresh wave-2 audit, storm-aware. Writes _pool/audit2/slide_005.txt only
# when the transcript is valid ([winner] AND >=4000 bytes AND completes section 9).
# Distinct temp file so it never collides with _pool/audit2/run_one.sh's .tmp.
set -u
NS=/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example
TOOL=/home/codespace/ai_llm_slides/.agents/skills/image-analysis/scripts/analyze_image.py
cd "$NS" || exit 9
OUT=_pool/audit2/slide_005.txt
TMP=_pool/audit2/slide_005.b03.tmp
LOG=_pool/b03_audit5c.log

valid() { grep -qa "\[winner\]" "$TMP" 2>/dev/null && \
          [ "$(wc -c <"$TMP" 2>/dev/null || echo 0)" -ge 4000 ] && \
          grep -qa "## 9. VERDICT" "$TMP" 2>/dev/null; }

for r in 1 2 3 4 5 6 7 8; do
  echo "$(date '+%F %T') b03 audit5c try $r start" >> "$LOG"
  env VISION_SLOTS=3 bash _pool/vision_gate.sh python3 "$TOOL" analysis \
    unique_slides/slide_005.jpg --timeout 900 --rounds 1 --tries 1 \
    --max-tokens 32768 \
    -p "$(cat _pool/audit_prompt.txt)" > "$TMP" 2>&1
  rc=$?
  if valid; then
    cp "$TMP" qa/slide005/rejudge/b03/audit2_slide005_valid_$(date +%H%M%S).txt
    cp "$TMP" "$OUT"
    echo "$(date '+%F %T') b03 audit5c OK try $r rc=$rc bytes=$(wc -c <"$OUT")" >> "$LOG"
    exit 0
  fi
  echo "$(date '+%F %T') b03 audit5c try $r failed rc=$rc bytes=$(wc -c <"$TMP" 2>/dev/null)" >> "$LOG"
  cp "$TMP" "qa/slide005/rejudge/b03/audit2_slide005_b03try${r}_failed.txt" 2>/dev/null
  sleep 240
done
echo "$(date '+%F %T') b03 audit5c EXHAUSTED" >> "$LOG"
exit 1
