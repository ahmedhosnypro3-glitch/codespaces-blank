#!/usr/bin/env bash
# One integrator poll: drift-check canonical files (restore if needed), then
# detect a complete new candidate asset set. Prints CANDIDATE=<dir> on stdout
# if a fresh complete candidate is found (and not yet claimed).
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
W=$RJ/slide025
PPTX=$NS/recreated_pptx/slide_025_recreated.pptx
CAN_PPTX=c50e78bf39531523dcf69d652254b647
CAN_TL=cd62022fbf0cfe30a351309c0230adb3
CAN_TR=b45c723af19e2cf11659109d63134cad
CAN_BL=7a8e7210f118b728245d268552a7d32d
CAN_BR=f6af102ec110ff5113482659ff4f9d73
LOG=$W/CLOBBER_WATCH.log
ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }

# --- drift check on deliverable + build assets ---
m() { md5sum "$1" 2>/dev/null | awk '{print $1}'; }
drift=0
[ "$(m "$PPTX")" = "$CAN_PPTX" ] || drift=1
for p in tl:$CAN_TL tr:$CAN_TR bl:$CAN_BL br:$CAN_BR; do
  n=${p%%:*}; c=${p##*:}
  [ "$(m "$NS/recreated_pptx/build/assets/plot_025_$n.png")" = "$c" ] || drift=1
done
if [ "$drift" = 1 ]; then
  echo "[$(ts)] INTEGRATOR DRIFT DETECTED — restoring canonical from preK17n.bak + assets_k17g" >> "$LOG"
  cp "$W/slide_025_recreated.preK17n.bak.pptx" "$PPTX"
  for n in tl tr bl br; do cp "$W/assets_k17g/plot_025_$n.png" "$NS/recreated_pptx/build/assets/plot_025_$n.png"; done
  echo "[$(ts)] INTEGRATOR restore done: pptx=$(m "$PPTX") bl=$(m "$NS/recreated_pptx/build/assets/plot_025_bl.png")" >> "$LOG"
fi

# --- candidate detection ---
# Permitted producer sets (k17t original-crop is NOT permitted — skip).
for tag in k17r k17s k17t2 k17t3; do
  d=$W/assets_$tag
  [ -d "$d" ] || continue
  [ -f "$W/INTEGRATOR_CLAIM_$tag" ] && continue
  ok=1
  for n in tl tr bl br; do [ -s "$d/plot_025_$n.png" ] || ok=0; done
  [ "$ok" = 1 ] || continue
  # stable: newest file at least 20s old
  newest=$(find "$d" -name 'plot_025_*.png' -printf '%T@\n' | sort -nr | head -1)
  now=$(date +%s)
  if [ -n "$newest" ] && [ $(( now - ${newest%.*} )) -ge 20 ]; then
    echo "CANDIDATE=$d TAG=$tag"
    exit 0
  fi
done
# single-best-BL candidates: a dir with only plot_025_bl.png (fresh, unclaimed)
for tag in k17r_bl k17s_bl k17t3_bl; do
  d=$W/assets_$tag
  [ -s "$d/plot_025_bl.png" ] || continue
  [ -f "$W/INTEGRATOR_CLAIM_$tag" ] && continue
  newest=$(stat -c %Y "$d/plot_025_bl.png" 2>/dev/null) || continue
  now=$(date +%s)
  if [ $(( now - newest )) -ge 20 ]; then
    echo "CANDIDATE=$d TAG=$tag BLONLY=1"
    exit 0
  fi
done
exit 1
