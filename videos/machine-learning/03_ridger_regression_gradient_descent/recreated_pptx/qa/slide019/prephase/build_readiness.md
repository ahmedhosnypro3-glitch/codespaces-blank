# Slide 019 — build readiness (S20b prephase pack)

Read with `prephase/delta_vs_related.md` (Δ# references its table rows).
Namespace law: `videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md`.

## State of the lane (verified 2026-10-25 ~15:05)

- Build: `build/slide_019.js` md5 `9e77242326ed6cae0b4e999dcc27d66b`
  (2026-10-25 14:49), lane attempt 17–18 (`qa/slide019/dispatch_B18.sh`).
- Attempt-8 park record + currency resolution stand
  (`worker_report.md`, `worker_report_s4_20261025.md`); judge_attempt_6 FAIL
  applies to superseded bytes only.
- **Already actioned in current bytes** (verified by reading the build):
  g1 W = 0/2/0 top→bottom (crop_16 FAIL → lane fix, attempt 17); W-block
  enclosure rects; rule-drawn test grids with the label column inside; row-group
  alignment y205/310/420; yellow bands; outlier bracket + yellow patches behind
  the 22s; inter-column arrows correctly absent; house chrome numeral 19.
- **Not yet actioned** = D1..D9 below.

## Preconditions

- House chrome: `shared_patterns/house_chrome.js` (already wired) —
  `shared_patterns/house_chrome_check.py` must PASS on the 150-dpi render
  BEFORE any judging.
- Judge payloads byte-for-byte from the frozen template
  `shared_patterns/judge_protocol_03.md`. Zoomed crop certificates: ≥1 per
  dense region — this slide warrants 4–5 pairs (title/vector panel; outlier
  column; each model column's W+table rows).
- Every dispute in delta_vs_related.md §Disputes is adjudicated PIL-FIRST
  before it gates a fix (judging.md law).
- Yield law while the gate is saturated: `pgrep -c -f analyze_image.py` < 8
  before any dispatch, else sleep 120.

## Build actions (Δ# → action)

- **D1 (Δ2) Title zone** — keep box geometry x68..435 y65..158; stroke color
  #2A2AA5 pending dispute-1 PIL (current 0000FF); "Test Data" size per
  dispute-2 PIL (current 24pt, P1 says ≈17–18pt); z-group details: red
  underline under the z ONLY (current: whole "z₁ =" run underlined), math-italic
  serif z, tall parens #4A4A4A (current black), serif upright digits, blue
  y=NN serif italic-y, group pitch ≈94pt (current 90/96 — minor).
- **D2 (Δ3) Outlier column** — header → TWO italic lines "Outlier"/"Xₛ"
  (current: one line, 9pt); bracket color → #2E3B96 (PIL; current black);
  **g3 first value BLUE → RED** (current `outlierRow(428, "60", BLUE)`); rest ✓.
- **D3 (Δ4) Headers + tints** — header runs → ITALIC, inks #2040C0/#C00000
  (PIL); tint bands → light RED (NO REG) / light ORANGE (RIDGE 3) / light GREEN
  (RIDGE 10) per attempt-9, pending dispute-6 PIL (current FFF4E0/FFF4E0/E8FFE8).
- **D4 (Δ5/6/7/8) W blocks** — enclosure stroke BLACK → RED (~2px, per P1);
  ‖W‖² line BLACK → BLUE #2040C0; **NO REG g2 third entry '0.61' → '0.64'**
  (closure-proven; keep the norm 8.11 as printed); RIDGE 10 g3 '1.07' vs '1.1'
  per dispute-4 PIL (current 1.07; 018-certified print is 1.1); RIDGE 3 values
  digit-read + §Closure check (dispute 5) before certification; entry/paren
  typography per P1.
- **D5 (Δ9) Arrows** — fill → WHITE (renders identically to the current
  transparent on white; record the choice), size toward the measured ~19×19
  (current 26×21 — minor).
- **D6 (Δ10/11) Test grids** — header strings → TRUE subscripts Test₁/Test₂/Test₃
  (current "Test1/2/3"); grid rule color BLACK → #B05050-family (PIL);
  y-row label cell #FFF200 solid + value cells pale-green tint (PIL; current
  flat FFFF80 band); RIDGE 10 g2 y '46' → '46.4' (inherit 018's certified print);
  RIDGE 3 y values await dispute-5.
- **D7 (Δ12) Rule colors** — thematic per column (outlier blue #3F51B5, NO REG
  #B05050, RIDGE 3 orange, RIDGE 10 green) pending dispute-6 PIL census per
  segment (current navy/maroon mix).
- **D8 (Δ15) Equation-format decision** — ‖W‖² lines (and optionally the W
  column vectors + z stacks) via matplotlib-mathtext 600-dpi PNGs following the
  certified 018 pattern (`build/assets/make_018_wbox.py` +
  `wbox018_sidecar.json`; certified tooling `scripts/render_eq*.py`) — OR keep
  rule-drawn text and record the deviation explicitly in the certification
  note. Lane decision; the z-stacks already satisfy the 2D requirement.
- **D9 Re-certify** — house_chrome_check 150dpi PASS → full judge
  (judge_protocol_03 payload) + zoomed crop certificates → per-slide
  re-certification per `scripts/17_worker_instructions.md`.

## Reusable components inventory

- `shared_patterns/house_chrome.js` + `house_chrome_check.py` (deck-03 values;
  NO top stroke; 150dpi PASS gate).
- `build/components/slide_017.js` exports (`renderBase`, `makeTrainTable`,
  `TITLE_BOX`/`TITLE_RUNS`, `TRAIN_BANDS`/`TEST_BANDS`, `WBOX_RECT`, `runsFor`,
  color constants) — reference material. **019 does NOT reuse makeTrainTable**:
  019's tables are rule-drawn grids, not addTables (018's addTable pattern
  doesn't transfer; the rule geometry is already correct in the current build).
- `build/assets/make_018_wbox.py` + `wbox018_sidecar.json` — the certified
  STIX/mathtext PNG pattern for D8.
- `scripts/render_eq*.py` — certified math tooling. `eq_*` assets are NOT
  needed for 019 unless D8 chooses mathtext.

## Parked legs (do not re-dispatch without a window; pgrep < 8)

- 019 full-frame read, RIDGE 3 crop read, RIDGE 10 crop read (crops already
  cut in `prephase/orig_judges/crops/`).
- Corroboration: lane crop_10..18 judges, judge_attempt_9, certified 018
  (RIDGE 10), delta §Closure. RIDGE 3 is the least-corroborated region [?].
