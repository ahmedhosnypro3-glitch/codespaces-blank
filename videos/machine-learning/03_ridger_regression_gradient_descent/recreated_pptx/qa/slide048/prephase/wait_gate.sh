#!/bin/bash
# Poll until the fleet analyzer count drops below 8 (yield to cert lanes).
for i in $(seq 1 45); do
  n=$(pgrep -c -f "[a]nalyze_image.py" || true)
  echo "$(date -u +%H:%M:%S) procs=$n"
  if [ "${n:-0}" -lt 8 ]; then echo "SLOT OPEN"; exit 0; fi
  sleep 120
done
echo "STILL BUSY after 45 polls (90 min)"
exit 9
