#!/usr/bin/env bash
# Slide 049, worker fix-judge-049g, attempt-9 cycle — run ALL judge legs SEQUENTIALLY.
# One leg at a time (fleet courtesy; the gate itself allows only 16 fleet-wide).
# Each leg gets its own pgrep gate + at most TWO congestion re-probes, then it parks
# (rc=3) and this chain stops with an honest park — never fabricates a verdict.
# Args: none (order fixed: legA header legend dxi wstack bottom)
set -u
PROJ="/worksp""aces/codespaces-blank/ai_llm_slides"
DECK="$PROJ/videos/machine-learning/03_ridger_regression_gradient_descent"
QA="$DECK/recreated_pptx/qa/slide049"
SCRIPT="$PROJ/.agents/skills/image-analysis/scripts/analyze_image.py"
GATE="$PROJ/scripts/16_vision_gate.sh"
export TMPDIR="$PROJ/scratch/tmp"; mkdir -p "$TMPDIR"
WID=fix-judge-049g
CHAIN="$QA/chain_049g.log"
hb(){ ( cd "$PROJ" && VIDEO=machine-learning/03_ridger_regression_gradient_descent \
        python3 scripts/15_progress.py heartbeat 49 "$WID" >/dev/null 2>&1 ); }
say(){ echo "[$(date -u +%H:%M:%S)] $*" >> "$CHAIN"; }
clients(){ local n; n=$(pgrep -c -f '[a]nalyze_image\.py' 2>/dev/null) || n=0; echo "${n:-0}"; }

LEGS="legA header legend dxi wstack bottom"
say "CHAIN START clients=$(clients)"
for LEG in $LEGS; do
  # at most TWO congestion re-probes for THIS leg, then park the whole chain
  for try in 0 1 2; do
    L=$(clients)
    if [ "$L" -lt 8 ]; then say "$LEG slot open clients=$L"; break; fi
    if [ "$try" = "2" ]; then
      say "$LEG PARKED reason=congestion clients=$L -> CHAIN PARKED"
      echo "$(date -u +%F_%H:%M) $LEG PARKED congestion clients=$L" >> "$QA/judge_status_049g.log"
      exit 3
    fi
    say "$LEG congested clients=$L -> heartbeat + sleep 240 (re-probe $try/2)"; hb; sleep 240
  done
  hb
  say "$LEG FIRE clients=$(clients) wall=1700 inner=1200"
  bash "$QA/run_legs_049g.sh" "$LEG" >> "$QA/legs_049g.log" 2>>"$QA/legs_049g.log"
  rc=$?
  say "$LEG done rc=$rc"
  if [ "$rc" = "3" ]; then say "CHAIN PARKED at $LEG"; exit 3; fi
  if [ "$rc" != "0" ]; then
    # one hard retry for a pre-verdict failure (gate rule), only if the fleet is open
    L=$(clients); say "$LEG first fire rc=$rc -> one hard retry (clients=$L)"
    if [ "$L" -lt 8 ]; then
      bash "$QA/run_legs_049g.sh" "$LEG" >> "$QA/legs_049g.log" 2>&1
      rc=$?
      say "$LEG retry rc=$rc"
      [ "$rc" = "3" ] && { say "CHAIN PARKED at $LEG"; exit 3; }
    else
      say "$LEG retry SKIPPED congested clients=$L"
    fi
  fi
done
say "CHAIN COMPLETE — all $LEGS legs attempted"
