#!/usr/bin/env bash
# Gate law: before EACH vision call, if >=8 analyze_image.py are queued, do NOT dispatch.
N=$(pgrep -c -f analyze_image.py || echo 0)
if [ "$N" -ge 8 ]; then
  echo "GATE CONGESTED: $N analyze_image.py processes queued -- NOT dispatching. Heartbeat, sleep 240, re-probe."
  exit 3
fi
echo "gate open: $N queued"
exit 0
