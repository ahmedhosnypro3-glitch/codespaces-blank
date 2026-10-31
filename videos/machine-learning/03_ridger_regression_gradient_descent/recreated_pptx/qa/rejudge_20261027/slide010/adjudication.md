# Adjudication 2026-10-31 — slide010 CROP FAIL (crop_dense_judge_retry.txt) — DISMISSED

Read-only PIL-first adjudication, crop pair `crop_dense_render.png` vs `crop_dense_orig.png`
(592x434, matched effective scale; slide-space region x60-344 y304-512 of the left panel).
Helper output: `adjudication_010_crop.txt`.

| claim | sev | disposition | key pixel evidence (slide-space px) |
|---|---|---|---|
| 1 orange dataset does not coincide (points shifted) | MAJOR | REFUTED | all 7 orange point clusters in the crop match within ~0.5 px: render (176.1,380.4) (188.1,355.4) (233.3,361.9) (242.2,327.3) (260.1,333.3) (293.7,333.4) (328.3,331.7) vs orig (175.9,380.1) (187.8,355.2) (233.1,361.3) (242.4,327.1) (260.5,333.0) (293.4,333.1) (327.9,331.3); analysis records 12 points with CC-measured centres |
| 2 fitted blue line geometry differs (IMG1 steeper, ~48deg vs ~43deg) | MAJOR | REFUTED | measured line slopes in slide space: render -0.5123 (27.1 deg, x141-234 in crop, resid std 0.17) vs orig -0.53 from clean columns (x150 y348.5 -> x230 y306 => -0.531); analysis verbatim: left line (142,352)->(432,200) = slope -0.524. Render matches the recorded original geometry; the judge's angles are not reproducible and its direction claim is reversed. Naive orig fit (-0.65) is contaminated by blue ink at x97-140 y430-470 (non-line) |
| 3 blue line heavier in render | MINOR | advisory | build line width 2pt vs ~1-2px ink in frame; style-level, not FAIL-sustaining |
| 4 residual dashes shifted / extra dash | MINOR | REFUTED as defect | dashes anchor to the points, which match within 0.5 px; no orphan dash measurable |

Net: both MAJORs refuted by pixels; only MINOR/advisory items remain. Per judge_protocol_03
the crop leg is adjudicated CLEAN. CROP FAIL DISMISSED 2026-10-31. FULL leg PASS
(judge_full_retry.txt). No reopen, no rebuild, no edits to deck pptx/build/DB. No git.
