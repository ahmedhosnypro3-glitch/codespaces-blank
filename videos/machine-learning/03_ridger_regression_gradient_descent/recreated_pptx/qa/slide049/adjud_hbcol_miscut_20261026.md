# Adjudication — 049 paren-sweep hb_col crop leg (2026-10-26)

## Disposition: NO-RESULT (mis-cut original crop), not a render defect

The paren-sweep lane's one finished vision leg, `crop_15_hb_col_judge.txt`,
returned FAIL with two findings:

1. BLOCKER — "row-6 label reads 3 vs 6"
2. MAJOR — "digits black vs green"

Both findings were adjudicated against pixels as **artifacts of a mis-cut
original crop**, not render defects:

- Template match of the sweep's `crop_15_hb_col_orig.png` content against the
  full original frame places its best match at frame x≈371 (mean diff 4.2) —
  a DIFFERENT table column than the render crop, which maps to x≈434.
- A fresh PIL cut of the original at the render crop's true geometry
  (x433..473, y138..530) is nearly empty — the sweep compared the render's
  hb_col column against the wrong original region, so the model was shown
  non-corresponding content.
- Per verdict law (image-analysis SKILL.md, W2/wrong-subject class), a
  comparison built on non-corresponding content is NO-RESULT; its findings
  are DISMISSED and the pair is not reused. No re-fix of the render was
  made or warranted from this leg.

## Render fix verification (independent of the mis-cut leg)

The underlying real defect — build-time-drawn (non-media) mirrored
parentheses in the wcol column of 049, found by the sweep and fixed in
`render_wcol_049p.py` (bezier tip direction bug) — is verified good by
PIL forensics banked in `dxdelim_16e.out`:

- Orig vs render_15 paren bow direction + position agree row-by-row
  (dx pair at frame x378-403, W pair at x722-748).
- render_13 → render_15 pixel diff = exactly 6 wcol bands (1426 px each)
  + the initial-W block (render y120..224, x183..739) and nothing else —
  so digit colors/labels are unchanged from the att14-certified bytes.

## Carry numbers into att15 (render_13 vs render_15 per-region diffs)

| region    | diff px | disposition                        |
|-----------|---------|------------------------------------|
| aug_box   | 0       | carried from att14 certification   |
| iter_stop | 0       | carried from att14 certification   |
| legend    | 132     | paren-fix corner intrusion → re-judge in att15 |
| top_band  | —       | re-judge in att15                  |
| calc_rows | —       | re-judge in att15                  |

att15 legs: top_band, calc_rows, legend (runner `run_legs_049_a15.sh`,
payload byte-for-byte from `shared_patterns/judge_protocol_03.md`).

## Addendum 2026-10-26 (later) — att17 Step-line truth + underline-law correction

The att15 top_band FAIL (2 MAJOR: missing "=", order inverted) was fixed in
att16 (label "Initial W =" left at x267, vector PNG unchanged at x330.02) —
verified ±1-3px. att17 adds the pixel-proven Step-line completion: the build
had NO dark "Step η = 1" text and drew "REPEAT using Step η = 1" all-red
(x426, w150). Fresh forensics (`qa/slide050/adjud_step_line_20261026.md`)
prove 049's orig = 050's orig in this zone (IoU 1.000): dark underlined
"Step η = 1" x366..421 (underline y71..72 REAL) + red "REPEAT using Step"
x425..530. att17 build mirrors certified 050's composition (CHART_RED
"92211B"); render_16→17 diff confined to x365..567 y60..74; chrome PASS.
The earlier "NO underline anywhere" note above is corrected: no underline
under the LABEL's W (that reading was right), but the y71..72 band under the
Step text is real and now drawn. The att15 judge's "original underlines W"
and its acceptance of the all-red line are both dismissed per pixels
(DESC-primed misreads). Carries unchanged: aug_box/iter_stop 0-diff (att14),
calc_rows (att15 PASS). Re-judge att17: top_band, legend, legA.

## Addendum 2026-10-26 (att18) — word-order correction: the line reads "REPEAT using Step η = 1"

Glyph forensics on the origs (pixel-identical 049/050 in this zone: label XOR
3px, top-box XOR 84px, dark-band IoU 1.000) supersede the att17 word order
above: the dark underlined italic text at x366..421 y61..70 is "REPEAT" —
six uniform caps-height glyphs, ZERO descenders ("Step η = 1" is impossible
there: p/η would descend below y72, which is blank) — with the real
underline bar y71..72 x366..419; the red text at x425..530 y60..74 is
"using Step η = 1" (i-dot x442; descenders g/p/η at x452/481/508). Two
independent att17 judges (049 top_band, 050 mathzone) both read the orig as
"REPEAT using Step η = 1" — the certified att17 composition had the words
SWAPPED. att18 rebuild: the slide draws black italic underlined "REPEAT"
(fontSize 14, box x365 y56 w64 h18) + red bold italic "using Step η = 1"
("92211B", box x424.5 y57 w112 h17); render_18 PIL-verified (REPEAT
x365.8..420.6 y60.9..70.5, underline y72.0 continuous, red x425.4..531.0
y61.3..73.8, i-dot + all 3 descenders present); r17→r18 diff confined to
x365..531 y60..74. The att17 addendum's "underline under the Step text"
phrasing reads the RIGHT pixels but the WRONG words: the y71..72 bar sits
under "REPEAT". 051 caveat unchanged: its own red bbox (x420..435 y67..77)
is short red text — scan 051's line with the same forensics before any
rewrite; the REPEAT-line law may not apply there.
