# pil_adjudication_legA12.md — slide 049, attempt 12 (all legs)

Inputs: `judge_attempt_12.txt` (full, judged render_11), `crop_11_{top_band,aug_box,legend,calc_rows,iter_stop}_judge.txt`.
render_11 pixel-identical to a fresh soffice render of the current `slide_049_recreated.pptx`
(0 / 2,251,125 px differ); all crop_11 pairs pixel-identical to re-cuts (`cut_crops_049_v10.py`).
Method: PIL on `unique_slides/slide_049.jpg` (960x540, 1px = 1pt). Coordinates are frame pt.

## Top band (leg FAIL — 8 findings)

1. Class row renders "1 1 2 4 5 6" where orig has C₁ C₁ C₁ C₂ C₂ C₂ — **CONFIRMED**
   (cluster widths w10-11 = two-glyph labels vs digits w1-5; C-strokes align x92/114/137/158/180/202;
   red fringes x114/x135; supersedes prior F9 "third value row" = misread). FIX.
2. Initial-W vector in straight bars |4;−2;−2| vs orig parentheses — **CONFIRMED**
   (4th judge consensus: att12-full MINOR2, top_band #2, legend boundary note, prior F1 tips-converge;
   asset `eq_initial_w_col.png` is straight bars — 048 keeps it, 049 gets its own paren asset). FIX.
3. "w =" missing / label-vector order — **REFUTED** (no '=' ink anywhere x354..365 y58..76;
   vector x330..353 sits LEFT of "Initial" x367..422 / W x426..449 in the orig too; prior F1 stands).
4. Z-grid parentheses missing — **CONFIRMED**, geometry measured: THREE paren pairs, bows at
   (641.5, 655.5), (664.5, 677.5), (686.5, 699.5) — one pair per Z column (0;0)(7;6)(3;2) —
   ink y88..118, mid-bulge curves (x655 continuous + x656 mid-only = right bulge). FIX.
5. Z labels need subscripts + italic (orig Z₁ Z₂ Z₃ italic) — **CONFIRMED**. FIX.
6. REPEAT underlined in orig — **REFUTED** (red ink y71..73 = three descender clusters
   x456 / x480-481 / x501-502 — 'g'/'p' bowls, no continuous band).
7. Underline scope: judge claims "orig underlines only the w" — **REFUTED as stated; scope fix
   CONFIRMED**: underline band y71..72 x365..422 = exactly "Initial" (x367..422); W (x426..449)
   has NO underline. Judge inverted the scope; PIL wins; fix = underline "Initial" only.
8. W lowercase — **REFUTED** (orig W w19-23 px = capital).

## Aug box (leg FAIL — 2 MAJORs + 2 MINORs)

1. Delimiters square/straight vs orig tall parentheses — **CONFIRMED** (orig bows at the same
   centres the 1px rects occupy: lp x93-94/115-116/137-138/159-160/182-183/204-205,
   rp x106-107/128/150-151/173/195-196/218; ink y181..223; mid-bulge). FIX.
2. Class tags "C1"/"C2" flat vs orig C₁/C₂ subscripts — **CONFIRMED**. FIX (unicode + italic).
3. Title upright vs orig italic — **CONFIRMED** (styling). FIX (italic; color stays measured VIOLET).
4. x-headers heavier/bolder than orig lighter italic — **CONFIRMED**. FIX (italic, de-bold).

## Legend (leg FAIL — 2 MAJORs + 3 MINORs)

1-2. C₁/C₂ subscripts missing — **CONFIRMED**. FIX (unicode ₁₂, same idiom as 044/045/047).
3. Typeface sans vs serif/italic — **ADJUDICATED OUT** (top_band leg: "colors and italics match";
   047-certified legend idiom is upright; video blur explains the look).
4. Zero green shade — **REFUTED** (render uses the measured frame core 5B9C4E; crop average is
   antialiasing-contaminated).
5. C₁ red saturation — **REFUTED** (orig video-muted (171,63,68) vs crisp FF0000; capture artifact).
Boundary note (|-2| vs (-2) fragment at crop top) = the Initial-W delimiter finding (top band #2);
not scored by the judge, same single fix.

## Calc rows (leg FAIL — 8 MAJORs + 2 MINORs)

1-2. Row-1 label d(x₂) / row-6 label mismatch — **REFUTED** (all six subscript zones structurally
   IDENTICAL, same two-cluster shape x298..303 + x304..307; att12 full judge read x₁…x₆ clean).
3. Missing |bars| around triplets — **REFUTED** (no flanking strokes rows 4-6: tall cols are the
   digits' own verticals; x376..380 holds only the adjacent wcol left delimiter; judge fused the
   '1' glyphs with the wcol stroke).
4. Triplet color coding missing — **CONFIRMED** (rows 1-3 ink avg (164,95,110) = red family;
   rows 4-6 (85,77,149) = INK 211776 blue-violet family; render all-black). FIX (RED / INK).
5. W-column square brackets vs orig tall parentheses — **CONFIRMED** (orig right stroke serif-less
   with mid-drift; render assets carry 2.2pt serif hooks). FIX (regenerate 6 W assets + the shared
   high-bracket asset as parens; geometry otherwise certified: pitch 16.4, gap 21.72, span 45.5).
6. "W" label plain vs orig bold + underlined — **CONFIRMED** (underline y172 x696..707 under
   W x697..705). FIX.
7. ⇒ red vs orig black — **CONFIRMED MINOR** (rows 1/4 ink avg (88,90,87)/(85,86,85), zero red
   excess). FIX (BLACK, keep bold).
8. Thin spaces around = / − — ADJUDICATED OUT (cosmetic spacing; GROUND RULES cover format).
9. Mouse-cursor artifact on row-1 vector — N/A per rule (e).
10. Green tint row-1 column — no action (n=7 greenish px = cursor/JPEG; all other row values
   measure dark (91,92,90)/(107,108,107)).

## iter_stop (leg PASS — 3 MINORs)

1. W underline extent — no action (current matches the measured band; video medium).
2. "Stop" italic in orig — **CONFIRMED** (styling). FIX (italic).
3. "in…W" gap — no action (raster spacing).

## Full att12 (leg PASS — 3 MINORs)

1. "Iteration 2" filled box vs orig red-text-only — **REFUTED** (orig box fillfrac 72.6% red,
   white text bbox x99..199 y284..298 = same box as render; judge misread).
2. Delimiter family — **CONFIRMED** (= master fix above).
3. "Initial W =" order/equals — **REFUTED** (top band #3).

## FIX LIST (one cycle → att13)

Assets (new files only — nothing shared is mutated):
- `build/assets/gen_parens049.py` → `parens049/paren_aug_{lp,rp}` (inkH 44.5, DGRAY) and
  `paren_z49_{lp,rp}` (inkH 30, DGRAY) — certified 044 bezier pattern (S 1.5, D 1.0).
- `build/assets/render_wcol_049p.py` → paren-variant column assets, black, same certified
  geometry (pitch 16.4, gap 21.72, span 45.5, fs 12): `slide_049_wcol_paren_1..6.png` +
  `eq_initial_w_col_paren.png` (pitch 15.5, gap 22.0, rows 4/−2/−2), sidecar
  `eq_slide049_wcol_paren.json`.

Build (`slide_049.js`):
1. Top-table row3 → class tags C₁C₁C₁C₂C₂C₂, bold+italic, RED/INK.
2. Aug 1px-rect delimiters → paren_aug pairs at bows x93.5/115.5/137.5/160.5/182.5/205.5 (lp)
   and x106.5/128.5/151.5/173.5/196.5/218.5 (rp), ink top y180.
3. Z-grid: add paren_z49 pairs at bows (641.5,655.5)(664.5,677.5)(686.5,699.5), ink top y88.
4. Subscripts: Z labels Z₁Z₂Z₃ (italic, de-bold), aug tags C₁/C₂ (italic), top class row (above),
   legend C₁/C₂.
5. Underline "Initial" only (rich-text run split).
6. Initial-W asset → eq_initial_w_col_paren.png (bow x330.5, ink top y58).
7. wcol assets → paren variants (lp bows x379.5 / x722.5 / x733.5, ink top b+7 / b+8).
8. Triplet digits colored RED (rows 1-3) / INK (rows 4-6).
9. "W =" → W bold+underlined run + " =" plain run.
10. ⇒ color BLACK (was CRED), keep bold.
11. Aug title italic; aug x-headers italic non-bold.
12. "Stop" italic.

Adjudicated out (no change): d(xᵢ) labels, triplet bars, REPEAT underline, W case, legend
typeface/colors, Iteration-2 box, label order/"=", spacing MINORs.
