#!/bin/bash
# Verify-wing corroboration read for slide 26 (08_performance_measure).
# Runs from repo root; all writes stay inside the namespace.
cd /home/codespace/ai_llm_slides || exit 1
NS=videos/machine-learning/08_performance_measure
OUT="$NS/recreated_pptx/qa/slide026/judge_verify_1.txt"
TMP="$NS/pool_run/.verify_wing_slide26_attempt.tmp"
PROMPT=$(cat "$NS/pool_run/judge_prompt_template.txt")

S=$((RANDOM % 61 + 90))
echo "[verify-wing slide26] random pre-call sleep ${S}s $(date -u +%FT%TZ)" | tee -a "$OUT"
sleep "$S"

for i in $(seq 1 8); do
  echo "=== verify attempt $i/8 $(date -u +%FT%TZ) ===" | tee -a "$OUT"
  python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$NS/unique_slides/slide_026.jpg" \
    "$NS/recreated_pptx/qa/slide026/render.png" \
    --thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1 \
    -p "$PROMPT" > "$TMP" 2>&1
  rc=$?
  cat "$TMP" >> "$OUT"
  echo "=== attempt $i rc=$rc bytes=$(wc -c < "$TMP") ===" | tee -a "$OUT"
  if grep -q 'FINAL VERDICT:' "$TMP" && ! grep -qiE '429|HangError|RateLimit' "$TMP"; then
    echo "[verify-wing slide26] verdict obtained on attempt $i" | tee -a "$OUT"
    break
  fi
  if [ "$i" -lt 8 ]; then
    echo "[verify-wing slide26] attempt $i unusable (429/empty/HangError); sleeping 300s before retry" | tee -a "$OUT"
    sleep 300
  fi
done
rm -f "$TMP"
wait
echo "[verify-wing slide26] job done $(date -u +%FT%TZ)" | tee -a "$OUT"
