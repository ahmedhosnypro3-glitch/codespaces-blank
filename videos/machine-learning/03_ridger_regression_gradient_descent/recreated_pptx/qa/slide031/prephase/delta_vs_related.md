# S20c pre-phase — slide 031 element delta vs certified slide 032

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent/`
Frame ground truth: `unique_slides/slide_031.jpg` (960×540, 1px = 1pt).
Delta basis: **certified slide 032** (`qa/slide032/`, certified 2026-10-25, serif
Times finding) — same gradient-descent topic family; certified 030 secondary.
Build reference: `recreated_pptx/build/slide_031.js`, current re-render
`qa/slide031/render_cur.png` (md5 9d42391f…) **as read 2026-10-25** — the S5 cert
lane is actively working 031 (judge attempts up to 30, render_30.png 16:28);
re-verify current build before applying any fix.
Vision transcripts: `qa/slide031/prephase/orig_judges/desc_*.txt` (S20c legs).
PIL forensics banked: `pil_forensics_031.txt` (curve/stroke census, dashed-guide
columns, arrow/label band census, eq-box border pin, title run extents).

**Lane status caveat:** 031's lane terminated degenerately 2026-10-24 ~19:31 after
real non-vision work; the three banked FAIL verdicts (attempts 1/2/4) were judged
against SUPERSEDED builds and must not be certified/fixed against.

Legend: **ADD** = in frame, absent from build · **DELETE** = in build, absent from
frame · **DIFFER** = both present, different geometry/color/text · OK = match.
Rows marked **[PIL]** carry values measured directly from the frame with PIL pixel
scans; vision reads confirm/extend them (text content still needs the transcripts).

| # | Element | 031 FRAME (ground truth) | 032 certified | 031 build (as read) | Verdict | Fix action |
|---|---------|--------------------------|---------------|---------------------|---------|------------|
| 1 | House chrome | panel + red frame + badge per deck AGENTS.md; house L/R red strokes measured at x58 / x901 | same | same | OK | — |
| 2 | Title | ONE line y66..88, three color runs; verbatim (analysis record): **"Convex Function,  Learning Rate =0.3, Start at X=3"**, red/green/blue bold segments; [PIL] green strokes ~x270..320, blue ~x470..555 (blue #00007F at x555), red run in x81..260 (samples hit background between glyphs) | 21.2pt three runs, same y-band | one line three runs | OK | verify run px-spans vs `desc_topblock.txt` (text known from analysis record) |
| 3 | Typeface | [VISION PENDING — serif vs sans; CONFLICT: analysis record says "sans-serif throughout" but 032's certified finding is serif Times; analysis color calls are demonstrably unreliable on this frame (see rows 4/12), so defer to the `desc_topblock.txt` zoom read] | serif Times New Roman everywhere | Arial | **DIFFER?** | if frame serif → switch all runs to Times family (032's certified finding) |
| 4 | Param table | [PIL] row fills GREEN #EFFFD9 / PINK #F4C4C4 / YELLOW #FCFF1D (label AND value cells same fill per row; yellow row y~230..250); VALUES (analysis record): **step 0.3 · initial X 3 · delta 0.1** (note: analysis's "yellow labels, white value cells" color call is contradicted by direct pixels — PIL wins) | x81..206 y179..250, divider x153.5, fills E9FFD5 / F3BEC2 / FAFF0D | labels EAFFD5 / EAFFD5 / F2C4C6 + values E7E9E6 gray | **DIFFER** | rebuild fills to frame values (032 certified family: green/pink/yellow incl. yellow 3rd value cell — NOT gray); values 0.3/3/0.1 |
| 5 | Main table frame | [PIL] outer border NAVY/INDIGO (#1F1E7C left, #3F3D90 right) x64..894; bottom navy y~529/530; band fill spans x~75..880 (padding inside navy frame); faint column separators at ~42px pitch: x≈131,172,214,256,298,339,381,423,465,506,548,590,631,673,715,756,798,840 (≈18 data cols; label col x75..~131) | narrow table x298..600, outer frame 564BA7, 5 color bands, TBX 8 cols | full-width 17-col (x63 + label 80px + 16×50px → right edge x943 — EXCEEDS panel x903), 0.5pt black all-cell grid | **DIFFER** | rebuild per frame: navy frame x64..894, ~42px-pitch columns, NO black grid; exact column count/text from `desc_table.txt` |
| 6 | Main table bands | [PIL] band1 olive #D8E281-family y~345..381; rule y387; band2 violet #CEB2E2/#BF9DDA y~388..425; rule y432; band3 peach #F7E2C5 y~433..468; rule y469; band4 green #B0EFA9/#E5FFD4 y~474..495; band5 pink #FAC6C8 y~504..528; white gap rows between bands (#FCFBFF y383..386, #FDFFFA y426..431, #EDEFEC y471..473, #FFFDF2 y496..498); dark in-band text rows at ~22px pitch | D8E175 / D4B2F5 / F6DDC1 / E7FFD2 / F4BEC2 5-band system, labels right-aligned | 8 "rainbow" fills (D0D97C, FCFBF6, BF9DDA, FFFFFD, F8DDC8, EFEDF0, 93D186, FCBCBD) — same families, but modeled as grid rows instead of bands+white gaps | **DIFFER (structure)** | keep the band color families (they match), restructure to bands separated by white gaps + sparse rules (y387, 432, 469, 475/476, 494, 500, 519, 529/530); no black interior grid |
| 7 | Table bottom anomalies | [PIL] dark red in-band text y~499..503 and y~517..519 (x200); dark blue-violet #211778 at y529..531 | n/a | per build | **DIFFER?** | vision `desc_table.txt` settles whether these are red-text cells and the bottom border color |
| 8 | Plot box | [PIL] RED borders: top y~66, bottom y~308..311, left x573, right x809 → box x573..809 **y66..309**; x-axis gray #969897 at y266; y-axis gray at x631 | x573..810 y66..309 (interior 67..307), gray axes 969696 x631/y266 | x573..809 y66..267 red border | **DIFFER** | fix plot bottom edge y267 → 309 (matches 032 calibration y266 for the axis) |
| 9 | Plot calibration | [PIL] axis positions match 032 (x631 / y266) | gray axes 969696; x=630.5+11.5v, y=266−12v | per build | OK? | reuse 032 calibration if `desc_graph.txt` ticks match |
| 10 | Curve | [PIL] near-black chord stroke y143..150 at x690; plot-interior dark-stroke census: near-black/gray strokes concentrate x620..700 y144..148 (chord) and steel-blue-gray family (170,181,187)≈AAB5BB n=567 px — curve is STEEL-BLUE-GRAY (032's certified 7D9AAA family; analysis calls it "blue parabola" of f(x)=(x-5)^2+1, same function as 032); point labels (5,1) AND (7,9) in frame per analysis record; [VISION PENDING curve extent/dots + exact (7,9) label text] | `curve_032.png` steel-blue 7D9AAA-family; black chord y146 x652..727 + 3 dots | per build; draws "(5,1)" at x497..535 y249..261 but NO "(7,9)" label | **DIFFER?** | chord black ✓ matches 032; curve steel-blue-gray ✓ 032 family — reuse `curve_032.png/json` if `desc_graph.txt` extent/dots match; check "(7,9)" label presence |
| 11 | Dashed x=5 guide | orig x658..664; [PIL] red dash columns confirmed at x658..663 (4-8 red px/col, neighbors n=1) (lane: MINOR placement delta vs build) | DASHED C00000 | red dashed | OK | keep |
| 12 | Annotation box | [PIL] box x243..566 y243..289; borders GREEN ALL SIDES — direct samples #45873F top (300,244), #62B75A bottom (300,288), green left (244,260), green right (565,260) (analysis record's "red border" is a model color error; the lane's own `adjudicate_annotbox_031.txt` confirms frame x566 green n=46); fill pale green (239,252,226)=#EFFCE2; verbatim lines (analysis record): **"X is in between 4.8 and 5.1" with 5.1 red bold** (= RED text run y248..260) + **"f(x) is in between 1.04 and 1.01"** (= BLUE text run y270..283) | green box x333..538 y234..280 ("X = 5" red, "f(x) Minimum value is 1.0" blue) | x243..809 with "red right border" — WRONG: conflates the plot's red left border (x573) and right border (x809) with the annotation box | **DIFFER** | rebuild annotation box x243..566 y243..289, green ≈45873F borders all sides, pale green #EFFCE2 fill; runs "X is in between 4.8 and " (black) + "5.1" (red bold) / "f(x) is in between 1.04 and 1.01" (blue) |
| 13 | Arrows / labels | analysis record: purple **"Bouncing"** label + purple arrow pointing down/right toward oscillating table columns; red arrow above table pointing down/right toward first columns; NO pink band on 031 (the 032 analog's pink band does not appear in the frame analysis, and PIL's sparse pink n=200 is AA around the purple label); [PIL] purple (116,26,114) n=174 first (314,304), navy (19,25,103) n=144 first (404,313) | down-arrow (350,317,16,37) rotate 25, white fill 8B1A2B outline; pink band x335..570 y292..320 "Reach Minimum after 6 Steps" 800080 | red/purple arrows + "Bouncing" label | OK-family | verify-only: arrow geometry/colors + "Bouncing" position from `desc_full.txt`; no pink band to add |
| 13 | Arrows / labels | [PIL band census x230..570 y292..330] purple/magenta (116,26,114)≈741A72 n=174 first (314,304); NAVY text (19,25,103)≈131967 n=144 first (404,313); light pink/lavender (206,194,206) sparse n=200 bbox x302..599 y280..326 — colors match 032's certified pattern (purple label + pink band), text verbatim [VISION PENDING] | down-arrow (350,317,16,37) rotate 25, white fill 8B1A2B outline; pink band x335..570 y292..320 "Reach Minimum after 6 Steps" 800080 | red/purple arrows + "Bouncing" label | **DIFFER?** | frame read settles real arrow inventory/colors/labels |
| 14 | Eq box | **[PIL PINNED]** box x399..529 y186..211: red border ALL SIDES (left vertical x399 n=24 rows, right x529 n=25, top y186 n=113 cols, bottom y211 n=131), interior near-white with sparse dark content — geometry within 1-2px of 032's certified x398..530 y184..212; equation content **f(x)=(x-5)^2+1** (analysis record) — IDENTICAL formula to 032's certified box (032: f(x)=(x-5)²+1; same parabola, same Start X=3, only learning rate differs 0.3 vs 0.4) | x398..530 y184..212 + `eq_032_main.png` (600dpi, 15pt, #000000) | per build | OK | **reuse `eq_032_main.png/json` directly** — same formula, same box geometry, same certified style; update the sidecar copy for 031 |

## Notes for the fixer
- Dominant fix = rows 5–7 (table frame/columns/bands) + row 8 (plot bottom) + row 12
  (annotation box) — all now PIL-measured; text content pending the S20c reads.

### TRANSCRIPT AUDIT — `desc_full.txt` banked 17:5x 2026-10-25 (PIL re-verified 17:58)
Geometry/text sections are usable; the following transcript claims are WRONG (direct
pixel probes, this frame) — the PIL cells of this table win where they conflict:
1. **"thin dark-gray #404040 outer frame ≈(8,8)–(952,532)" — HALLUCINATED.** Probes at
   x8/x12/x948/x952/y8/y12 are pure white (254,255,253). The only full-height
   verticals are the house red strokes x58/x901. Never add such a frame.
2. **"title one run, all red #FF0000" — WRONG.** Green ink confirmed x≈285..320
   (samples 77,147,111 / 85,135,108), blue ink x≈470..555 (39,32,136 / 0,0,134);
   red run lives in x81..260. Row 2's three-run model stands; per-run spans settle
   from `desc_topblock.txt` when it lands.
3. **"badge outline red, numeral red" — WRONG.** Numeral ink near-black (14,17,0)
   ≈ house 333333; ring sample (876,56) purple (80,27,97) ≈ 6A5ACD; fill yellow.
   House chrome (row 1) is never a fix target anyway.
CONFIRMED by PIL (transcript agrees with forensics): annotation box green borders +
red/blue text runs, plot red box x573..809 y66..309, navy table frame x64/x894/y529.

### TRANSCRIPT AUDIT 2 — `desc_full.txt` table section (PIL y/h-scan 18:1x)
The transcript's CELL VALUES are ground truth (oscillating x `3, 3.3, … 4.8, 5.1`,
f(x) `… 1.04, 1.01, 1.04, 1.01 …` — coherent with the annotation box and delta 0.1)
and its 18-data-column count agrees with PIL's ~42px-pitch separators. Its STRUCTURE
model is a misread — row 6's band+gap census is frame-true, direct probes agree:
1. **"8 uniform rows ≈24.4px, rules y381/429/477/501" — WRONG.** y-scan x=400 shows
   paired-row BANDS with white gaps: olive y343..380 (x + f(x) rows share ONE band,
   two text lines), gap 383..386, rule 387, violet y389..424 (x-delta + f(x-delta)),
   gap 425..431, rule 432, peach y433..468 (x+delta + f(x+delta)), rule 469, gap
   471..473, green y474..496 (slope; dark-green in-band rows y475/476 + y493/494),
   gap 497..498, pink y499..519 (next-x; DARK RED text rows y500, y510/511, y518/519
   — row 7's red-text anomaly confirmed), navy bottom y529/530. Build to row 6's
   band/gap structure; take values only from the transcript.
2. **"Row-1 data cells alternate light green/light yellow per cell" — WRONG.**
   h-scan y360: UNIFORM olive (218,226,123) across x100..880.
3. **"Label column khaki #CCCC99 with thin black outline" — WRONG.** Label cells
   carry the SAME band fill as their row (olive at y360, x80..145 all ≈218,226,123).
4. **"Outer box (70,333)–(883,528)"** — inward-shifted like 034's table box; frame
   border x64/x894 (row 5, navy #1F1E7C..#3F3D90), top navy ≈y334..336, bottom y529/530.
5. **Plot "curve: blue #0066CC" — color misread.** Tinted-ink histogram over the plot
   interior (red/gray/near-black excluded) peaks at (140,160,180)/(140,160,160) with
   direct samples (172,189,196)/(135,154,161) — steel-blue-gray, row 10's AAB5BB /
   032-certified 7D9AAA family. No #0066CC-family pixels exist. Reuse `curve_032`.

### TRANSCRIPT AUDIT 3 — `desc_full.txt` eq box / annotation runs / arrows (PIL 18:2x)
1. **Eq box: transcript's "(388,181)–(535,214), black border" — WRONG.** Column x388 is
   pure background; direct border probes RED on all four sides: left x399 (131,57,70),
   right x529/530 (144,74,82), top y185/186 (178,107,113), bottom y211 (139,37,51).
   Row 14's PIL pin stands: box x399..529 y186..211, RED border — reuse `eq_032_main`
   (its certified style is red-bordered). Transcript's formula content `f(x)=(x−5)²+1`
   agrees.
2. **Annotation line 2 runs (y266..288 x-bucket scan): math tokens ALL BLUE.**
   f(x) x244..291 blue + "is in between" x292..387 black + "1.04" x388..435 blue +
   "and" x436..459 black + "1.01" x460..483 blue. Transcript's "f(x) red / 1.04 red"
   are misreads. Line 1 (y246..262): "X" red, "4.8" red, "5.1" red, connectors black —
   and the phrase **"and color red bold" is LITERALLY printed** on the slide
   (`desc_full.txt` and 034's `desc_leftblock.txt` independently transcribe it;
   034's even flags "this phrase is literally printed"). Reconciled line 1:
   `X`(red bold) ` is in between ` `4.8`(red bold) ` and color red bold ` `5.1`(red
   bold); line 2: `f(x)`(blue bold) ` is in between ` `1.04`(blue bold) ` and `
   `1.01`(blue bold).
3. **CONFIRMED (transcript + PIL density map agree):** pink "Bouncing" label box
   (303,296)–(392,323) fill pink w/ purple-magenta text; FOUR blue down-arrows
   x≈397..529 y≈310..342 (16px wide, ~32px pitch) overlapping the table top border —
   row 13's "verify-only" resolves to: red block arrow ≈(150,310)→(176,348) + these
   four blue arrows + the pink Bouncing box; NO 032-style wide pink band.

### TRANSCRIPT AUDIT 4 — `desc_table.txt` (18:37) + `desc_topblock.txt` (18:39) — RESOLUTIONS
`desc_table.txt` (the 2× table crop) is the AUTHORITATIVE table read and CONFIRMS
Audit 2's band+gap census: "eight data rows in four visually-grouped pairs, ~3px
white gaps", fills `x`/`f(x)` yellow-green #C4D96C ≈ PIL olive, `next x` pink
#F3A6A0; **18 data columns at 42px pitch, boundaries x≈135,177,…,895** (row 5's
column model settles; navy frame x64 + label col to ≈x135); boundary ticks thin
dark-gray rows 1–6, GREEN ticks in slope row, RED ticks in next-x row (red
verticals PIL-confirmed at x177/x219 y500 — same red-cell-grid family as 034's
next-x row; build the bottom rows accordingly). Row 27's task: NO full-height
black grid — confirmed; thin boundary ticks + colored bottom-row ticks only.
Label-column "slightly darker/saturated" fills = AA artifact — PIL h-scans show
label cells share the band fill EXACTLY (uniform (208,217,116) across x82..858 at
y360; uniform (233,255,211) across the slope band).
`desc_topblock.txt` settles the pending rows:
- **Row 3 typeface SETTLED: title is BOLD SERIF (Times-like)** — adopt 032's serif
  treatment for title, eq math (serif italic), and annotation lines; param-table
  and main-table text read as bold sans (Arial-like) — keep sans there unless the
  S5 judge flags it.
- **Row 2 title runs SETTLED:** `Convex Function,` dark red x81..244 ·
  `Learning Rate =0.3,` dark green x256..421 · `Start at X=3` dark blue x431..556,
  one line y67..83, cap-height ≈14–15px (~21–24pt).
- **Row 14 eq box:** topblock independently reports x398..531 y186..212 RED border —
  matches Audit 3.1's PIL pin; desc_full's "(388,181) black" is dead. Reuse
  `eq_032_main.png/json`.
- **Rows 4/12:** param table label AND value cells share per-row fills
  (pale-green/pink/yellow; PIL families EFFFD9/F4C4C4/FCFF1D win for hex), box
  x≈90..217 y176..250 with steel-blue row dividers + divider column x≈164;
  annotation box x245..574 y241..288 green border uniform, and BOTH lines'
  run-colors match Audit 3.2 (line 1 with the literal "and color red bold").
- **Row 13 arrows refined:** the four blue arrows are HOLLOW (light-blue fill,
  dark-blue outline) at x≈403/439/476/518; the red arrow is HOLLOW (red outline,
  white fill) pointing DOWN-LEFT (176,312)→(152,342) per the 2× crop — desc_full's
  "solid, down-right" is the inferior read.

### TRANSCRIPT AUDIT 5 — `desc_graph.txt` banked 18:43 (PIL re-verified 18:52)
Geometry is gold; two color/position claims corrected by PIL:
1. **Dashed guide: x659..663 ONLY** (red-ink column census n≥4: exclusively
   659–663). The transcript's "red dashed at x≈684 (symmetry axis)" is a
   pattern-completion — no red column exists at 684. Row 11 stands: guide marks the
   start x=3, PIL columns x658..663.
2. **"Two bright-green dots straddling the vertex" — shape misread** (same as
   034's): ONE horizontal green ellipse x678..699 y248..256 (n=131), centered
   ≈(688.5,252) on the vertex.
3. **Curve "blue #4472C4"** — color misread again (Audit 2.5's steel-blue-gray
   histogram stands; reuse `curve_032`). The transcript's CURVE GEOMETRY is the
   take: vertex (683,252)=(5,1) ✓, branches exit top at (640,58)/(737,58).
4. **Chord:** black ~3px (649,145)→(717,145) — 031's own measure (032's 652..727
   was the analog; right end ≈717 per black-dot bbox 711..723). Black end-dots at
   (650..655,143..149) and (711..723,143..150) ✓; red dot (658..663,180..186) ✓
   (= value (3,~7) position; build aligns to px).
5. **Plot text (from the 2× crop):** `(2, 10)` at (629..656,148..158) · `(?, ?)` at
   (722..748,139..150) — row 10's analysis-record "(7,9)" is almost certainly this
   "(?, ?)" glyph-misread; verify on the crop before drawing · `(5, 1)` at
   (700..724,247..257) (build already draws it) · purple `3`/`3` distance marks at
   ≈(670,134)/(703,134) above the chord — NEW elements, verify on crop.
6. **Calibration from ticks:** 0 at (626,264), 11.5 px/unit x / 11.8 px/unit y —
   scale matches 032's certified 11.5 (row 9 reuse OK); origin 626 vs 032's 630.5 —
   probe the axis column during the fix. Cursor artifact at (665..673,264..274):
   omit per ground-rule (c).
- Reuse candidates from certified assets (`recreated_pptx/build/assets/`):
  `eq_032_main.png/json` (row 14 — geometry PIL-pinned to match), `curve_032.png/json`
  (row 10 — curve color family PIL-confirmed steel-blue-gray), 032's
  title-run/param-table/plot calibration code — ONLY where the frame matches
  (rows 9, 10, 14).
- Do not touch house chrome (row 1) or title runs (row 2).
- The lane may have already applied fixes (judge attempts up to 30 as of 16:28);
  re-read current build before editing. Re-certify per
  `scripts/17_worker_instructions.md` after fixes.
