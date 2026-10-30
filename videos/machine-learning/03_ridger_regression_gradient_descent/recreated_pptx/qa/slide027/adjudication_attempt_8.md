# Slide 027 — adjudication record, attempt 8 (CONTROLLING for the "Learning step" chain)

**Worker:** `w10-s027-a7-20261021T1945` · **Date:** 2026-10-21 · **Deck:** `03_ridger_regression_gradient_descent`
**Slide:** 027 — "Follow Negative Direction of Gradient with Selected Learning Rate"
**Deliverable:** `recreated_pptx/slide_027_recreated.pptx` (single plain-named version; no equations on this
slide, so no OMML pass applies) — 85726 bytes, md5 `f0d25a8180735556543e75092d4e6887`
**Live build:** `recreated_pptx/build/slide_027.js` (md5 `ee4876ff0e88adb7a53d9677dc50ccad`, byte-identical
to the banked `build_attempt_8.js`)

> **Numbering note.** The dispatch message named this round "attempt 7 / render_7". The banked lineage
> already reaches attempt 7 (`build_attempt_7.js` = the 13-straight-chord chain build that this round's
> fix supersedes), so this round is banked as **attempt 8** to keep `build_attempt_K.js`, `render_K.png`,
> `judge_attempt_K.txt` and this record aligned. Read `adjudication_attempt_8.md` for the attempt-8 fix;
> `adjudication_attempt_6.md` remains the record of the earlier rounds (its A1/A2 refutations still stand;
> its fix spec was implemented as attempt 7 and is now superseded on stroke geometry — see §4).

---

## 1. What was being fixed

Attempt 7 (`build_attempt_7.js`, `render_7.png`) passed its full-slide leg and the `min_cluster` /
`axis_top` legs, but **`crop_7_dot_sequence_judge.txt` FAILed** on one MAJOR (high confidence):

> item 1 — "short *curved, head-tipped arrows* … one per inter-dot interval … sitting just above the
> black curve … The recreation does **not** have these; instead it draws ~5-6 straight, head-less rays …
> (a) the connectors are straight chords/rays rather than the original's per-step curved arrows …
> (b) they are **absent over the lower-right part** of the descent (intervals dot6→dot7 and dot7→dot8)".

## 2. PIL-first adjudication of that FAIL (findings are hypotheses; measure before fixing)

Banked in `probe_adj7_dotseq_output.txt`, `probe_adj7_curve_output.txt`, `probe_adj7_arc_output.txt`.

| sub-claim | ruling | banked evidence |
|---|---|---|
| marks **absent** over dot6→7 / dot7→8 / dot9→min | **REFUTED** | render ink exceeds the original in every interval window: dot6→7 **68 vs 32** px, dot7→8 **63 vs 25**, dot9→yellow **55 vs 34**; the original's own ink there is one component of area 21 px at frame (378,379)-(387,381) versus render_7's area 12 px at (378,380)-(380,381) — both present, mine not the thinner of the two |
| marks are **head-tipped arrows** | **REFUTED** | zero solid head candidates (fill≥0.75 AND area≥40) anywhere in the chain window; the 4×10 fill≈0.9 blobs at x261 are the dashed leader's dashes |
| marks are **curved**, one per interval | **CONFIRMED → this is the defect** | nine genuine arcs: quadratic R² **0.91-0.98**, lineRMS **0.80-1.49** vs quadRMS **0.08-0.43** (lineRMS 3-7× quadRMS); the render's own known-straight chords read lineRMS ~0.1-0.3 through the identical code path |

Net: the only real defect was **shape** — attempt 7 drew straight 1pt chords where the original has nine
thin arcs. The judge's "absent" sub-claim was a perception of the *straight* chords' thin 1pt weight and
their inter-stroke gaps, not of missing ink.

## 3. The measured model that attempt 8 implements

From the halo-excluded component census of the original (`probe_adj7_curve` / `probe_adj7_arc`):

- **Nine marks, one per inter-dot interval**, chained from frame (272.5,262.8) to (444.0,395.9);
  each 9-24 fpx long with **sagitta 0.98-5.16 fpx always bowing AWAY from the parabola**.
- **Mean thickness 1.99-2.28 fpx ≈ 2 pt** (this supersedes attempt 7's 1 pt mains / 0.75 pt companions —
  the "bundle of thin strokes" reading was an artefact of splitting each blurred arc at its contact with
  the dots/curve).
- **Colour** `ACACAD` = measured median of the original's own arc ink (172,171,173), lum 171.5.
  Hue-neutral, spread ≤ 18.
- **Ends stop 8-12 fpx from the adjacent disc centres** (disc radius 6.5 fpx) i.e. **just OUTSIDE the
  rims** — this supersedes attempt 7's "re-aim each end 2.5 fpx INTO the rim" rule, which the judges
  read as the leader piercing the dots.
- **Inter-link gaps 1.6-10.8 fpx** — preserved deliberately: the original's own marks are separated
  (its only ≥2-column zero-ink run is x412-415).
- **No heads, no fill**: open strokes, drawn before the discs in z-order.

## 4. The fix (attempt 8) — and what did NOT change

`build_attempt_8.js` — one block replaced, everything else byte-identical:

- replaced the 13-stroke `// ---- LEARNING-STEP CHAIN:` block (13 `pptx.ShapeType.line` chords, 1 pt mains
  + 0.75 pt companions, rim-overlap re-aiming) with **nine open `custGeom` polylines** (2 pt, `ACACAD`,
  no `fill` option → `<a:noFill/>`), one per interval, 9 points each, coordinates exactly as measured
  (they are banked verbatim in `scratch/probe_adj8_shape.py` as `CHAIN_LINKS`).
- Unchanged: title (Calibri Bold 31.5 pt `8B0000`, two lines), white graph box with its 2 pt red border,
  axes with custGeom triangle heads on the **axes only**, dashed leaders, the 54-point Catmull-Rom
  parabola (black 2 pt), the nine blue dots `5F41C4` d=13, the yellow minimum dot d=12.5, all labels,
  theta glyphs, the gray `+`, the theta-hat caret, and the house chrome require.

Proof that nothing else moved: `selfcheck_8_output.txt` is identical to `selfcheck_7_output.txt` except
trace→ink mean 0.30 vs 0.32 and ±1-3 px of ink inside the dot windows (the arcs merge with the disc
blobs); and the `title` / `lower_left` / `axis_right` render crops are **pixel-identical** between
render_7 and render_8 (0 differing px — see §6).

## 5. Gates on render_8

- `house_chrome_check_8.txt` → **PASS** (panel x112-1882, y94-bottom; L/R/bottom strokes present, top
  bare; badge centre (1824,152) d≈68; all within tol 8).
- `selfcheck_8_output.txt` → **clean**: no `NO INK … <<< CHECK` marker for any element; every element's
  band inside its banked expectation; graph ink contained inside the box; title ink inside the panel.
- **Build-geometry verification** (does the pptx actually draw the measured arcs?):
  - `probe_adj8_shape_output.txt` — **9/9 arcs**: ink present on 100% of stations along the built
    centre-line, mean |deviation| **0.11-0.29 fpx**; the rendered bow matches the built bow within
    **0.37 fpx on all nine** (a straight chord would read 0.00). 2pt thickness confirmed.
  - `probe_adj8_chain_output.txt` — ink present in **all nine** interval windows (more than render_7 in
    7 of 9; render_7's dot6→7 and dot7→8 windows were the thin ones); nearest gray ink to each iterate
    centre **7.1-8.9 fpx** (just outside the 6.5-fpx rim, per the superseding rule); **0** FAT components
    (len-ratio > 6); the nine substantial components have len-ratio 3.8-4.3 render px = **1.8-2.1 fpx**
    thick; no filled heads.
  - `probe_adj8_arc_output.txt` — chain-window continuity **164/195** columns with ink vs render_7's
    **156/195** and the original's 188/195; zero-ink runs down from 12 to 7.

## 6. Crops (Template B) — what was retained and what was re-cut

All six regions re-cut from `render_8.png` at matched scale (render crop straight from the 150 dpi
render, original crop LANCZOS-upscaled to the exact same pixel size; eff. scale 2.083-2.088 both axes).
Retention is proven by diff, not assumed:

| region | differing px render_7 → render_8 | treatment |
|---|---|---|
| `title` | **0 of 187704 (0.000%)** | retained from attempt 7 (region untouched by the chain) |
| `lower_left` | **0 of 33184 (0.000%)** | retained |
| `axis_right` | **0 of 8979 (0.000%)** | retained |
| `axis_top` | 638 of 75184 (0.849%), bbox render x165-204 y192-253 | **re-cut + re-judged** |
| `dot_sequence` | 3665 of 159040 (2.304%), bbox x51-342 y77-358 | **re-cut + re-judged** |
| `min_cluster` | 1820 of 221379 (0.822%), bbox x254-519 y0-96 | **re-cut + re-judged** |

Every dispatch used the frozen protocol payloads byte-for-byte (verified: Template A 4115 chars
identical to `shared_patterns/judge_protocol_03.md`; Template B 1914 chars identical apart from the
mandated `NNN`→027 and region-description substitutions), through `scripts/16_vision_gate.sh` wrapped in
`timeout 1700`, `--thinking high --max-tokens 65536 --timeout 600`, one attempt each, no retry loops.
Dispatch scripts: `.run_full8.sh`, `.run_crop8_{dot_sequence,min_cluster,axis_top}.sh`.

## 7. Attempt-8 leg results

| leg | transcript | verdict |
|---|---|---|
| full-slide (Template A) | `judge_attempt_8.txt` | **PASS** — "Discrepancies found: none" |
| `dot_sequence` | `crop_8_dot_sequence_judge.txt` | **PASS** — 4 MINORs only |
| `min_cluster` | `crop_8_min_cluster_judge.txt` | **PASS** — 4 MINORs only |
| `axis_top` | `crop_8_axis_top_judge.txt` | **PASS** — 2 MINORs only |

The previously failing MAJOR is gone. `judge_attempt_8.txt` now reads, of the chain: *"Labels 'Minimum'
and 'Learning step' (with its step arc) present in both, same placement relative to the dots"*, and
`crop_8_dot_sequence_judge.txt` item 2 reads: *"IMG1 draws the inter-dot connectors as smooth, uniform
gray Bézier arcs … IMG2 shows the same connectors as slightly wavy, hand-drawn/uneven arcs … The
connectivity pattern between successive dots is the same."* — i.e. the judge now sees nine per-interval
arcs, which is the measured model.

## 8. PIL-first adjudication of every new MINOR (all legs PASSed; numbers below)

| # | finding (leg) | ruling | evidence |
|---|---|---|---|
| 1 | label typed vs handwritten ink (dot_sequence 1) | medium difference | protocol rule (c) — at most MINOR; spelling verbatim |
| 2 | arcs smooth vs slightly wavy (dot_sequence 2) | **the defect, now fixed** | the smoothened 2 pt arc IS the measured model (§3); the original's waviness is capture (rule e) |
| 3 | dashed leader crisp vs soft (dot_sequence 3) | capture softness | the leader is byte-identical to attempts 6-7 (0-px crop diff, §6) |
| 4 | JPEG halos on dots/curve (dot_sequence 4) | not a content difference | protocol rule (e), stated as such by the judge |
| 5 | arcs "lighter gray and finer weight … noticeably lower-contrast" (min_cluster 1, HIGH) | **REFUTED as a colour/weight defect** | (a) the stroke colour is the measured median of the original's own arc ink: `ACACAD` (172,171,173), lum 171.5; (b) ink coverage in the same windows EXCEEDS the original — `probe_adj8_weight_output.txt`: **7.6%** of band pixels at lum≤200 vs the original's **6.6%**; **94/181** columns with ink vs **71/181**; **1.27 vs 0.92 fpx** mean ink height per column (attempt 7, which the dot_sequence judge read as absent, was at 2.4% / 40/181 / 0.38); (c) the perceptual gap is the blur *profile*, not the colour: the original's ink is a wide feathered band (peak darkness mean 75-86) while mine is crisp and narrow (peak 0), which is the same effect the judge rates MEDIUM on the black parabola in its own item 2 and which rule (e) covers |
| 6 | general stroke weight finer/lighter — parabola, theta axis, dashed line (min_cluster 2, MEDIUM) | **REFUTED — capture blur, not weight** | control on the RIGHT parabola branch, where both images draw the same 2 pt black: original core **2.66 vs 2.11 fpx**, full **5.21 vs 2.62 fpx**, peak darkness 73-86 vs 0-3 — the original reads WIDER there too, in the same direction as the left branch. `probe_adj8_axis_output.txt` §3 |
| 7 | yellow minimum-dot fill softer (min_cluster 3, low) | house palette is intentional | the judge itself declined to score it ("the house palette yellow (FDFD96 family) may be the intended fill") |
| 8 | "+" glyph fainter (min_cluster 4) | recreation is correct per the region's own description | the judge: *"Per the stated content of the region ('faint gray +') I treat IMG1 as correct"* |
| 9 | y-axis shaft "markedly bolder (~2×)" + wider arrowhead base / different slope (axis_top 1, HIGH) | **REFUTED by measurement** | shaft core width: ORIGINAL **3.50 fpx** (uniform, p10=p90=3.5) vs RENDER_8 **2.00 fpx** — mine is 0.57×, not 2×; the original's extra width is blur (full 4.50 vs 2.00 fpx; peak darkness mean 80 vs 0). Arrowhead: original base **12 fpx** at rows y+12..16 with a blurred 2-4 fpx tip; render base **11 fpx** at y+15 with a 1 fpx tip — mine is 1 fpx NARROWER, same ~15-16 fpx height, matching flank (width grows 6→12 over rows 6-16 in the original vs 5→11 in the render) |
| 10 | left parabola branch "visibly heavier" (axis_top 2, HIGH) | **REFUTED by measurement** | original core **5.55 fpx** / full **8.25** vs render core **4.70** / full **5.13** — the original is heavier on both measures; the crisp pure-black core (peak 0 vs 44) is what reads as heavy, and that effect appears on the known-matched right branch too (#6) |
| 11 | small horizontal dashes (axis_top 3) | no discrepancy | stated by the judge |

No MINOR required a rebuild: every numeric/colour/weight claim was refuted with banked measurements, and
the one claim that was confirmed (the arcs' shape) is exactly what the attempt-8 fix implements.

## 9. Result

All four attempt-8 legs PASS, house chrome PASS, selfcheck clean, single plain-named deliverable on disk.
DB: `visual_check=PASS`, `gen_status=passed`, `visual_attempts=8`, `visual_transcript` = the four
attempt-8 transcript paths; claim released back to the pool.

## 10. Banked evidence index (this round, `recreated_pptx/qa/slide027/`)

`build_attempt_8.js`, `render_8.png`, `house_chrome_check_8.txt`, `selfcheck_8_output.txt`,
`judge_attempt_8.txt`, `crop_8_{dot_sequence,min_cluster,axis_top}_judge.txt`,
`crop_8_*_{render,orig}.png` (all six regions), `.run_full8.sh`, `.run_crop8_*.sh`,
`probe_adj8_chain_output.txt`, `probe_adj8_shape_output.txt`, `probe_adj8_arc_output.txt`,
`probe_adj8_weight_output.txt`; scratch scripts `scratch/probe_adj8_{chain,shape,arc,weight}.py`.
Nothing was deleted; attempt-6 and attempt-7 transcripts and builds remain banked.
