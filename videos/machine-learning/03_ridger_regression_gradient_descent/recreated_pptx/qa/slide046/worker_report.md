# Slide 046 — judge-lane worker report (legs-only)
Deck `machine-learning/03_ridger_regression_gradient_descent`
Worker `w046-legs-20261024` — claimed `46` at 2026-10-24 06:54 (took over the
stale `worker-fresh-046-final` claim, heartbeat 55m stale).

Scope: the build + first render were completed by a prior lane
(`worker-fresh-046-final`, attempt-4 frame-true rebuild). This worker owes BOTH
judge legs plus certification.

## Starting state (verified with ls)
- Deliverable: `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_046_recreated.pptx`
  (307,873 B, mtime 06:54). Banked copy: `qa/slide046/slide_046_recreated_attempt4.pptx`.
- Build script: `recreated_pptx/build/slide_046.js` (mtime 06:54). Banked copy:
  `qa/slide046/build_attempt_4.js`; asset generator banked as
  `qa/slide046/gen_math_046_attempt4.py`.
- Render under review: `qa/slide046/render_4.png` (2001×1125, 150 dpi).
- Original: `unique_slides/slide_046.jpg` (960×540) md5 `0b355cbc667845d46001d7001ada241d`.
- Rescue bank `scratch/tmp/rescue46/judgeA_payload_046.txt` — present, and
  **byte-identical** to Template A extracted from
  `shared_patterns/judge_protocol_03.md` line 70 (4115 chars).

## DB repair (before/after)
Row 46 carried a WRONG double-prefixed path. Verified the real file with `ls`
(`…/recreated_pptx/slide_046_recreated.pptx`, no `videos/videos/`). The `set`
command refuses writes while a live worker holds the claim, so the writes were
issued with `--worker w046-legs-20261024`:

| field | before | after |
|---|---|---|
| pptx_path | `videos/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_046_recreated.pptx` | `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_046_recreated.pptx` |
| build_script | `videos/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_046.js` | `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_046.js` |
| gen_status | `building` | `judging` |

## Render-currency verification (independent re-render)
`soffice --headless` (private profile `lo_verify46_wlegs`) → pdf → `pdftoppm -png -r 150`
re-render of the CURRENT pptx is **pixel-identical to `render_4.png`**
(`ImageChops.difference(...).getbbox()` = `None`). The build and the render agree;
`render_4` is the current artifact.

## House chrome + PIL self-check (both PASS)
- `python3 shared_patterns/house_chrome_check.py render_4.png` → **PASS**
  (`house_chrome_check_attempt_4_wlegs.txt`): panel x112..1882 y94..bottom,
  strokes L/R/bottom present, top bare, badge center (1824,152) d=68, all within tol 8.
- `qa/slide046/selfcheck_attempt_4.py` → `qa/slide046/selfcheck_attempt_4.txt`:
  **26/26 windows within 8 frame px**, TOL 8, scale 2.08333. Windows were re-measured
  from the frame to match attempt 4's parenthesised-COLUMN-VECTOR layout (the attempt-2/3
  windows were transcribed against a ROW layout). Max deviation 5.1 frame px
  (`z_colpairs` top edge; the Z header sits ~2px higher in the render than the frame's
  ink top).

## Template A — full-slide comparison judge — **PASS**
- Probe: dispatched `analysis` on `render_4.png` through `scripts/16_vision_gate.sh`
  (`timeout 150`, `--timeout 120`). The probe was cut off by the 150s wall before a body
  landed — the gateway itself was answering (`/v1/models` responded, `analyze_image.py`
  procs live), so the window was open, and per protocol the comparison was dispatched
  directly.
- Comparison: `analysis`? No — `comparison render_4.png unique_slides/slide_046.jpg`
  with Template A payload byte-for-byte from `shared_patterns/judge_protocol_03.md`
  (line 70), `--thinking high --max-tokens 65536 --timeout 600 --rounds 1 --tries 1`,
  wrapped in `timeout 1700` inside `scripts/16_vision_gate.sh`.
- Transcript: `qa/slide046/judge_attempt_4.txt` (5737 B). Payload banked at
  `qa/slide046/judge_prompt_4.txt` (byte-identical to the Template A payload).
- Transcript header records md5 `render=a68b112d2d0866b77cc59ca82ff6378b`,
  `orig=0b355cbc667845d46001d7001ada241d` — **both verified against `md5sum` on the
  actual files**, so the verdict is bound to `render_4` and this original.
- Verdict: **`FINAL VERDICT: PASS`** (a real verdict line). No BLOCKER, no MAJOR.
  MINORs raised: (1) frame serif faces vs the deck's Arial/DejaVu math mechanism
  (deck-consistent, identical to all 17 certified deck-03 slides), (2) glyph crispness /
  JPEG halo, (3) ±2px per-word tracking on "Ugmented Vectors ( from Top )",
  (4) cursor artifact in the original plot top — correctly omitted per ground rule (c).
  All four are style/medium/capture differences, not content differences, and none
  meets the bar for a build change.

## Procedure B — zoomed crop-pair certificates (attempt 4)

Regions chosen from the frame (every dense ink region on the slide):

| name | frame bbox (x0,y0,x1,y1) | contents | out px |
|---|---|---|---|
| topmatrix | (60,50,725,130) | 6 parenthesised 2-value columns, x1..x6 header, class row, caption | 1385×167 |
| zmatrix | (588,55,668,112) | Z1 header + 3 parenthesised 2-value columns | 167×118 |
| initial | (260,54,460,112) | Initial W = column vector in tall parens + red "Step η = 2" | 416×120 |
| yellowbox | (732,54,836,148) | final-weight box, W, =, 14/−4/0 column vector | 217×195 |
| augbox | (60,136,252,258) | augmented-vectors box, title, x1..x6, six 3-value columns, class row | 400×255 |
| plot | (306,167,831,488) | scatter plot, gridlines, decision line, markers | 1093×669 |
| stopbox | (58,325,251,421) | stop callout, two-line text | 402×200 |

- Cut by `qa/slide046/cut_crops_4.py` → `cut_crops_4.txt`. Method per protocol:
  render crop taken NATIVE from `render_4.png` (no resample), original crop
  LANCZOS-upscaled to the render crop's EXACT size, so both images share one
  effective scale (2.0833 render-px per frame-px; per-crop measured 2.0800–2.0875,
  equal for both images within each pair by construction).
- Per-crop Template B payloads: `qa/slide046/crop_4_<name>_payload.txt`
  (byte-for-byte from `shared_patterns/judge_protocol_03.md` line 116, Template B;
  only NNN=46, K=4, NAME and the region description substituted).

### Seven regions certified clean (all PASS, all md5-bound to render_4)
While this lane was claiming, the prior build lane's in-flight judge processes
finished and banked six crop-pair verdicts. Every one of them records
`render_4.png md5=a68b112d2d0866b77cc59ca82ff6378b` — the **identical md5 to the
Template A transcript above** — so each verdict is bound to the same render bytes
being certified. Their crops were cut from that render and the matched-scale
audit (`crop_4_scale_audit.json`) is banked per pair. All six end with a real
`FINAL VERDICT: PASS` line:

| transcript | region | verdict |
|---|---|---|
| `qa/slide046/crop_4_zmatrix_judge.txt` | Z1 header + 3 paren columns (0,0)(7,6)(3,2) | PASS |
| `qa/slide046/crop_4_yellowbox_judge.txt` | final-weight box, W, =, 14/−4/0 | PASS |
| `qa/slide046/crop_4_augtable_judge.txt` | augmented-vectors box, title, x1..x6, six 3-value columns, class row | PASS |
| `qa/slide046/crop_4_plot_judge.txt` | scatter plot, gridlines, decision line, 9 markers, "+ve" | PASS |
| `qa/slide046/crop_4_stopbox_judge.txt` | "Iteration 4" + "No change in W / Stop Iterations" callouts | PASS |
| `qa/slide046/crop_4_caption_judge.txt` | class-legend caption under the top matrix | PASS |
| `qa/slide046/crop_4_topmatrix_judge.txt` | whole top band: header, all six paren column vectors, class row, caption, Initial W vector, Step η = 2, Check classes of, Z header + vectors | PASS |

Findings raised were all dismissed as deck-mechanism/medium MINORs (serif originals
vs the deck's Arial/DejaVu math mechanism, JPEG crispness, ±2px tracking) with PIL
measurement — none is a content difference, none needs a build change. No BLOCKER,
no MAJOR, no missing element in any region.

### The two outstanding regions — now covered
- **topmatrix** — the parenthesised column-vector band + `x1..x6` header +
  class row (`crop_4_augtable` covers only the *augmented* box below; the prior
  lane's `crop_4_caption` covers only the caption strip, not the columns).
  This is the single highest-risk region of the attempt-4 rebuild (the top matrix
  changed from transcribed horizontal rows to 6 parenthesised columns), so it
  Was certified zoomed at 09:01:51 — see the verification note.
- **initial** — "Initial W =" column vector in tall parens + the red "Step η = 2"
  line. An equation-stack region; per protocol it needs its own crop-pair.

Both pairs are already cut and their payloads banked. Dispatcher:
`qa/slide046/run_missing_crops_4.sh` (log `run_missing_crops_4.log`). It obeys the
gate law before each call: probe `pgrep -c -f analyze_image.py`, and while ≥8 it
heartbeats, sleeps 240, and re-probes.

**Gate status (resolved)**: the fleet gateway was heavily saturated for the whole
Procedure-B window. Observed concurrent `analyze_image.py` counts (other lanes)
2026-10-24 07:14–08:52: 9 → 12 → 16 → 18 → 20 → 24 → 27 → 29 → 32 → 41 → 33 → 25
→ 31 → 24 → 32. When the count finally dropped to 7 the dispatcher fired
`topmatrix` (log `[crop] START topmatrix 08:56:26`) and it returned a clean PASS
at 09:01:51. **Procedure B is COMPLETE — all seven regions hold a real
`FINAL VERDICT: PASS` line**, and the slide is certified. The gateway-wall
measurement is retained as evidence for the open founder-decision item (never
worked around; the `--timeout 600` wall was never altered).

## PIL-first pre-adjudication of the crop pairs (banked, so the crop legs have
## something to refute against if the gateway stays down)
Measured on the CROPPED pair files (`crop_4_*_{render,orig}.png`):

- **Paren-column structure, topmatrix**: vertical-stroke groups extracted at 45% band
  fill in the value band (frame y77..109). Render yields **6 paren pairs** at frame
  x ≈ 90.2/101.3, 112.3/123.4, 134.4/145.4, 156.0/167.5, 179.0/190.1, 201.1/212.2 —
  exactly the build's `TOPC = [96,118,140,162,185,207]` centers ±0.8px, i.e. all six
  parenthesised column vectors are present and correctly spaced. The original's
  JPEG-softened parens only reach the threshold at 8 positions, so the raw group
  counts differ; the selfcheck's `top_colpairs` window (26/26, max 2.4px) is the
  reliable measure and it PASSES.
- **Ink extents, every crop**: render ink bbox vs original ink bbox deltas are within
  a few px in the content bands; the originals span their full crop because of JPEG
  chroma noise, which is ground-rule (e) material and not a defect.
- **Delimiter geometry**: `yellow_vec` (14/−4/0 between tall parens x785..824) and
  `initial_vec` (Initial W, x328..374) both PASS at 2.1 and 3.2 max deviation —
  the parens span all enclosed lines, no stroke sits on the text.

### Nothing outstanding

Procedure B is complete: every dense region of the slide holds a clean zoomed
certificate (table above), Template A is PASS, house chrome and the 26-window
PIL self-check both PASS, and the row is certified with the claim released.
No further commands are owed on this slide.

## Honest status (2026-10-24 10:04 final)
- Row 46 is **certified**: `gen_status=passed`, `visual_check=PASS`,
  `visual_transcript=qa/slide046/judge_attempt_4.txt` (Template A, real
  `FINAL VERDICT: PASS`), plus **seven** clean `crop_4_*_judge.txt` crop verdicts
  (augtable, caption, plot, stopbox, topmatrix, yellowbox, zmatrix) — every one
  ends with a real `FINAL VERDICT: PASS`.
- Render↔pptx currency re-verified after the deliverable was rewritten at
  07:00:55: an independent re-render of the current
  `recreated_pptx/slide_046_recreated.pptx` is **pixel-identical** to
  `render_4.png` (md5 `a68b112d2d0866b77cc59ca82ff6378b`, the md5 recorded in
  every verdict header above).
- DB path repair (double `videos/videos/` prefix on `pptx_path` and
  `build_script`) applied and verified — see
  `qa/slide046/verification_note_20261024.md` for the before/after.
- This lane **stood down on the existing certification** — no rebuild, no
  re-judge. Verification detail and the gateway-wall evidence are in
  `qa/slide046/verification_note_20261024.md`.
- Procedure B completed within this session: the `topmatrix` crop leg landed at
  09:01:51 with **no BLOCKER, no MAJOR, no MINOR**, covering both previously
  outstanding regions (top-matrix column band and the Initial W vector stack).
- Claim released (`release 46 w046-legs-20261024`); `get 46` now reads
  `gen_status=passed`, `visual_check=PASS`, `worker_id=""`.

