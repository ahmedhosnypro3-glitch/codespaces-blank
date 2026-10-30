# Source verification — slide 043

## Claims checked

- (none — this slide carries no verifiable DATA claim)

The slide shows only: a red-framed white plot area on light gray, a scatter plot with
seven colored dot clusters (dark blue, red, cyan top band; yellow, magenta, green, black
lower bands) over a dotted grid, axis tick labels −10/0/10/…/40 (y) and 0/10/…/40 (x),
and a yellow badge with the numeral "43". No title, no bullet, no formula, no dataset or
library name, no hyperparameter, and no theorem attribution appears anywhere in the frame
(doc-parse returns only the chart table; vision analysis records `slide_title: "Untitled"`
and empty `verbatim_text.bullets`).

Per the protocol's pure-prose rule the slide needs no source verification: the cluster
positions, dot counts, and region geometries are invented teaching graphics — no
authoritative source exists to confirm or correct them, and no external source may be
used to introduce content the slide does not show. 0 searches spent.

## Overall

- VERDICT: NEEDS_NO_SOURCE
- 0 web searches spent; the slide carries no DATA for sources to confirm or correct.
- Tolerance notes for the rebuild:
  - Axis ranges and tick values are graphical scale, not data claims: y −10→40, x 0→40,
    major ticks every 10. Reproduce exactly as the frame prints them.
  - Cluster centroids/spreads come from the analysis spec (`slide_043_final.json`,
    recreation_brief step 7); they are approximations, so keep them within the recorded
    per-cluster ranges rather than matching any published dataset.
  - No per-cluster dotted background is a verifiable convention — the frame shows dotted
    grid backgrounds behind only some clusters; mirror the frame's inconsistency rather
    than "fixing" it to a uniform rule.
  - Badge numeral stays exactly `43` (house rule: badge = printed number on the original).
  - Frame text is authoritative as-is — nothing to correct, nothing to normalize.
