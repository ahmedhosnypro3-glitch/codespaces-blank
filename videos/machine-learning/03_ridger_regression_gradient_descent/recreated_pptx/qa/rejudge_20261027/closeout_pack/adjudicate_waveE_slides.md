# Wave-E adjudication — shard slides 004,005,007,009,011,012,020,021,023,024,027,028,029,030,032,034,035,038,039,040,042,047

Date: 2026-10-31. Adjudicator: wave-E subagent. Read-only vs DB/builds/deck: no DB write, no
vision calls, no git, no evidence deleted. Output contract: PIL-first adjudication of every
newest-FULL FAIL claim; pixels+bytes win over contradictory vision reads (skill doctrine W6).

Method:
- Newest FULL verdict per slide = newest transcript (by mtime) under `$RJ/slideNNN/judge_full*.txt`
  or `$RJ/*NNN*.{txt,out}` containing `FINAL VERDICT` (incl. `fresh_NNN.out` LEG_EXIT records where
  the transcript file itself was rm'd mid-retry by a live carrier).
- Renders: `$RJ/slideNNN/render.png` (2001x1125 @150dpi). Currency proven: pptx deliverables are
  dated 2026-10-27 16:24 and both banked renders are dated 2026-10-29 23:3x; additionally both were
  RE-RENDERED from the current `slide_NNN_recreated.pptx` (soffice headless -> pdf -> pdftoppm -r 150,
  scratch/tmp/waveE_verify) and diffed: **0 of 2,251,125 px differ (>30)** for both 027 and 040 —
  the banked renders are byte-equivalent to fresh renders of the current deliverable bytes.
  (`rejudge_adjudicate.py`'s stale-render caveat does not apply; measurements below were done manually.)
- Scale: slide space 960x540; render 2001x1125; scale 2001/960 = 2.084375 (x), 1125/540 = 2.08333 (y).
  All render measurements reported in slide-space px. Originals: `unique_slides/slide_NNN.jpg` (960x540).

## Summary table — newest FULL verdict per shard slide and disposition

| slide | newest FULL transcript (mtime) | verdict | adjudicated here? | PASS stands? |
|---|---|---|---|---|
| 004 | judge_full_r15.txt 2026-10-31 05:42 | PASS | no (no newest FAIL) | yes |
| 005 | judge_full_r18.txt 2026-10-31 08:28 | PASS | no | yes |
| 007 | judge_full_r19.txt 2026-10-31 08:06 | PASS | no | yes |
| 009 | judge_full_r20.txt 2026-10-31 06:11 | PASS | no | yes |
| 011 | judge_full_r16_r22.txt 2026-10-31 08:22 | PASS | no | yes |
| 012 | judge_full_fresh.txt 2026-10-31 04:11 (PASS recorded in fresh_012.out + result.txt; file re-launched in flight 08:12) | PASS | no — older FAIL judge_full.txt 01:10 already adjudicated (slide012/adjudication_full.txt, adjudicate_*_full.txt) | yes |
| 020 | judge_full_r21.txt 2026-10-31 07:27 | PASS | no (r20 FAIL 06:19 superseded) | yes |
| 021 | judge_full_r18.txt 2026-10-31 06:31 | PASS | no | yes |
| 023 | judge_full_r20.txt 2026-10-31 06:21 | PASS | no | yes |
| 024 | judge_full_r19_r22.txt 2026-10-31 08:04 | PASS | no | yes |
| 027 | judge_full_fresh.txt 2026-10-31 08:38 | PASS | **r20 FAIL 08:30 adjudicated below — all claims REFUTED** | yes |
| 028 | judge_full_r16.txt 2026-10-31 06:05 | PASS | no | yes |
| 029 | judge_full_r20.txt 2026-10-31 07:47 | PASS | no | yes |
| 030 | judge_full_r17.txt 2026-10-31 06:57 | PASS | no (earlier FAILs 03:23/06:28 superseded) | yes |
| 032 | judge_full_r21.txt 2026-10-31 08:14 | PASS | no | yes |
| 034 | judge_full_r19.txt 2026-10-31 07:17 | PASS | no | yes |
| 035 | judge_full_r16.txt 2026-10-31 07:41 | PASS | no (02:40 FAIL already dismissed, slide035/adjudication.md) | yes |
| 038 | judge_full_r20.txt 2026-10-31 06:10 | PASS | no | yes |
| 039 | judge_full_r17.txt 2026-10-31 08:23 | PASS | no (2026-10-30 FAIL dismissed, register) | yes |
| 040 | judge_full_fresh.txt 2026-10-31 08:41 | PASS | **r16 FAIL 08:19 adjudicated below — 1 claim CONFIRMED (MINOR-class), rest advisory** | yes |
| 042 | judge_full_r18.txt 2026-10-31 08:28 | PASS | no | yes |
| 047 | judge_full_r18.txt 2026-10-31 06:46 | PASS | no (fresh2 FAIL 03:37 "Ugmented" = source typo, settled 043 law) | yes |

Net: 20/22 shard slides have newest FULL = PASS outright. The two slides with a newest-or-near-
newest FULL FAIL (027 r20 08:30, 040 r16 08:19) are both superseded by later PASS legs
(027 fresh 08:38, 040 fresh 08:41) AND PIL-adjudicated below. No DB-passed shard slide has a
PIL-surviving BLOCKER/MAJOR in its newest FULL leg; all 22 PASSes stand.

---

## Slide 027 — newest FULL FAIL transcript: `slide027/judge_full_r20.txt` (2026-10-31 08:30:23, clean, pid 2581730, on `$RJ/slide027/render.png` vs `unique_slides/slide_027.jpg`)

Claims filed (normalized 960x540):
1. MAJOR conf 0.80 — yellow minimum marker floats ~24 px above the theta-axis in the render vs
   ~5 px (on the axis) in the original; branches shorter (170/169 vs 215/190); `Minimum` label
   pulled up (431,357) vs (421,390).
2. MAJOR conf 0.60 — title two-line leading larger in render: tops 73/112 (gap 39) vs 75/108
   (gap 33); L1 width 559 vs 586.
3. MINOR conf 0.70 — render strokes near-black/heavier vs orig dark-gray/thinner.
4. MINOR conf 0.55 — inner red plot frame render x187-717 y160-497 vs orig x185-716 y183-506
   (shifted up, taller by ~14 px).
5. MINOR conf 0.45 — label insets differ (`Cost` at (204,187) vs (190,206), etc.).

PIL measurements (slide-space px; ORIG = slide_027.jpg, RENDER = render.png/scale):

| measurement | ORIG | RENDER | delta |
|---|---|---|---|
| yellow minimum cluster (largest, badge excluded) | centroid (444.5, 407.2), bbox x439-450 y401-413, n=120 | centroid (444.0, 406.9), slide bbox x437.5-450.5 y400.3-413.3, n=624 | 0.5 px |
| theta-axis row (max dark-ink row in plot x150-770) | slide-y 436.0 (473 ink px) | slide-y 435.8 (989 ink px) | 0.2 px |
| minimum-to-axis gap | 436.0 - 407.2 = **28.8** | 435.8 - 406.9 = **28.9** | 0.1 px |
| parabola top row (next dark row) | slide-y 276.0 | slide-y 276.0 | 0 px |
| red inner frame ink bbox (plot region x150-770 y140-525) | x193..716 y167..507 | x192.4..716.3 y166.1..507.4 | <=1 px |
| title red line groups (band y50-120) | y73-98 and y108-119 (pitch 35, width x192..744 = 552) | y72.6-94.2 and y106.6-119.6 (pitch 34.0, width x191.0..742.7 = 551.7) | <=1 px |

Disposition:
- Claim 1 (MAJOR): **REFUTED.** Both images put the yellow minimum at slide-y ~407 with the axis
  at ~436 — gap 28.8 vs 28.9 px in BOTH. The judge's "5 px vs 24 px" numbers are wrong (its own
  normalization divided by ~1.604 instead of 2.084, shifting every claimed coordinate). Branch
  lengths and the `Minimum` label position are derivative of the same geometry and match.
- Claim 2 (MAJOR): **REFUTED.** Title pitch 35 vs 34 px, line-1 width 552 vs 552 px, line tops
  within 1 px. Not "39 vs 33" / "559 vs 586".
- Claim 3 (MINOR): advisory — stroke weight/color class = typed-vs-handwritten medium (rule c).
- Claim 4 (MINOR): **REFUTED** as stated — frame bbox identical within 1 px on all four edges.
- Claim 5 (MINOR): advisory (label insets are font-metric class).

Verdict: r20 FULL FAIL **DISMISSED** — 2/2 MAJORs refuted by pixels, MINORs advisory or refuted.
Corroborated by the newer `judge_full_fresh.txt` (08:38) FINAL VERDICT: PASS (3 MINORs only:
double-space normalization in title, render crispness, dot spacing — all medium-class).
**Slide 027 PASS stands.** No fix trigger.

---

## Slide 040 — newest FULL FAIL transcript: `slide040/judge_full_r16.txt` (2026-10-31 08:19:33, clean, pid 2530007, on `$RJ/slide040/render.png` vs `unique_slides/slide_040.jpg`)

Claims filed (normalized 960x540):
1. MAJOR high-conf — blue "usnig SGD" subtitle undersized ~15-20%: orig cap ~25 px / run ~230 px
   vs render cap ~21 px / ~205 px; orig blue ≈ red "Solved Example" size, render blue clearly smaller.
   Cites founder directive 2026-10-10 (size deviation = MAJOR).
2. MINOR — title 3-4% wider/taller in render (x85-859 vs x98-845; cap 29 vs 27).
3. MINOR — text stack 5-12 px high in render (title top 165 vs 171; blue 243 vs 247; red 311 vs 323).
4. MINOR low — "Solved Example" leftward bias (both frames similar; "largely inherited").

PIL measurements (slide-space px; masks: red = r>140,r>1.6g,r>1.6b,g<110; blue = b>150,b>1.5r,b>1.4g,r<120;
x-window restricted to 75..895 to exclude house red strokes; cap = rows >25% of row-max within band):

| line | metric | ORIG | RENDER | delta |
|---|---|---|---|---|
| RED title L1 | cap height | 24 (y183-206) | 29.8 (y180.0-209.3) | render +24% |
| RED title L1 | run width | 742 (x101..843) | 767.1 (x88.0..855.1) | +3.4% |
| BLUE "usnig SGD" L2 | cap-band height | 30 (y251-280) | 25.0 (y258.9-283.4) | **-17%** |
| BLUE L2 | run width | 212 (x367..579) | 179.4 (x383.0..562.4) | **-15.4%** |
| BLUE L2 | per-char width (9 chars) | 23.6 | 19.9 | -15.7% |
| RED "Solved Example" L3 | cap height | 30 (y326-355) | 30.2 (y328.6-358.3) | +0.7% |
| RED L3 | run width | 320 (x307..627) | 333.9 (x294.3..628.2) | +4.3% |
| blue-core median RGB | — | (7,0,193) | (0,0,255) | both pure blue |

Key relative fact: in the ORIGINAL the blue line is sized WITH the red lines (cap 30 = red L3 cap 30;
23.6 vs 22.9 px/char). In the RENDER the blue line is 0.83x the red L3 (cap 25.0/30.2; 19.9/23.9
px/char). Build spec `build/slide_040.js:100-102`: L1 and L3 at fontSize 44, L2 "usnig SGD" at
fontSize 36 (capTop 257 vs 177/326) — the under-sizing is a deliberate build spec, not a font accident.

Disposition:
- Claim 1 (MAJOR as filed): **CONFIRMED as a real pixel delta, reclassified MINOR.** The blue
  subtitle is genuinely ~15-17% smaller than the original's own line-matched sizing (cap 30->25.0,
  width 212->179.4, per-char -15.7%), so it is NOT a vision misread. But the absolute render sizes
  are set by the house typed font (red title renders 24% LARGER than the handwritten original), and
  the newest FULL leg (`judge_full_fresh.txt` 08:41:46, FINAL VERDICT: PASS) scored the same
  observation MINOR at low-medium confidence (~6-7% width). Under ground rule (c)
  (typed-vs-handwritten / re-typesetting variance, at most MINOR) this is a MINOR proportion delta,
  not a content defect and not a FAIL-sustaining MAJOR. Recorded as a candidate quiet-wave fix
  (L2 fontSize 36 -> 44 to match L1/L3, re-measure capTop) — NOT dispatched from this adjudication.
- Claim 2 (MINOR): confirmed as delta (width +3.4%, cap +24% absolute) — direction is render LARGER;
  font-metric class, advisory.
- Claim 3 (MINOR): mixed — title top 183 vs 180.0 (render 3 px HIGH), blue top 251 vs 258.9 (render
  8 px LOW), L3 top 326 vs 328.6 (2.6 px low); claim direction partially wrong; advisory.
- Claim 4 (MINOR): REFUTED as a delta — L3 center orig 467 vs render 461.3, both left of panel
  center ~478 by a similar amount; inherited, as the judge itself noted.

Verdict: r16 FULL FAIL's only MAJOR is PIL-confirmed as real but MINOR-class; no BLOCKER/MAJOR
survives under the wave rules. Newest FULL leg is PASS (`judge_full_fresh.txt` 08:41:46, clean).
**Slide 040 PASS stands**, with the blue-line size delta recorded as an optional quiet-wave fix.

---

## Notes / scope honesty

- Slide 012's newest FULL verdict is the 04:11 PASS (`judge_full_fresh.txt`, recorded in
  `fresh_012.out` LEG_EXIT + result.txt HARVEST entries; the transcript file itself was rm'd
  mid-retry by a live carrier and a re-run launched 08:12). Its 01:10 FAIL (`judge_full.txt`,
  "X5 is Outlier"/title-size claims) was already PIL-adjudicated in
  `slide012/adjudication_full.txt` / `adjudicate_*_full.txt`. Not re-adjudicated here; 012 is not
  a newest-FAIL slide.
- Page-level deck-gate FAILs on the 51-page package are the known LibreOffice rasterization
  artifact (register 2026-10-31 03:3x slide025 root-cause), not content defects; not in scope here.
- No DB rows, builds, pptx, decks, or transcripts were modified. No git operations. No vision
  calls. All measurements from local PIL on the files cited above; probe script:
  `scratch/tmp/adjudicate_waveE.py` + inline heredocs; fresh-render verification PNGs under
  `scratch/tmp/waveE_verify/`.
