#!/usr/bin/env bash
# Slide 015 judge-leg runner at the approved 1200s inner wall (timeout 1700 outer).
# Payload bytes come from the staged dispatch files; only the --timeout flag was raised.
# Usage: run_legs_1200.sh <judgeA|eq_stack|deriv_stack|solution|pinkbox|peachbox|probe>
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
LEG="${1:?usage: run_legs_1200.sh <leg>}"

gate() { pgrep -c -f analyze_image.py 2>/dev/null || echo 0; }

G="$(gate)"
if [ "$G" -ge 8 ]; then
  echo "[run_legs_1200] leg=$LEG REFUSED: gate=$G >= 8"
  exit 3
fi

case "$LEG" in
  probe) src="$DIR/dispatch_4_probe.txt" ;;
  judgeA) src="$DIR/dispatch_1200_judgeA.txt" ;;
  *) src="$DIR/dispatch_1200_crop_$LEG.txt" ;;
esac
[ -f "$src" ] || { echo "[run_legs_1200] missing $src"; exit 2; }

CMDLINE="$(sed -n '/^REPO=/,$p' "$src")"
echo "[run_legs_1200] leg=$LEG gate=$G running:"
echo "$CMDLINE"
bash -c "eval \"\$1\"" _ "$CMDLINE"
rc=$?
echo "[run_legs_1200] leg=$LEG exit=$rc"
exit $rc
