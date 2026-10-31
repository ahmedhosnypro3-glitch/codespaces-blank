# Deck md5 audit — 03_ridger_regression_gradient_descent (rejudge_20261027 wave)

- Audit run: 2026-10-31T08:45:47Z (UTC), read-only; no git, no deletions, no `final_deck_tool.py update` executed.
- Ledger: `$NS/recreated_pptx/final_deck_state.json` (51 pages, events through 2026-10-31T08:26:31).
- Deck file: ledger `deck_md5` = `872284b7f41336fddf39b84ef5ddc63e`; on-disk md5 = `872284b7f41336fddf39b84ef5ddc63e` -> **MATCH**.
- Sources: disk md5 = md5sum of `$NS/recreated_pptx/slide_NNN_recreated.pptx`; DB = `$NS/slides_progress.db` (gen_status/visual_check/visual_attempts).
- Caveat: several slide pptx were rewritten by concurrent workers during this audit (OMML wrap ~08:37Z, slide 013 fix 08:19Z); disk md5s below are a snapshot at audit time and were stable across 3 re-reads ~5s apart.

**Result: 43/51 pages match; mismatched pages: [4, 5, 10, 13, 15, 21, 25, 30].**

| page | ledger source_md5 | disk md5 | match? | render_check | DB gen/visual (att) | src mtime | events tail (last 2) |
|---|---|---|---|---|---|---|---|
| 1 | `2e5fe75840168abfe052f6b41afe9f1e` | `2e5fe75840168abfe052f6b41afe9f1e` | MATCH | FAIL | passed/PASS (att 2) | 10-27 16:24 | 10-31T07:47 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 2 | `2abe6240bef59a9573b24f13af134d44` | `2abe6240bef59a9573b24f13af134d44` | MATCH | FAIL | passed/PASS (att 2) | 10-27 16:24 | 10-31T07:47 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 3 | `42248b9ddfc7725abd09be0a593092b7` | `42248b9ddfc7725abd09be0a593092b7` | MATCH | FAIL | passed/PASS (att 35) | 10-27 16:24 | 10-31T07:47 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 4 | `761bcac779b717283a562386447856c9` | `f65fd3007566b26ba7c36894692c2ad0` | DIFF | FAIL | passed/PASS (att 10) | 10-31 08:37 | 10-31T07:47 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 5 | `03b77ff50b9b0764d4f0b5c77a2604c4` | `c72f0be14ff279b19a993dae0e11a568` | DIFF | FAIL | passed/PASS (att 15) | 10-31 08:37 | 10-31T07:47 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 6 | `ee8d5b547eca67f71e94ee64996006b3` | `ee8d5b547eca67f71e94ee64996006b3` | MATCH | FAIL | passed/PASS (att 2) | 10-27 16:24 | 10-31T07:47 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 7 | `0f4e5544536b8f837bfa9347bdc56d41` | `0f4e5544536b8f837bfa9347bdc56d41` | MATCH | FAIL | passed/PASS (att 3) | 10-27 16:24 | 10-31T07:47 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 8 | `a8c49f182c8310121793a44fad153730` | `a8c49f182c8310121793a44fad153730` | MATCH | FAIL | passed/PASS (att 4) | 10-27 16:24 | 10-31T07:47 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 9 | `0003d2cbb6f3717154a5eef9df3de8c2` | `0003d2cbb6f3717154a5eef9df3de8c2` | MATCH | FAIL | passed/PASS (att 7) | 10-27 16:24 | 10-31T07:47 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 10 | `9b4ee43ad50f90f09df108c1645c4d26` | `67b341efaf3ac298c9b5cba604e97881` | DIFF | FAIL | passed/PASS (att 3) | 10-27 16:24 | 10-31T07:47 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 11 | `07d246aabbaeaa9c635545889b3464ea` | `07d246aabbaeaa9c635545889b3464ea` | MATCH | FAIL | passed/PASS (att 2) | 10-27 16:24 | 10-31T07:54 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 12 | `c65c53b5e1dae8dd23516c1adc28a8f2` | `c65c53b5e1dae8dd23516c1adc28a8f2` | MATCH | FAIL | passed/PASS (att 4) | 10-27 16:24 | 10-31T07:54 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 13 | `468d84817c02b4ffe703b2f87cc5ea40` | `244dde61917015d674f650242fa92ae3` | DIFF | FAIL | passed/PASS (att 6) | 10-31 08:19 | 10-31T07:54 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 14 | `18a724a03609dcf4a84ce81750ec2abe` | `18a724a03609dcf4a84ce81750ec2abe` | MATCH | FAIL | passed/PASS (att 8) | 10-31 06:31 | 10-31T08:02 render-check=PASS; 10-31T08:44 render-check=FAIL |
| 15 | `39dc053a3a4ca2d75da8081daec3f5d2` | `b6b3a99d9afb17f28cf8ad889eadc473` | DIFF | FAIL | passed/PASS (att 7) | 10-31 08:37 | 10-31T07:54 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 16 | `d4b1c0e80bf22325441f0d427ae836a6` | `d4b1c0e80bf22325441f0d427ae836a6` | MATCH | FAIL | passed/PASS (att 9) | 10-27 16:24 | 10-31T07:54 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 17 | `db7e79028abb0c39b6259e4dc689f2c5` | `db7e79028abb0c39b6259e4dc689f2c5` | MATCH | FAIL | passed/PASS (att 5) | 10-27 16:24 | 10-31T07:54 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 18 | `9ae2d3b960b2a08bf6f762d913c6fe49` | `9ae2d3b960b2a08bf6f762d913c6fe49` | MATCH | FAIL | passed/PASS (att 5) | 10-27 16:24 | 10-31T07:54 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 19 | `e7da1c782adc886ed2845d1e54ba8d82` | `e7da1c782adc886ed2845d1e54ba8d82` | MATCH | FAIL | passed/PASS (att 0) | 10-31 07:03 | 10-31T08:02 render-check=PASS; 10-31T08:44 render-check=FAIL |
| 20 | `ae9f5fa5a6e92842bbddb98aa9006c4b` | `ae9f5fa5a6e92842bbddb98aa9006c4b` | MATCH | FAIL | passed/PASS (att 4) | 10-27 16:24 | 10-31T07:54 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 21 | `c094b309d669b7561dc27fc6f9802511` | `9099303fa50a5280d9a9adea43a2e430` | DIFF | FAIL | passed/PASS (att 13) | 10-31 08:37 | 10-31T08:02 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 22 | `67eb3387b886e44f2a1190ce5ae83592` | `67eb3387b886e44f2a1190ce5ae83592` | MATCH | FAIL | passed/PASS (att 2) | 10-27 16:24 | 10-31T08:02 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 23 | `8015445ba6de72d21bffb4f6836d5b81` | `8015445ba6de72d21bffb4f6836d5b81` | MATCH | FAIL | passed/PASS (att 8) | 10-27 16:24 | 10-31T08:02 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 24 | `085290299267b3929d1dd917cc2c3fe8` | `085290299267b3929d1dd917cc2c3fe8` | MATCH | FAIL | passed/PASS (att 3) | 10-27 16:24 | 10-31T08:02 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 25 | `8a355c242807bcdac9574b941dcf85f5` | `c50e78bf39531523dcf69d652254b647` | DIFF | FAIL | building/- (att 4) | 10-31 07:37 | 10-31T08:02 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 26 | `93dbb4bd80f988706db86da3f5e291c1` | `93dbb4bd80f988706db86da3f5e291c1` | MATCH | FAIL | passed/PASS (att 6) | 10-27 16:24 | 10-31T08:02 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 27 | `577046d241cf66c21301179f9d903611` | `577046d241cf66c21301179f9d903611` | MATCH | FAIL | passed/PASS (att 11) | 10-27 16:24 | 10-31T08:02 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 28 | `cba49e51d031a37a9d8f003bbfee95a5` | `cba49e51d031a37a9d8f003bbfee95a5` | MATCH | FAIL | passed/PASS (att 9) | 10-27 16:24 | 10-31T08:02 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 29 | `68c5814414e591251b0d382494796b89` | `68c5814414e591251b0d382494796b89` | MATCH | FAIL | passed/PASS (att 2) | 10-27 16:24 | 10-31T08:02 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 30 | `bbb6a6345ed77601baf3631c3268dee7` | `c48f8fa3a74f880a1f54d0a0b97236ca` | DIFF | FAIL | passed/PASS (att 25) | 10-31 08:37 | 10-31T08:02 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 31 | `c650aa102da5473b4690adb7b5c0840e` | `c650aa102da5473b4690adb7b5c0840e` | MATCH | FAIL | passed/PASS (att 34) | 10-27 16:24 | 10-31T08:05 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 32 | `6c544c9299dd421e85201f3f0a5ae074` | `6c544c9299dd421e85201f3f0a5ae074` | MATCH | FAIL | passed/PASS (att 25) | 10-27 16:24 | 10-31T08:05 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 33 | `655eb34ed827f01e499eda9ed1097f0e` | `655eb34ed827f01e499eda9ed1097f0e` | MATCH | FAIL | passed/PASS (att 25) | 10-31 04:52 | 10-31T08:19 render-check=PASS; 10-31T08:44 render-check=FAIL |
| 34 | `00029ccfc4cc2ac5a79318b0d7796f3e` | `00029ccfc4cc2ac5a79318b0d7796f3e` | MATCH | FAIL | passed/PASS (att 3) | 10-27 23:02 | 10-31T08:05 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 35 | `ac7ccad3321716d49315a4541b7f0b32` | `ac7ccad3321716d49315a4541b7f0b32` | MATCH | FAIL | passed/PASS (att 1) | 10-27 16:24 | 10-31T08:05 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 36 | `ee60a2abd2eedcf665b241ff3f594f49` | `ee60a2abd2eedcf665b241ff3f594f49` | MATCH | FAIL | passed/PASS (att 8) | 10-27 16:24 | 10-31T08:05 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 37 | `39fb487c9a48772c711e330626ffc40c` | `39fb487c9a48772c711e330626ffc40c` | MATCH | FAIL | passed/PASS (att 6) | 10-27 16:24 | 10-31T08:05 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 38 | `8037d317792d8921d77d5bc843f9f4b3` | `8037d317792d8921d77d5bc843f9f4b3` | MATCH | FAIL | passed/PASS (att 2) | 10-27 16:24 | 10-31T08:05 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 39 | `f91f80995c1875596e696aef9b780479` | `f91f80995c1875596e696aef9b780479` | MATCH | FAIL | passed/PASS (att 3) | 10-27 16:24 | 10-31T08:05 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 40 | `7d859ee249570cd771d556b195c517ed` | `7d859ee249570cd771d556b195c517ed` | MATCH | FAIL | passed/PASS (att 4) | 10-27 16:24 | 10-31T08:05 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 41 | `b4575a48f98a17d2b9794d6bfbaef5eb` | `b4575a48f98a17d2b9794d6bfbaef5eb` | MATCH | FAIL | passed/PASS (att 5) | 10-27 16:24 | 10-31T08:14 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 42 | `e3c8f38013575843ccedba7fd550928a` | `e3c8f38013575843ccedba7fd550928a` | MATCH | FAIL | passed/PASS (att 25) | 10-27 16:24 | 10-31T08:14 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 43 | `0a978ee3ea2dd41632c9230c6158e80d` | `0a978ee3ea2dd41632c9230c6158e80d` | MATCH | FAIL | passed/PASS (att 1) | 10-30 21:54 | 10-31T08:14 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 44 | `ccd2f9378556979ef9bb972a0aa5c9b9` | `ccd2f9378556979ef9bb972a0aa5c9b9` | MATCH | FAIL | passed/PASS (att 0) | 10-30 22:03 | 10-31T08:14 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 45 | `83e7cc61f1bb636f57ceb41a0994c5e2` | `83e7cc61f1bb636f57ceb41a0994c5e2` | MATCH | FAIL | passed/PASS (att 4) | 10-27 16:24 | 10-31T08:14 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 46 | `29cafaafa8b1234a6f063a6a2c909706` | `29cafaafa8b1234a6f063a6a2c909706` | MATCH | FAIL | passed/PASS (att 4) | 10-27 16:24 | 10-31T08:14 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 47 | `fcfd2713e095d8ad9e26459ac0035776` | `fcfd2713e095d8ad9e26459ac0035776` | MATCH | FAIL | passed/PASS (att 6) | 10-27 16:24 | 10-31T08:14 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 48 | `e5cfcf57546a1ea7c353028a0d8bddc7` | `e5cfcf57546a1ea7c353028a0d8bddc7` | MATCH | FAIL | passed/PASS (att 0) | 10-30 21:54 | 10-31T08:14 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 49 | `5917ea7de132b26692eda26a76a6fcfb` | `5917ea7de132b26692eda26a76a6fcfb` | MATCH | FAIL | passed/PASS (att 18) | 10-27 16:24 | 10-31T08:14 render-check=FAIL; 10-31T08:44 render-check=FAIL |
| 50 | `503cc992efd4d0e38a236dbc849af485` | `503cc992efd4d0e38a236dbc849af485` | MATCH | FAIL | passed/PASS (att 20) | 10-27 16:24 | 10-31T08:19 render-check=PASS; 10-31T08:44 render-check=FAIL |
| 51 | `210712ebf0abea3b5804530f954ba32c` | `210712ebf0abea3b5804530f954ba32c` | MATCH | FAIL | passed/PASS (att 5) | 10-31 04:29 | 10-31T08:26 update-page md5=210712eb; 10-31T08:44 render-check=FAIL |

## Mismatch analysis (task step 2)

| page | reason (from events + evidence) | on-disk pptx judge-certified (DB visual_check)? | disposition |
|---|---|---|---|
| 4 | OMML wrap landed in place at ~08:37Z (`OMML_WRAP_LOG.md`: 4d21712f -> f65fd300, 1 of 4 eq rel ids wrapped, 3 skipped fail-loud on \underline/\mathbf; earlier wrap precondition had failed so it was deliberately not restaged at ledger time). Ledger still holds pre-wrap 761bcac7. | PASS (att 10) | restage (see restage_plan.md) |
| 5 | OMML wrap in place ~08:37Z (03b77ff5 -> c72f0be1, 8 of 9 rel ids wrapped, rId7 skipped; 0 px vs banked pdf). | PASS (att 15) | restage |
| 10 | On-disk file stable since 2026-10-27 (67b341ef); pptx has **no ppt/media at all** (0 eq images, 0 AlternateContent) — nothing to OMML-wrap; drift is a pre-wrap-era rebuild, deliberately skipped per instruction. | PASS (att 3) | SKIP — no restage |
| 13 | Rebuilt 2026-10-31 08:19Z with the r18 PIL-confirmed fix (row-label column X1/X2/y in the three TEST tables; build/slide_013.js header; pre-fix backup `$RJ/slide013/slide_013_recreated.pre_fix_20261031.pptx` md5 == ledger 468d8481 exactly). No update-page event after the rebuild -> ledger stale. | PASS (att 6) | restage |
| 15 | OMML wrap in place ~08:37Z (39dc053a -> b6b3a99d, 1 of 9 rel ids wrapped; 0 px vs banked pdf). | PASS (att 7) | restage |
| 21 | OMML wrap in place ~08:37Z (c094b309 -> 9099303f, 5 of 6 rel ids wrapped; 0 px vs banked pdf). | PASS (att 13) | restage |
| 25 | In flux: deck page gate FAIL since 02:55Z (19.36% px, bbox 172,138,1834,1107); on-disk c50e78bf (mtime 07:37) != ledger 8a355c24; rejudge k17z2/k17z3 legs in flight at audit time. DB: gen_status=building, visual_check EMPTY (att 4) — only non-passed row in the DB. | **NO — not certified** | **BLOCKED** until DB shows passed/PASS |
| 30 | OMML wrap in place ~08:37Z (bbb6a634 -> c48f8fa3, 2 of 2 rel ids wrapped; 0 px vs banked pdf). | PASS (att 25) | restage |

## render_check PASS consistency (task step 4)

| page | ledger md5 == disk md5? | PASS evidence | status at audit time |
|---|---|---|---|
| 14 | yes (18a724a0) | PASS 08:02:56 gate_20261031-075342_p14-19-33-51 (0 px); re-PASS 08:02:49 gate_..._080104_p14 | consistent; md5 still matches, but the 08:44:56 full-deck gate re-marked render_check=FAIL |
| 19 | yes (e7da1c78) | PASS 07:57:24 gate_..._075246_p19 + 08:02:56 gate_..._075342 (0 px) | consistent; same 08:44:56 re-mark |
| 33 | yes (655eb34e) | PASS 08:19:31 watcherA re-mark; gate_20261031-080637_p33-50-51 (0 px) + 07:59:22 gate_..._075444_p33 | consistent; same 08:44:56 re-mark |
| 50 | yes (503cc992) | PASS 08:19:31 re-mark; gate_20261031-080637_p33-50-51 (0 px) | consistent; same 08:44:56 re-mark |
| 51 | yes (210712eb) | PASS 08:15:53 gate_..._081426_p51 + 08:19:31 re-mark; 08:26:31 update-page re-staged identical md5 (render_check reset to PENDING, then FAIL by 08:44:56 gate) | md5-consistent — needs only a re-gate, not a restage |

Note on the 08:44:56 event: a full-deck `render-check` (all 51 pages, result FAIL, mismatched [1, 3, 4, 7, 12, 13, 23, 25, 27, 36, 37, 46, 49]) ran while this audit was being written and overwrote every page's `render_check` mark to FAIL in the live ledger. The per-page PASS gates above remain valid 0-px evidence; the 08:44 mismatches are expected for the un-restaged drifted pages (13 is in the list; 5/15/21/30 are not, because their OMML wraps render pixel-identical under LO via mc:Fallback) plus known deck-gate debt on 1/3/7/12/23/27/36/37/46/49/25. The audit table's render_check column reflects the ledger as re-read at 08:45:47Z (post-08:44:56).

DB census at audit time: 50/51 rows `gen_status=passed` + `visual_check=PASS`; only slide 25 is `building`/empty (att 4, last_error = rejudge 2026-10-27 wave FULL=FAIL CROP=FAIL, deck page gate FAIL, fix in progress).
