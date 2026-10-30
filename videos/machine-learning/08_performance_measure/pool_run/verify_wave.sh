#!/usr/bin/env bash
# verify_wave.sh — dual-read certification + fresh re-analysis for certified slides.
# Idempotent: a slide whose corroboration transcript for its current PASS attempt is
# already banked is never re-judged. Re-runnable from cron.
set -uo pipefail

VIDEO_DIR="/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
REPO="/home/codespace/ai_llm_slides"
QA_ROOT="$VIDEO_DIR/recreated_pptx/qa"
PROMPT_FILE="$VIDEO_DIR/pool_run/judge_prompt_template.txt"
LEDGER="$VIDEO_DIR/pool_run/verification_ledger.md"
REANA_DIR="$VIDEO_DIR/analysis/reanalysis"
LOG="$VIDEO_DIR/pool_run/verify_wave.log"
PYBIN="/home/codespace/.pyenv/versions/3.15.2/bin/python3"
VERDICT="$VIDEO_DIR/pool_run/verdict.py"
GATE="$REPO/scripts/16_vision_gate.sh"
ANALYZE="$REPO/.agents/skills/image-analysis/scripts/analyze_image.py"

log() { echo "[$(date '+%F %T')] $*" >>"$LOG"; }

# Verdict of a transcript: PASS | FAIL | NONE.
read_verdict() { "$PYBIN" "$VERDICT" "$1" 2>/dev/null; }

[ -f "$PROMPT_FILE" ] || { log "FATAL: judge prompt template missing: $PROMPT_FILE"; exit 1; }
mkdir -p "$REANA_DIR"

if [ ! -f "$LEDGER" ]; then
  {
    echo "# Verification ledger — dual-read certification + re-analysis"
    echo
    echo "| slide | first PASS transcript | corroboration transcript | verify verdict | reanalysis | certified |"
    echo "|---|---|---|---|---|---|"
  } >"$LEDGER"
fi

# Original frame for a slide number; tolerates the slide_028-.jpg naming quirk.
find_original() {
  local num="$1" padded f
  padded=$(printf '%03d' "$num")
  for f in "$VIDEO_DIR/unique_slides/slide_${padded}".jpg "$VIDEO_DIR/unique_slides/slide_${padded}"-*.jpg; do
    [ -f "$f" ] && { printf '%s' "$f"; return 0; }
  done
  return 1
}

# Latest attempt transcript carrying a PASS verdict.
latest_pass() {
  local qa="$1" f found=""
  for f in $(ls -1 "$qa"judge_attempt_*.txt 2>/dev/null | sort -V); do
    if [ "$(read_verdict "$f")" = "PASS" ]; then found="$f"; fi
  done
  printf '%s' "$found"
}

# A PASS transcript filed under any other judge_*.txt name (workers are not
# perfectly uniform). The prompt echo files are excluded by verdict.py, which
# returns NONE for them.
latest_pass_any_name() {
  local qa="$1" f found=""
  for f in $(ls -1 "$qa"judge_*.txt 2>/dev/null | sort -V); do
    case "$f" in *judge_prompt_*) continue ;; esac
    if [ "$(read_verdict "$f")" = "PASS" ]; then found="$f"; fi
  done
  printf '%s' "$found"
}

judged=0; skipped=0; failed=0
for qa in "$QA_ROOT"/slide*/; do
  [ -d "$qa" ] || continue
  base=$(basename "$qa")
  digits=$(printf '%s' "$base" | tr -cd '0-9')
  [ -n "$digits" ] || continue
  num=$((10#$digits))
  pass_file=$(latest_pass "$qa")
  if [ -z "$pass_file" ]; then
    # Fallback: a PASS filed under a non-canonical judge_*.txt name.
    pass_file=$(latest_pass_any_name "$qa")
    [ -n "$pass_file" ] && log "slide $num: PASS found under non-canonical name $(basename "$pass_file")"
  fi
  [ -n "$pass_file" ] || continue

  attempt=$(basename "$pass_file" | sed -E 's/judge_attempt_([0-9]+)\.txt/\1/')
  case "$attempt" in
    ''|*[!0-9]*) attempt=$(ls -1 "$qa"render_*.png 2>/dev/null | sort -V | tail -1 | sed -E 's/.*render_([0-9]+)\.png/\1/') ;;
  esac
  [ -n "$attempt" ] || { log "slide $num: PASS present but attempt number undeterminable"; continue; }
  verify="$qa/judge_verify_${attempt}.txt"
  if [ -f "$verify" ]; then
    skipped=$((skipped+1)); continue
  fi

  render="$qa/render_${attempt}.png"
  [ -f "$render" ] || render=$(ls -1 "$qa"render_*.png 2>/dev/null | sort -V | tail -1)
  if [ -z "${render:-}" ] || [ ! -f "$render" ]; then
    log "slide $num: PASS present but no render PNG — skipped"
    continue
  fi
  # The certified render must belong to the pptx that is actually delivered:
  # a pptx rebuilt after the judged render invalidates the corroboration.
  deck_pptx="$VIDEO_DIR/recreated_pptx/slide_$(printf '%03d' "$num")_recreated.pptx"
  if [ -f "$deck_pptx" ] && [ "$deck_pptx" -nt "$render" ]; then
    log "slide $num: pptx is NEWER than the judged render — stale certification, skipped"
    continue
  fi
  orig=$(find_original "$num") || { log "slide $num: original frame not found"; continue; }

  log "slide $num: corroboration read starting (attempt $attempt, render=$(basename "$render"))"
  "$GATE" timeout 540 "$PYBIN" "$ANALYZE" comparison "$orig" "$render" \
    --view "Slide $num recreation — INDEPENDENT corroboration read vs original lecture frame" \
    --capture "IMG1=original lecture video frame (ground truth, read first); IMG2=150dpi PNG render of a 13.33x7.5in PPTX recreation (read second)" \
    --thinking high --max-tokens 65536 \
    --timeout 420 --rounds 1 --tries 1 \
    --transcript "$verify" \
    -p "$(cat "$PROMPT_FILE")" >>"$LOG" 2>&1
  rc=$?
  judged=$((judged+1))
  if [ $rc -ne 0 ] || [ ! -s "$verify" ]; then
    log "slide $num: corroboration read FAILED rc=$rc — slide stays single-read"
    failed=$((failed+1))
    continue
  fi

  v="$("$PYBIN" "$VERDICT" "$verify" 2>/dev/null)"
  [ -n "$v" ] || v="FAIL"
  padded=$(printf '%03d' "$num")
  stage="$REANA_DIR/_staging/slide_${padded}"
  mkdir -p "$stage"
  cp -f "$orig" "$stage/slide_${padded}.jpg"
  cp -f "$VIDEO_DIR/unique_slides/slides_index.json" "$stage/slides_index.json" 2>/dev/null || true
  # Staging index: the frame is renamed to slide_NNN.jpg (so the analysis
  # output lands on slide_NNN_raw.json); align the index entry to that name so
  # the reanalysis keeps its slide metadata. Patches the copied index in place
  # and leaves it untouched if it cannot be parsed.
  "$PYBIN" - "$stage/slides_index.json" "$padded" <<'PYEOF' 2>/dev/null || true
import json, sys
path, padded = sys.argv[1], sys.argv[2]
try:
    idx = json.load(open(path))
except Exception:
    sys.exit(0)
if isinstance(idx, list):
    for e in idx:
        if isinstance(e, dict) and str(e.get("slide")) == str(int(padded)):
            e["image"] = "slide_%s.jpg" % padded
    json.dump(idx, open(path, "w"))
PYEOF
  "$GATE" "$PYBIN" "$REPO/scripts/12_analyze_slides.py" "$stage" "$REANA_DIR" --slides 1 >>"$LOG" 2>&1
  if [ -s "$REANA_DIR/slide_${padded}_raw.json" ]; then
    reana="analysis/reanalysis/slide_${padded}_raw.json"
  else
    reana="MISSING"
  fi
  cert="no"
  [ "$v" = "PASS" ] && cert="yes"
  # Continuous final deck: a corroborated PASS replaces its placeholder page at the
  # OPC level (byte-verbatim, media renamed per slide, fleet-global deck lock).
  if [ "$cert" = "yes" ]; then
    deck_pptx="$VIDEO_DIR/recreated_pptx/slide_$(printf '%03d' "$num")_recreated.pptx"
    [ -f "$deck_pptx" ] || deck_pptx=$(ls -1 "$VIDEO_DIR/recreated_pptx"/slide_*.pptx 2>/dev/null | head -1)
    if [ -f "$VIDEO_DIR/08-performance_final.pptx" ] && [ -f "$deck_pptx" ]; then
      "$PYBIN" "$VIDEO_DIR/pool_run/merge_final_deck.py" update "$num" "$deck_pptx" "$VIDEO_DIR/08-performance_final.pptx" >>"$LOG" 2>&1 \
        && log "slide $num: final deck page $num updated" \
        || log "slide $num: final deck update FAILED (pptx remains single-slide deliverable)"
    else
      log "slide $num: final deck update skipped (deck or per-slide pptx missing)"
    fi
  fi
  echo "| $num | ${pass_file#$VIDEO_DIR/} | ${verify#$VIDEO_DIR/} | $v | $reana | $cert |" >>"$LEDGER"
  log "slide $num: verify=$v reanalysis=$reana certified=$cert"
done

log "verify wave complete: judged=$judged skipped=$skipped failed=$failed"
