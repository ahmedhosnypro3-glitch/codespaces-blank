# build_readiness — slide 004 (S20a prephase, pool run 299640)

Readiness verdict: **READY TO BUILD/FIX** — attempt-2 build matches the original on every
PIL-verified element (all eight box geometries, fills, border colors re-verified 2026-10-25).
Remaining work is vision-gated confirmation of text details; at most one structural tweak
(Where-block true subscripts) is plausible.

## Certified components to reuse (do NOT re-derive)

1. `shared_patterns/house_chrome.js` + `house_chrome_check.py` (numeral 4) — in use; run the
   checker on every 150dpi render before judging.
2. `recreated_pptx/build/slide_007.js` (CERTIFIED) — run-splitting for selective underline,
   bordered-box idiom.
3. `build/assets/eq_004_Yvec.png`, `eq_004_Yhatvec.png`, `eq_004_norm.png`,
   `eq_004_formula.png` (+ .json sidecars) — 600dpi professional-2D equation PNGs, placed at
   exact px/600. If any desc leg changes equation TEXT, re-render via
   `scripts/render_eq.py` (matplotlib mathtext, 600dpi, transparent) — never hand-edit a PNG.
4. pptxgenjs laws already encoded (keep): lineSpacing in POINTS (a ratio emits spcPts
   hundredths → LO drops runs); separate addText per line (breakLine emits no <a:br/>);
   explicit pitch (WHERE_Y=285, WHERE_PITCH=30) instead of auto-flow.

## Build checklist (delta row → concrete action)

| Delta row | Action |
|-----------|--------|
| #1-#11, #13, #14 | none pending desc evidence — geometries/fills/borders PIL-verified |
| #12 Where-block | after `desc_where_block`: if the original shows true subscript positioning for the dimensions (N×(d+1), N×1), replace the literal-brace text runs ("X_{N×(d+1)}") with run pairs {text:"X",…},{text:"N×(d+1)", subscript:true} — matching how slide_003.js writes its dimension labels; if the literal-brace form is what the original prints, keep as-is; also settle letter x vs × |
| #13 salmon fill | leave FAEBD7 (founder-spec adjudication stands); the measured (238,215,195) delta is recorded in the delta doc for the judge's ground rules, not as a fix trigger |
| #4/#6/#7/#14 equations | only if a desc leg contradicts a sidecar mathtext — then re-render that asset via scripts/render_eq.py and re-place with the sidecar's ink-box law; do not rescale the PNG by hand |
| all | after any fix: re-render 150dpi, run house_chrome_check.py, re-certify per scripts/17_worker_instructions.md judge template |

## Pre-dispatch state (honesty note)

- 004's five legs were dispatched in this run's pack (`run_pack.sh full label_boxes remember
  where_block bottom_full`, probe law, parks under load ≥ 8). [transcripts pending at doc
  write time — gateway saturated; rows above carry no unverifiable claims]
- No certification judge run by this worker; PIL-first evidence only.
