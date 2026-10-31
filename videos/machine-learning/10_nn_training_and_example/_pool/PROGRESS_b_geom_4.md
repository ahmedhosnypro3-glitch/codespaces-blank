# Lane G / scope `b_geom_4` — PROGRESS

Slides in scope: 025, 026, 027, 029, 032. Gateway-free (PIL/geometry only).

## Status

| slide | report path | state |
|---|---|---|
| 025 | `qa/slide025/geom_b_geom_4.md` | TODO |
| 026 | `qa/slide026/geom_b_geom_4.md` | TODO |
| 027 | `qa/slide027/geom_b_geom_4.md` | TODO |
| 029 | `qa/slide029/geom_b_geom_4.md` | TODO |
| 032 | `qa/slide032/geom_b_geom_4.md` | TODO |

## Established facts (do not re-derive)

- Renders banked: `_pool/tmp_geom_b_geom_4/png_<NNN>/render-1.png`, all
  2001x1125, means 226.3..228.2 (PASS dimension + non-blank checks).
- LO private profile: `_pool/lo_geom_b_geom_4/`; TMPDIR `_pool/tmp_geom_b_geom_4/`.
- **Normalization**: render 2001x1125 @150dpi -> 960x540 frame scale via
  `frame_px = render_px * 960/2001` (x) and `* 540/1125` (y).
  Cross-checks that validate this: 029 red box orig x140-833/y201-399 vs render
  x142-830/y201-397; 032 panels match within 2px; 027 diagram/Forward/calc boxes
  within 1.5px.
- Originals are 960x540 **video captures with white letterbox**: slide area is
  frame x38..921, y43..539; the original carries its own thin red border
  (v-cols x38-39 & x919-920, bottom h-rows y537-539, top edge ~y43) and its own
  yellow badge near x872-915, y52-91.
- House chrome to EXCLUDE from both sides (never a finding): outer red frame
  (0.15in inset), yellow badge (x=12.48,y=0.30,0.5x0.5in), title box
  (x=0.6,y=0.28,w=12.13 centred).
- Tolerance: ~4 px @150dpi == ~2 px at 960x540 frame scale.

## Tooling written (this lane)

- `_pool/geom_core_b_geom_4.py` — measurement engine
- `_pool/geom_spec_b_geom_4.py` — per-slide element specs
- `_pool/geom_run_b_geom_4.py` — runner -> JSON + text
- `_pool/geom_fiducial_b_geom_4.py`, `geom_fine_b_geom_4.py`,
  `geom_blocks_b_geom_4.py`, `geom_regions_b_geom_4.py`,
  `geom_measure_b_geom_4.py`, `geom_verify_b_geom_4.py`,
  `geom_declared_b_geom_4.py`, `geom_probe_b_geom_4.py`,
  `geom_scan_b_geom_4.py`, `geom_colorsample_b_geom_4.py`,
  `geom_color_b_geom_4.py` — calibration probes (kept as evidence)
