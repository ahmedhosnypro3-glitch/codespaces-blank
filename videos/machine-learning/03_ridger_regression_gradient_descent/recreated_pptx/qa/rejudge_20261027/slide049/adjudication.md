# slide049 — FULL-leg FAIL adjudication (2026-10-31, fresh worker F01, PIL-first)

Transcript: `judge_full.txt` (2026-10-31 ~03:1x, clean, no 429) — FINAL VERDICT: FAIL.
Claims: (1) MAJOR duplicated data row `1 1 2 4 5 6` in the "Ugmented Vectors (from Top)"
table (render allegedly 4 data rows vs orig 3, box taller, Iteration-2 block shifted);
(2) MINOR delimiter bars vs parens; (3) MINOR red/green accents on d/W digits;
(4) MINOR box fill styling.

Evidence (read-only PIL, slide space; render 2001x1125):
- `adjudicate_049_augrows.txt` (probe below + `adjudicate_full.txt`): aug-box digit-row
  census x75-240 y178-229 — ORIG row tops [184.0, 199.0, 214.0] (count 3); RENDER
  [184.2, 199.6, 214.5] (count 3). Max row-top delta 0.6 slide px. NO fourth row exists
  in the render; the render's extra ink at y233-235 is the C1/C2 class-tag row (build y230),
  which the judge folded into the data rows.
- Build `build/slide_049.js:200-212`: exactly 3 value bands [183,198,213] x 6 columns,
  vals column-major = rows (1,1,1,1,1,1)/(1,2,1,5,6,6)/(1,1,2,4,5,6) — identical to the
  judge's own "original shows 3 data rows" reading. `adjudicate_full.txt`: 215,041 diff px
  (9.55%), densest cells in text glyph bands (y112-135, y382-405) — typed-vs-handwritten AA,
  no localized missing block.
- Claim 2: straight delimiter bars are founder-mandated (build comment line 4: "paren
  delimiters → straight 1px delimiter bars (founder …)"; same ruling as 048 att-17
  top_band #3 — exempt). Claim 3: color accents match the original's red C1/ink C2 and the
  computation-row coloring already certified on sibling slides 042-051; MINOR advisory.
  Claim 4: house box styling — ground-rule exempt.

Disposition: MAJOR REFUTED by pixels (3 rows in both images, geometry within 0.6 px).
No BLOCKER/MAJOR survives. FULL = PASS (FAIL dismissed).
CROP leg pending at this entry. Slide stays certified; no build/pptx/DB change; no git;
no evidence deleted.
