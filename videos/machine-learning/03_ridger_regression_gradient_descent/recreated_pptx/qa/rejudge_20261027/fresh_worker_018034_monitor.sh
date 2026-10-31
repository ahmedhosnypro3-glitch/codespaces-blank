#!/usr/bin/env bash
# fresh_worker_018034_monitor.sh — FRESH worker 2026-10-31, slides 018-034 (skip 25).
# Self-healing gap filler + harvester for the rejudge_20261027 legs:
#  - launches a leg ONLY when no clean (FINAL VERDICT, no 429) transcript is banked
#    AND no live vision_leg.sh carrier is on that slide (never duplicates in-flight legs)
#  - when both legs of a slide have clean banked verdicts and no carrier is live,
#    writes slideNNN/result.txt (PASS/PASS direct; FAIL -> rejudge_adjudicate.py PIL-first)
#    and appends one bullet to REJUDGE_REGISTER.md (idempotent via marker files)
# Evidence-only under qa/; never deletes, never git.
set -u
ROOT=/home/codespace/ai_llm_slides
cd "$ROOT" || exit 1
NS=videos/machine-learning/03_ridger_regression_gradient_descent
RJ=$NS/recreated_pptx/qa/rejudge_20261027
export TMPDIR=$ROOT/scratch/tmp
mkdir -p "$TMPDIR" "$RJ/legs_20261031.pids"
LOG=$RJ/fresh_worker_018034_monitor.log
SCOPE="018 019 020 021 022 023 024 026 027 028 029 030 031 032 033 034"

clean() { [ -f "$1" ] && grep -q 'FINAL VERDICT' "$1" 2>/dev/null && ! grep -qi '429' "$1" 2>/dev/null; }
verdict() { # file -> PASS|FAIL|NORESULT
  local f=$1
  [ -f "$f" ] || { echo NORESULT; return; }
  if grep -q 'FINAL VERDICT' "$f" && ! grep -qi '429' "$f"; then
    grep -oE 'FINAL VERDICT: *\*{0,2} *(PASS|FAIL)' "$f" | tail -1 | grep -oE '(PASS|FAIL)'
  else echo NORESULT; fi
}
live() { ps -eo args | grep '[v]ision_leg[.]sh' | grep -q "rejudge_20261027/slide$1/"; }
title_of() { sqlite3 "$NS/slides_progress.db" "SELECT title FROM slides WHERE slide_id=$((10#$1));" 2>/dev/null | head -1; }
region_of() { python3 "$RJ/pick_dense_region.py" "$1" 2>/dev/null | awk '{printf "%s,%s-%s,%s", $1,$2,$3,$4}'; }

# best clean verdict across candidate transcripts, preferring newest clean file
best() { # file1 file2 ... -> "VERDICT path" (empty if none clean)
  local bestv="" bestf="" f v m
  for f in "$@"; do
    v=$(verdict "$f"); [ "$v" = NORESULT ] && continue
    if [ -z "$bestf" ] || [ "$f" -nt "$bestf" ]; then bestv=$v; bestf=$f; fi
  done
  [ -n "$bestf" ] && echo "$bestv $bestf"
}

launch_full() { # N
  local N=$1 D=$RJ/slide$N NN=$((10#$N)) OUT=$D/judge_full.txt
  [ -f "$D/judge_full.txt" ] && OUT=$D/judge_full_fresh.txt
  setsid nohup bash "$RJ/vision_leg.sh" "$OUT" 1200 "$D/render.png" "$NS/unique_slides/slide_$N.jpg" \
    "Slide $NN recreation — fidelity check vs original lecture frame" \
    "IMG1=150dpi PNG render of 13.33x7.5in PPTX; IMG2=original 960x540 lecture frame" \
    "$RJ/payload_A.txt" > "$OUT.wrapper.out" 2>&1 &
  echo $! > "$RJ/legs_20261031.pids/${N}_full.pid"
  echo "$(date -u +%FT%TZ) LAUNCH $N F -> $(basename "$OUT") pid=$!" >> "$LOG"
}
launch_crop() { # N
  local N=$1 D=$RJ/slide$N NN=$((10#$N)) OUT=$D/crop_dense_judge.txt T R
  [ -f "$D/crop_dense_judge.txt" ] && OUT=$D/crop_dense_judge_fresh.txt
  [ -f "$RJ/payload_B_$N.txt" ] || sed "s/slide NNN/slide $N/g" "$RJ/payload_B.tmpl" > "$RJ/payload_B_$N.txt"
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
  R=$(region_of "$N")
  setsid nohup bash "$RJ/vision_leg.sh" "$OUT" 600 "$D/crop_dense_render.png" "$D/crop_dense_orig.png" \
    "Slide $NN zoomed crop dense — render vs original at matched scale (rejudge 1)" \
    "IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: densest content region of slide $NN (frame px $R) — $T" \
    "$RJ/payload_B_$N.txt" > "$OUT.wrapper.out" 2>&1 &
  echo $! > "$RJ/legs_20261031.pids/${N}_crop.pid"
  echo "$(date -u +%FT%TZ) LAUNCH $N C -> $(basename "$OUT") pid=$!" >> "$LOG"
}

harvest() { # N — both legs clean, no live carrier
  local N=$1 D=$RJ/slide$N NN=$((10#$N))
  local FB FV FT CB BV CT
  FB=$(best "$D/judge_full_fresh.txt" "$D/judge_full.txt" "$D/judge_full_retry.txt")
  CB=$(best "$D/crop_dense_judge_fresh.txt" "$D/crop_dense_judge.txt" "$D/crop_dense_judge_retry.txt")
  FV=${FB%% *}; FT=${FB#* }; [ "$FT" = "$FB" ] && FT=$D/judge_full.txt
  BV=${CB%% *}; CT=${CB#* }; [ "$CT" = "$CB" ] && CT=$D/crop_dense_judge.txt
  local T R
  T=$(title_of "$N"); [ -n "$T" ] || T="slide $NN"
  R=$(region_of "$N"); [ -n "$R" ] || R="?"
  # PIL-first adjudication on any FAIL
  local NOTE=""
  if [ "$FV" = FAIL ]; then
    python3 "$RJ/rejudge_adjudicate.py" "$N" > "$D/adjudicate_fresh_full.txt" 2>&1
    NOTE="full FAIL PIL-adjudicated -> adjudicate_fresh_full.txt; "
  fi
  if [ "$BV" = FAIL ]; then
    python3 "$RJ/rejudge_adjudicate.py" "$N" --crop > "$D/adjudicate_fresh_crop.txt" 2>&1
    NOTE="${NOTE}crop FAIL PIL-adjudicated -> adjudicate_fresh_crop.txt; "
  fi
  cat > "$D/result.txt" <<EOF
SLIDE=$N
TITLE=$T
RENDER=$NS/recreated_pptx/qa/rejudge_20261027/slide$N/render.png
REGION=$R
FULL=$FV
CROP=$BV
FULL_TRANSCRIPT=$FT
CROP_TRANSCRIPT=$CT
EOF
  if [ ! -f "$RJ/.w20261031_registered_$N" ]; then
    {
      echo ""
      echo "- 2026-10-31 fresh wave (slides 018-034, skip 25) — slide $N: FULL=$FV CROP=$BV; transcripts $(basename "$FT") + $(basename "$CT"); ${NOTE:-no FAIL to adjudicate.} result.txt written. No git; no evidence deleted."
    } >> "$RJ/REJUDGE_REGISTER.md"
    touch "$RJ/.w20261031_registered_$N"
  fi
  echo "$(date -u +%FT%TZ) HARVEST $N FULL=$FV CROP=$BV" >> "$LOG"
}

echo "monitor start $(date -u +%FT%TZ) pid=$$ scope=[$SCOPE]" >> "$LOG"
while true; do
  for N in $SCOPE; do
    D=$RJ/slide$N
    live "$N" && { echo "$(date -u +%FT%TZ) $N live-carrier, skip" >> "$LOG"; continue; }
    FB=$(best "$D/judge_full_fresh.txt" "$D/judge_full.txt" "$D/judge_full_retry.txt")
    CB=$(best "$D/crop_dense_judge_fresh.txt" "$D/crop_dense_judge.txt" "$D/crop_dense_judge_retry.txt")
    FOK=no; C_OK=no
    [ -n "$FB" ] && FOK=yes
    [ -n "$CB" ] && C_OK=yes
    if [ "$FOK" = yes ] && [ "$C_OK" = yes ]; then
      [ -f "$RJ/.w20261031_registered_$N" ] || harvest "$N"
    else
      [ "$FOK" = no ] && launch_full "$N"
      [ "$C_OK" = no ] && launch_crop "$N"
    fi
    sleep 10
  done
  # stop condition: every slide in scope has a registered marker
  all_done=yes
  for N in $SCOPE; do [ -f "$RJ/.w20261031_registered_$N" ] || all_done=no; done
  if [ "$all_done" = yes ]; then
    echo "monitor all-done $(date -u +%FT%TZ)" >> "$LOG"
    break
  fi
  sleep 90
done
echo "monitor exit $(date -u +%FT%TZ)" >> "$LOG"
