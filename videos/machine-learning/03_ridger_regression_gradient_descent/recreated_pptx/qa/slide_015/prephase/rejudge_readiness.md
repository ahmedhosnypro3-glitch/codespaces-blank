# Slide 015 — owner-facing ONE-COMMAND re-judge readiness (S20f prephase)

**Nothing in this pack was dispatched.** All commands below are staged for the
owner's sanctioned re-judge decision. `orig_judges/` STAGES description legs on
the ORIGINAL frame only (crop PNGs + frozen prompts + gate-aware
`dispatch_desc.sh`) — NOT dispatched; park packs spend no vision. They do not
touch the judge-attempt accounting.

## 1. Exact current build state (verified, not assumed)

| Artifact | Value |
|---|---|
| Deliverable | `recreated_pptx/slide_015_recreated.pptx` md5 `1bc9cd265612bfe7ff37f56466c8ecf4` |
| Build source | `recreated_pptx/build/slide_015.js` (PIL-measured geometry; mathtext PNG equations via `build/assets/eq015_table.json`) |
| Current render | `qa/slide_015/render_4.png` md5 `0019627f1ec094510c369801269762d3`, 2001×1125 @150dpi |
| Render currency | **PROVEN**: fresh LO render of the deliverable is md5-identical to render_4 (banked attempt-4 adjudication, `adjudicate_attempt_4.md` header). Re-judging needs NO rebuild and NO re-render. S20f re-verified the md5 on 2026-10-25. |
| House chrome | PASS (`house_chrome_check_2.txt` / re-run on render_4, banked in worker report) |
| Containment | 0 spills (`containment_4.txt`) |
| DB row | `gen_status=building`, `visual_check=null`, `visual_attempts=0`, `worker_id=judge-s2-20261025` (park note in `last_error`) |

### Attempt-4 refutation summary (why it is parked; what the re-judge must get past)

Attempt-4 legA ran on the CURRENT bytes and returned three consecutive
FINAL VERDICT: FAIL bodies whose claims were all refuted by pixel/doc-parse
measurement (`qa/slide_015/adjudicate_attempt_4.md`; refuted transcripts
`judge_attempt_4_refuted_garbage.txt`, `..._garbage2.txt`, third body
`judge_attempt_4.txt`):

1. "green term on an extra visual line" — REFUTED: the ½ is a full-height
   STACKED handwritten fraction in the ORIGINAL (1 y167..181, bar y187..189,
   2 y194..208 at x166..200); mathtext \frac is the same stacked 2D form; green
   ink is INSIDE each line's dark band in both images (L1 131..153 within
   105..153, L2 189..213 within 164..213, L3 242..265 within 217..265).
2. "missing ⇒ arrow" — REFUTED: gap x501..547 over y466..521 is ZERO-ink in the
   original (`adjudicate_arrow.txt`); the render correctly has none.
3. "missing underlines on Y variables" — REFUTED: the horizontal runs are the
   base bars of the stacked ½ (4 runs L1 x173/345/474/696 y148..150; 2+2 in
   L2/L3); the zoomed Y at x412..418 has no stroke beneath it; \underline{W}
   already covers the only real underlines.
4. (3rd body) "duplicated blue J(W)" — REFUTED: ink census = exactly ONE J(W)
   cluster per line; "text/boundary collisions" — REFUTED: containment_015.py
   = 0 spills.

Accounting: **judge attempts spent 1 of 6** (attempt 4); **garbage re-invokes
3 of 3 BURNED**. The park is a no-coherent-verdict park, NOT a cap park.

## 2. The one command (after owner sanction)

Leg A — full-slide judge, attempt 5 (payload byte-exact, only transcript/view
re-pointed; the banked garbage-3 transcript is preserved, not overwritten):

```bash
cd /home/ahmed/Projects/ai_llm_slides && pgrep -c -f analyze_image.py   # must read < 8
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/prephase/rejudge5_judgeA.txt
```

Then the 5 zoomed crop legs, ONE at a time, re-probing `pgrep -c -f
analyze_image.py < 8` before each (crop images crop_4_* are still VALID — cut
from render_4 which is the current bytes; no re-cut needed):

```bash
bash .../qa/slide_015/prephase/rejudge5_crop_eq_stack.txt
bash .../qa/slide_015/prephase/rejudge5_crop_pinkbox.txt
bash .../qa/slide_015/prephase/rejudge5_crop_peachbox.txt
bash .../qa/slide_015/prephase/rejudge5_crop_deriv_stack.txt
bash .../qa/slide_015/prephase/rejudge5_crop_solution.txt
```

(each line expanded with the full
`videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/`
prefix; run from the repo root).

Payload provenance: every staged file's `-p` payload was byte-compared against
the attempt-4 banked dispatch (`dispatch_4_judgeA.txt` /
`dispatch_4_crop_<slug>.txt`), which `gen_dispatch_4.py` byte-checked against
the frozen `shared_patterns/judge_protocol_03.md` — only `--transcript` paths
(`judge_attempt_4`→`judge_attempt_5`, `crop_4_`→`crop_5_`) and the `--view`
strings (attempt 4→5) differ. **Do NOT use `dispatch_driver_4.sh`** — its
`load()` integer test is buggy and sleep-loops (park note in DB `last_error`).

## 3. Crops to re-run (already cut, matched effective scale ~2.083 px/frame-px)

| Region | Frame bbox | Files |
|---|---|---|
| eq_stack (3× J(W)) | x89..799 y100..271 | `crop_4_eq_stack_render.png` / `_orig.png` |
| pinkbox (∂J/∂W=0 + sentence) | x73..710 y268..325 | `crop_4_pinkbox_render.png` / `_orig.png` |
| peachbox (Remember + identity) | x783..898 y271..337 | `crop_4_peachbox_render.png` / `_orig.png` |
| deriv_stack (gradient steps) | x71..518 y343..475 | `crop_4_deriv_stack_render.png` / `_orig.png` |
| solution (closed-form W) | x545..893 y466..523 | `crop_4_solution_render.png` / `_orig.png` |

## 4. What PASS / FAIL would mean

- **All legs PASS (or every finding PIL-refuted with banked refutation
  records)** → write certification via
  `VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py`
  : `set 15 visual_attempts 5`, `set 15 visual_check PASS`,
  `set 15 visual_transcript videos/.../qa/slide_015/judge_attempt_5.txt`,
  `set 15 gen_status passed`, `heartbeat 15 <worker>`, `release 15 <worker>`;
  confirm with `get 15` (gen_status=passed, visual_check=PASS, worker_id="").
- **FAIL with NEW findings** → PIL-first adjudication against the banked
  measurement baseline (`verify_build_4.txt`, `containment_4.txt`,
  `adjudicate_3.txt`, `adjudicate_arrow.txt`, `adjudicate_attempt_4.md`).
  Refutable → bank the refutation; a refuted-everything verdict on unchanged
  bytes is garbage — but the garbage-retry cap (3/3) is BURNED, so a fourth
  incoherent verdict goes back to the owner rather than re-rolling.
- **FAIL with a REAL finding** → fix, rebuild, re-render as render_5.png,
  RE-CUT all five crop pairs from render_5 (crop transcripts only survive if
  their region is pixel-identical across the rebuild), re-run BOTH legs at
  attempt 6. Note the two recorded geometric residuals (eq1 line widths
  w-ratio 0.87–0.90; solution w-ratio 0.76 with census 1.61) are
  containment-forced, documented in the worker report — a judge insisting on a
  filled solution box cannot be satisfied without breaking containment; that
  adjudication path is the owner's.

## 5. Fresh-eyes ground truth for the re-judge

`prephase/orig_judges/` STAGES 5 description legs of the ORIGINAL frame
(full + eq_stack + midrow + deriv_stack + normal_solution; coords in
`prephase/crops_manifest.json`) — NOT dispatched (PIL-first park pack, no
vision spend). Each leg = orig crop PNG + frozen pure-description prompt +
the gate-aware `prephase/dispatch_desc.sh` runner. If run in the unpark lane,
use them to pre-empt the known misperceptions
(stacked-½ base bars, zero-ink arrow gap, single J(W) cluster per line).
