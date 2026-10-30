#!/usr/bin/env bash
# S6 042 frame-read leg with gate back-off (park law): 6 probes x 240s then park.
# Args: NAME TRANSCRIPT  (image qa/slide042/readcrop_${NAME}.png, payload read_payload_${NAME}.txt)
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 1
NAME="$1"; TRANSCRIPT="$2"
export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp
GATE="scripts/16_vision_gate.sh"
PY=".agents/skills/image-analysis/scripts/analyze_image.py"
QA="videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042"
for i in 1 2 3 4 5 6; do
  n=$(pgrep -f "python3 .*analyze_image.py" | wc -l)
  if [ "${n:-0}" -lt 8 ]; then echo "GATE OK: $n"; break; fi
  echo "GATE BUSY: $n — probe $i, heartbeat + sleep 240"
  VIDEO=machine-learning/03_ridger_regression_gradient_descent \
    python3 scripts/15_progress.py heartbeat 42 kimi-s6-3756628 || true
  sleep 240
  [ "$i" = 6 ] && { echo "PARKED: gate never <8 after 6 probes"; exit 99; }
done
$GATE timeout 1700 python3 $PY analysis \
  $QA/readcrop_${NAME}.png \
  --view "Zoomed read-crop from the ORIGINAL slide 042 lecture frame" \
  --thinking high --max-tokens 65536 --timeout 1200 --rounds 1 --tries 1 \
  --transcript $QA/$TRANSCRIPT \
  -p "$(cat $QA/read_payload_${NAME}.txt)"
echo "READ $NAME EXIT=$?"
