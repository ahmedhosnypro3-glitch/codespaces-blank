# slide045 rejudge fresh2 adjudication (2026-10-31, this worker, PIL-first, read-only)

Legs (fresh2, clean transcripts, no 429):
- FULL `judge_full_fresh2.txt` (2026-10-31 03:24Z): FINAL VERDICT FAIL — claims 1-4 below.
- CROP `crop_dense_judge_fresh2.txt` (2026-10-31 ~03:3xZ): FINAL VERDICT FAIL — claim 5 below.
- Adjudication sweeps: `adjudicate_fresh2_full.txt`, `adjudicate_fresh2_crop.txt` (rejudge_adjudicate.py),
  `probe_fresh2_full.py` / `probe_fresh2_full_out.txt` (targeted probes).

## FULL-leg claims

| # | claim | sev | disposition | key pixel evidence (slide-space px) |
|---|---|---|---|---|
| 1 | sidebar heading IMG1 "Ugnmented" vs IMG2 "Unaugmented" | MAJOR | REFUTED | orig045 heading strip (x78-240 y144-163) IoU 0.982-0.989 vs the SAME handwritten heading on slide_047/048/049/051.jpg; build `slide_045.js:227` + `analysis/slide_045_final.json` labels[12] both "Ugmented" (sic, frame omits "A") — 043 typo law applies; judge misread the handwritten initial |
| 2 | top blue frame fill: orig cream ~#FFF7CC vs render white | MAJOR | CONFIRMED | orig top band x70-718 y56-128 bright-pixel median (254,255,232) = cream FEFFE8; render median (255,255,255) pure white; sibling builds 042/047 use CREAM for the identical band (slide_047.js:80-81) while `slide_045.js:117` uses `fill: WHITE` — real fill defect |
| 3 | six separate outlined row cards in orig vs continuous ruled field in render | MAJOR | REFUTED | orig h-rules in calc panel x336-950 at y263/272/329-330/338/395/404/461-462/470 = render's at y262.7-470.0 (<=0.6px); orig has NO per-row vertical card borders (only panel right edge x852-853 + house stroke x900-902); build draws outer rect x274-853 y139-528 + same band lines; inter-band gutters (9-10px) present in both |
| 4 | delimiter "[" vs "(" on column vectors | MAJOR/MINOR | REFUTED (exempt) | rule (e) 2D professional format renders column vectors as bracket strokes (build `slide_045.js:43-48` bracketVector, deliberate); 048 att-17 precedent: delimiter geometry is a rule-(e) template item |

## CROP-leg claim

| # | claim | sev | disposition | key pixel evidence |
|---|---|---|---|---|
| 5 | augmented block reoriented: render = row-wise grid of per-cell "(1)" parens, no x1..x6 header; orig = six labeled column vectors with parens spanning stacked entries | MAJOR | CONFIRMED | orig sidebar body y182-252: paren-stroke groups with max vertical runs 36-43 slide px (column-spanning) at 6 column positions pitch ~22.5 (cx 94/106/115/128/138/150/160/173/183/195/205/218), header zone y158-178 has SIX x-label clusters at x 96.2/122/144.3/167/189/212.5 — identical structure to slide_051.jpg (column vectors, certified build `slide_051.js` AUG parenPair). Render: strokes max run ~8-9 px (per-cell parens) at doubled positions, header zone = row-1 text clusters, no six x-labels. Build `slide_045.js:232-249` draws row-wise `CELL(cx,...,"(1)")` cells and omits the x_i header row |

## Disposition

FULL and CROP FAILs both stand — 2 PIL-confirmed MAJORs survive (top-panel fill cream->white; sidebar
augmented matrix row-wise instead of column-vector + missing x_i labels). Slide 045 is NOT clean in
this wave; reopen build `slide_045.js` (fill WHITE->FEFFE8 on the top panel; redraw sidebar as six
column vectors with x_1..x_6 header per the 051 pattern), rebuild, re-render, re-run both legs.
No DB/deck/pptx changes made by this worker. No git; no evidence deleted.
