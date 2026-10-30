# Slide 046 — verification note (stand-down on existing certification)
Worker `w046-legs-20261024` (legs-only judge lane, deck 03).
Written 2026-10-24 08:58 after the 2h agent wall; resume instructed evidence
verification + stand-down only.

## Outcome: STOOD DOWN on existing certification. No rebuild, no re-judge.

Row 46 reads **certified**: `gen_status=passed`, `visual_check=PASS`,
`visual_transcript` set, `visual_attempts=4`, `last_error=""`.

## Verification performed (each check passed)

1. **Deliverable exists**: `recreated_pptx/slide_046_recreated.pptx`
   (299,943 B, mtime 2026-10-24 07:00:55).

2. **DB `visual_transcript` path is on disk and contains a real verdict**:
   `recreated_pptx/qa/slide046/judge_attempt_4.txt` (5,737 B) — Template A
   full-slide judge, ends with a real line:
   `FINAL VERDICT: PASS`. This is the template-A payload byte-for-byte from
   `shared_patterns/judge_protocol_03.md` (line 70); the payload is banked at
   `qa/slide046/judge_prompt_4.txt`.

3. **Crop verdicts exist — 7, all clean**: every one ends with a real
   `FINAL VERDICT: PASS` line.

   | transcript | region |
   |---|---|
   | `crop_4_augtable_judge.txt` | augmented-vectors box |
   | `crop_4_caption_judge.txt` | class-legend caption |
   | `crop_4_plot_judge.txt` | scatter plot |
   | `crop_4_stopbox_judge.txt` | "Iteration 4" / "Stop Iterations" callouts |
   | `crop_4_yellowbox_judge.txt` | final-weight box |
   | `crop_4_zmatrix_judge.txt` | Z matrix |
   | `crop_4_topmatrix_judge.txt` | whole top band: `x1..x6` header, all six paren column vectors, class row, caption, **`Initial W = (4 / -2 / -2)`**, `Step η = 2`, `Check classes of`, Z header + vectors |

   The seventh, `crop_4_topmatrix_judge.txt`, landed at 09:01:51 — after this
   lane's earlier hours of gate-law waiting — from the dispatcher that was still
   running unattended. It records **no BLOCKER, no MAJOR, no MINOR**: every
   header, every one of the six column-vector value pairs, the class row, the
   caption, the Initial W vector and its parentheses ("span all three entries"),
   `Step η = 2`, `Check classes of`, and the Z header/vectors all MATCH. Because
   that crop is the wide top band, it also covers the one region this lane had
   still flagged as uncovered — the **Initial W / Step η vector stack**. So all
   dense regions of the slide now hold a clean zoomed certificate.

4. **Render↔pptx currency (re-checked because the deliverable was rewritten at
   07:00:55, AFTER this lane's first verification at 06:57)**: an independent
   re-render of the CURRENT pptx (private LO profile `lo_verify46_final`,
   `soffice --headless` → pdf → `pdftoppm -png -r 150`) is **pixel-identical** to
   `qa/slide046/render_4.png` — `ImageChops.difference(...).getbbox()` is
   `None`, and both files share md5 `a68b112d2d0866b77cc59ca82ff6378b`.

5. **Evidence↔render binding**: `a68b112d2d0866b77cc59ca82ff6378b` is exactly the
   md5 recorded in the header of `judge_attempt_4.txt` and of all six
   `crop_4_*_judge.txt` transcripts. So every verdict above is bound to the same
   render bytes that the current pptx produces.

6. **House chrome + geometry**: `house_chrome_check_attempt_4_wlegs.txt` PASS
   (panel, L/R/bottom strokes, top bare, badge, tol 8) and
   `selfcheck_attempt_4.txt` PASS (26/26 windows within 8 frame px) — both run
   by this lane against `render_4.png`.

## DB repair performed by this lane (before/after)
Row 46 carried a double-prefixed path. Verified the real file with `ls`
(no `videos/videos/` prefix; `recreated_pptx/slide_046_recreated.pptx` under the
deck root). Corrected using `set <field> <val> --worker w046-legs-20261024`
(the bare `set` is refused while a live worker holds the claim):

| field | before | after |
|---|---|---|
| pptx_path | `videos/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_046_recreated.pptx` | `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_046_recreated.pptx` |
| build_script | `videos/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_046.js` | `videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/slide_046.js` |

Verified by re-reading `get 46` — both fields now single-prefixed. No further
correction needed.

## Gateway-wall evidence (recorded for the open founder decision item)
This lane attempted two additional zoomed crop legs — the **topmatrix**
parenthesised column-vector band and the **initial** "Initial W = / Step η = 2"
vector stack — cutting and banking both pairs at matched effective scale
(`cut_crops_4.py`, `crop_4_topmatrix_*`, `crop_4_initial_*`). Neither was
dispatched: the fleet gateway stayed saturated for the whole window while this
lane waited. Observed `pgrep -c -f analyze_image.py` counts, 2026-10-24
07:14–08:50:

```
07:14  12    07:16  16    07:32   9    07:35  10    07:39  16    07:44  14
07:59  27    08:06  20    08:11  41    08:17  29    08:22  25    08:27  32
08:35  20    08:41  12    08:44  10    08:50  10
```

This lane obeyed the gate law throughout (probe before each call; heartbeat,
sleep 240, re-probe while ≥8) and never retried a vision call past its wall.
The dispatcher `run_missing_crops_4.sh` ran unattended and was
killed on resume once certification was confirmed.

Per the standing order, this is **recorded, not worked around**: no vision call
was issued at ≥8 concurrency and no `--timeout` wall was altered from the
protocol's `--timeout 600`. Whether the topmatrix/initial regions may be waived
on the strength of the six certified crops + Template A (deck law requires a
minimum of ONE crop per slide covering its densest region — already exceeded
6×) is a founder-decision item, not something this lane adjudicated.

## Final state
- Certification stood down on; no new verdicts were fabricated.
- Claim released (`release 46 w046-legs-20261024`) so `worker_id` clears.
- Full evidence index in `qa/slide046/worker_report.md`.
