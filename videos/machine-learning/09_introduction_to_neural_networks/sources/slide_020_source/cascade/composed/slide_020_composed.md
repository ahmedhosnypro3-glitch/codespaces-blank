# Composed parse: slide_020

- source frame: `slide_020.jpg` (md5 `2e775ec9db544a8bcf1470b43d87c7a5`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 5 (dedup collapsed 1) · crops: 5 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=36, y=41, w=887, h=476) — from full/slide_020.parse.md (level 0)
  <chart type="compound_panel"> title: Saturation Problem in Activation Functions panel: p1 ; line panel: p2 ; multi_line axis[p1.x]: F (x) = Parametric ReLU axis[p1.y]: f axis[p2.x]: x legend[color]: items=x = R.I ; x = R.F ; x = R.B ; x = S.R bind: f ; p1 ; y bind: x = R.I ; p1 ; x bind: x = R.F ; p1 ; x bind: x = R.B ; p1 ; x bind: x = S.R ; p1 ; y table[p1]: | f | x = R.I | x = R.F | x = R.B | x = S.R | | --- | --- | --- | --- | --- | | -3 | 0 | 0 | 0 | 0 | | -2 | 0 | 0 | 0 | 0 | | 0 | 0 | 0 | 0 | 0 | | 1 | 0.5 | 0 | 0 | 0 | | 2 | 1 | 0 | 0 | 0 | table[p2]: | x | x = R.I | x = R.F | x = R.B | x = S.R | | --- | --- | --- | --- | --- | | -3 | -0.2 | 0 | 0 | 0 | | -2 | 0 | 0 | 0 | 0 | | -1 | 0 | 0 | 0 | 0 | | 0 | 0 | 0 | 0 | 0 | | 1 | 1 | 0 | 0 | 0 | | 2 | 2 | 0 | 0 | 0 | </chart>
- `<class_Chart>` @(x=36, y=41, w=884, h=475) — from crops/slide_020.crop01__chart.parse.md (level 1)
  <chart type="compound_panel"> title: Saturation Problem in Activation Functions panel: p1 ; line panel: p2 ; multi_line axis[p1.x]: x axis[p1.y]: f legend[color]: items=z = 0.1 ; z = 0.2 ; z = 0.3 ; z = 1.0 bind: x ; p1 ; x bind: z = 0.1 ; p1 ; y bind: z = 0.2 ; p1 ; y bind: z = 0.3 ; p1 ; y bind: z = 1.0 ; p1 ; y annotation: reference_line ; value=0 ; axis=y table[p1]: | x | z = 0.1 | z = 0.2 | z = 0.3 | z = 1.0 | | --- | --- | --- | --- | --- | | -4 | 0 | 0 | 0 | 0 | | -2 | 0.1 | 0.1 | 0.1 | 0.1 | | 0 | 0 | 0 | 0 | 0 | | 2 | 2 | 2 | 2 | 2 | | 5 | 4 | 4 | 4 | 4 | table[p2]: | x | z = 0.1 | z = 0.2 | z = 0.3 | z = 1.0 | | --- | --- | --- | --- | --- | | -3 | -0.2 | -0.3 | -0.3 | -1 | | -2 | -0.1 | -0.2 | -0.1 | -0.8 | | -1 | 0 | 0 | 0 | 0 | | 0 | 0 | 0 | 0 | 0 | | 1 | 1 | 1 | 0 | 0 | | 2 | 3 | 3 | 3 | 3 | </chart>
- `<class_Chart>` @(x=36, y=42, w=884, h=475) — from crops/slide_020.crop02__chart.parse.md (level 2)
  <chart type="compound_panel"> title: Saturation Problem in Activation Functions panel: p1 ; line panel: p2 ; multi_line axis[p1.x]: x axis[p1.y]: f legend[color]: items=z = 0.1 ; z = 0.2 ; z = 0.3 ; z = 1.0 bind: x ; p1 ; x bind: z = 0.1 ; p1 ; y bind: z = 0.2 ; p1 ; y bind: z = 0.3 ; p1 ; y bind: z = 1.0 ; p1 ; y table[p1]: | x | z = 0.1 | z = 0.2 | z = 0.3 | z = 1.0 | | --- | --- | --- | --- | --- | | -4 | -0.1 | 0.0 | 0.0 | 0.0 | | -2 | 0.1 | 0.1 | 0.1 | 0.1 | | 0 | 0.1 | 0.1 | 0.1 | 0.1 | | 2 | 2.0 | 2.0 | 2.0 | 2.0 | | 5 | 4.0 | 4.0 | 4.0 | 4.0 | table[p2]: | x | z = 0.1 | z = 0.2 | z = 0.3 | z = 1.0 | | --- | --- | --- | --- | --- | | -3 | -0.2 | -0.3 | -0.3 | -1.0 | | -2 | -0.1 | -0.2 | -0.1 | -0.8 | | -1 | 0.0 | 0.0 | 0.0 | 0.0 | | 0 | 0.1 | 0.1 | 0.1 | 0.1 | | 1 | 1.0 | 1.0 | 1.0 | 0.1 | | 2 | 3.0 | 3.0 | 3.0 | 3.0 | </chart>
- `<class_Chart>` @(x=36, y=42, w=884, h=475) — from crops/slide_020.crop04__chart.parse.md (level 4)
  <chart type="compound_panel"> title: Saturation Problem in Activation Functions panel: p1 ; line panel: p2 ; multi_line axis[p1.x]: x axis[p1.y]: f axis[p2.x]: x legend[color]: items=z = 0.1 ; z = 0.2 ; z = 0.3 ; z = 1.0 bind: x ; p1 ; x bind: z = 0.1 ; p1 ; y bind: z = 0.2 ; p1 ; y bind: z = 0.3 ; p1 ; y bind: z = 1.0 ; p1 ; y table[p1]: | x | z = 0.1 | z = 0.2 | z = 0.3 | z = 1.0 | | --- | --- | --- | --- | --- | | -4 | -0.1 | 0 | 0 | 0 | | -2 | 0 | 0.1 | 0 | 0 | | 0 | 0 | 0 | 0 | 0 | | 2 | 2 | 2 | 2 | 0 | table[p2]: | x | z = 0.1 | z = 0.2 | z = 0.3 | z = 1.0 | | --- | --- | --- | --- | --- | | -3 | -0.2 | 0 | 0 | -10 | | -2 | 0 | 0 | 0 | -9 | | -1 | 0 | 0 | 0 | 0 | | 0 | 0 | 0 | 0 | 0 | | 1 | 1 | 1 | 0 | 0 | | 2 | 3 | 3 | 0 | 0 | </chart>
- `<class_Chart>` @(x=36, y=42, w=884, h=475) — from crops/slide_020.crop03__chart.parse.md (level 3)
  <chart type="compound_panel"> title: Saturation Problem in Activation Functions panel: p1 ; line panel: p2 ; multi_line axis[p1.x]: x axis[p1.y]: f axis[p2.x]: x legend[color]: items=z = 0.1 ; z = 0.2 ; z = 0.3 ; z = 1.0 bind: x ; p1 ; x bind: z = 0.1 ; p1 ; y bind: z = 0.2 ; p1 ; y bind: z = 0.3 ; p1 ; y bind: z = 1.0 ; p1 ; y table[p1]: | x | z = 0.1 | z = 0.2 | z = 0.3 | z = 1.0 | | --- | --- | --- | --- | --- | | -4 | -0.1 | 0.0 | 0.0 | 0.0 | | -2 | 0.1 | 0.1 | 0.1 | 0.1 | | 0 | 0.1 | 0.1 | 0.1 | 0.1 | | 2 | 2.0 | 2.0 | 2.0 | 2.0 | table[p2]: | x | z = 0.1 | z = 0.2 | z = 0.3 | z = 1.0 | | --- | --- | --- | --- | --- | | -3 | -0.2 | -0.3 | -0.3 | -1.0 | | -2 | -0.1 | -0.2 | -0.2 | -0.8 | | -1 | 0.0 | 0.0 | 0.0 | 0.0 | | 0 | 0.1 | 0.1 | 0.1 | 0.1 | | 1 | 1.0 | 1.5 | 1.9 | 1.7 | | 2 | 3.1 | 3.2 | 3.1 | 3.1 | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 6 · chat calls: 0 · retries: 0
