# adjud_a27_improvised_s4b.md — adjudication of the payload-less attempt-27 judge (S4b carrier, 2026-10-26)

## What happened

`dispatch_A27_1200.sh` was staged with a **filename typo**: it read
`judgeA8_payload_20271024.txt` (2027) while the banked payload is
`judgeA8_payload_20261024.txt` (md5 9387f5fbb94ef05a31db19f1e018dde1, byte-verified
vs `shared_patterns/judge_protocol_03.md` Template A). `P="$(cat ...)"` therefore
came up EMPTY and the leg dispatched with `-p ""` — the judge never saw the frozen
Template A. It improvised a "Fidelity Check Report" (transcript banked as
`judge_attempt_27.txt`, NOT overwritten): no `FINAL VERDICT:` line, verdict-in-its-
own-format "HIGH FIDELITY (~92%)". Per protocol a payload-less run cannot produce a
certifiable verdict — it does not count as a judge attempt (same rule as the attempt-8
hang/504 dispatches). The corrected dispatch is **attempt 28**
(`judge_attempt_28.txt`, payload md5 + len logged in `legs_status_27_s4b.md` at
04:46:42Z). Both dispatch scripts (A27/B27) were fixed to `20261024` and given a
fail-loud guard (`[ -s "$PAYF" ] || exit 3`) so an empty payload can never dispatch
again.

## Adjudication of the improvised report's findings (PIL-first; nothing fixed blind)

| # | Finding (improvised, payload-less) | Disposition | Evidence |
|---|---|---|---|
| 1 | `"22" tag color — original: black text on yellow; recreation: green` (3 instances) | **REFUTED** | `pil_adjud_a27findings.py` (log `scratch/tmp/pil_adjud_a27findings.log`): orig "22" ink inside all three yellow patches is GREEN (darkest-quartile core RGB ≈ (123,179,26) row 1, (128,184,33) row 2, (123,179,30) row 3 — green-dominated; JPEG chroma wash explains the olive tint at 1px glyph strokes). Render_27 ink = (0,128,0) = the build's `008000`. Patch geometry matches sub-pixel (orig x76..115 vs render x75.8..115.6). The build's GREEN spec is correct; crop_17's judge also read the orig 22 as green. |
| 2 | Global scale ~15–20% larger type; shrink fonts | **REFUTED (class)** | Probe geometry (`pil_clusters_26b.py` + `pil_probe_26.py` banked): all 9 outlier digit bboxes d≤3 at tol 4, s_sub d≤2.2, patches/arc tips align — a 15–20% scale error would produce far larger deltas. Recurring cosmetic claim; earlier Template A judges rate the same class MINOR-at-most. |
| 3 | Matrix parentheses thicker/oversized | **Not a defect (class)** | Delimiter geometry was adjudicated in earlier waves (attempt-8 adjudications; A24: "all delimiters that ARE rendered … span their full enclosed lines with correct curvature"); the outlier-pair delimiters were rebuilt to orig ink extents (pair-span fix, triple-verified). |
| 4 | Extra horizontal navy rule above header row; orig has none | **REFUTED as a fix trigger** | Same element read by `crop_23_header_strip_judge.txt` (FINAL VERDICT: PASS, on whose pass this region's carry decisions rest): "IMG1 uses a continuous navy rule across the top of the strip" — graded MINOR (first-cell boxing nuance) inside a PASS. The rule is the build's measured grid-outer rect (a21 mapping, `pil_grid_rules_a21.py`). |
| 5 | Page badge "19" larger with heavier border | **House chrome — overridden** | Badge geometry is house-fixed per deck AGENTS.md (circle d≈35px at (876,73), FDFD96 + 6A5ACD ring); judge discrepancies about house chrome are never fix triggers. |
| 6 | Header weight larger/bolder | **Not a defect (class)** | Same class as #2; earlier waves graded it MINOR-at-most; header strip carries a PASS at crop_23 on near-identical bytes (region changed only in the arc-tip zone y180..193, 1540 px). |
| 7 | Mouse cursor in IMG2 | Non-finding | Ground rule (c) — video artifact, correctly omitted. |

## Net effect

- **No build change.** render_27 (arc-pair-span fix) stands as the judge target.
- A27's improvised transcript is banked as evidence of the empty-payload incident;
  the cert verdict comes from attempt 28 (protocol payload).
- `crop_27_header_strip`'s fresh judge (region changed 1540 px vs crop_23 bytes) and
  `crop_27_table_left` (9008 px, arc zone) proceed per task #86;
  `crop_27_noreg_rows` and `crop_27_table_right` carry/judge per
  `diff_23_26_carry.md` (noreg_rows crop_23 PASS carries — region byte-identical;
  table_right has no cert → fresh).
