#!/usr/bin/env bash
# S6 042 LEG B crop with gate back-off (park law): 6 probes x 240s then park.
# Args: NAME K PAIRK REGION
set -u
cd /home/ahmed/Projects/ai_llm_slides || exit 1
NAME="$1"; K="$2"; PAIRK="$3"; REGION="$4"
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
bash $QA/dispatch_crop_generic.sh "$NAME" "$K" "$PAIRK" "$REGION"
