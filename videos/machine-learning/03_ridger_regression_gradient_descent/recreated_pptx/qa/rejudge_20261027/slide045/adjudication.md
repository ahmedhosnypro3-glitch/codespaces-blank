# slide045 — FULL + CROP FAIL adjudications (2026-10-31, fresh worker F01, PIL-first)

Transcripts: `judge_full_fresh2.txt` (03:24, clean) FAIL; `crop_dense_judge_fresh2.txt`
(03:28, clean) FAIL. Evidence: `adjudicate_045_pil.txt` (read-only PIL, slide space).

FULL claims:
1. MAJOR heading "Ugnmented" vs "Unaugmented" — **REFUTED**. Standing law from the 043
   adjudication: the original frames print "Ugmented" (sic, no "A"); sibling-strip
   comparison here: orig045 heading strip (x82-236 y148-171) vs orig047/048/049/051 —
   mean|diff| 2.80-3.19, ink 46-51 px, i.e. identical handwriting. Build
   `slide_045.js:227` renders exactly "Ugmented Vectors ( from Top )" (comment line 27
   records the sic). Both images show the same word; judge misread the glyph.
2. MAJOR cream fill of top panel — **CONFIRMED as a small delta, DOWNGRADED to MINOR
   (palette class)**: orig panel interior (x75-715 y58-127) light-pixel median
   (254,255,232) vs render (255,255,255) — pale cream vs white, ~23 levels in B only.
   Per register precedent (slide015 palette deltas = MINOR) this is advisory, not
   FAIL-sustaining. (Build chose white from a single-point sample (240,242,220).)
3. MAJOR "row cards vs continuous field" — **REFUTED**: per-row horizontal rules at
   IDENTICAL positions in both — orig thr220 lines y197/206, 263/272, 329/338, 395/404;
   render y197/206.6, 262.7/271.9, 329/337.6, 394.7/403.8. Each of the 4 row bands is
   outlined in both; render even has one extra faint vertical divider at x403 (MINOR).
   No card/gap deviation exists.
4. Delimiter shape `[ ]` vs `( )` — **EXEMPT**: founder-mandated straight 1px delimiter
   bars (build comment line 4; same ruling as 048 att-17 top_band #3).
5. Paren spacing in heading — same class as claim 1, REFUTED.

CROP claim (aug block reoriented, missing x₁..x₆ labels, per-cell parens) — **REFUTED**:
both images have the header row (orig cluster y167-171, render y166.7-177.8) and exactly
3 digit rows (orig tops 184/199/215; render 184/199.3/214.2, delta ≤0.8 px); values match
column-wise; render's spanning delimiters are the founder-mandated bars. The judge read
the column-major grid row-wise and misattributed the delimiter style.

Net: no BLOCKER/MAJOR survives. FULL = PASS (FAIL dismissed); CROP = PASS (FAIL dismissed).
Slide stays certified; no build/pptx/DB change; no git; no evidence deleted.
