#!/usr/bin/env bash
# fresh_w20261031_legs_018034.sh — FRESH worker 2026-10-31 (w20261031): slides 018-034, skip 25.
# Dispatch rule: result.txt leg != PASS and no live vision_leg.sh wrapper on that leg ->
#   setsid nohup vision_leg.sh <leg>_fresh.txt (full t=1200 payload_A.txt; crop t=600 payload_B_0NN.txt).
# Clean banked verdict on a non-PASS leg -> harvest (PASS -> surgical result.txt; FAIL -> PIL-first
#   census via rejudge_adjudicate.py banked as adjudicate_w20261031_<leg>.txt). Append register.
# Evidence-only under qa/; never deletes transcripts; no git; does not resume foreign legs.
set -u
ROOT=/home/codespace/ai_llm_slides
NS=$ROOT/videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$RJ/legs_20261031.pids"
LOG=$RJ/fresh_w20261031_legs_018034.log
REG=$RJ/REJUDGE_REGISTER.md
SCOPE="018 019 020 021 022 023 024 026 027 028 029 030 031 032 033 034"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verdict() { grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$1" | tail -1 | grep -oE 'PASS|FAIL'; }
live_leg() { ps -eo args | grep '[v]ision_leg[.]sh' | grep -q "rejudge_20261027/slide$1/$2"; }
legval() { grep -m1 "^$2=" "$RJ/slide$1/result.txt" 2>/dev/null | cut -d= -f2- | awk '{print $1}'; }
title_of() { sqlite3 "$NS/slides_progress.db" "SELECT title FROM slides WHERE slide_id=$((10#$1));" 2>/dev/null | head -1; }
region_of() { python3 "$RJ/pick_dense_region.py" "$1" 2>/dev/null | awk '{printf "%s,%s-%s,%s", $1,$2,$3,$4}'; }
ts_of() { stat -c %y "$1" | cut -d. -f1 | sed 's/ /_/'; }
log() { echo "$(date -u +%FT%TZ) w20261031 $*" >> "$LOG"; }

set_leg() { # N FULL|CROP value transcript
  local N=$1 LEG=$2 VAL=$3 TR=$4 D=$RJ/slide$N F=$D/result.txt TMPF=$D/result.txt.w20261031tmp
  local vline tline tsline
  vline="$LEG=$VAL"; tline="${LEG}_TRANSCRIPT=$D/$TR"
  tsline="${LEG}_VERDICT_TS=$(ts_of "$D/$TR") UTC (clean, no 429)"
  awk -v vl="$vline" -v tl="$tline" -v sl="$tsline" -v leg="$LEG" '
    BEGIN { done_v=0; done_t=0; done_s=0 }
    $0 ~ "^"leg"=" { if (!done_v) { print vl; done_v=1 } next }
    $0 ~ "^"leg"_TRANSCRIPT=" { if (!done_t) { print tl; done_t=1 } next }
    $0 ~ "^"leg"_VERDICT_TS=" { if (!done_s) { print sl; done_s=1 } next }
    { print }
    END { if (!done_v) print vl; if (!done_t) print tl; if (!done_s) print sl }
  ' "$F" > "$TMPF" && mv "$TMPF" "$F"
}

launch_full() { # N
  local N=$1 D=$RJ/slide$N NN=$((10#$N)) OUT=$D/judge_full_fresh.txt T
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
  setsid nohup bash "$RJ/vision_leg.sh" "$OUT" 1200 "$D/render.png" "$NS/unique_slides/slide_$N.jpg" \
    "Slide $NN recreation — fidelity check vs original lecture frame" \
    "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
    "$RJ/payload_A.txt" >> "$LOG" 2>&1 < /dev/null &
  echo "$! slide$N full judge_full_fresh.txt $(date -u +%FT%TZ)" >> "$RJ/legs_20261031.pids/w20261031.pids"
  log "LAUNCH $N FULL -> judge_full_fresh.txt pid=$!"
}
launch_crop() { # N
  local N=$1 D=$RJ/slide$N NN=$((10#$N)) OUT=$D/crop_dense_judge_fresh.txt T R
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
  R=$(region_of "$N")
  [ -f "$RJ/payload_B_$N.txt" ] || { log "NO payload_B_$N.txt — skip crop launch $N"; return; }
  setsid nohup bash "$RJ/vision_leg.sh" "$OUT" 600 "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
    "Slide $NN zoomed crop dense — render vs original at matched scale (rejudge 1)" \
    "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $NN (frame px $R) — $T" \
    "$RJ/payload_B_$N.txt" >> "$LOG" 2>&1 < /dev/null &
  echo "$! slide$N crop crop_dense_judge_fresh.txt $(date -u +%FT%TZ)" >> "$RJ/legs_20261031.pids/w20261031.pids"
  log "LAUNCH $N CROP -> crop_dense_judge_fresh.txt pid=$!"
}

best_clean() { # N full|crop -> echoes "file verdict" of first clean among fresh/plain/retry/w03
  local N=$1 D=$RJ/slide$N kind=$2 f
  if [ "$kind" = full ]; then flist="judge_full_fresh.txt judge_full.txt judge_full_retry.txt judge_full_w03.txt"
  else flist="crop_dense_judge_fresh.txt crop_dense_judge.txt crop_dense_judge_retry.txt crop_dense_judge_w03.txt"; fi
  for f in $flist; do if clean "$D/$f"; then echo "$f $(verdict "$D/$f")"; return 0; fi; done
  return 1
}

log "scan start pid=$$ scope=018-034 skip 25"
for N in $SCOPE; do
  D=$RJ/slide$N
  [ -f "$D/result.txt" ] || { log "$N: no result.txt, skip"; continue; }
  FV=$(legval "$N" FULL); CV=$(legval "$N" CROP)
  [ "$FV" = PASS ] || {
    if bc=$(best_clean "$N" full); then
      f=${bc%% *} v=${bc##* }
      if [ "$v" = PASS ]; then set_leg "$N" FULL PASS "$f"; log "HARVEST $N FULL=PASS from $f (was $FV)"
      else log "CLEANFAIL $N FULL from $f (was $FV) — PIL-first below"; fi
    elif live_leg "$N" judge_full; then log "SKIP $N FULL — live foreign wrapper (was $FV)"
    else launch_full "$N"; fi
  }
  [ "$CV" = PASS ] || {
    if bc=$(best_clean "$N" crop); then
      f=${bc%% *} v=${bc##* }
      if [ "$v" = PASS ]; then set_leg "$N" CROP PASS "$f"; log "HARVEST $N CROP=PASS from $f (was $CV)"
      else log "CLEANFAIL $N CROP from $f (was $CV) — PIL-first below"; fi
    elif live_leg "$N" crop_dense_judge; then log "SKIP $N CROP — live foreign wrapper (was $CV)"
    else launch_crop "$N"; fi
  }
done

# PIL-first adjudication censuses for clean FAILs on dispatch legs (read-only; banked, never deletes)
python3 "$RJ/rejudge_adjudicate.py" 033 --full > "$RJ/slide033/adjudicate_w20261031_full.txt" 2>&1
log "ADJUDICATE 033 FULL census -> slide033/adjudicate_w20261031_full.txt"
python3 "$RJ/rejudge_adjudicate.py" 030 --crop > "$RJ/slide030/adjudicate_w20261031_crop.txt" 2>&1
log "ADJUDICATE 030 CROP census -> slide030/adjudicate_w20261031_crop.txt"

# targeted probe: 030 crop FAIL claim = x-header row fill white (render) vs yellow (orig)
python3 - "$RJ" > "$RJ/slide030/adjudicate_w20261031_crop_probe.txt" 2>&1 <<'EOF'
import sys, numpy as np
from PIL import Image
RJ = sys.argv[1]; NS = RJ.split('/recreated_pptx')[0]
r = Image.open(f"{RJ}/slide030/crop_dense_render.png").convert("RGB")
o = Image.open(f"{RJ}/slide030/crop_dense_orig.png").convert("RGB")
W,H = r.size; print(f"crop size {W}x{H}")
# claimed header band ~y60-95 full width; sample middle of that band, away from edges/borders
for name,img in (("render",r),("orig_crop",o)):
    a = np.asarray(img).astype(int)
    band = a[65:90, int(W*0.2):int(W*0.8)]
    print(f"{name}: x-row band y65-90 median RGB = {np.median(band.reshape(-1,3),axis=0).round(1)}")
# frame-wins check: map crop band back to original frame slide_030.jpg (region 64,304-368,512)
fx0,fy0,fx1,fy1 = 64,304,368,512
scale = W/(fx1-fx0)
orig = Image.open(f"{NS}/unique_slides/slide_030.jpg").convert("RGB")
a = np.asarray(orig).astype(int)
y0,y1 = fy0+int(65/scale), fy0+int(90/scale)
x0,x1 = fx0+int(W*0.2/scale), fx0+int(W*0.8/scale)
band = a[y0:y1, x0:x1]
print(f"frame slide_030.jpg mapped x-row band x{x0}-{x1} y{y0}-{y1} median RGB = {np.median(band.reshape(-1,3),axis=0).round(1)}")
EOF
log "PROBE 030 crop header-fill -> slide030/adjudicate_w20261031_crop_probe.txt"

for N in $SCOPE; do touch "$RJ/.w20261031_registered_$N"; done
log "scan end"
echo "done $(date -u +%FT%TZ)"
