#!/usr/bin/env bash
# fresh_leg_chain.sh NNN — fresh-worker (2026-10-31) rejudge legs for one slide.
# usage: fresh_leg_chain.sh 003 [full|crop|both] [full|crop|both ...]
# Runs vision_leg.sh legs (full t=1200 payload_A; crop t=600 payload_B_0NNN),
# writes result.txt from the resulting/banked verdicts, PIL-adjudicates any
# FAIL via rejudge_adjudicate.py, appends REJUDGE_REGISTER.md.
# Never deletes banked transcripts: if judge_full.txt exists, the fresh full
# leg writes judge_full_fresh.txt instead.
set -u
N="${1:?usage: fresh_leg_chain.sh NNN legs...}"; shift
LEGS=$(echo "$*" | sed 's/\bboth\b/full crop/g')
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
D=$RJ/slide$N
NN=$((10#$N))
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$D"
OUT=$RJ/fresh_${N}.out
exec >> "$OUT" 2>&1
echo "=== fresh chain slide $N legs=[$LEGS] start $(date -u +%FT%TZ) pid=$$"

# payload_B_0NNN from template (same sed as rejudge_driver.sh)
PB=$RJ/payload_B_${N}.txt
[ -f "$PB" ] || sed "s/slide NNN/slide $N/g" "$RJ/payload_B.tmpl" > "$PB"

# render + crop pair must exist; else re-render via soffice+pdftoppm + chrome check
if [ ! -f "$D/render.png" ] || [ ! -f "$D/crop_dense_render.png" ] || [ ! -f "$D/crop_dense_orig.png" ]; then
  echo "--- $N re-render"
  PPTX=$NS/recreated_pptx/slide_${N}_recreated.pptx
  rm -f "$D/slide_${N}_recreated.pdf" "$D/render.png"
  soffice --headless "-env:UserInstallation=file://$TMPDIR/lo_fresh_${N}" \
    --convert-to pdf "$PPTX" --outdir "$D" > "$D/render.log" 2>&1
  pdftoppm -png -r 150 -singlefile "$D/slide_${N}_recreated.pdf" "$D/render" >> "$D/render.log" 2>&1
  python3 "$NS/shared_patterns/house_chrome_check.py" "$D/render.png" "$NN" > "$D/chrome_check.txt" 2>&1 || { echo "CHROME_FAIL $N"; exit 1; }
  read -r X0 Y0 X1 Y1 < <(python3 "$RJ/pick_dense_region.py" "$N")
  python3 - "$D/render.png" "$NS/unique_slides/slide_$N.jpg" "$D" "$X0" "$Y0" "$X1" "$Y1" <<'PY'
import sys
import numpy as np
from PIL import Image
rp, op, out, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], sys.argv[3], *map(int, sys.argv[4:8])
r = Image.open(rp).convert("RGB"); o = Image.open(op).convert("RGB")
sc = r.size[1] / 540.0
rc = r.crop((int(x0*sc), int(y0*sc), int(np.ceil(x1*sc)), int(np.ceil(y1*sc))))
oc = o.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
rc.save(f"{out}/crop_dense_render.png"); oc.save(f"{out}/crop_dense_orig.png")
PY
fi

clean() { # transcript -> PASS|FAIL|NORESULT (clean = has FINAL VERDICT and no 429)
  local f=$1
  [ -f "$f" ] || { echo NORESULT; return; }
  grep -q 'FINAL VERDICT' "$f" && ! grep -qi '429' "$f" || { echo NORESULT; return; }
  grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$f" | tail -1 | grep -oE '(PASS|FAIL)'
}

FULL_T=""; CROP_T=""
for leg in $LEGS; do
  case $leg in
    full)
      if [ -f "$D/judge_full.txt" ]; then FT=judge_full_fresh.txt; else FT=judge_full.txt; fi
      FULL_T=$D/$FT
      echo "--- $N FULL leg -> $FT $(date -u +%FT%TZ)"
      bash "$RJ/vision_leg.sh" "$D/$FT" 1200 "$D/render.png" "$NS/unique_slides/slide_$N.jpg" \
        "Slide $NN recreation — fidelity check vs original lecture frame" \
        "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
        "$RJ/payload_A.txt"
      echo "LEG_EXIT full $N=$? $(date -u +%FT%TZ) verdict=$(clean "$D/$FT")"
      ;;
    crop)
      CROP_T=$D/crop_dense_judge.txt
      echo "--- $N CROP leg -> crop_dense_judge.txt $(date -u +%FT%TZ)"
      bash "$RJ/vision_leg.sh" "$D/crop_dense_judge.txt" 600 "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
        "Slide $NN zoomed crop — fidelity check vs original" \
        "IMG1=zoomed crop of 150dpi render; IMG2=matched-scale crop of original frame" \
        "$PB"
      echo "LEG_EXIT crop $N=$? $(date -u +%FT%TZ) verdict=$(clean "$D/crop_dense_judge.txt")"
      ;;
  esac
done

# resolve verdicts: prefer fresh transcripts, fall back to banked ones
FV=$(clean "$FULL_T"); [ -z "$FV" ] || [ "$FV" = NORESULT ] && FV=$(clean "$D/judge_full.txt")
[ -z "$FV" ] || [ "$FV" = NORESULT ] && FV=$(clean "$D/judge_full_retry.txt")
BV=$(clean "$CROP_T"); [ -z "$BV" ] || [ "$BV" = NORESULT ] && BV=$(clean "$D/crop_dense_judge_retry.txt")
[ -z "$FV" ] && FV=NORESULT; [ -z "$BV" ] && BV=NORESULT
[ -z "$FULL_T" ] && FULL_T=$D/judge_full.txt
[ -z "$CROP_T" ] && CROP_T=$D/crop_dense_judge.txt

# carry TITLE/REGION forward from the previous result.txt when present
TITLE=$(grep -m1 '^TITLE=' "$D/result.txt" 2>/dev/null | cut -d= -f2-)
REGION=$(grep -m1 '^REGION=' "$D/result.txt" 2>/dev/null | cut -d= -f2-)
[ -n "$TITLE" ] || TITLE="slide $N"
[ -n "$REGION" ] || REGION="?"

cat > "$D/result.txt" <<EOF
SLIDE=$N
TITLE=$TITLE
RENDER=$NS/recreated_pptx/qa/rejudge_20261027/slide$N/render.png
REGION=$REGION
FULL=$FV
CROP=$BV
FULL_TRANSCRIPT=$FULL_T
CROP_TRANSCRIPT=$CROP_T
EOF

# FAIL -> PIL-first adjudication
if [ "$FV" = FAIL ]; then
  python3 "$RJ/rejudge_adjudicate.py" "$N" > "$D/adjudicate_fresh_full.txt" 2>&1
  echo "ADJUDICATED full FAIL -> $D/adjudicate_fresh_full.txt"
fi
if [ "$BV" = FAIL ]; then
  python3 "$RJ/rejudge_adjudicate.py" "$N" --crop > "$D/adjudicate_fresh_crop.txt" 2>&1
  echo "ADJUDICATED crop FAIL -> $D/adjudicate_fresh_crop.txt"
fi

{
  echo ""
  echo "## Fresh-worker wave 2026-10-31 (slides 001-017 sweep, no live wrapper at scan time)"
  echo ""
  echo "| slide | FULL | CROP | legs run | notes |"
  echo "|---|---|---|---|---|"
  echo "| $N | $FV | $BV | $LEGS | fresh legs $(date -u +%FT%TZ); transcripts $(basename "$FULL_T") + $(basename "$CROP_T") |"
} >> "$RJ/REJUDGE_REGISTER.md"

echo "=== fresh chain slide $N DONE FULL=$FV CROP=$BV $(date -u +%FT%TZ)"
