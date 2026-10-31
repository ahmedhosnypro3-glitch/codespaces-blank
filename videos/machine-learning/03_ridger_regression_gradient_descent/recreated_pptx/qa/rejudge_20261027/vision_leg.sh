#!/usr/bin/env bash
# vision_leg.sh — storm-proof single vision judge leg for deck 03.
# All retry/backoff happens INSIDE this one bash call so the calling agent
# never sees a 429 as a tool failure and never dies on it.
# usage: vision_leg.sh <transcript_out> <timeout_s> <img1> <img2> <view> <capture> <payload_file>
# exit 0 + transcript contains FINAL VERDICT and no 429 => success.
set -u
ROOT=/home/codespace/ai_llm_slides
OUT=$1; TMO=$2; IMG1=$3; IMG2=$4; VIEW=$5; CAP=$6; PAY=$7
cd "$ROOT" || exit 2
occ() { ps -eo args | grep -c '[a]nalyze_image[.]py'; }
OCC_MAX=${OCC_MAX:-6}
ATTEMPTS=${ATTEMPTS:-5}
for attempt in $(seq 1 "$ATTEMPTS"); do
  for i in $(seq 1 30); do
    n=$(occ); [ "$n" -lt "$OCC_MAX" ] && break; sleep 30
  done
  sleep $((RANDOM % 60))
  rm -f "$OUT"
  timeout 1700 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py comparison \
    "$IMG1" "$IMG2" --view "$VIEW" --capture "$CAP" \
    --thinking high --max-tokens 65536 --timeout "$TMO" --rounds 1 --tries 1 \
    --transcript "$OUT" -p "$(cat "$PAY")" > "${OUT}.log" 2>&1
  rc=$?
  if [ -f "$OUT" ] && grep -q 'FINAL VERDICT' "$OUT" && ! grep -qi '429' "$OUT"; then
    echo "OK attempt=$attempt rc=$rc"
    grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$OUT" | tail -1
    exit 0
  fi
  echo "attempt=$attempt rc=$rc no-clean-verdict; backoff 240s" >> "${OUT}.log"
  sleep 240
done
echo "EXHAUSTED after $ATTEMPTS attempts"
exit 1
