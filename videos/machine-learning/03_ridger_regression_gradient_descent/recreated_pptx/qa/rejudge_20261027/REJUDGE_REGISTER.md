# Rejudge wave — evidence register (append-only)

Deck: videos/machine-learning/03_ridger_regression_gradient_descent (Ridge Regression & Gradient Descent)
Wave: rejudge_20261027 — fresh vision reads over ALL certified slides per the 2026-10-27 directorate:
"rejudge all certified slides, reanalyze them visually again". Each slide needs BOTH legs clean:
FULL = full-slide Template A comparison vs the original frame; CROP = zoomed crop-pair Template B over
the densest content region at matched effective scale (AGENTS.md zoomed-judge mandate).

Execution: detached drivers `rejudge_driver.sh` (setsid/nohup, one per scope), payloads byte-for-byte
from recreated_pptx/shared_patterns/judge_protocol_03.md (md5 8fc119623b1f020c6d135c834969bf75 for
Template A), adjudication helper `rejudge_adjudicate.py` (PIL diff, slide-space px).

Rule: every FULL/CROP FAIL is PIL-adjudicated (rejudge_adjudicate.py + targeted measurements) before
any slide is reopened; a vision claim refuted by pixels is DISMISSED and recorded here as such.
No slide is re-certified or un-certified on prose alone.

## Certified set (44 slides) — rejudge status

| slide | FULL | CROP | notes |
|---|---|---|---|
| 004 | PASS | pending | full verdict banked 2026-10-27 22:5x (clean transcript) |
| 007 | PASS | pending | full verdict banked; one MINOR ("linearly" not bolded) — advisory |
| 022 | PASS | pending | full verdict banked (clean) |
| 026 | PASS | pending | full verdict banked (clean) |
| 029 | PASS | pending | full verdict banked (clean) |
| 001 | pending | pending | driver R01 in flight |
| 002 | pending | pending | driver R01 in flight |
| 003 | pending | pending | driver R01 in flight |
| 010 | pending | pending | driver R04 in flight |
| 011 | pending | pending | driver R04 queued |
| 012 | pending | pending | driver R04 queued |
| 013 | pending | pending | driver R05 in flight (dependency parent of 17) |
| 016 | pending | pending | driver R05 queued |
| 017 | pending | pending | driver R05 queued (13>12 chain) |
| 018 | pending | pending | driver R06 in flight (17>13 chain) |
| 020 | pending | pending | driver R06 queued |
| 021 | pending | pending | driver R06 queued — watch task-129 (eq_021 underbars) |
| 023 | pending | pending | driver R07 queued |
| 024 | pending | pending | driver R07 queued |
| 027 | pending | pending | driver R08 queued |
| 028 | pending | pending | driver R08 queued |
| 030 | pending | pending | driver R09 queued |
| 031 | pending | pending | driver R09 queued |
| 032 | pending | pending | driver R10 in flight |
| 033 | pending | pending | driver R10 queued |
| 035 | pending | pending | driver R10 queued |
| 036 | pending | pending | driver R11 in flight |
| 037 | pending | pending | driver R11 queued |
| 038 | pending | pending | driver R11 queued |
| 039 | pending | pending | driver R12 in flight |
| 040 | pending | pending | driver R12 queued |
| 041 | pending | pending | driver R12 queued |
| 042 | pending | pending | driver R13 in flight |
| 045 | pending | pending | driver R13 queued |
| 046 | pending | pending | driver R13 queued |
| 047 | pending | pending | driver R14 in flight |
| 049 | pending | pending | driver R14 queued (OMML wrap missing at S9) |
| 050 | pending | pending | driver R14 queued (OMML wrap missing at S9) |
| 051 | pending | pending | driver R15 in flight |
| 034 | pending | pending | driver R16 in flight |

## Open slides (not certified — rejudge applies after certification)

014 (att10 subagent), 015 (leg on unchanged bytes), 019 (2 PIL MAJOR claims), 025 (att14 legs staged),
043 (small fix), 044 (rebuild+judge), 048 (attempt 17 dispatched 2026-10-28 04:55 UTC).

## Harvest sweep 2026-10-30 21:45 UTC (drivers relaunched; verdicts from banked transcripts)

| slide | full leg | crop leg |
|---|---|---|
| slide001 | PASS | PASS |
| slide002 | PASS | PASS |
| slide003 | — | — |
| slide004 | PASS | PASS |
| slide005 | — | — |
| slide006 | PASS | PASS |
| slide007 | PASS | PASS |
| slide008 | PASS | PASS |
| slide009 | PASS | PASS |
| slide010 | PASS | — |
| slide011 | PASS | PASS |
| slide012 | — | — |
| slide013 | — | — |
| slide016 | FAIL | PASS |
| slide017 | — | — |
| slide018 | — | — |
| slide020 | PASS | PASS |
| slide021 | FAIL | PASS |
| slide022 | PASS | PASS |
| slide023 | PASS | — |
| slide024 | PASS | FAIL |
| slide026 | PASS | FAIL |
| slide027 | PASS | PASS |
| slide028 | FAIL | — |
| slide029 | PASS | PASS |
| slide030 | — | — |
| slide031 | PASS | — |
| slide032 | — | — |
| slide033 | — | — |
| slide034 | — | — |
| slide035 | — | — |
| slide036 | — | — |
| slide037 | PASS | — |
| slide038 | PASS | PASS |
| slide039 | FAIL | PASS |
| slide040 | PASS | FAIL |
| slide041 | FAIL → DISMISSED | — | PIL-adjudicated 2026-10-30, see Adjudications below + slide041/adjudication.md |
| slide042 | — | — |
| slide045 | — | — |
| slide046 | — | — |
| slide047 | — | — |
| slide049 | — | — |
| slide050 | — | — |
| slide051 | — | — |

## Adjudication 2026-10-30 — slide039 FULL FAIL (read-only; details in slide039/adjudication.md)

FAIL transcript: `slide039/judge_full_retry.txt` (banked 2026-10-30 00:21; `judge_full.log` empty,
`judge_full.txt` never written — driver died on grep miss/syntax error, retry is the banked verdict).
CROP leg PASS (`crop_dense_judge.txt`). PIL-adjudicated vs `slide039/render.png` (2001x1125 @150dpi,
scale 2.0833) vs `unique_slides/slide_039.jpg`; chrome_check PASS; eq_039_main.json + OMML wrap
(AlternateContent/oMath in slide1.xml) verified present and consistent with the black-ink render.

| claim | filed | disposition | key measurement (slide-space px, core ink medians) |
|---|---|---|---|
| 1 title line-break after "and" vs after "SGD)" | MAJOR | REFUTED | both 2 title bands (orig y62.2/108.3, rend y64.1/109.7); L1 ends x839/x834 at ")", L2 starts x279/x281 with "and" |
| 2 title L2 color (orig all-blue vs rend red "Gradient Descent") | MAJOR | REFUTED | orig L2 runs: and (161,40,53) red, Mini-Batch (25,17,137) navy, Gradient Descent (158,40,53) RED; rend (192,0,0)/584CA8/(192,0,0) — same scheme; residual blue-hue shift MINOR |
| 3 eq box white+dark border, caption green | MAJOR | REFUTED | box fill orig (223,255,238) = rend (225,255,239) light green; border green both ((89,129,76) rend); caption core orig (167,64,69) = rend (192,5,4), both RED |
| 4 blue/underlined emphasis in Why-SGD bullets | MAJOR | REFUTED | orig B4/B5 cores (84,84,84)/(80,81,80) black; 0 blue ink px in x94-700 y330-380; below-text 32/65 px = descenders only; rend black |
| 5 "GD and SGD" black in orig, blue-purple in rend | MAJOR | REFUTED | orig x347-454 y409-425 core (151,54,67) RED = rend (192,0,0) RED; rest of caption black both |
| 6 double space "gradient  of" | MINOR | CONFIRMED (advisory) | orig gap gradient→of 11.03px ≈ 2x normal (5.3-6.7px); rend 5.76px single |
| 7 heavier/larger title+body in rend | MINOR | REFUTED | glyph extents within ≤1px (title L1 ~40.8 vs 40.3px, L2 19.7 both, B1 18.2 vs 17.3, cap 18.2 vs 17.3) |

Verdict: FULL FAIL DISMISSED — 6/7 claims refuted by pixels, 1 MINOR confirmed (double space,
advisory). No BLOCKER/MAJOR survives; CROP was PASS; slide 039 stays certified, no reopen, no fixes.
Vision re-read leg skipped: gate busy (pgrep analyze_image.py = 28 >= 8, all slide014 fleet calls).

## Adjudication 2026-10-30 — slide024 CROP FAIL (crop_dense_judge.txt)

- **Claim 1 (MAJOR: title missing "Gradient", heading block shifted left): REFUTED.** Ground truth: `build/slide_024.js:54` TITLE = "Gradient Descent (GD)"; `analysis/slide_024_final.json` slide_title = "Gradient Descent (GD)". PIL red-ink measurement, title band y 222..270: ORIG 3 word clusters x 242..423 / 440..609 / 625..718 (w 182/170/94); RENDER (scale 2.0844) x 240.4..422.2 / 438.5..609.3 / 624.6..717.7 (w 182.3/171.3/93.6) — "Gradient" present at identical geometry. In the crop pair both crops' title-band leftmost ink is crop x≈31 (slide x≈439, the "D" of "Descent"); crop x 0..30 is background in the render and only the antialiased edge of that same "D" in the orig — no clipped glyph fragments exist. Title-band ink-column IoU = 0.94. One gate vision leg (title-band zoom, matched scale 1250×141, transcript slide024/title_band_vision.txt) independently reads both as "Gradient Descent (GD)", verdict PASS. DISMISSED per register rule.
- **Claim 2 (MINOR: red tone): CONFIRMED as MINOR/advisory** — not a content defect, not a fix trigger.
- Net: slide024 crop_dense FAIL **overturned**; certification stands; no fix dispatched. Detail: `slide024/adjudication.md`.


## Slide 048 attempt-17 crop-leg adjudication (2026-10-30, PIL-first, render_17 vs unique_slides/slide_048.jpg, scale 2001/960, 1125/540)

Evidence: `scratch/tmp/adjudicate_048_att17_out.txt`, `adjudicate_048_zglyphs*_out.txt` (scripts in scratch/tmp).

| leg | claim | verdict | pixel evidence |
|---|---|---|---|
| top_band #1 | "Initial W =" label on wrong side of vector | **REFUTED** | orig ink vector zone x330-356 y55-105 = 368 px, label zone x360-430 = 668 px — original also has vector LEFT, label RIGHT, same as build (consistent with att-16 refutation, orig digits x338-349) |
| top_band #2 | Z headers Z1 Z2 Z3 vs orig Z1 Z1 Z1 | **CONFIRMED** | orig Z-subscripts mutually identical (best-shift xor 3/4/6 px); each best-matches handwritten "1" vs large-digit templates from same frame (scores 27/28/23 for '1', next-best 28/29/24); render subs distinct (xor 10-30). Fixed build to Z1 Z1 Z1 |
| top_band #3 | delimiter bars vs parens | REFUTED (exempt) | delimiter geometry is a template/rule-(e) item; dbar width 1 already att-17 patched |
| top_band #4 | REPEAT red vs black | **REFUTED** | orig REPEAT box x426-576 y60-76: red=513 px vs dark=143 px — original REPEAT is red, build matches |
| top_band #5 | missing vertical rules in Z table | REFUTED | orig ink x636-706 y84-118 is scattered digit ink (6-54 px per 2px col), no full-height rule columns |
| top_band #6 | row-2 parens added | **REFUTED** | orig row2 y96-108 paren-edge ink (L 0-8, R 0-9 per cell) matches row1 control y77-89 (L 0-9, R 0-11) — original row 2 IS parenthesized |
| top_band #7/#8 | X-case, C-subscript baseline | REFUTED (exempt) | typed-vs-handwritten / subscript rendering = ground-rule non-discrepancies |
| aug_iter #1 | red emphasis on 4 aug row-2 digits | **CONFIRMED** | orig aug row-2 cells y196-210: red=0 in ALL six cols; render red=162/162/191/179 in cols 1,3,4,5. Same false-red found in top table row1 col1 (render red=162, orig 0) and row2 cols 2-5 (render 163-179, orig 0). Fixed: all these digits now BLACK in build/slide_048.js |
| aug_iter #2-6 | missing "=" at crop edge, badge serif, title weight, delimiter width, panel shift | REFUTED (exempt) | crop-edge/styling/typed-vs-handwritten items per ground rules |

Post-fix build changes (slide_048.js): Z header array -> ["Z1","Z1","Z1"]; top-table row1/row2 digit colors -> all BLACK; aug-box row colors -> all BLACK. Rebuild + re-render as render_18, chrome-check, crop legs re-run.

## Adjudication 2026-10-30 — slide028 FULL FAIL (judge_full_retry.txt)

- **Claim 1 (MAJOR: inner plot regions proportioned differently — original's right region wider, "Value of weight" termini close together at center, recreation made regions equal-width with larger central gap): REFUTED.** PIL slide-space measurements, ORIG vs RENDER: left plot width 269 vs 269.6 px, right plot width 268 vs 269.6 px (in the ORIGINAL the right is 1 px NARROWER, not wider — ratio 1.004 vs 1.000); central gap (left x-tip -> right y-axis) 84 vs 82.5 px; "Value of weight" labels x 366..454 / 711..799 (orig) vs 367.5..453.9 / 711.5..797.8 (render); y-axes x 158/511 vs 157.4/509.5; x-axes x 158..427 / 512..779 vs 159.8..427 / 508.5..779.1; headings, title, teal curve bboxes, blue frame all within <=1.5 slide px. `rejudge_adjudicate.py 028 --full`: densest diff cells all in text/badge bands (title y67-90, labels y427-472, headings y180-202, badge y67-90), none inside plot interiors. No original-side asymmetry exists to reproduce. DISMISSED per register rule.
- **Claim 2 (MINOR: small-LR staircase floor closer to x-axis in recreation): CONFIRMED in direction, magnitude 1.0 slide px** (floor gap above axis top: orig 2.0 px vs render 0.9 px; right plot 2.0 vs 1.0) — matches the transcript's own "cosmetic only"; below AA/JPEG noise, not a fix trigger.
- Transcript MATCH rows corroborated (chrome_check PASS; containment: right rise tip 121 px clear of frame right edge in both). Optional gate vision re-read leg skipped: `pgrep -c -f analyze_image.py` = 26 (>= 8, wave drivers occupy the gateway); PIL evidence decisive.
- Net: slide028 FULL FAIL **overturned**; certification stands; no fix dispatched; no build/pptx/DB touched. Detail: `slide028/adjudication.md`.

## Adjudications

### slide041 FULL FAIL — DISMISSED 2026-10-30 (adjudication notes: slide041/adjudication.md, helpers slide041/adjudicate_pil*.py)

Transcript: `slide041/judge_full_retry.txt` (1 MAJOR + 1 MINOR, verdict FAIL).
Verdict rested solely on the MAJOR; pixels refute it. Slide-space 960x540, render
2001x1125 (scale 2.0844); vision re-read leg not run (gate busy: pgrep -c -f
analyze_image.py = 30 then 25, gate needs < 8).

- MAJOR "extra/invented x3=(1;2)/C1 column; original has 5 columns with a gap; class row C1 C1 C2 C2 C2" — REFUTED.
  Original header runs y58-73: SIX groups x92-100, 114-123, 136-145, 158-168,
  181-191, 204-213, uniform 13-14 px gaps (no gap at col3); render six clusters at
  same positions. Original vector band y76-112: six paren+digit triplets, col3
  x134-147 inked (paren pair x134/x147, digit ink 27 px, band 53% cream like the
  other columns 44-52%). Original class row y108-124: red at x90-92, x114-115,
  x135-137 = THREE red C1; blue at x158-159, x180-181, col6 blue+dark. Render
  identical pattern (C1 C1 C1 C2 C2 C2). Per-column diff uniform: table 414/437/439/
  452/448/444 px cols 1-6; digit bands 100-129 px — no col3 spike. Build header
  (build/slide_041.js) records the analysis' 5-column reading as a self-flagged
  vision misread, glyph-verified as six columns at build time.
- MINOR "W-vector '(' vs '['" — REFUTED as discrepancy. Bow profile: ORIG left
  delim mid leftmost x330 < top x331 (bows left at middle => "("); ORIG right delim
  mid x349-353 w=5 vs top w=2 (middle bulge => ")"). A bracket would show constant
  leftmost + wide top AND bottom serifs. Render shows the same paren bow. Judge
  itself rated this style-only ~60% "typed-vs-ink".
- Full-frame diff 117,586 px (5.223%), densest cells in legend row y112-135
  (anti-aliasing); ink-only-in-original 60,090 vs render-only 17,096 px =
  handwriting heavier than typed text, not missing content.

Disposition: FAIL DISMISSED per register rule (vision claim refuted by pixels).
Certification stands; no reopen; no edits to builds/pptx/DB. No git operations.

## Adjudication 2026-10-30 — slide026 CROP FAIL (crop_dense_judge.txt, banked 2026-10-29 23:45) — OVERTURNED

Read-only PIL-first adjudication (details: `slide026/adjudication.md`). Slide space 960x540; render
2001x1125 (scale 2.0844/2.0833); crop pair 634x434 over slide region (136,88)-(440,296).
Crop-pair geometry proven: `crop_dense_render.png` == render.png crop of that region (0 diff px);
`crop_dense_orig.png` == slide_026.jpg same region LANCZOS-upscaled (0 diff px); effective scales
2.0855/2.0865 vs 2.0844/2.0833 — matched. Vision re-leg skipped: `pgrep -c -f analyze_image.py` =
61 at adjudication time (>= 8; live drivers for slides 014/015 occupy the gateway).

| claim | sev | disposition | key pixel evidence (slide space) |
|---|---|---|---|
| 1 region-wide serif orig vs sans render | MAJOR | REFUTED | native-res glyph art (title S/G 27.5pt, body t 17.5pt): constant 2-3px stems, flat terminals, no serif flares; `slide_026_raw.json` typography = "Sans-serif typeface"; 2.09x "serifs" = LANCZOS+JPEG ringing (Template B rule e); recreation font = house Arial (`build/slide_026.js:70` FONT="Arial"; full leg `judge_full.txt` already settled font house-mandated MINOR) |
| 2 missing underline under "Random Weights" [1] | MAJOR | REFUTED | no bar below rowA in EITHER image: max run 12px orig / 16px render over x146-500 y157-164 (descender noise; real bars are 150-350px — positive control rowB bar found in both: 365px orig @y192 / 367 slide-px render @y191.9). Bank lists bars only at rowB y192-194, rowD y258-260, N3 y458 |
| 3 underline stops before "almost zero" [3] in render | MAJOR | REFUTED | continuous bar in BOTH over x287-473: orig 181px run @y259 (cov 0.905), render 202px @y257.2 (cov 0.921); x287-340 100%, x340-473 97.5%; at crop right edge both crops show identical 74px run |
| 4 [1]/[2]/[3] bold orig vs regular render | MINOR | PARTIALLY SUPPORTED (advisory) | orig label bracket stems 3-4 slide px vs render 1.92; label ink 130-146px orig vs 113-126px render-downscaled (downscale biased toward more ink) — orig labels genuinely heavier; MINOR, not FAIL-sustaining |
| 5 W italic in "(w.r.t. W)" | MINOR | PARTIALLY SUPPORTED (advisory) | W glyph x201-216 y210-227: slant 0.27 px/row orig vs 0.141 render (~2x lean); MINOR, confounded with claim 1 |
| 6 top blue rule thicker+darker in render | MINOR | REFUTED | content-box top border y90-92: thickness 3.0 orig vs 3.04 render slide px (equal); orig core (45,33,130) vs render (0,0,255) — render BRIGHTER pure blue; claim direction reversed |
| 7 heading red darker in render | MINOR | REFUTED | render red core median (192,0,0) = house C00000; orig red JPEG-diluted (p50 (222,138,147), p97 (255,177,187)) — rule (e) artifact |
| note right-edge "z" vs "s" truncation | — | DISMISSED | both crops proven the same slide-space region (0-diff reconstruction); same glyph at the edge, vision misread |

Net: all 3 MAJORs REFUTED by pixels; MINORs 6/7 refuted, 4/5 advisory-only. Per `judge_protocol_03.md` §7
(crop-pair clean when every finding is PIL-refuted) the slide026 crop leg is adjudicated CLEAN; harvest-sweep
row `slide026 | PASS | FAIL` -> CROP FAIL overturned 2026-10-30. FULL leg was PASS (`judge_full.txt`).
Slide 026 certification stands; no reopen; no edits to builds/pptx/DB; no git.

## Slide 021 r1 FAIL — PIL adjudication + r2 fix wave (2026-10-30, worker r2)

r1 FULL leg (transcript `slide021/judge_full_r1fail.txt`, verdict FAIL) findings D1-D5, each PIL-adjudicated
vs `unique_slides/slide_021.jpg` (scale 2.0833, census in `qa/slide021/worker_report.md`):

| finding | disposition |
|---|---|
| D1 MAJOR "P2/P3 frames collide, gutter 0-3px, P3 ~25px high" | REFUTED as stated (r1 render frame lines 128.88/257.52/287.76/417.84/436.56/529.68 vs orig 128.96/256.0/289.0/416.5/438.0/528.0; gutter 18.2px vs 19px — no collision, max drift 1.7px). CONFIRMED in weakened form: systematic ~1-2px drift + 1pt-vs-2px stroke -> FIXED in slide_021.js (rects re-aligned to orig stroke centers, stroke 2pt) |
| D2 MINOR "λ = 3 vs λ=3" | CONFIRMED (orig green ink 42px wide x247..288; render 43.2px x245.3..288.5; analysis verbatim `λ=3`) -> eq_021_lambda3 mathtext `\lambda=3`, PNG regen 378x131 |
| D3 MINOR det bars look like serifed "I" | REFUTED (asset bar = 16px plain rectangle, uniform top/mid/bottom at 600dpi; orig bar plain thin bar) — cosmetic misread |
| D4 MINOR pen circles on 43/95 dropped | DISMISSED per payload ground rule (d) typed-vs-handwritten, at most MINOR |
| D5 MINOR P2 table 9px right of heading | HALF-REFUTED (left edge orig x90 vs render 88.8 = aligned); real defect = table width: orig x90..294 (68px cols) vs render x89..279 -> FIXED (x90 w204) |
| task 129 (paren sweep out-of-class MAJOR) eq_021_invexpr missing X underbars | CONFIRMED (orig underbar runs rows 487-488 x165-176 / x193-203) -> segment mathtext `\underline{X}^T \underline{X}`, PNG regen 1140x259 via qa/slide021/compose_eq_021_r2.py |

Rebuild + render_r2.png (150dpi, house_chrome PASS): frame lines now within 0.2 frame px of orig
(128.88/256.08/289.2/416.4/438.0/528.0), tables on orig gridlines, λ label at x247, underbars present.
r2 rejudge legs re-dispatched via rejudge_slide.sh 021 (driver `slide021/r2_driver.out`); verdicts pending.

## Adjudication 2026-10-30 22:20 — slide015 attempt-8 legs (O28 takeover continuation) — FAILs adjudicated PIL-first

Legs (all on UNCHANGED pptx md5 39dc053a, render_6.png 2001x1125, chrome PASS): full FAIL
(judge_att8_full.txt), crops FAIL deriv_stack/peachbox/solution/pinkbox, PASS eq_stack
(crop_8_*_judge.txt). Evidence: `recreated_pptx/qa/slide_015/adjudicate_att8_full.md` (read-only PIL census,
slide-space px).

| leg | claim | sev | disposition | key pixel evidence |
|---|---|---|---|---|
| full | reg terms green in orig, blue in render | MAJOR | DOWNGRADED MINOR | orig eq rect green=2397; render green=0 blue=45504 — palette delta confirmed, class = typed-vs-handwritten/2D-format MINOR per GROUND RULES |
| full | arrow light-orange in orig | MAJOR | REFUTED | orig arrow band has no orange class (green=443 black=74 red=35); render blue=2745 — direction of claim wrong |
| full | final W underline missing | MINOR | CONFIRMED MINOR | orig sol-Y band y505-516 rows 20px/45px vs render flat 2px — notation cue lost, MINOR |
| full | green box right-edge contact | MINOR/MAJOR | REFUTED overflow | right-edge strip dark 199 vs 62 includes border itself; no ink beyond box |
| deriv_stack | J missing in ∂J(W)/∂W L1 | MAJOR | REFUTED | render dark-map x78-115 y348-378 shows ∂,J,(,W (J slot dark=446 render vs 41 orig; bolder glyphs) |
| deriv_stack | λIW not green | MINOR | CONFIRMED MINOR | orig L2 tail green=339; render green=0 blue=2516 — same palette class |
| peachbox | W should be green | MAJOR | REFUTED | orig peach eq green=0 (black=273 only) |
| solution | palette + missing Y underline | MAJOR | MINOR (palette class + underline MINOR as above) | orig sol box green=13347 black=1227; render green=60538 blue=6450 |
| pinkbox | missing W underlines | MAJOR | REFUTED | underline band y318-334: orig runs 15/10/2/2, render 16/11/10/2 — bars in both |
| pinkbox | missing red pointer | MINOR | REFUTED | red px render=22434 > orig=5113 (mark present, render heavier) |

No BLOCKER survives adjudication; equation content/structure clean on all six legs. Gate note: pgrep count
was 7 at dispatch, 65 after (fleet-shared; slide014 sibling legs also queued) — gate serialized correctly.
Certification basis: both leg classes clean-or-adjudicated per AGENTS.md zoomed-judge mandate.
| slide014 (CERT att8 2026-10-30, was parked att7) | PASS | PASS | full=judge_att8_full.txt crop=judge_att8_crop.txt render_10.png (chrome PASS); dense region 280,208-584,416; crop-leg only MINOR typographic/colour notes, 0 BLOCKER/MAJOR |

## Adjudication 2026-10-30 22:2x — slide004 post-blue-fix rejudge (FULL leg FAIL, PIL-adjudicated)

Context: banked rejudge adjudication found ONE confirmed defect — error-box token "Ŷ≠Y" was INK
in the build but BLUE in `unique_slides/slide_004.jpg` (slide x136-181, core [0,0,139]). Fixed in
`build/slide_004.js` (run color -> 00008B), rebuilt, re-rendered (qa/slide004/render.png, chrome
PASS), both legs re-dispatched on the NEW bytes (pre-fix transcripts banked as
`slide004/judge_full_att_prebluefix.txt` / `crop_dense_judge_att_prebluefix.txt`).

PIL proof of the fix (strict blue = b>=110, b>=r+50, b>=g+50, 150dpi render scale 2.0833):
OLD render error-box interior (x80-484, y308-363): 0 blue px. NEW render: token run x97.3-122.2,
y327.2-339.2, 272 strict-blue px, core median [0,0,139] = 00008B exactly. Original token run
x134-182 y327-342 (235-336 blue px depending on threshold). The ~39px x-offset of the token is
pre-existing (render's "If " is narrower than the original's handwritten one); slide XML contains
exactly one new srgbClr val="00008B" — no other run changed.

Leg A (judge_full.txt, 2026-10-30 22:21, verdict FAIL) claims, PIL-adjudicated vs
`unique_slides/slide_004.jpg` (render 2001x1125, scale 2.0844; `rejudge_adjudicate.py 004 --full`:
densest diff cells all in title band y67-90 = typed-vs-handwritten AA, none structural):

| # | claim | sev | disposition | key pixel evidence (slide space) |
|---|---|---|---|---|
| 1 | right white box: "Predicted" right-aligned, eq left-aligned vs orig heading-over-eq/centered | MAJOR | REFUTED | "Predicted" word left edge x676 orig vs x672.5 render (same box x672..760 per build), eq line x506..580 orig vs x505.1..565.6 render — both left-aligned in both; only glyph widths differ (rule d typed-vs-handwritten) |
| 2 | where-block looser vertical spacing / indentation, right-aligned tags differ | MAJOR | REFUTED as MAJOR | line x-origins orig 507/573/568 vs render 506.9/573.6/565.0 (match); tops orig y284/313/345 vs render y282.2/307.2/336.5 — render is TIGHTER not looser, max delta 8.5px cumulative, x-end/tags x776-877 both — MINOR spacing at most; identical geometry was PASSed by the banked pre-fix full leg (judge_full_att_prebluefix.txt) |
| 3-7 | LOSS eq red carry-through, ellipsis/subscript geometry, Let-variable color, Remember eq, box fill tints | MINOR | advisory / previously adjudicated | style-level; underline claims already REFUTED in the banked att9 record; not fix triggers |

Disposition: FULL-leg FAIL DISMISSED — both MAJORs refuted by pixels; the only byte change vs the
certified render is the Ŷ≠Y blue fix. No BLOCKER/MAJOR survives. CROP leg verdict pending
(crop_dense_judge.txt re-run on new bytes). Slide 004 stays certified; DB/ledger updated per the
fix protocol (visual_attempts+1, last_error=NULL). No git; no evidence deleted.

CORRECTION 2026-10-30 22:5x: the first re-dispatched pair (judge_full.txt 22:21 FAIL,
crop_dense_judge.txt 22:37 FAIL) had run on STALE bytes — a mis-ordered `cp` had overwritten
qa/slide004/render.png with the pre-fix render before restaging, so $S4/render.png was the old
image (0 blue px at the token; proven by re-measurement). Those two transcripts are banked as
`slide004/judge_full_att_oldbytes.txt` / `crop_dense_judge_att_oldbytes.txt` and their FAILs are
VOID for the fix (adjudicated refuted above AND stale). The correct post-fix render (chrome PASS;
272 strict-blue px at slide x97-122 y327-339, core [0,0,139]; crop token window 266 blue px) was
restaged and both legs re-dispatched as v2; v2 verdicts in judge_full.txt / crop_dense_judge.txt.

## 2026-10-31 00:1x — slide 021 recert completed (main agent, no vision needed)
- judge_full.txt (2026-10-30 22:43, post-fix bytes md5 c094b309…): FINAL VERDICT PASS, no 429 markers.
- crop_dense_judge.txt (re-read 2026-10-31 00:04 on same post-fix render): FINAL VERDICT PASS.
- DB: slide 21 gen_status='passed', visual_check='PASS', last_error=NULL.
- Final deck: final_deck_tool.py update 21 staged page from slide_021_recreated.pptx; render_check_pages.py 21 → PASS (0 px differ); deck md5 bf267cede55f1593c04712739cf56a81.
- Certified count now 47/51. Open: 19, 25, 43, 44, 48.

## Adjudication 2026-10-31 00:2x — slide004 CROP leg (Template B) on post-fix bytes

Crop leg re-dispatched via `vision_leg.sh` (attempt 2 clean; attempt 1 hit upstream 429) on the
post-fix crop pair `slide004/crop_dense_render.png` vs `slide004/crop_dense_orig.png` (region
60,232-344,440 at matched effective scale; render verified post-fix: 272 strict-blue px at slide
x97-122 y327-339, core [0,0,139]; house_chrome_check.py on render.png = PASS rc=0).
Transcript `slide004/crop_dense_judge.txt` (2026-10-31 00:23): **FINAL VERDICT: FAIL**.

| # | claim | sev | disposition | key pixel evidence |
|---|---|---|---|---|
| 1 | missing underline under RHS Y in "Objective is Ŷ=Y" and under Y in "If Ŷ≠Y" | BLOCKER/high | **REFUTED** | `rejudge_adjudicate.py 004 --crop` + slide-space PIL on `unique_slides/slide_004.jpg` (960x540) and `slide004/render.png` (2001x1125, sc 2.0844): objective box interior x78-302 y242-301 — orig text ink ends y286 (descenders), NO run >=8 slide-px below the line anywhere in the box (the y284 marks x220-233/x254-267 are glyph feet inside the descender zone; the inherited "x254 w17 y283" bar was already REFUTED in the banked att8 record `qa/slide004/worker_report.md`); render has zero ink below its objective text line (slide y276-290 empty). Error box x78-486 y306-365 — orig 00008B token Ŷ≠Y at slide x136-181 y327-342, rows below (slide y344-352) EMPTY in both crop images and in the 1:1 frame; render token x97-122 y327-339 (post-fix, 272 px) with empty rows below; the horizontal runs mid-line are the ≠ sign's bars (slide y333.6/337.6), not underlines. Real underlines in this deck are separate strokes >=15px wide below the descender zone (where-block Ŷ x508-526 / W x566-584 y277-283). |
| 2 | thinner text stroke weight in recreation | MINOR/high | advisory | ground rule (c) typed-vs-handwritten medium difference |
| 3 | small color/contrast differences | MINOR/med | advisory | style-level |
| 4 | horizontal advance/placement differs | MINOR/med | advisory | font metrics; words match |

Disposition: CROP-leg FAIL **DISMISSED** — the only BLOCKER is refuted by pixels; no
BLOCKER/MAJOR survives. `slide004/result.txt` CROP=NORESULT -> **PASS**. Slide 004 rejudge is now
complete: FULL=PASS (v2 transcript 2026-10-30 23:01, post-fix bytes) + CROP=PASS (dismissed).
Slide stays certified; DB and deck untouched. No git; no evidence deleted (stale old-bytes
transcripts remain banked as `slide004/*_att_oldbytes.txt` / `*_att_prebluefix.txt`). Full record:
`slide004/adjudication.md`.
