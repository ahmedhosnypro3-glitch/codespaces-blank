#!/usr/bin/env bash
# CLOBBER_WATCH.sh — guard slide 25 canonical build while k17z2 certification is in flight.
# Polls md5 of the 4 plot_025 assets + slide_025_recreated.pptx every 60s for up to 60 min.
# On ANY deviation from canonical k17g assets / c50e78bf pptx: log to CLOBBER_WATCH.log,
# bank the clobbered files (never delete), restore assets from assets_k17g/, restore the
# byte-exact canonical pptx from a banked copy if one exists (else rebuild via
# node slide_025.js), then re-render render_k17z3.png, chrome-check, regenerate the dense
# crop pair, and relaunch both vision legs (OCC_MAX=700 ATTEMPTS=10).
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 2
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
D=$ROOT/$RJ/slide025
BUILD=$ROOT/$NS/recreated_pptx/build
PPTX=$ROOT/$NS/recreated_pptx/slide_025_recreated.pptx
LOG=$D/CLOBBER_WATCH.log
BANK=$D/assets_k17g
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$D"

CAN_TL=cd62022fbf0cfe30a351309c0230adb3
CAN_TR=b45c723af19e2cf11659109d63134cad
CAN_BL=7a8e7210f118b728245d268552a7d32d
CAN_BR=f6af102ec110ff5113482659ff4f9d73
CAN_PPTX=c50e78bf39531523dcf69d652254b647

m() { md5sum "$1" 2>/dev/null | cut -d' ' -f1; }

# locate a banked byte-exact canonical pptx, if any
CAN_BANK=""
for f in "$D"/*.pptx; do
  [ -f "$f" ] || continue
  if [ "$(m "$f")" = "$CAN_PPTX" ]; then CAN_BANK=$f; break; fi
done

respond() {
  local ts clobber_ts tl tr bl br pp cb np
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  clobber_ts=$(date -u +%Y%m%d_%H%M%SZ)
  tl=$(m $BUILD/assets/plot_025_tl.png); tr=$(m $BUILD/assets/plot_025_tr.png)
  bl=$(m $BUILD/assets/plot_025_bl.png); br=$(m $BUILD/assets/plot_025_br.png)
  pp=$(m $PPTX)
  {
    echo "=================================================="
    echo "[$ts] CLOBBER EVENT — observed: tl=$tl tr=$tr bl=$bl br=$br pptx=$pp"
    echo "canonical: tl=$CAN_TL tr=$CAN_TR bl=$CAN_BL br=$CAN_BR pptx=$CAN_PPTX"
    echo "--- suspect processes (slide025/plot_025/promote/br_search/node) ---"
    ps -eo pid,etimes,args | grep -E 'slide025|plot_025|promote_|br_search|node .*slide_025|search_k17' | grep -v grep
    echo "--- mtimes ---"
    ls -la --time-style=full-iso $BUILD/assets/plot_025_*.png $PPTX
  } >> "$LOG"

  cb=$D/clobbered_assets_$clobber_ts
  mkdir -p "$cb"
  [ "$tl" != "$CAN_TL" ] && cp -p "$BUILD/assets/plot_025_tl.png" "$cb/"
  [ "$tr" != "$CAN_TR" ] && cp -p "$BUILD/assets/plot_025_tr.png" "$cb/"
  [ "$bl" != "$CAN_BL" ] && cp -p "$BUILD/assets/plot_025_bl.png" "$cb/"
  [ "$br" != "$CAN_BR" ] && cp -p "$BUILD/assets/plot_025_br.png" "$cb/"
  echo "[$ts] banked clobbered assets -> $cb" >> "$LOG"

  if [ "$pp" != "$CAN_PPTX" ]; then
    cp -p "$PPTX" "$D/slide_025_recreated_clobbered_${clobber_ts}_${pp:0:8}_bank.pptx"
    echo "[$ts] banked clobbered pptx md5=$pp -> slide_025_recreated_clobbered_${clobber_ts}_${pp:0:8}_bank.pptx" >> "$LOG"
  fi

  cp -f "$BANK/plot_025_tl.png" "$BANK/plot_025_tr.png" "$BANK/plot_025_bl.png" "$BANK/plot_025_br.png" "$BUILD/assets/"
  echo "[$ts] restored canonical k17g assets into build/assets/" >> "$LOG"

  if [ "$pp" != "$CAN_PPTX" ]; then
    if [ -n "$CAN_BANK" ]; then
      cp -p "$CAN_BANK" "$PPTX"
      echo "[$ts] restored byte-exact canonical pptx from bank $CAN_BANK" >> "$LOG"
    else
      echo "[$ts] no canonical bank found -> rebuilding via node slide_025.js" >> "$LOG"
      ( cd "$BUILD" && node slide_025.js ) >> "$LOG" 2>&1
    fi
    np=$(m "$PPTX")
    echo "[$ts] pptx after restore/rebuild md5=$np (canonical=$CAN_PPTX)" >> "$LOG"

    echo "[$ts] re-render render_k17z3.png (unique LO profile under TMPDIR=$TMPDIR)" >> "$LOG"
    rm -f "$TMPDIR/slide_025_recreated.pdf"
    soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_rejudge_025_k17z3" \
      --convert-to pdf "$PPTX" --outdir "$TMPDIR" > "$D/render_k17z3.log" 2>&1
    if [ -f "$TMPDIR/slide_025_recreated.pdf" ]; then
      mv "$TMPDIR/slide_025_recreated.pdf" "$D/render_k17z3.pdf"
      pdftoppm -png -r 150 -singlefile "$D/render_k17z3.pdf" "$D/render_k17z3" >> "$D/render_k17z3.log" 2>&1
    fi
    [ -f "$D/render_k17z3.png" ] && echo "[$ts] render_k17z3.png written" >> "$LOG" || echo "[$ts] RENDER_K17Z3_FAIL" >> "$LOG"

    python3 "$ROOT/$NS/shared_patterns/house_chrome_check.py" "$D/render_k17z3.png" 25 > "$D/chrome_check_k17z3.txt" 2>&1
    echo "[$ts] house_chrome_check rc=$? -> chrome_check_k17z3.txt" >> "$LOG"

    read -r X0 Y0 X1 Y1 < <(python3 "$ROOT/$RJ/pick_dense_region.py" 025)
    echo "dense region: $X0 $Y0 $X1 $Y1" > "$D/crop_region_k17z3.txt"
    python3 - "$D/render_k17z3.png" "$ROOT/$NS/unique_slides/slide_025.jpg" "$D" "$X0" "$Y0" "$X1" "$Y1" >> "$LOG" 2>&1 <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out, x0, y0, x1, y1 = sys.argv[1:8]
x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
r = Image.open(rp).convert("RGB")
o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
rc = r.crop((int(x0 * sc), int(y0 * sc), int(np.ceil(x1 * sc)), int(np.ceil(y1 * sc))))
oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(f"{out}/crop_dense_render_k17z3.png")
oc.save(f"{out}/crop_dense_orig_k17z3.png")
print("crop render", rc.size, "orig", oc.size, "k17z3")
PY

    OCC_MAX=700 ATTEMPTS=10 setsid nohup bash "$ROOT/$RJ/vision_leg.sh" \
      "$D/judge_full_k17z3.txt" 1200 "$D/render_k17z3.png" "$ROOT/$NS/unique_slides/slide_025.jpg" \
      "Slide 25 recreation — fidelity check vs original lecture frame (k17z3)" \
      "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
      "$ROOT/$RJ/payload_A.txt" > "$D/judge_full_k17z3.wrapper.out" 2>&1 < /dev/null &
    echo $! > "$D/leg_full_k17z3.pid"
    OCC_MAX=700 ATTEMPTS=10 setsid nohup bash "$ROOT/$RJ/vision_leg.sh" \
      "$D/crop_dense_judge_k17z3.txt" 600 "$D/crop_dense_render_k17z3.png" "$D/crop_dense_orig_k17z3.png" \
      "Slide 25 zoomed crop — fidelity check vs original (k17z3)" \
      "IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame" \
      "$ROOT/$RJ/payload_B_025.txt" > "$D/crop_dense_judge_k17z3.wrapper.out" 2>&1 < /dev/null &
    echo $! > "$D/leg_crop_k17z3.pid"
    echo "[$ts] launched full_k17z3 pid $(cat $D/leg_full_k17z3.pid) crop_k17z3 pid $(cat $D/leg_crop_k17z3.pid)" >> "$LOG"
  else
    echo "[$ts] pptx still canonical ($pp) — assets restored only, no rebuild/render/legs" >> "$LOG"
  fi
}

echo "CLOBBER_WATCH v2 start $(date -u +%Y-%m-%dT%H:%M:%SZ) canonical pptx=$CAN_PPTX (bank=${CAN_BANK:-none}) assets tl=$CAN_TL tr=$CAN_TR bl=$CAN_BL br=$CAN_BR" >> "$LOG"
END=$((SECONDS + 3600))
poll=0
while [ $SECONDS -lt $END ]; do
  poll=$((poll + 1))
  tl=$(m $BUILD/assets/plot_025_tl.png); tr=$(m $BUILD/assets/plot_025_tr.png)
  bl=$(m $BUILD/assets/plot_025_bl.png); br=$(m $BUILD/assets/plot_025_br.png)
  pp=$(m $PPTX)
  if [ "$tl" != "$CAN_TL" ] || [ "$tr" != "$CAN_TR" ] || [ "$bl" != "$CAN_BL" ] || [ "$br" != "$CAN_BR" ] || [ "$pp" != "$CAN_PPTX" ]; then
    respond
  else
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] poll#$poll OK (all 5 canonical)" >> "$LOG"
  fi
  [ $SECONDS -lt $END ] && sleep 60
done
echo "CLOBBER_WATCH v2 end $(date -u +%Y-%m-%dT%H:%M:%SZ) polls=$poll" >> "$LOG"
