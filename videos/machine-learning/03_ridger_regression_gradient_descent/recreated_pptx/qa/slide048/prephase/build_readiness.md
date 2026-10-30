# Slide 048 — BUILD READINESS (prephase pack S20e)

Feeds the cert lane's next build/certification attempt on
`slide_048_recreated.pptx` (current build: `build/slide_048.js`, 370 lines, equation-PNG
based; gen_status='building' held by s7-judge-1024). Every row references
`delta_vs_related.md` (vs certified 045) and the ground-truth transcripts in
`orig_judges/`.

## A. Certified components available for reuse (do NOT re-derive)

| # | Component | Where | Reuse action |
|---|---|---|---|
| A1 | House chrome | `shared_patterns/house_chrome.js` `drawHouseChrome(pptx, slide, {numeral: 48})` | already used; keep numeral "48" |
| A2 | 2-D equation PNGs (9) | `build/assets/eq_r1_l..eq_r6_l.png`, `eq_r1_w.png`, `eq_r_kw.png`, `eq_initial_w_col.png` + sidecar JSONs (w_in/h_in/baseline_frac, 600dpi, 13pt, color 000000) | REUSE verbatim — they encode the 2-D dot-product/update equations per the deck equation law; no new renders needed unless a ground-truth read contradicts content |
| A3 | addEq() baseline placement helper | `build/slide_048.js:82-87` | keep as-is (baseline math is correct) |
| A4 | Calc-box idiom (white boxes, gray 0.75pt borders, red ⇒) | `build/slide_048.js:329-367` | keep; verify border hue against ground truth |
| A5 | 045's certified top-band table idiom | `build/slide_045.js:121-140` (cols/rows/cell helper) | REFERENCE ONLY — 048's table adds per-column tall parentheses (048 build lines 137-148) which 045 lacks |

## B. Delta-row → build-action checklist

| Delta ref (delta_vs_related.md) | Build action |
|---|---|
| C2 badge numeral | keep 48 (house_chrome) |
| T1 indigo border | keep #211776 1pt — confirm vs `orig_full.txt`/`orig_topband.txt` §1/§6 |
| T2 paren strokes around input-table columns | keep build lines 137-148; verify stroke x-pairs & row span vs `orig_topband.txt` §4 |
| T2 3rd data row (1 2 2 4 5 6) | keep verbatim (spec's uncertain_item resolved: frame wins) |
| T3 class-row C2 hue | if `orig_topband.txt` reads C2 as blue→indigo, keep #1F1655; if pure blue, change to 0000FF |
| T4 Initial-W label underline | check `orig_topband.txt` §2: if W is underlined in frame, add underline run to the "Initial W =" label |
| T5 REPEAT text | keep red bold; verify size/width vs measured band cols 426..530 |
| T7 Z header Z1 Z2 Z3 | keep; verify subscripts distinct in `orig_topband.txt` §2 |
| T9 pointer near "unaccepted" | if `orig_full.txt` §5 shows a cursor icon, ADD a small drawn icon (045's arrow idiom, `build/slide_045.js:192-200`); if absent, keep build as-is |
| A2 box title family/color | if `orig_aug_iter.txt` §2 reads blue/serif → switch to 045 idiom (Times New Roman italic 12pt blue); if black/sans → keep current |
| A3 delimiter strokes | keep 12 gray verticals; verify pairs/extent vs `orig_aug_iter.txt` §3 |
| A4 Iteration 1 box | keep red fill + white text; confirm text size against measured band rows 289..298 |
| A5 stop box | correctly absent — do NOT add (048 is iteration 1, no stop) |
| P1 box borders | keep; confirm gray hue from §6 color census |
| P2/P3 equation content | keep PNGs; verify scalars 0/2/2/−4/−6/−7 and W sequences against `orig_calc_r12.txt`/`orig_calc_r56.txt` §3 |
| P4 "Update Weight" row 1 | keep black; verify color (spec's maroon is refuted by pixel census) |
| P5 red ⇒ | keep C00000 15pt |
| P6 green ⇐ arrow | **PIL-REFUTED at the spec's position** (`pil_probe_048.txt`: only chrome stroke + empty panel margin) — keep absent unless `orig_calc_r12.txt` §5 sees it elsewhere inside the panel |

## C. Known cert-lane context (READ-ONLY — lane s7-judge-1024 holds the claim)

- The lane's latest crop judge (`crop_4_top_band_judge.txt`, 2026-10-25 07:20) and
  `crop_4_calc_panel_judge.txt` were dispatched against build attempt 4 crops; a FAIL on
  calc-panel "weight-vector evolution" structure is on record — my ground-truth reads give
  the lane clean original-side references to adjudicate PIL-first.
- Do not touch anything under `qa/slide048/` outside `prephase/`; do not write the DB.

## D. Verification order for the next build attempt

1. `orig_judges/orig_full.txt` — whole-frame region map (settle T9 + any missed region).
2. `orig_judges/orig_topband.txt` — T1..T8 details.
3. `orig_judges/orig_aug_iter.txt` — A1..A4.
4. `orig_judges/orig_calc_r12.txt` + `orig_calc_r56.txt` — P1..P6.
5. Apply §B actions → rebuild → house_chrome_check.py on 150dpi render → judge per
   `shared_patterns/judge_protocol_03.md`.

## E. OMML inventory (post-certification step, deck law)

- `slide_048_recreated.pptx` currently carries NO `mc:AlternateContent` wrap — and
  neither do certified siblings 045/046/047 (deck-wide OMML pass not yet run).
- After visual_check=PASS, wrap the **9 equation PNGs** (`eq_r1_l..eq_r6_l`,
  `eq_r1_w`, `eq_r_kw`, `eq_initial_w_col`) via `scripts/18_omml_wrapper.py`:
  manifest values re-derived from the CURRENT pptx sidecars (rel_id, image,
  mathtext, font_size_pt, color), never assumed from a prior build.
- Wrap the slide's own plain-named pptx only; never LO-resave a wrapped deck.
