# OMML_WRAP_PLAN_r4 — deck 03 remaining wraps (PREP ONLY, 2026-10-31)

Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`.
Derived from OMML_INVENTORY_r4.md (fresh unzip scan of all 51 current
`slide_NNN_recreated.pptx`). Wrapper contract unchanged:
`python3 scripts/18_omml_wrapper.py <in.pptx> <manifest.json> [-o out.pptx]`, rel_ids
re-derived from the CURRENT pptx at wrap time, single plain-named deliverable per slide,
never LO-resave a wrapped file, backups under `$RJ/slideNNN/*.preOMML.bak.pptx`.
No wrap was run by this plan; no pptx modified; no git touched.

## Remaining slides (15) and manifests needed

Shard ownership note: agents 392/405 own 031, 032, 037, 043, 044 "and the rest";
043 has NO eq pics embedded (sidecars only) so it is a no-op for wrapping.

| slide | remaining pics | manifest to author | mathtext source |
|---|---|---|---|
| 004 | 3 (rId1 Yvec, rId2 Yhatvec, rId4 formula) | `$RJ/slide004/omml_manifest.json` (extend agent-391's `omml_manifest_parseable_only.json`) | sidecars carry mathtext; Yvec/Yhatvec are COMPOSED (`\underline{\mathbf{Y}}` + drawn parens + pieces) — blocked, see blocker section |
| 005 | 1 (rId7 deriv2) | `$RJ/slide005/omml_manifest.json` | sidecar mathtext, `\underline` — blocked |
| 014 | 3 (rId1 Yvec, rId2 Yhatvec, rId3 final) | `$RJ/slide014/omml_manifest.json` | re-bank from build/slide_014.js (sidecars absent from build/assets; PNGs in qa/slide014/assets_backup_att10/) |
| 015 | 8 (rId1-4,6-9) | `$RJ/slide015/omml_manifest.json` | sidecar mathtext, all `\underline` — blocked |
| 021 | 1 (rId6 invexpr) | `$RJ/slide021/omml_manifest.json` | sidecar mathtext `\underline`, color=multi — blocked |
| 023 | 1 (rId1 main) | reuse banked `qa/slide023/omml_manifest.json` after rel-id re-derivation | sidecar mathtext `\underline` — blocked (prior fail-loud) |
| 031 | 1 (rId1 main) | `$RJ/slide031/omml_manifest.json` | re-bank mathtext from build/slide_031.js (sidecar geometry-only) |
| 032 | 1 (rId2 main) | `$RJ/slide032/omml_manifest.json` | re-bank from build/slide_032.js / render_curve_032.py |
| 033 | 1 (rId1 main_v7b) | `$RJ/slide033/omml_manifest.json` | re-bank from build/slide_033.js (sidecar qa/slide033/eq_033_main_v7b.json is geometry-only) |
| 034 | 1 (rId1 main) | `$RJ/slide034/omml_manifest.json` | mathtext in build/gen_eq_034.py: `f(x) = \frac{x^2 \cos(x) - x}{10}` (fontsize 18, color 000000) |
| 037 | 5 (rId1/4/5 sigma; rId2/3 frac) | `$RJ/slide037/omml_manifest.json` | re-bank; anisotropic rescale + per-instance fontsize re-derivation per qa/slide037/omml_prepass_note.md |
| 044 | 54 (48 distinct sidecars) | `$RJ/slide044/omml_manifest.json` (one entry per rel id; multi-rel sidecars repeat) | re-bank per piece from build/gen_eq_044.py + slide_044.js; per-piece colors |
| 048 | 6 (rId1-6 eq_r1_l..eq_r6_l) | `$RJ/slide048/omml_manifest.json` | re-bank from build/gen_assets_048.py |
| 050 | 4 (rId15-18) | `$RJ/slide050/omml_manifest.json` | finalW sidecar mathtext has `\underline`+`\substack` — blocked; Z1-Z3 re-bank geometry-only |
| 051 | 11 (9 distinct sidecars) | `$RJ/slide051/omml_manifest.json` | step/dzlabel_1/rowvec_1-3 sidecars already parseable (`\;` only) — wrappable now; initw/dzlabel_2-3/wcol_green re-bank |

Already done (do NOT re-wrap): 009, 030, 036, 039 fully; 004/005/015/021 partial
(agent-391 subset manifests wrapped the parseable subset only).

## `\underline` blocker — proposal

The wrapper fail-louds on `\underline` (measured on slide 023,
qa/slide023/omml_prepass_note.md; agent-391 confirmed on 004/005/015/021/050-finalW).
Affected remaining mathtext: 004 Yvec/Yhatvec, 005 deriv2, 015 (all 8), 021 invexpr,
023 main, 050 finalW. Also `\mathbf{\hat{Y}}` inside 004's COMPOSED entries.

Proposal, in order of preference:

1. **Extend the wrapper to map `\underline{X}` to native OMML `m:bar` with
   `m:barPr pos="bot"`** — that IS an underline in OMML (bar below the base), so the
   rendered math is semantically and visually identical to the PNG. This preserves
   semantics exactly and is the correct fix.
2. Do NOT pre-transform `\underline{X}` into an overline (`m:bar pos="top"` /
   `\overline{X}`): the bar moves above the symbol, which changes what the slide says —
   rejected as non-semantics-preserving.
3. If the wrapper cannot be extended in this pass, leave the `\underline` pics as plain
   PNG embeds (subset manifests, the agent-391 pattern — idempotent, a later extended
   wrapper run picks them up) and record them as an **accepted limitation per plan r3**.

## Final-deck restage list

`recreated_pptx/final_deck_state.json` maps deck page N -> `slide_NNN_recreated.pptx`
1:1 for all 51 pages (verified). The current
`03_ridger_regression_gradient_descent_final.pptx` (md5
872284b7f41336fddf39b84ef5ddc63e) has mc:AlternateContent on pages 9, 36, 39 only
(verified by unzip).

Pages needing restage after the remaining wraps land (re-merge from per-slide pptx +
re-gate): **4, 5, 14, 15, 21, 23, 30, 31, 32, 33, 34, 37, 44, 48, 50, 51** (16 pages).
Of these, 4/5/15/21/30 are already stale today (agent-391 wrapped the per-slide pptx
2026-10-31 after the deck build); 9/36/39 are already wrapped inside the deck and need
no restage.

## Remaining-slide list (handoff)

**004, 005, 014, 015, 021, 023, 031, 032, 033, 034, 037, 044, 048, 050, 051**
(101 unwrapped eq pics total; of which 12 sidecars carry `\underline`-blocked mathtext:
004x2, 005x1, 015x8, 021x1, 023x1, 050-finalWx1 — count of remaining pics on those
slides: 3+1+8+1+1+1 = 15 pics blocked on `\underline`).
