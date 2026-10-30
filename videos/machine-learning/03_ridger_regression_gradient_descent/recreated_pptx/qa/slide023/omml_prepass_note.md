# OMML prepass note — slide 023 (scope S13, run 299640)

RESULT: WRAPPER FAIL-LOUD — deliverable NOT modified. No output file was written by
`scripts/18_omml_wrapper.py` (its safety contract), so there are no superseded bytes; the
banked backup is byte-identical to the current pptx (pre-wrap md5 8015445ba6de72d21bffb4f6836d5b81).

| step | value |
|---|---|
| wrapper exit | 1 (no output written) |
| error | `cannot convert mathtext for rId1: unsupported mathtext command: \underline` |
| root cause | sidecar `eq_023_main.json` mathtext uses `\underline` (x2); the v2 wrapper's converter supports bar/overline, hat, vec — no underline |
| contributing limit | the PNG is a multi-color composite (symbol_colors: green lambda/I, red `^{-1}`); the single-color OMML Choice could not represent it faithfully either |
| pre-wrap pptx md5 | 8015445ba6de72d21bffb4f6836d5b81 (unchanged after attempt) |
| backup | pre_omml_backup_8015445b.pptx (identical bytes) |
| manifest (banked) | omml_manifest.json (rel id rId1 re-derived from current pptx) |
| wrapper log | omml_wrap_log.txt |

Follow-up (task-added to mission run 299640): either extend the wrapper with underline support
(edge-positioned m:bar, `m:pos m:val="bot"`), or wrap the composite as multiple single-color
equations per source asset — whichever the deck owner prefers. Do NOT re-run this scope on 023
without that decision.
