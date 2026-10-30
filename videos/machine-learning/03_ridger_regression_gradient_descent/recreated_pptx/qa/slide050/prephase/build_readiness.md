# Slide 050 — BUILD READINESS (prephase pack S20e)

Feeds the in-flight attempt on `slide_050_recreated.pptx` (current build:
`build/slide_050.js`, 398 lines; gen_status='building'; lane `w050-legs-20261024`
re-judge pending gate as of its last heartbeat). Rows reference `delta_vs_related.md`
(vs certified 046) and the ground-truth transcripts in `orig_judges/`.

## A. Certified components available for reuse (do NOT re-derive)

| # | Component | Where | Reuse action |
|---|---|---|---|
| A1 | House chrome | `drawHouseChrome(pptx, s, {numeral: "50"})` | keep |
| A2 | Initial-W PNG | `build/assets/eq_050_initialW.png/.json` | REUSE (2-entry underlined-W vector) |
| A3 | Z column PNGs | `build/assets/eq_050_Z1/Z2/Z3.png/.json` | REUSE |
| A4 | Final-W PNG | `build/assets/eq_050_finalW.png/.json` — RE-RENDERED 2026-10-25 (substack+phantom rows, 677×496) after attempt-9 size finding | REUSE the CURRENT png; the `.pre_w7_3comp` backups are lane evidence — do not resurrect |
| A5 | Chart composition | `build/slide_050.js:236-342` (axis mapping X2PX/Y2PY, gridlines, markers, decision line, +ve) | keep; it is measured, not approximated |
| A6 | 046 plot idiom | `plot_046_scatter.png` | NOT reusable (different data) — 050 must keep its native composition |

## B. Delta-row → build-action checklist

| Delta ref | Build action |
|---|---|
| C2 badge | keep "50" |
| T1 navy box | keep 2pt #1E1A76 + cream fill; verify hue vs `orig_topbox.txt` §6 |
| T2 two parenthesized rows | keep; verify row values (…6) vs (…4) in `orig_topbox.txt` §4 |
| T3 C1 RED/C2 BLUE | keep; confirm §4 |
| T4 Initial W (4/−2) | keep PNG; verify entry count + underline from §3 |
| T5 "REPEAT using Step" (no η=1) | **PIL-SETTLED** (`pil_probe_050_eta.txt`: rows y58..70 in x540..717 hold ZERO ink — the zone right of the red text is blank; y71+ hits are Z-vector tops) — keep build as-is; the vision read confirms the red text's own wording |
| T6/T7 Z vectors | keep PNGs at x641/664/686; verify pitch/labels §3 |
| T8 legend | keep C1 red/C2 blue/Zero green; verify §2 |
| T9 pink box | keep #F9E8FA; GROUND-TRUTH border: if §1/§6 shows a visible border stroke, add 1pt line; if flat fill, keep borderless |
| A1 white caption box | keep #A1ABB5 1pt |
| A2 "Augmented" spelling | GROUND-TRUTH: `orig_aug_caption.txt` §2 — if the frame prints "Ugmented", rename (verbatim law); if "Augmented", keep |
| A3 bias row | keep 3 rows with bias (1,1,1,1,1,1); verify values §4 |
| A4 Iteration 2 | keep #C90004; size per measured band |
| A5 stop text 20pt | keep (this was the attempt-9 finding #8 fix — 11→20pt); verify band y350..371/375..394 from `orig_redstop.txt` §2 |
| G1/G2/G3 chart | keep native composition; verify markers/line/+ve against `orig_chart.txt` §3/§5 |
| G4 triangle at (3,3) | GROUND-TRUTH: if `orig_chart.txt` §5 sees a red triangle near data (3,3), ADD it (shape idiom already present); if only (7,6), keep |

## C. Lane context (READ-ONLY)

- Attempt-9 findings #3 (finalW construct size) and #8 (stop-text size) are CONFIRMED and
  already fixed in the current build (re-render + 20pt, PIL-verified) — re-judge pending.
- My pinkbox/topbox/redstop/chart/aug_caption ground-truth reads give the lane fresh
  original-side references for the re-judge adjudication.
- Do not touch `qa/slide050/` outside `prephase/`; do not write the DB.

## D. Verification order

1. `orig_judges/orig_full.txt` — region map.
2. `orig_topbox.txt` — T1..T8 (incl. the η=1 question).
3. `orig_aug_caption.txt` — A1..A3.
4. `orig_redstop.txt` — A4/A5.
5. `orig_chart.txt` — G1..G4.
6. `orig_pinkbox.txt` — T9.
7. Apply §B → rebuild → house_chrome_check.py → the lane's re-judge.

## E. OMML inventory (post-certification step, deck law)

- `slide_050_recreated.pptx` currently carries NO `mc:AlternateContent` wrap — and
  neither do certified siblings 045/046/047 (deck-wide OMML pass not yet run).
- After visual_check=PASS, wrap the **5 equation PNGs** (`eq_050_initialW`,
  `eq_050_Z1/Z2/Z3`, `eq_050_finalW` — CURRENT re-render, 677×496; the
  `.pre_w7_3comp` backups are lane evidence, never the manifest source) via
  `scripts/18_omml_wrapper.py` — manifest values re-derived from the CURRENT pptx.
- Wrap the slide's own plain-named pptx only; never LO-resave a wrapped deck.
