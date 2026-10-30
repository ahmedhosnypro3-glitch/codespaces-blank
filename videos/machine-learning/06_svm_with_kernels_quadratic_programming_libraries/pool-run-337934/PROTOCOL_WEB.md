
## The spec-correction protocol (binding)

- Web sources **confirm or correct DATA**: numbers, formulas, dataset/library names, sign
  conventions, hyperparameter names, theorem attributions.
- Sources NEVER change **frame text** — `verbatim_text` stays exactly what the slide shows,
  typos included. A source saying the slide's number is wrong does NOT license editing the
  transcript; it is recorded in the report instead.
- Sources NEVER invent content the slide does not show. If the slide shows `K(x,z) = exp(-g
  ||x-z||^2)` and the source says the RBF kernel is `exp(-gamma*||x-z||^2)`, you may record
  that the symbol `g` plays the role of `gamma` — you may not add text the slide does not show.
- Never fetch a page twice; reuse a URL already cited earlier in the report.

## Output — write exactly one file

`web_sources/slide_NNN/SOURCES.md` (create the dir), in this shape:

```
# Source verification — slide NNN
## Claims checked
- <the claim as the slide states it, linear> — <CONFIRMED | CORRECTED | UNVERIFIABLE> — <source name> <url>
  <if CORRECTED: what the authoritative form is; if UNVERIFIABLE: why>
## Overall
- VERDICT: CONFIRMED | CORRECTED | NEEDS_NO_SOURCE | UNVERIFIABLE
- Tolerance notes for the rebuild (sign conventions, symbol roles, value rounding).
```

Rules: ≤ 45 lines. Max 75 lines per Write call. Markdown, UTF-8, no images.
