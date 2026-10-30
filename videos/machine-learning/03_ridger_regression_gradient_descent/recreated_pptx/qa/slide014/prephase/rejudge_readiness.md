# Slide 014 — owner-facing ONE-COMMAND re-judge readiness (S20f prephase)

**Nothing in this pack was dispatched.** All commands below are staged for the
owner's sanctioned re-judge decision. `orig_judges/` STAGES description legs on
the ORIGINAL frame only (crop PNGs + frozen prompts + gate-aware
`dispatch_desc.sh`) — NOT dispatched; park packs spend no vision. They do not
touch the judge-attempt accounting.

## 1. Exact current build state (verified, not assumed)

| Artifact | Value |
|---|---|
| Deliverable | `recreated_pptx/slide_014_recreated.pptx` md5 `906c97ba8a365ea13d388ae11ffdd569` |
| Build source | `recreated_pptx/build/slide_014.js` (2026-10-25 w-s2 rebuild from PIL measurement) |
| Current render | `qa/slide014/render_7c.png` md5 `8f36444418649096095e3d438c3066f2`, 2001×1125 @150dpi |
| Render currency | **PROVEN by S20f (2026-10-25)**: fresh LO render of the deliverable is pixel-identical to render_7c — diff bbox None, 0 of 2,251,125 pixels differ (≥8 luma). Proof artifacts: fresh render `scratch/tmp/s20f_rendercheck_014/slide-1.png` (LO 2001×1125) + S20f PIL re-compare (same result, re-run 2026-10-25). Re-judging needs NO rebuild and NO re-render. |
| House chrome | PASS on render_7c (`chrome_reverify_3`, `house_chrome_check_rebuild` banked; strokes L/R/bottom only, top bare, badge (875.3,72.7) d32.6) |
| DB row | `gen_status=building`, `visual_check=FAIL` (by cap), `visual_attempts=7`, `worker_id=judge-s2-20261025` |

### All verified fixes banked on render_7c (attempt chain 4→7)

1. **Attempt-4 rebuild** from PIL measurement of the frame (cleared the 3
   inherited 0-ink BLOCKERs): vector boxes x80..433 / x457..810 with maroon
   `8F1220` borders y99..238; bands y243..285 + y303..341 (full-width,
   navy `1E0060` 3px rules); define-loss x90..665 y347..392 peach `F9DEC1`;
   term boxes y399..448 (left peach `F9DFC8` border `742C2D`, right pale-yellow
   `F9FEDE` border navy); final band x87..880 y469..528 pale cyan `ECFFFD`.
2. **Attempt-5 fix** (CONFIRMED finding): "(λ is a weighting factor)" merged
   INLINE into the band-2 run list (was a wrapped second line).
3. **Attempt-6 fix** (CONFIRMED finding): `eq_014_Yvec.png` recolored
   matplotlib-blue → `C00000` (original's left vector is red; left-box census
   now red 2953 px).
4. **Attempt-7 fixes** (3 REAL findings, fixed post-verdict, verified on 7c by
   doc-parse + PIL):
   - bold **underlined X** restored in "from Model Ŷ = X̲W̲" (was dropped in the
     attempt-7 rebuild);
   - vector-box label lines 18pt → **14pt** (matches measured original glyph
     height; now 2 clean lines `Original Labels` / `from Training Samples`);
   - **underlines** added on Ŷ/Y in the Define-Loss band (ink band y378..392).
5. Accepted MINORs (adjudicated, NOT fix triggers): red PNG delimiter style
   (#4, style-level, med confidence), band-1 inter-phrase gap width (#5),
   λW mathtext spacing (#7), ⋮ vs … ellipsis form.

### Attempt accounting

Attempts 1–7 all spent (1: textless shell FAIL; 2: never judged, build
superseded; 3: parked on congestion, never judged; 4,5,6,7: judged). **Attempt
7 was the last roll under the 6-cap** (`adjudicate_attempt_7.md`). The park is
a cap park with all refutable/fixable claims already resolved — so the
sanctioned re-judge, if granted, is **attempt 8** (same shape as 016's
sanctioned 7th roll = its attempt 8).

## 2. The one command (after owner sanction)

```bash
cd /home/ahmed/Projects/ai_llm_slides && pgrep -c -f analyze_image.py   # must read < 8
bash videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/prephase/rejudge_attempt8.sh legA
```

Then the 3 zoomed crop legs, ONE at a time, re-probing `pgrep -c -f
analyze_image.py < 8` before each:

```bash
bash .../qa/slide014/prephase/rejudge_attempt8.sh vectors
bash .../qa/slide014/prephase/rejudge_attempt8.sh bands
bash .../qa/slide014/prephase/rejudge_attempt8.sh final
```

(each line expanded with the full
`videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/`
prefix; run from the repo root). The script self-gates (one yield, then honest
PARK, exit 42 — never retry-loops), and on first crop use RE-CUTS the pair
from **render_7c** (the attempt-7 crops came from pre-fix render_7 and are
stale for the vectors/define-loss regions).

Payload provenance: legA sources `-p` from `qa/slide014/payload_A_7.txt`
(md5 `9387f5fbb94ef05a31db19f1e018dde1` = byte-identical to frozen Template A —
the template carries no NNN/K tokens); crops source
`payload_B_7_<mode>.txt` (md5 `978be75de7b83501d09f8f0c5576cbee` = frozen
Template B with only the `slide 014` substitution; all three identical because
the crop NAME lives in `--capture`, not the payload). S20f re-verified both
md5s on 2026-10-25. Transcript paths are FRESH (`judge_attempt_8.txt`,
`crop_8_<mode>_judge.txt`) — no banked evidence is overwritten.

## 3. Crops to re-run (regions = create_crops_7.py REGIONS, re-cut from 7c)

| Region | Frame bbox (slide space) | Covers |
|---|---|---|
| vectors | x48..910 y50..240 | both vector boxes — the label-14pt and bold-underlined-X fix zones |
| bands | x48..910 y242..347 | ridge + objective navy-ruled bands with per-phrase colors |
| final | x48..910 y462..532 | final pale-cyan band with the 2D stacked-½ formula |

## 4. What PASS / FAIL would mean

- **legA PASS + 3 crop certificates clean (or findings PIL-refuted with banked
  records)** → write certification via
  `VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py`
  : `set 14 visual_attempts 8`, `set 14 visual_check PASS`,
  `set 14 visual_transcript videos/.../qa/slide014/judge_attempt_8.txt`,
  `set 14 gen_status passed`, `heartbeat 14 <worker>`, `release 14 <worker>`;
  confirm with `get 14` (gen_status=passed, visual_check=PASS, worker_id="").
- **FAIL** → PIL-first adjudication against the baseline
  (`adjudicate_attempt_7.md` + the S20f pixel-identity proof). Findings that
  re-raise attempt-7's already-refuted claims (#1 collision, #5 gaps, #7
  spacing, ⋮) are candidates for the garbage-refutation path; genuinely NEW
  corroborated findings → fix, rebuild, re-render as render_9.png, re-cut
  crops, re-run BOTH legs — which needs a fresh owner sanction (cap exhausted).
- A judge re-flagging the red delimiters (#4, style-level) or the mandated
  2D fraction format (ground clause (e)) is not a fix trigger.

## 5. Fresh-eyes ground truth for the re-judge

`prephase/orig_judges/` STAGES 5 description legs of the ORIGINAL frame
(full + vectors + bands + terms + final; coords in `prephase/crops_manifest.json`)
— NOT dispatched (PIL-first park pack, no vision spend). Each leg = orig crop
PNG + frozen pure-description prompt + the gate-aware `prephase/dispatch_desc.sh`
runner. Run them in the unpark lane only if fresh-eyes reads are wanted;
`prephase/delta_vs_related.md` maps every element against certified 016.
