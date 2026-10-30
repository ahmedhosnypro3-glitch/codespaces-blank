# doc-parse lane — scope_d1 (slides 8, 9, 14–21)

Worker: `worker-docparse-d1-1793139000` · claimed + completed 2026-10-27.
Lane is **advisory**: it never blocks or gates any other lane. Per-page
failures are recorded as `task-add` rows, not scope failures.

## Deliverables (canonical, untouched as the script wrote them)

| Slide | `.parse.md` bytes | `finish_reason` |
|---|---|---|
| 008 | 55 | stop |
| 009 | 453 | stop |
| 014 | 459 | stop |
| 015 | 468 | stop |
| 016 | 403 | stop |
| 017 | 509 | stop |
| 018 | 68 | stop |
| 019 | 585 | stop |
| 020 | 619 | stop |
| 021 | 394 | stop |

All 10 pairs live at `analysis/parse/slide_NNN.parse.{md,json}`. Inputs were
960×540 — under the 1664×2048 ceiling, **never upscaled**. No storm retries
were needed: every full-frame call succeeded on attempt 1.

## Crop cascades (dense / picture-only pages)

| Slide | Run dir | parse calls | crops | chat lane |
|---|---|---|---|---|
| 008 | `_pool/cascade_008` | 1/24 | 0/16 | degraded (404) |
| 009 | `_pool/cascade_009` | 3/24 | 2/16 | healthy |
| 014 | `_pool/cascade_014` | 3/24 | 2/16 | healthy |
| 018 | `_pool/cascade_018` | (root stop) | — | healthy |
| 019 | `_pool/cascade_019` | 3/24 | 2/16 | degraded (404) |
| 020 | `_pool/cascade_020` | 4/24 | 3/16 | healthy |

For 008 and 018 the automated cascade stopped at the root: the full-frame
parse carried a single `<class_Picture>` block and **no text lines**, so
`has_new_information()` had nothing to diff against. Per the playbook's
anchor law I applied targeted native-resolution crops instead
(`_pool/cascade_008/{manual,pass2}`, `_pool/cascade_018/{manual,pass2,pass4}`).

The enriched merge for each slide is `<run_dir>/composed/slide_NNN_composed.md`
(the crop-cascade contract output). Where shapes/labels only appeared in
crops, the canonical `analysis/parse` pair stays as the direct transcript.

## Residual gaps (below glyph floor — vision-reader leg, not more crops)

- **018** `Input Data` — 12 crop attempts returned empty/Picture shells.
- **014** `Error Error Error` — vertical dark-red bar text unread at any cut.
- **019** `Sample Data` — diagram label, unread.
- **020** `Node Mode`, `Output` — diagram labels, unread.

Minor notation variants (subscripts) such as 009 `Net1/Net2/O1/O2/Om` and
008 `Multi Bias`/`∂E/∂w_ij` **were** recovered in crops as `Net`, `O`,
`Read Bias`, `∂E ∂w ji`.

## Config note

`scripts/.doc-parse-config` was never read, printed, or copied. The chat
lane's 404 (`docparsechat` model not found) is an operator routing fix; the
lane completed degraded as the skill documents.
