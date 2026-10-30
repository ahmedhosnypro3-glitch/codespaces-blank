# S20c pre-phase — slide 031 build readiness checklist

Companion to `delta_vs_related.md` (row numbers below reference that file's table).
Basis: frame ground truth (`unique_slides/slide_031.jpg`), certified 032 construction
(`build/slide_032.js`), build as read 2026-10-25 (`build/slide_031.js`, re-render
`qa/slide031/render_cur.png`). **2026-10-25 18:55: all four S20c transcripts have
landed in `orig_judges/`; every [VISION-PENDING] item below is now settled in the
TRANSCRIPT AUDIT sections (1–5) of `delta_vs_related.md` — read those first; the
audited transcript claims override the unaudited ones.**

## Preflight (before any fix)
0.1 Re-read the CURRENT `build/slide_031.js` and current deliverable pptx — the S5
    cert lane is actively working 031; only deltas still present are actionable.
0.2 031's lane terminated degenerately 2026-10-24; the three banked FAIL verdicts
    (attempts 1/2/4) were judged against superseded builds — ignore them as fix
    targets; the current re-render is the only valid comparison surface.
0.3 Never write into the lane's dirs or dispatch judge legs; this checklist is the
    fix map, not a fix authorization.

## Build actions (delta row → action)
**All items below are SETTLED (2026-10-25 18:55–18:52 transcript audits 1–5 in
`delta_vs_related.md`); no [VISION-PENDING] remains. Values inline here; the
audit sections hold the full evidence.**
1. **Row 5 — main table (THE dominant fix).** Rebuild to the frame's real
   structure per `desc_table.txt` + `desc_full.txt` + AUDIT 2/4: navy/indigo
   outer frame x64..894 (top ≈y334..336, bottom y529/530, #1F1E7C..#3F3D90);
   ~18 data columns at ≈42px pitch, boundaries x≈135,177,…,895 (label col
   x75..≈135); band fills x/f(x) yellow-green #C4D96C, next-x pink #F3A6A0
   (families olive/violet/peach/green/pink per row 6) as BANDS separated by
   white gap rows; NO full-height black grid — thin dark-gray boundary ticks
   rows 1–6, GREEN ticks in the slope row, RED ticks in the next-x row
   (red verticals x177/x219 y500); build right edge must NOT exceed the panel
   (drop the current x943 overshoot). Cell values from `desc_full.txt`
   (x: 3,3.3,…,4.8,5.1; f(x): …,1.04,1.01,1.04,1.01,…) — values are ground
   truth, its structure model is not.
2. **Row 3 — typeface (SETTLED).** Title is BOLD SERIF (Times-like) — adopt
   032's serif treatment for the title, eq math (serif italic), and the
   annotation lines; param-table and main-table text read bold sans
   (Arial-like) — keep sans there.
3. **Row 4 — param table (SETTLED).** Label AND value cells share per-row
   fills: GREEN EFFFD9 / PINK F4C4C4 / YELLOW FCFF1D (yellow 3rd value cell —
   NOT gray); box x≈90..217 y176..250 with steel-blue row dividers + divider
   column x≈164; values 0.3 / 3 / 0.1.
4. **Row 8 — plot box (SETTLED).** Red border, box x573..809 y66..309 (fix the
   build's bottom y267 → 309); gray axes x631 / y266 (#969897-family).
5. **Row 12 — annotation box (SETTLED).** Box x≈243..570 y≈241..289 (PIL
   x243..566 y243..289; topblock x245..574 y241..288 — AA-level agreement),
   GREEN ≈45873F borders ALL sides, pale green #EFFCE2 fill. Runs (audit 3.2):
   line 1 `X`(red bold) ` is in between ` `4.8`(red bold) ` and color red bold `
   `5.1`(red bold) — the phrase "and color red bold" is LITERALLY printed;
   line 2 `f(x)`(blue bold) ` is in between ` `1.04`(blue bold) ` and `
   `1.01`(blue bold).
6. **Row 13 — arrows/labels (SETTLED, audit 3.3 + audit 4).** Red block arrow
   HOLLOW (red outline, white fill) pointing DOWN-LEFT (176,312)→(152,342);
   FOUR HOLLOW blue down-arrows (light-blue fill, dark-blue outline) at
   x≈403/439/476/518, y≈310..342; pink "Bouncing" label box (303,296)–(392,323),
   pink fill + purple-magenta text; NO 032-style wide pink band.
7. **Row 10 — curve (SETTLED).** Reuse `build/assets/curve_032.png/json`
   (steel-blue-gray family PIL-confirmed; #0066CC/#4472C4 reads were color
   misreads). Geometry from `desc_graph.txt` (audit 5): vertex (683,252)=(5,1),
   branches exit top (640,58)/(737,58); chord black ~3px (649,145)→(717,145);
   black end-dots (650..655,143..149)/(711..723,143..150); red dot
   (658..663,180..186); ONE horizontal green ellipse x678..699 y248..256 on the
   vertex (not two dots); plot text: `(2, 10)` (629..656,148..158) · `(?, ?)`
   (722..748,139..150) — the analysis record's "(7,9)" was a glyph misread,
   verify the crop before drawing · `(5, 1)` (700..724,247..257); purple `3`/`3`
   distance marks ≈(670,134)/(703,134); cursor artifact at (665..673,264..274)
   — omit, ground rule (c).
8. **Rows 9, 11, 14 — verify-only (SETTLED).** Calibration: 0 at (626,264),
   11.5 px/unit x / 11.8 px/unit y — 032's 11.5 scale reuse OK; probe the axis
   column during the fix (origin 626 vs 032's 630.5). Dashed red x=5 guide:
   x659..663 ONLY (the "x≈684 symmetry axis" claim was pattern-completion; no
   red column at 684). Eq box PIL-pinned x399..529 y186..211, RED border all
   sides (topblock independently confirms) → reuse `eq_032_main.png/json`
   (same formula f(x)=(x−5)²+1, same certified style); update the sidecar copy
   for 031.

## Reusable certified assets
- `build/assets/house_chrome.js` + `house_chrome_check.py` (chrome, row 1).
- `build/assets/eq_032_main.png/json` (row 14 — PIL-pinned geometry match).
- `build/assets/curve_032.png/json` (row 10 — PIL-confirmed color family).
- 032's `build/slide_032.js`: title-run construction, param-table construction,
  plot calibration constants, serif type treatment (actions 2, 3, 8).

## Closeout
9. After any fix: re-render, re-run `house_chrome_check.py`, re-certify per
   `scripts/17_worker_instructions.md`. Per-slide re-certification is mandatory.
