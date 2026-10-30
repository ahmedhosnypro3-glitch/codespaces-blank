# Composed parse: slide_019

- source frame: `slide_019.jpg` (md5 `e0021d06d78c49eb8fdb64d59b254c9c`)
- parse model: `nemotron-3.5-parse` · chat model: `docparsechat`
- degraded: True (chat probe failed — decisions use the deterministic-conservative fallback)
- elements kept: 2 (dedup collapsed 1) · crops: 2 · failed calls: 0

## Positioned elements (reading order: y then x)

- `<class_Chart>` @(x=37, y=42, w=860, h=474) — from full/slide_019.parse.md (level 0)
  <chart type="line"> axis[x]: r axis[y]: sig(t) legend[color]: items=sig(t) = 1 (12+) bind: r ; ; x bind: sig(t) = 1 (12+) ; ; y | r | sig(t) = 1 (12+) | | --- | --- | | -9 | 0.0 | | -8 | 0.05 | | -4 | 0.1 | | -2 | 0.3 | | 2 | 0.7 | | 4 | 0.98 | | 6 | 1.0 | | 8 | 1.0 | </chart>
- `<class_Chart>` @(x=37, y=42, w=859, h=475) — from crops/slide_019.crop01__chart.parse.md (level 1)
  <chart type="line"> axis[x]: f, axis[y]: sig(t) legend[color]: items=sig(t) = (1+2) bind: f, ; ; x bind: sig(t) ; ; y | f, | sig(t) | | --- | --- | | -8 | 0.0 | | -6 | 0.02 | | -4 | 0.1 | | -2 | 0.3 | | 2 | 0.9 | | 4 | 0.97 | | 6 | 1.0 | | 8 | 1.0 | </chart>

## Unpositioned text

- (none)

## Failed calls

- (none)

## Notes

- backstop stops: 0
- parse calls spent: 3 · chat calls: 0 · retries: 0
