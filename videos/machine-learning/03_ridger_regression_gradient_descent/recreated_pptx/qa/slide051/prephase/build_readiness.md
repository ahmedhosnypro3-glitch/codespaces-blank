# Slide 051 — BUILD READINESS (prephase pack S20e)

Feeds the parked attempt on `slide_051_recreated.pptx` (current build:
`build/slide_051.js`, 398 lines, attempt 2, re-render verified pixel-identical;
gen_status='building'; lane `w051-takeover-20261024` parked 2026-10-24 on an upstream
504 wedge on the models:images leg — resumed lanes ran fine on 2026-10-25). Rows
reference `delta_vs_related.md` (vs certified 047) and the ground-truth transcripts in
`orig_judges/`.

## A. Certified components available for reuse (do NOT re-derive)

| # | Component | Where | Reuse action |
|---|---|---|---|
| A1 | House chrome | `drawHouseChrome(pptx, s, {numeral: "51"})` | keep |
| A2 | bracketColumn() straight-stroke idiom | `build/slide_051.js:83-103` | keep (051's frames show straight tall brackets, not 047's paren PNGs) |
| A3 | classTag() subscript idiom | `build/slide_051.js:106-114` | keep |
| A4 | implyArrow() double-line arrow | `build/slide_051.js:315-332` | keep |
| A5 | 047's decision-row band geometry | `build/slide_047.js:170-192` | REFERENCE for row pitch (tops 139/206/271 ≈ 051's 140/206/272) |

## B. Delta-row → build-action checklist

| Delta ref | Build action |
|---|---|
| C2 badge | keep "51" |
| K1 card border | keep NAVY 2pt; verify hue vs `orig_topcard.txt` §6 |
| K2/K3/A3/D4 delimiters | GROUND-TRUTH: straight strokes (current build) vs paren pairs (047) — `orig_topcard.txt` §3/`orig_aug_redbox.txt` §3 decide; if parens, render_eq.py PNG fallback (no assets today) |
| K4 Step η = 1 | keep red 12pt; value 1 (not 047's 2) |
| K7 Z headers | GROUND-TRUTH: "Z1 Z2 Z3" (current build, arithmetic-forced) vs "Z1 Z1 Z1" (047/048 family) — `orig_topcard.txt` §2 |
| A1 augmented box | GROUND-TRUTH: box vs bare — add #9FA8B1 0.75pt rect if `orig_aug_redbox.txt` §1 shows one |
| A2 "Augmented" spelling | GROUND-TRUTH from `orig_aug_redbox.txt` §2: frame wins (047 prints "Ugmented"; 051's build prints "Augmented") |
| A4 red button size | GROUND-TRUTH: 047 certified 23pt; 051 build 13pt — measured white-glyph band in `orig_aug_redbox.txt` §2 settles |
| D2 label Z3 | keep d(Z3) row 3 |
| D3 bare blue glyphs | verify parens presence in `orig_dec_r1.txt` §3 |
| D5 results 5/−8/0 | verify in `orig_dec_r1.txt`/`orig_dec_r23.txt` §3 |
| D7 Undefined Class | keep blue; verify in `orig_dec_r23.txt` §2 |
| D8 cursor | **PIL-REFUTED at the spec's position** (`pil_probe_051.txt`: only chrome stroke in 845..902,454..486) — keep absent unless `orig_dec_r23.txt` §5 / `orig_full.txt` show it elsewhere |

## C. Lane context (READ-ONLY)

- The lane's resume path (banked in DB last_error): `qa/slide051/dispatch_legA_attempt2.sh`
  then `dispatch_legB_attempt2.sh` once the images leg is healthy. Build attempt 2 is
  CURRENT — my pack is for adjudication, not a rebuild trigger.
- Do not touch `qa/slide051/` outside `prephase/`; do not write the DB.

## D. Verification order

1. `orig_judges/orig_full.txt` — region map (D8 cursor + any missed region).
2. `orig_topcard.txt` — K1..K7.
3. `orig_aug_redbox.txt` — A1..A4.
4. `orig_dec_r1.txt` + `orig_dec_r23.txt` — D1..D8.
5. Apply §B → rebuild (only if a ground-truth read overturns the build) →
   house_chrome_check.py → the lane's legA/legB judges.

## E. OMML inventory (post-certification step, deck law)

- `slide_051_recreated.pptx` currently carries NO `mc:AlternateContent` wrap — and
  neither do certified siblings 045/046/047 (deck-wide OMML pass not yet run).
- 051 has **zero equation PNGs** (native text + stroke delimiters) → **no OMML wrap
  candidates**; the step is a no-op for this slide unless a ground-truth read forces
  an equation-PNG re-render (e.g. delimiter-shape overturn), in which case the new
  PNG joins the wrap list.
- If wrapping ever applies here: wrap the slide's own plain-named pptx only; never
  LO-resave a wrapped deck.
