# S20c pre-phase — slide 034 build readiness checklist

Companion to `delta_vs_related.md` (row numbers below reference that file's table).
Basis: frame ground truth (`unique_slides/slide_034.jpg`), certified 033 construction
(`build/slide_033.js`), build as read 2026-10-25 (`build/slide_034.js`, attempt 6).
**2026-10-25 20:2x: ALL FOUR transcripts (table/leftblock/plot/full) are banked
in `orig_judges/` and PIL-audited in the TRANSCRIPT AUDIT sections (1–4) of
`delta_vs_related.md` — read those first; the audited claims override the
unaudited ones. No vision item remains pending in this pack.**

## Preflight (before any fix)
0.1 Re-read the CURRENT `build/slide_034.js` and current deliverable pptx — the S5
    cert lane is actively working 034 and may have landed attempt ≥ 6 fixes; only
    deltas still present in the current build are actionable.
0.2 Never write into the lane's dirs or dispatch judge legs; fixes belong to the
    lane's own run. This checklist is the fix map, not a fix authorization.

## Build actions (delta row → action)
1. **Row 3 — subtitle L1 color.** "May reach different minimum value based on:" →
   dark red, 8B0000-family (settled: PIL dominant ink bucket r≈128 with both
   transcripts agreeing dark red; AUDIT 4 item 10 covers the title's one-run
   settlement likewise — LOW-priority: merge build title runs to one dark-red
   run if the build draws two). Keep geometry y94..113 x113..533.
2. **Row 5 — eq box border.** Black → C00000; keep frame geometry
   **x465..600 y169..218** (PIL-pinned: right edge x600; x607 is the plot's left
   red border, not the box).
3. **Row 6 — param box rebuild.** Replace flat FFFACD with 033's certified
   cell-row pattern: GREEN cell row / PINK cell row / YELLOW cell row
   (frame-sampled 232,251,209 / 244,190,193 / 249,253,15 ≈ E9FFD4 / F9BBC1 / FDFD00)
   with white padding strips above/below; navy border (31,22,101)≈1E1856; values
   **step 0.2 / initial X 7 / delta 0.1 — CONFIRMED by the 034 analysis record**
   (verbatim_text parameter_box: "step=0.2, initial X=7, delta=0.1"); the
   leftblock crop read is now only a belt-and-braces verify.
4. **Row 7 — plot border.** Black → C00000. Keep frame box x607..845 y58..313.
5. **Row 8 — curve color.** Regenerate/recolor `build/assets/graph_034_main.png`
   to teal (135,205,208) with identical curve shape; update the eq-style sidecar
   json if present so the manifest stays true.
6. **Row 11 — table band system.** Replace AFEEEE/FFFACD/FFB6C1/98FB98 fills with
   033's certified band fills (D9E275-family band1 spanning x+f(x) rows, violet
   band2, peach band3 — frame-sampled 205,214,112 / 199,165,229 / 225,202,176);
   banded/gapless rows; interior column separators WHITE (remove 0.5pt black grid);
   rules ONLY at the measured full-width inventory (AUDIT 4 item 7): y320/321
   violet-blue top · y330/331 gray-olive top edge · y356 dark olive · y367/y410/
   y453 within-pair separators (olive-gray/gray-violet/gray-brown — NOT white) ·
   y373/374 + y416-418 between-band separators (gray-violet/gray-brown) · y435
   dark-peach pair separator · y459-461 + y477/478 DARK GREEN slope edges ·
   y483/484 + y502 DARK RED next-x edges · y517 navy bottom.
   Copy 033's XSEP band construction (XSEP=[143,184,224,264,304,344,384,425,465,
   505,546,586,626,666,707,747,787,827,867]) and verify against
   `orig_judges/desc_table.txt` column boundaries.
7. **Row 12 — cyan insert.** Replace the build's green highlight on f(x) row
   cols 14–18 with the frame's insert on the BAND-1 rows (header+f(x)) of data
   columns **14–16 only** (index corrected by AUDIT 4 addendum; the audit-4
   text's "13–15" is a counting slip — geometry x≈666..790 spans c14..c16 on
   both the frame grid and 033's XSEP): x≈669..789 (XSEP 666..787), y≈331..368
   (PIL: y390 pure violet); fill saturated green-cyan (135,244,178) ≈ #87F4B2
   family (banked #8BF6C0/#95F6AF); dashed darker-green border. Settled by
   `desc_table.txt` + AUDIT 4 item 5 + addendum.
8. **Row 13 — slope row (CORRECTED by AUDIT 4 item 6 — the 033-inherited
   special-cell model was wrong for 034).** Rebuild: row bg pale green
   ((233,255,210)/(195,255,180) family; dark-green edge rules y459-461/y477-478);
   18 inset inner boxes (~36×15, red #C00000 border ~1.5px) with SALMON fills
   (#E89B82 family, measured (199,156,128)) EXCEPT **c15 and c17 = pale-yellow
   #FFFFBE boxes carrying value 3.2** (PIL yellow census n=451 at x703..832).
   Values (from `desc_table.txt`): −4.5, −6.7, −8.7, −10.6, −12.2, −13.3,
   −13.9, −14, −13.4, −12.1, −10.1, −7.5, −4.4, −0.7, 3.2, −0.7, 3.2, −0.7 —
   NOT "yellow 0.3-cells at cols 14/16". Label cell pale-green (fill shared
   with row bg family).
9. **Row 14 — next-x row.** Pink #F49B9B-family fill (measured (235,171,176)/
   (247,190,197)) with FULL red cell grid (red border around every cell;
   dark-red edge rules y483/484 + y502). Verify the build draws the complete
   red grid, not just the outer border.
10. **Row 9 — plot markers (SETTLED: `desc_plot.txt` + `desc_full.txt` both
   banked and audited).** ONE red dot (784,148) blob + red dashed guide
   x781..785 (peak x782) down to the axis y≈172; orange arrow (763,115)→(783,143)
   pointing down-right; pink label box "Reach"/"global Minima" (2 lines, magenta
   text, (743,268)–(842,307)); ONE horizontal green ellipse x800..815 y255..266
   at the global minimum (NOT a circle, NOT two dots); axes cross (721.5,172),
   1 unit 9.5px, gridlines #DDDDDD-family; OMIT the "pencil icon" — cursor
   artifact, ground rule (c). Curve dark teal ✓ (action 5).

## Reusable certified assets
- `build/assets/house_chrome.js` + `house_chrome_check.py` (chrome, rows 1).
- `build/assets/eq_034_main.png` — 034's own certified-pattern equation asset; keep.
- `build/assets/graph_034_main.png` — keep shape, recolor teal (action 5).
- 033's `build/slide_033.js`: param-box cell-row pattern (action 3), XSEP band
  construction + white separators + boundary-rules-only (action 6), cyan-insert
  construction (action 7), plot border C00000 (action 4).

## Closeout
11. After any fix: re-render, re-run `house_chrome_check.py`, and re-certify per
    `scripts/17_worker_instructions.md` (per-slide re-certification is mandatory).
