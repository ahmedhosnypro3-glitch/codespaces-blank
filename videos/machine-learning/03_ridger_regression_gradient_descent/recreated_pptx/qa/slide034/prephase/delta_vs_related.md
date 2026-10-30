# S20c pre-phase — slide 034 element delta vs certified slide 033

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent/`
Frame ground truth: `unique_slides/slide_034.jpg` (960×540, 1px = 1pt).
Delta basis: **certified slide 033** (`qa/slide033/`, certified 2026-10-25) — same deck
family (gradient-descent iteration tables), nearest structural sibling.
Build reference: `recreated_pptx/build/slide_034.js` (attempt 6, == slide_034.js,
render_6.png md5 71c03bfa…) **as read 2026-10-25** — the S5 cert lane is actively
working 034; re-verify current build before applying any fix.
Vision transcripts: `qa/slide034/prephase/orig_judges/desc_*.txt` (S20c legs).
PIL forensics banked: `pil_forensics_034.txt` (plot census, red-dot clusters, teal
profile, label-band rows, orange arrow, eq-box border pin, top-rule extent).
PIL pixel samples were taken directly from the frame; values below are from those
samples and from the vision reads.

Legend: **ADD** = in frame, absent from build · **DELETE** = in build, absent from
frame · **DIFFER** = both present, different geometry/color/text · OK = match.

| # | Element | 034 FRAME (ground truth) | 033 certified | 034 build (as read) | Verdict | Fix action |
|---|---------|--------------------------|---------------|---------------------|---------|------------|
| 1 | House chrome | panel + red frame + badge per deck AGENTS.md | same | same | OK | — |
| 2 | Title "Non-Convex Function" | ink x195..434 y67..84, two runs 8B0000 / C00000, ~24pt bold | n/a (033 title differs) | matches per worker_report | OK | — |
| 3 | Subtitle L1 "May reach different minimum value based on:" | [PIL] y94..113 x113..533, text strokes DARK RED #8B0000-family (#8D1828/#800D1E/#7B0008) — RED text confirmed | — (033 has no L1) | black text | **DIFFER** | recolor run to dark red (≈8B0000/C00000 family) |
| 4 | Subtitle L2 "initial point and learning rate" | y122..140 x192..461, BLUE bold | — | per worker_report bold blue | OK | — |
| 5 | Eq box | **[PIL PINNED]** x465..600 y169..218; red border ALL SIDES (left vertical x465 n=48 rows, right x600 n=49, top y169 n=132 cols, bottom y218 n=136); interior near-white #FFF7F6 with gray bar y198..200. NOTE: the earlier read's right edge x607 was the PLOT's left red border (that column spans n=64 rows over y160..225 — taller than the box), not the box | x449..585 y182..230, border C00000 | border black | **DIFFER** | border → C00000 (RED confirmed by PIL); box geometry x465..600 y169..218 (≈033 shifted — frame wins) |
| 6 | Param box | x75..174 y246..308, navy border (31,22,101) ≈ 033 1E1856; 3 cell rows GREEN (232,251,209) y~250..266 / PINK (244,190,193) y~270..284 / YELLOW (249,253,15) y~288..298 with white padding strips above/below; values **step 0.2 / initial X 7 / delta 0.1 CONFIRMED by analysis record** | x75..174 y246..308 navy 1E1856, cells E9FFD4 / F9BBC1 / FDFD00 | flat FFFACD fill | **DIFFER** | rebuild as 3 colored cell rows using 033's certified pattern (reuse param-box code from slide_033.js); values step 0.2 / initial X 7 / delta 0.1 |
| 7 | Plot box | x607..845 y58..313, border RED (samples 121,46,56 / 155,8,22 / 137,50,62 / 151,77,86) | x607..845 y60..313, C00000 | border black | **DIFFER** | border → C00000 (lane confirmed same trigger 2026-10-25) |
| 8 | Curve color | TEAL (135,205,208) | n/a | blue | **DIFFER** | recolor/regenerate `graph_034_main.png` teal (keep same curve shape) |
| 9 | Plot markers | **[PIL CLUSTERED]** ONE solid red dot (783,148) (blob n=48, x780..786 y144..152) + 4-px red trace (781..783, y168..171); ORANGE pointer/arrow x765..778 y116..134 (strong orange (208,122,61)/(238,128,41) n=75); pink/magenta label text INSIDE plot lower-right bbox x753..823 y277..301 n=328 (~(191,92,112)≈BF5C70 family) — "Reach global Minima" per build; teal curve profile x616..829 peak 44 px/col at x621 | n/a | per build | **DIFFER?** | vision `desc_plot.txt` settles verbatim label text + arrow shape; colors/geometry now PIL-pinned |
| 10 | Table frame | dark verticals ONLY x68, x881; **[PIL] full-width violet-blue top rule y320..321 (2px, ≈(95,85,156)≈#5F559C) spanning x68..880**; rows y321..517; label col 82..136, 18 data cols to x879 | x86..869 y320..519, XSEP=[143,184,224,264,304,344,384,425,465,505,546,586,626,666,707,747,787,827,867] | uses 033-family XSEP | OK (verify exact XSEP via `desc_table.txt`; top-rule color ≈#5F559C is frame-truth) | — |
| 11 | Table bands | band1 D9E275-family (205,214,112) spanning rows x+f(x); band2 violet (199,165,229); band3 peach (225,202,176); banded/gapless rows; interior separators WHITE (not dark) | D8E175 / D4B2F5 / F6DDC1 band system | AFEEEE / FFFACD / FFB6C1 / 98FB98 + 0.5pt black gridlines | **DIFFER** | adopt 033 certified band fills; drop black interior gridlines → white separators (033 pattern) |
| 12 | Cyan insert | [PIL] on band-1 row ONLY (y340 scan: cyan #8BF6C0/#95F6AF family; y390 scan: pure violet — no cyan); x-extent ≈666..790 with brownish/darker-green DASHED border verticals (x682..692, 722..733, 762..774) | 8BF8AB x666..787 y332..368 (band-1 row), maroon dashed border | green highlight on f(x) row cols 14–18 instead | **DIFFER** | replace with cyan insert x≈666..790 on band-1 row, dashed border per `desc_table.txt` |
| 13 | Slope row | label cell pale-green (196,217,178) ≈ E9FFD4; data cells salmon (199,156,128) ≈ DEAC95; yellow 0.3-cells cols 14/16 | label E9FFD4, data DEAC95, yellow 0.3 cells cols 14/16 | per build | OK-family | verify fills in build; fix if not E9FFD4/DEAC95 |
| 14 | Next-x row | pink (235,171,176) ≈ F7BEC4, red border | F7BEC4, red border | per build | OK-family | verify |
| 15 | Dark rules | full-width dark only at y459, 477/478, 483/484, 502, 517 | row boundary lines at band/slope/next-x edges | black grid everywhere | **DIFFER** | only the certified boundary lines, none interior |
| 16 | x-row values | c16/c18 = 9.6 (banked fix) | n/a | fixed in attempt 6 | OK | — |
| 17 | Assets | — | eq_033_main_v7b.png, slide_033_plot_v7.png | own eq_034_main.png + graph_034_main.png exist | OK | keep 034's own assets; recolor graph only |
| 18 | Explanatory text | (analysis record) two lines below eq box: **"X is in between 9.6 and 9.8"** with **9.8 red bold** + **"f(x) is in between -10.03 and -9.92"**; approx x48..480 y227..281 (5-50% w, 42-52% h) | n/a | build draws both lines, 16pt, "9.8" FF0000 bold, cols ~270..600 rows ~262/280 | OK | verify-only: exact position/colors from `desc_leftblock.txt`/`desc_full.txt` |

## Notes for the fixer
- Rows 3, 5, 6, 7, 8, 11, 12, 15 are the fix triggers; rows 13–14, 18 verify-only.
- 033's certified construction (`build/slide_033.js`): param-box cell-row pattern,
  XSEP band construction with white separators, boundary-lines-only rules, cyan
  insert with maroon dashed border — copy the pattern, substitute 034 frame values.
- Do not touch house chrome (rows 1) or title runs (row 2).
- The lane may have already applied some fixes (attempt ≥ 6); re-read current build
  before editing. Re-certify per `scripts/17_worker_instructions.md` after fixes.

### TRANSCRIPT AUDIT — `desc_table.txt` banked 2026-10-25 (PIL re-verified 17:58)
Cell TEXT/contents and band/cell FILL families are usable (band1 (215,226,124) at
y345, band2 (205,170,238) at y390, band3 (249,225,199) at y440, cyan insert green
(139..149,245..248,169..175) on band-1 row only with y390 pure violet, next-x pink
(246,191,196) — all PIL-confirmed against the frame). One systematic error:
- **The transcript's outer-box coords "navy box (81,328)–(874,519)" are SHIFTED.**
  Direct probes: x81 is glyph-gray (138,137,142), x874 WHITE, y328 WHITE, y519
  whitish. Frame-true geometry (PIL, row 10 wins): dark navy verticals at x68
  (102,95,147) and x881 (37,28,93), violet-blue top rule y320/321 (94,90,164),
  dark bottom rule y517 (43,35,110). Use row 10 geometry + transcript cell grid.
- Vision fill hexes for the param box (90EE90/FFB6C1/FFFF00 in `desc_leftblock.txt`)
  are color-call approximations; task 24's PIL-sampled cell hexes (232,251,209 /
  244,190,193 / 249,253,15) win for build values — the green/pink/yellow family
  order is what the transcript usefully confirms.

### TRANSCRIPT AUDIT 2 — `desc_leftblock.txt` banked 18:03 (PIL re-verified 18:25)
High-quality read; eq box (466,170)–(600,215) red border matches row 5's PIL pin, and
it contributes NEW ground truth the table rows lacked:
- **Equation content (verbatim):** `f(x) = (x²·cos(x) − x) / 10` rendered as a BUILT-UP
  FRACTION (numerator `x² cos(x) − x`, bar, denominator `10`), black italic serif
  ≈18pt — professional-2D format per house law; feed this to the eq render sidecar.
- **Param values confirmed:** step 0.2 / initial X 7 / delta 0.1; navy border ≈#000080
  box (74,245)–(175,307), divider x≈130.
- **Subtitle L2 run split CONFIRMED by PIL x-bucket scan (y116..143):**
  `initial point` BLUE x185..304 · `and` DARK RED x305..344 · `learning rate` BLUE
  x345..464 — row 4's all-blue model refines to blue/red/blue.
- **Explanatory box** (270,252)–(597,300) green border, line 1 includes the literally
  printed `and color red bold` phrase, line 2 math tokens blue — matches row 18.
- Title read as ONE dark-red run ≈#A00000 (row 2's two-run 8B0000/C00000 split from
  the analysis record is a minor delta; both agree dark red — settle from
  `desc_full.txt` when it lands).

### TRANSCRIPT AUDIT 3 — `desc_plot.txt` banked 18:24 (PIL re-verified 18:30)
Excellent read — orange arrow (764..778,116..135) and pink label bbox (753..823,
277..301) match row 9's PIL clusters exactly; teal curve confirmed (TEAL/GREEN
n=3616 x616..830). Corrections/refinements:
- **"Two green dots side-by-side" — shape misread.** It is ONE horizontal green
  ellipse x799..816 y255..265 (n=149 green px, samples (120,214,154)/(178,255,192))
  sitting on the global-minimum flat bottom, ≈18×10px centered (807.5,260).
- **Red dashed vertical guide x783 y≈148..172** — PIL confirms (red col histogram
  peaks at x783, n=44) — row 9 gains this guide (marks the red dot's x).
- **"Gray pencil icon (826–838,146–163)"** — sparse gray pixels present, but this is
  a video-capture cursor artifact (031's frame has the same kind at (658,264));
  ground-rule (c): correctly OMITTED from recreations. Not a build element.
- Plot calibration from the read: axes cross at slide (721.5,171.5), 1 axis unit =
  9.5px, light-gray #C8C8C8 gridlines every 19px, black axes with arrowheads —
  useful for the rebuild; reconcile with `desc_full.txt` when it lands.

### TRANSCRIPT AUDIT 4 — `desc_full.txt` banked 20:07 (PIL re-verified 20:2x;
### forensics `pil_forensics_034_full.py` → `pil_forensics_034_full.txt`,
### `pil_forensics_034_full2/3.txt`)

Full-frame read banked after a wedged first dispatch (task 72). Cell VALUES, the
eq/param/explanatory text, and element inventory are usable; its COLOR calls and
several box coords are unreliable — PIL wins on every conflict below.

1. **Chrome claim "gray #D9D9D9 rect (55,38)–(905,540) with red border ALL
   sides" — WRONG.** Panel fill measures (231,233,230) ≈ E7E9E6 (deck law
   E9E9E7 family); red pixels in the top band y38..48 = 0 (deck chrome has NO
   top stroke). House chrome is never a fix target anyway (row 1).
2. **Eq box "blue #2E4FD8 border" — color misread.** Direct border probes RED on
   all four sides ((160,77,85) top / (124,34,46) bottom / (118,46,57) left /
   (129,35,49) right; red n=378, blue n=0). Row 5's RED + PIL-pinned geometry
   x465..600 y169..218 stand; built-up fraction content agrees with
   `desc_leftblock` (authority).
3. **Param box "green #00A000 border" — WRONG.** Border probes NAVY
   ((28,22,84)/(31,23,100); blue-family n=492). Row 6's navy ≈1E1856 stands.
   Fill structure: label AND value cells share the row fill — GREEN
   (235,255,211) / PINK (238,191,197) / YELLOW (247,255,5); the transcript's
   per-cell split ("row 1: green label + pink value") is wrong. Label "stop" is
   a misread of **"step"** (analysis record verbatim + `desc_leftblock` agree);
   values 0.2 / 7 / 0.1 ✓.
4. **Explanatory box line 2 "all black" — WRONG.** Blue ink n=699 in
   y280..301 — the math tokens (−10.03 / −9.92) are BLUE, matching 031's
   line-2 pattern and `desc_leftblock`; line-1 red tokens n=163 ✓; the literally
   printed "and color red bold" phrase ✓ both reads.
5. **Cyan insert rect "(628,333)–(750,371)" — SHIFTED ≈40px left.** Green-fill
   columns measure x669..789 at y340/345/350/360, none at y368, y390 pure
   violet — row 12's banked model (x≈666..790, band-1 rows only) wins. Corrected
   with the right coords, the transcript's column story is right: the insert
   covers header cells 9.6/9.8/9.6 + f(x) cells −10.03/−9.92/−10.03 =
   **data columns 13–15 (XSEP 666/707/747/787)**. Fill is the saturated
   green-cyan (135,244,178) ≈ #87F4B2 family (banked #8BF6C0/#95F6AF), not
   #CCFFCC.
6. **Slope row "data cells RED #CC4444; 3.2 in GREEN #66FF66 cells" — color
   misreads, but position right.** `desc_table.txt` §9 (2× crop, authority) +
   PIL: row bg pale green ((233,255,210)/(195,255,180) below-text; DARK-GREEN
   edge rules y459-461 / y477-478, (39..85,118..160,30..80)); 18 red-bordered
   inset boxes with SALMON fills (measured (195..206,159..170,122..134) ≈ the
   earlier (199,156,128) sample) EXCEPT **c15 and c17 pale-YELLOW #FFFFBE**
   (bright-yellow census n=451, bbox x703..832 = exactly c15/c17; zero
   #66FF66-class pixels). **This CORRECTS row 13:** the special cells are
   pale-yellow **3.2**-cells at columns **15/17** — row 13's "yellow 0.3-cells
   cols 14/16" (inherited from 033's pattern) had BOTH the value and the
   columns wrong; the build must be fixed accordingly. Slope VALUES: take
   `desc_table.txt`'s list (−4.5, −6.7, −8.7, −10.6, −12.2, −13.3, −13.9, −14,
   −13.4, −12.1, −10.1, −7.5, −4.4, −0.7, 3.2, −0.7, 3.2, −0.7) — desc_full's
   variants (−6.7 at c3/c14/c16/c18, −6.4 at c13) are the inferior full-frame
   read.
7. **Rule inventory "ONLY y354..356 + top edge" — WRONG.** Full-width thin
   rules measured (max<190, ≥600px over x80..870): y320/321 violet-blue
   (94,90,164) top rule · y330/331 gray-olive table top edge · y356 dark olive
   (82,85,6) partial density · y367 olive-gray (150,150,122) — `desc_table`'s
   pair-separator position ✓, color NOT white · y373/374 gray-violet (105,94,108)
   · y409/410 gray-violet (110,103,119) pair separator ✓ · y416-418 gray-brown
   (116,110,102) · y435 dark-peach (176,155,128) pair separator · y453/454
   gray-brown (125,117,107) pair separator ✓ · y459-461 + y477/478 DARK GREEN
   slope-row edges · y483/484 + y502 DARK RED next-x-row edges
   ((173,0,16)/(189,12,32)) · y517 navy bottom (43,35,110). Row 15's list was
   the colored subset; the between-band and within-pair separators are muted
   gray-olive/violet/brown rules, NOT white (corrects `desc_table.txt` §7's
   "thin white line" color call too). Next-x fill pink #F49B9B-family ✓
   (measured (247,190,197)/(235,171,176)); white gap y503..516 below it inside
   the frame — no extra row.
8. **Table frame "solid blue #2222CC box (66,320)–(874,522)" — shifted +
   approximate.** Frame-true (row 10): verticals x68 (102,95,147) / x881
   (37,28,93), top rule y320/321, bottom y517 — navy-violet family. Band fills
   (olive/violet/peach) and 18-column grid ≈ XSEP agree with PIL ✓; the "label
   cell darker #B8B84D" claim is an AA artifact (label (215,224,115) ≈ data
   (204,212,113) — same finding as 031's label column).
9. **Plot:** border red ✓, box ≈(608,60)–(846,310) ✓, curve dark teal ✓,
   orange arrow (763,115)→(783,143) ✓, red dot (784,148) ✓, pink label box
   "Reach"/"global Minima" ✓. Corrections: axes cross **(721.5,172)** (dark row
   y172 n=178; dark cols x721/722 — the transcript's x-axis y165 is ≈7px off;
   `desc_plot`'s calibration wins); red dashed guide columns x781..785 (peak
   x782), y148..~172 down to the axis (not y164); the "green dot circle r6
   @(800,258)" is ONE horizontal ellipse x800..815 y255..266 (n=159) —
   `desc_plot` audit 3's ellipse wins; the "pencil icon (833–846,146–170)" is
   the video-capture cursor artifact — OMIT per ground rule (c) (already ruled
   in audit 3).
10. **Title "ONE run #B22222"** — settles row 2: `desc_leftblock` (one run
    ≈#A00000) and `desc_full` agree; PIL ink census dominant r≈128–160 with
    g,b≈0–32 = ONE dark-red run ≈8B0000-family. The analysis-record two-run
    split (8B0000/C00000) is downgraded — if the build renders two dark-red
    runs the visual delta is negligible (LOW-priority polish, verbatim
    fidelity only).

Confirms without correction: subtitle L1 dark red ✓ · L2 blue/red/blue runs
(PIL n=1087/163/1118) ✓ · eq fraction layout ✓ · badge numeral 34 ✓ ·
x/f(x)/delta/next-x cell values ✓ (take `desc_table.txt` where they differ).

**All four 034 transcripts are now banked and audited; no vision item remains
pending in this pack.**

### AUDIT 4 addendum (S20c carrier — probes banked as `s20c_probe_a4_*.py`,
### console output `s20c_audit4_probes_output.txt`)

Three items outside audit 4's coverage, one index correction. Independent
probes reproduce audit 4's findings (title one-run with flat brightness
buckets (145..158, 31..38, 45..51) across x195..435 and zero green/blue ink;
param navy border (28,22,84) + full-width green/pink/yellow row fills with
white padding strips, row-1 value cell GREEN 89%/76% at y258 — the per-cell
split refuted; top-stroke red px = 0; slope pale-yellow cells x711..745 and
x785..832 = c15/c17 on the frame's ~40.7px grid).

- **Item 5 column indices: the insert covers data columns c14..c16, not
  "13–15".** Geometry decides: insert x666..790 spans c14..c16 on BOTH candidate
  grids (frame pitch 40.7 from x140: c14=669..709, c15=709..750, c16=750..791;
  033 XSEP: c14=666..707, c15=707..747, c16=747..787). Value matching alone is
  ambiguous here (the x tail 9.6/9.8/9.6 and f tail −10.03/−9.92/−10.03 repeat
  at both c14..c16 and c16..c18), so the x-column window comes from the pixels,
  and audit 4's own XSEP parenthetical (666/707/747/787) brackets c14..c16 too.
- **x-row tail + copy-shift mechanism (extends audit 4's "cell values ✓"):
  desc_full's x-row dropped the leading c1=7** — the f(x) row's 2.99 = f(7)
  anchors c1 — so its 18-value list is the true row shifted left one cell, tail
  padded from next-x. Frame-truth tail: **c14=9.6 · c15=9.8 · c16=9.6 ·
  c17=9.8 · c18=9.6** (row 16's banked fix c16/c18=9.6 stands; c17=9.8 from
  desc_full's shifted c16 plus the 9.6/9.8 bounce; `desc_table.txt`'s x-row
  ends c16=9.6 and its row tables carry only 16 of 18 columns — c17/c18 are
  unread there, not `<empty>`).
- **Plot gridline pitch: every 2 axis units (≈18–19px), not per-unit.** PIL
  census: vertical gridline columns x≈632/650/668/686/704/739.5/757.5/775.5/
  793/811/829 (step ≈18), horizontal rows y≈116/135/153/191/209/228/246/265
  (step ≈18–19); 1 unit ≈ 9.3–9.5px → `desc_plot`'s "every 19px" stands and
  desc_full's "~9–10px at each unit" is wrong. Axes cross (721.5, 172)
  re-confirmed (dark col x721/722 n≈220; dark row y172 n≈170).
