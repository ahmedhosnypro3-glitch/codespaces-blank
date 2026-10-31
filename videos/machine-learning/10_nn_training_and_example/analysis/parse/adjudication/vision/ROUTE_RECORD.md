# Vision cross-check lane — route & evidence record

Adjudication scope `b_parse_2` (slides 007-012), namespace
`videos/machine-learning/10_nn_training_and_example/analysis/parse/`.
This file records the *transport* history of the parse-verification cross-check lane. A
transport failure is NO-RESULT, never a verdict.

## Route diagnosis (measured, not assumed)

| Event | Input | Result |
|---|---|---|
| `vision/probe.txt` | `unique_slides/slide_007.jpg` (JPEG), `--max-tokens 24000` | HTTP 400 `upstream_rejected_request` (Nvidia) |
| `vision/probe2_defaulttokens.txt` | same JPEG, default tokens | HTTP 400 — **not** a max-tokens issue |
| `vision/probe3_png.txt` | same frame re-saved as **PNG**, default tokens | **success** (1/1) |
| cross-check round 1 | PNG payloads | 012 exit 0; 007/009/010/011 exit 1; 008 wedged |
| cross-check round 1 detail (`prior_attempts/slide_009.vision.txt`) | PNG payload | attempt 1: `ABORT HangError hard wall-clock 450s`; attempts 2-3: HTTP 400 |

Conclusions carried into the adjudications:

1. **JPEG is rejected by the Nvidia upstream with HTTP 400.** The parse-verification lane
   must feed PNG. All cross-check inputs are re-saved from the source JPEG with no
   geometric change (960x540, `convert("RGB")`) and are banked in `vision/png/`.
2. **The 400 is intermittent and load-dependent, not payload-kind-dependent** — it recurred
   on PNG during round 1 while the identical PNG path succeeded minutes earlier on a probe
   and again on slide 012. It is route flakiness, so a failed cross-check call is re-probable
   and is recorded as NO-RESULT.
3. **Hang taxonomy:** `ABORT HangError: hard wall-clock 450s` (the script's `--timeout + 30s`
   wall) with a zero-delta stream — the documented `lane-hang` class. Round 1's `timeout 900`
   wrapper did **not** reap the wedged grandchild (bash `timeout` signals only its direct
   child; the python child survived and blocked the script), which is why round 2 uses
   `timeout --kill-after=45 700`.

## Banked artifacts

- `vision/png/slide_{007,008,009,010,011,012}.png` — cross-check inputs, PNG conversions of the
  source JPEGs (no geometry change).
- `vision/slide_012.vision.txt` — the **successful** cross-check read (round 1, exit 0);
  the only cross-check that landed before this record was written.
- `vision/prior_attempts/slide_{007,009,010,011}.vision.txt` — the failed round-1 transcripts
  (HTTP 400 / HangError), retained per "never delete banked evidence".
- `vision/run_status.log`, `vision/run_status2.log` — per-slide exit codes from the detached
  runners `run_one.sh` / `run_one2.sh` and the queues `run_queue.sh` / `run_queue2.sh`.
- `vision/p{NNN}.txt` — the exact prompt text used for each slide's cross-check (the
  "one question it was asked" required by the register).

## Corroboration policy applied to the adjudications

Cross-check transport failures do NOT downgrade an adjudication. Where the image-analysis
cross-check is a NO-RESULT, the second read is the already-banked script-12/reanalysis vision
analysis (`analysis/slide_NNN_final.json` / `analysis/reanalysis/slide_NNN_final.json`) — a
different-form read (a full vision model, not the nemotron-parse document parser) that read the
same frame. Each adjudication header names which source supplied its second read, and the
transcript path plus the one question asked are cited for successful cross-checks.
