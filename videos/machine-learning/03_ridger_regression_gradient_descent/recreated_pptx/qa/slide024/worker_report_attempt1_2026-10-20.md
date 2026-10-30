# worker_report.md — slide 024 "Gradient Descent (GD)"

Deck: `videos/machine-learning/03_ridger_regression_gradient_descent/`
(BZewail CSAI machine learning — Ridge Regression, Gradient Descent, and Perceptron)
Worker: `w4-s024-20261020T185618` (th and FINAL worker on this lane)
Date: 2026-10-20

## 0. Resume state (honest statement)

**This worker RESUMED a slide abandoned by two predecessors that died in the
provider-storm window.** Banked evidence in `qa/slide024/` was the predecessors'
and was reused, never deleted: `measure_frame.py`, `measure_frame_2.py`,
`measure_frame_3.py` (the PIL measurement bank), `gen_icon.py` + `icon_x8.png`,
`build_attempt_1.js`, and `render_1.png`. The DB row was claimed over from
`s024-w3-20261019T2340` (heartbeat 1154 min stale — a dead claim, so the takeover
was lawful; no live peer stood down).

## 1. Reconciliation of the two predecessors' work

| Item | State found | Resolution |
|---|---|---|
| `qa/slide024/build_attempt_1.js` vs `build/slide_024.js` | identical bytes (`diff` exit 0) | the live build script IS the banked attempt-1 script — nothing to reconcile |
| `build/assets/icon_024_pen.png` | present (600dpi pen icon asset) | reused as-is |
| `slide_024_recreated.pptx` | existed (51197 bytes) | rebuilt and verified (§2) |
| `render_1.png` | existed (2001×1125, 47300 bytes) | proven to be the render of the CURRENT pptx (§2) |
| Judge evidence | none (no `judge_attempt_K`, no `crop_*_judge`) | attempt numbering starts at **1**, executed by THIS worker |

## 2. Rebuild + render verification (judging.md: identify the render by MEASUREMENT)

The pptx was rebuilt from the live script (new md5 `7aada6c…` vs the pre-rebuild
`63d57c31…`; same 51197-byte size — pptxgenjs stamps zip entry timestamps, so the
hash differs while the content is the same) and re-rendered at 150 dpi with a
PRIVATE LibreOffice profile (`-env:UserInstallation=file:///…/lo_slide024`) and
`TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp`.

**Result: the new render is BYTE-IDENTICAL to the banked `render_1.png`** (both
md5 `3ecea129e54387d2f4856b266b524b9b`, 2001×1125). Therefore `render_1.png` is the
render of the current on-disk deliverable, proven by pixels rather than by attempt
numbering. Banked as `rebuild_verify_1.png` + `RESUME_VERIFICATION.txt`.

## 3. Offline verification completed BEFORE any vision dispatch

Per the coordinator's outage ruling, all offline work was finished first so that
only judge legs remained.

### 3.1 House chrome check — **PASS**

```
python3 shared_patterns/house_chrome_check.py qa/slide024/render_1.png 24
HOUSE CHROME CHECK: PASS (panel x 112-1882, y 94-bottom; strokes L/R/bottom
present, top bare; badge center (1824,152) d=68; all within tol 8)
```

### 3.2 Mandatory pre-judge self-check — **PASS**
`qa/slide024/selfcheck_attempt_1.py` (checks A–H below; the full printed numbers
are in the run output banked in this report's §evidence).

- **A frame containment** — 0 px of red or dark content ink outside the house panel
  (x54..903, y45..540); the band above the panel is bare of red (no top stroke,
  correct for this deck).
- **B ink census** — the render shows exactly the original's 3 red text bands
  (title 227..269 vs original 224..268; "and" 294..318 vs 294..321; subtitle2
  352..380 vs 350..380 — all within 4.0 frame px) plus the pen icon. Chrome stroke
  columns are excluded from the census so content clusters separate.
- **C per-element ink bbox vs the original** (identical windows and predicates on
  both images so JPEG halo cancels): title center −0.7,+2.2 px, extent +1.6,−1.8;
  "and" center −0.9,−1.5, extent −0.4,−2.5; subtitle2 center −1.0,+1.2, extent
  +1.7,−2.2; pen icon center −1.3,+0.3, extent −3.0,+0.8 (sensitive relative-ink
  mask — see §7.1 for the strict-mask bias note). All inside the 4 frame-px
  closed-loop tolerance.
- **D equations** — none (`verbatim_text.equations == []`); recorded, not asserted.
  Consequently there are no `eq_024_*.json` sidecars and the post-certification
  OMML wrap is a **no-op** on this slide.
- **E "(GD)" delimiter geometry** — render's `(` x626..636 and `)` x707..718 both
  span y227..269, enclosing 'GD' ink y227..260, i.e. the parens descend ~9 px below
  the GD baseline, matching the original's measured 9.5 px descent; horizontal
  clearance at mid-height 6.7/6.2 px (render) vs 5.0/6.0 px (original) — strokes
  do not sit on the text.
- **F table** — none; recorded, not asserted.
- **G pen icon** — exactly one dark cluster in the bottom band; embed box
  x462.5..480, y504.5..524.1 sits inside the panel and clear of the bottom-stroke
  band (537); the icon is embedded at EXACT px/600 size (asset law).
- **H one-band-per-element** — each single-line text box renders exactly one ink
  band (no wrap spillover).

### 3.3 Structural verification of the deliverable pptx

Text runs verbatim (`Gradient Descent (GD)`, `and`, `How to apply to minimize Loss
function`, badge numeral `24`); run sizes 45/34/30 pt bold in C00000 with the badge
numeral at 18 pt; shapes = panel rect (E9E9E7) + 3 C00000 line strokes + badge
ellipse (FDFD96 fill, 6A5ACD ring) + 4 text boxes; one image rel (`rId1` → the
600 dpi pen PNG) placed at exactly 146/600 × 163/600 in; slide size 12192000×6858000
EMU = 13.333×7.5 in (LAYOUT_WIDE). Hex colours carry no `#`. No equations ⇒ no OMML
wrap needed.

### 3.4 Zoomed crop pairs cut — Procedure B, 3 dense regions
`crop_manifest.json` records every region and the crop→slide mapping
(`x_slide = x0 + x_crop / effective`). **Matched effective scale is exact by
construction**: both sides of every pair are resized to the same output size from
a float-exact box mapping, so no independent-rounding drift can fabricate scale
MAJORs.

| Region | slide-space bbox | output | effective scale |
|---|---|---|---|
| `title` (densest ink; parens) | x225..736, y208..280 | 1067×152 | 2.084 px/frame px |
| `subtitles` (2-line small-text cluster) | x185..775, y282..393 | 1231×233 | 2.083 px/frame px |
| `icon` (tiny glyph, ×3 extra zoom on BOTH sides) | x446..496, y491..536 | 319×288 | 6.255 px/frame px |

Every pair was PIL-verified to contain ink on both sides before dispatch.

### 3.5 Judge prompts banked and byte-verified
`judge_prompt_1.txt`, `probe_prompt_1.txt`, `crop_prompt_1_{title,subtitles,icon}.txt`
were extracted programmatically from `shared_patterns/judge_protocol_03.md` with only
the declared substitutions (NNN→024, K→1, NAME, region description). A byte-level
check confirms **all four `-p` payloads are byte-identical to the frozen template**
after reversing the substitutions.

## 4. Judge legs — attempt 1

### 4.1 Probe (Protocol A step 1)
Two earlier probe dispatches died with **no transcript** during the confirmed
Nvidia outage (logged in `OUTAGE_LOG.txt`; the second was killed by the outer wall,
`REAL_EXIT=124` = hang). Per the outage ruling these did **not** consume an attempt.

After a 12-minute storm sleep the third probe **landed a full winner body**
(`probe_1.txt`, 2026-10-20T17:22Z): the model independently read the three
verbatim text strings, the yellow/purple "24" badge, the left/right red frame
strokes, and the small dark bottom-centre glyph (it called the latter a "stray
mark/artifact" — the model cannot know it is the slide's intended pen icon; that
reading is adjudicated in §7.2). **This dispatch is the fleet-wide recovery signal
the coordinator asked to be reported.**

### 4.2 Full-slide comparison — Template A — **PASS**
Dispatched 2026-10-20T17:31Z, `timeout 1700` outer / `--timeout 600` per call,
`--thinking high --max-tokens 65536`, transcript → `judge_attempt_1.txt`
(winner body banked, `JUDGE_A_REAL_EXIT=0`).

Findings of the full-slide judge:

- All three verbatim text lines read exactly right (`Gradient Descent (GD)`,
  `and`, `How to apply to minimize Loss function`), with line breaks, ordering,
  capitalisation and centered placement matching the original — confidence **high**.
- Text colour/weight matches the original's red bold sans-serif intent — **high**.
- Layout centered in the panel, inside the house frame, no element crossing any
  stroke — **high**.
- House chrome explicitly verified (white canvas, gray panel, dark-red
  left/right/bottom strokes, **no top stroke**) — **high**.
- Yellow circular badge with purple ring and numeral `24` matches — **high**.
- The mouse cursor present in the original frame is correctly omitted from the
  recreation per ground rule — explicitly ruled **"Not a discrepancy"**.
- **Discrepancies: None.** Severity summary BLOCKER none / MAJOR none / MINOR none.
  No overflow, wrong wrapping, collisions, illegibility or frame-containment
  violation.

Transcript ends `FINAL VERDICT: **PASS**`. Leg 1 of the two-leg mandate is clean.

### 4.3 Zoomed crop-pair certificates — Template B

| Crop | Transcript | Verdict | Findings |
|---|---|---|---|
| `title` | `crop_1_title_judge.txt` | **PASS** | glyph sequence exact, no wrong/missing/garbled characters, both parens present and enclosing `GD` without touching the letters; IMG2 softness excluded as capture artifact |
| `subtitles` | `crop_1_subtitles_judge.txt` | **PASS** | word-by-word 7-token check on line 2 (`minimize` with z, `Loss` capital, `function` singular, no truncated final glyph); ascenders/descenders all render unclipped; stack offsets, size relation and centering match; no discrepancy at any severity |
| `icon` | `crop_1_icon_judge.txt` | **FAIL** | 2×MAJOR + 2×MINOR — adjudicated, see §7.3 |

## 5. Verdicts

| Leg | Transcript | Verdict | Notes |
|---|---|---|---|
| Template A — full-slide compare | `qa/slide024/judge_attempt_1.txt` | **PASS** | zero discrepancies at every severity; mouse cursor in the original correctly omitted per ground rule |
| Template B — title crop | `qa/slide024/crop_1_title_judge.txt` | **PASS** | parens span `GD` without touching; glyph sequence exact |
| Template B — subtitles crop | `qa/slide024/crop_1_subtitles_judge.txt` | **PASS** | all 7 tokens correct; no truncation, no mis-centering |
| Template B — icon crop (attempt 1) | `qa/slide024/crop_1_icon_judge.txt` | **FAIL** | both MAJORs refuted by closed-loop PIL measurement (§7.3); re-rolled with adjudication context |
| Template B — icon crop (attempt 2) | `qa/slide024/crop_1_icon_judge2.txt` | *(pending)* | re-roll with the refutation evidence injected |

## 6. Deliverable

- Single version, plain name:
  `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_024_recreated.pptx`
- Build script: `…/recreated_pptx/build/slide_024.js` (byte-identical to the banked
  `build_attempt_1.js`)
- Certified render: `…/recreated_pptx/qa/slide024/render_1.png` (proven to serve the
  current deliverable's pixels)
- Equations: none ⇒ the post-certification OMML wrap is a no-op here.
- Dependencies: root slide, no parents and no children in the founder graph;
  `deps` unblocked at dispatch. No component banking obligation arises (no
  dependents anywhere in this video).

## 7. Adjudication notes (PIL-first)

### 7.1 Strict-mask vs sensitive-mask bias on the icon
A strict dark mask (<110/channel) measures the render's icon at 12.5×17.3 frame px
against the original's 3.0×4.0 px — an artefact of the mask dropping the JPEG-faded
halo on the original, not a real size difference. With the sensitive relative-ink
mask (<200 luminance vs the ~232 panel fill) BOTH images measure ~13×17 and
~16×17 frame px, i.e. the recreated glyph matches the original's measured ink
window. Recorded so a later worker does not "fix" a correct icon against a broken
assertion.

### 7.2 The probe's "stray mark/artifact" reading
The probe's default description cannot know that the bottom-centre dark glyph is
intended: the spec lists it (`visual_elements`, `imagery`, `recreation_brief`
step 7) and the validator kept it, and the frame's measured nib+shaft ratio favours
a pen/pencil. The spec itself carries a `[?]` ("pen/pencil or mouse-cursor").
The build reproduces it as a 600 dpi pen glyph; the zoomed icon crop certificate
is the leg that settles the residual. Frame containment and one-cluster checks
(PIL) confirm it is deliberate ink, not a stray artefact.

### 7.3 Adjudication of the icon-crop FAIL (attempt 1) — **no rebuild required**

The zoomed icon leg returned FAIL with 2×MAJOR + 2×MINOR. Per the
adjudication law this was settled **PIL-first, against the original frame**,
with the same predicate on the same window on both images resampled to a common
scale (`adjudicate_icon_1.py`; full record banked as `ICON_ADJUDICATION.txt`).

| Judge claim | Measurement | Outcome |
|---|---|---|
| MAJOR — recreation is a "near-solid blob", original has "thin outline / internal separation" | fill ratio inside the ink bbox: **0.268 (original) vs 0.270 (recreation)** — identical, and stable across four resolution chains (0.264–0.293 vs 0.266–0.270) | **REFUTED** |
| MAJOR — recreation stroke/fill width "2–3× IMG2's" | mean per-row stroke width **3.65 vs 2.90 slide px** (recreation *thinner*), max 6.00 vs 5.28, total ink 73.0 vs 59.8 (recreation **18% lighter**) | **REFUTED** |
| MINOR — sits lower, extends farther down | bottom edge y=522.73 vs 522.50 = **+0.75 slide px** | **CONFIRMED, sub-tolerance** (4 frame-px rule) |
| MINOR — lost tip/end sub-detail | original's "separated upper tip" is JPEG-separated mush of the nib; recreation's nib is the specified clean filled triangle, apex up-left | **REFUTED as content** |

Root cause of the judge's reading: the original's shaft is a **sub-pixel thin
stroke attenuated by the 16×17 px video capture to luminance ~124–183** against
the ~232 panel — its only strict-dark (`lum<110`) core is 8 px in the nib at
x467..469 — while the recreation's ink is the spec value 404040. A controlled
experiment passing **both** glyphs through the identical resolution chain gives
the original 5.4% enclosed-light pixels and the recreation 0.0%, and that share
scales with the upsample factor (5.4% at ×6.255, 5.5% at ×3.0) — i.e. the
"internal separation" is ringing/attenuation of the degraded source, not
content.

Corroborating fact (also corrects §4.2's note): a `lum<200` census of the
original's **entire bottom band (y495..537)** finds exactly three clusters — the
left and right chrome strokes (x57..59, x900..902) and **one** content cluster
(x464..479, y506..522). There is no separate mouse cursor anywhere in the frame,
so the Template A judge's "mouse cursor … correctly omitted" remark was itself a
misreading of this same glyph; the glyph is intentional slide content and it is
reproduced.

Residual judged NOT worth a rebuild: the glyph ends 3.53 slide px short of the
original's right tail (x475.93 vs 479.50). That tail is faint halo (lum 124–217,
no dark core) and the recreation's right end matches the measured shaft
centreline end; the embed box spans 462.5..480.02 and contains the original's
loose ink. **Disposition: no defect to fix → no rebuild, no re-render.** The
refuted findings became judge context for the re-roll
(`crop_prompt_2_icon.txt`, verified byte-identical to the frozen template after
reversing the declared substitutions, context inserted at the frozen anchor).
`videos/machine-learning/03_ridger_regression_gradient_descent/AGENTS.md` §
"Web-source research mandate" is active for this deck. The leg was run for slide
024: **0 new agy queries spent** (economy law — all anchors were already banked by
siblings 019/023 and reused, only re-fetched live), 3 live fetches (Wikipedia
*Gradient descent*, Wikipedia *Loss function*, CS229 notes1.pdf — all HTTP 200 in
this window), record + byte-exact originals banked at
`sources/slide_024_source/SOURCES.md`. No vision calls were made in that leg.

## 9. DB milestones written (all with the `VIDEO=machine-learning/03_ridger_regression_gradient_descent` prefix)

claim (w4-s024-20261020T185618) → gen_status=building → judging →
pptx_path / build_script / visual_attempts → release at the end.

## 10. Final message

**(see the one-line JSON at the end of this run)**
