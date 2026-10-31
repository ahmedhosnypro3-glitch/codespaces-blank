# docparse_i lane status — slides 010-019 (2026-10-31, UTC)

Full-frame parse command per slide: `parse_document.py <slide_NNN.jpg> -o pool_run/docparse_i/slideNNN --timeout 300` (run from namespace root, absolute paths). All first-attempt, exit 0, `finish_reason=stop`, non-empty content — no retries needed. Cascades run only on dense slides with thin full-frame reads.

- slide_010: full-frame OK (486 chars, 145 tok, slide010/); cascade OK exit=0 (7 parse calls, 14 elements, cascade_slide010/composed/slide_010_composed.md)
- slide_011: full-frame OK (1799 chars, 437 tok, slide011/); read substantive (tables+fractions), no cascade
- slide_012: full-frame OK (1750 chars, 401 tok, slide012/); read substantive (tables+fractions), no cascade
- slide_013: full-frame OK (563 chars, 168 tok, slide013/); cascade OK exit=0 (2 parse calls, 6 elements, cascade_slide013/)
- slide_014: full-frame OK (309 chars, 83 tok, slide014/); cascade OK exit=0 (6 parse calls, 4 elements, cascade_slide014/)
- slide_015: full-frame OK (330 chars, 122 tok, slide015/); cascade OK exit=0 (3 parse calls, 3 elements, cascade_slide015/)
- slide_016: full-frame OK (333 chars, 90 tok, slide016/); cascade OK exit=0 (4 parse calls, 3 elements, cascade_slide016/)
- slide_017: full-frame OK (1379 chars, 659 tok, slide017/); chart data table captured in full, no cascade
- slide_018: full-frame OK (281 chars, 77 tok, slide018/); cascade OK exit=0 (5 parse calls, 5 elements, cascade_slide018/)
- slide_019: full-frame OK (420 chars, 110 tok, slide019/); cascade OK exit=0 (3 parse calls, 2 elements, cascade_slide019/)

Notes: probe on slide_010 green before batch (1.7s). Batches capped at 4 parse calls in flight. Chat adjudicator lane timed out intermittently during cascades (60s x up to 4 attempts per decision); all cascades completed exit 0 with degraded.chat=false. Per-call logs: slideNNN.attemptN.log, cascade_slideNNN.log, cascade run dirs contain run.log/manifest.json.
