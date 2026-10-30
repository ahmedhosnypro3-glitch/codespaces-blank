# doc-parse spec coverage cross-check

Parse transcript (different model family) vs consumed vision spec. Words present in the parse but absent from the spec are candidate MISSING-CONTENT items for the build worker to verify against the original.

| slide | state | spec_words | parse_only_words |
|---|---|---|---|
| 001 | checked | 99 | 2 |
| 002 | checked | 132 | 0 |
| 003 | checked | 126 | 0 |
| 004 | checked | 100 | 0 |
| 005 | checked | 133 | 2 |
| 006 | checked | 117 | 0 |
| 007 | checked | 133 | 0 |
| 008 | checked | 147 | 0 |
| 009 | NO-COMPOSED | - | - |
| 010 | checked | 121 | 0 |
| 011 | checked | 143 | 0 |
| 012 | checked | 152 | 0 |
| 013 | checked | 87 | 1 |
| 014 | NO-COMPOSED | - | - |
| 015 | NO-COMPOSED | - | - |
| 016 | NO-COMPOSED | - | - |
| 017 | checked | 193 | 4 |
| 018 | checked | 86 | 1 |
| 019 | checked | 108 | 0 |
| 020 | checked | 109 | 1 |
| 021 | checked | 126 | 2 |
| 022 | checked | 272 | 0 |
| 023 | checked | 239 | 0 |
| 024 | checked | 135 | 1 |
| 025 | checked | 130 | 1 |
| 026 | checked | 106 | 1 |
| 027 | checked | 68 | 0 |
| 028 | checked | 83 | 1 |
| 029 | checked | 105 | 0 |
| 030 | checked | 130 | 0 |
| 031 | checked | 89 | 2 |
| 032 | checked | 91 | 0 |
| 033 | checked | 102 | 0 |
| 034 | checked | 100 | 0 |
| 035 | NO-SPEC | - | 1 |
| 036 | checked | 99 | 0 |
| 037 | checked | 109 | 2 |

## Candidate missing content (parse-only words, len>=4)

### Slide 1 (slide_001_composed.md)

- `csai`, `spring`

### Slide 5 (slide_005_composed.md)

- `note`, `other`

### Slide 13 (slide_013_composed.md)

- `category`

### Slide 17 (slide_017_composed.md)

- `axis`, `color`, `items`, `multi`

### Slide 18 (slide_018_composed.md)

- `docg`

### Slide 20 (slide_020_composed.md)

- `other`

### Slide 21 (slide_021_composed.md)

- `normal`, `other`

### Slide 24 (slide_024_composed.md)

- `other`

### Slide 25 (slide_025_composed.md)

- `other`

### Slide 26 (slide_026_composed.md)

- `other`

### Slide 28 (slide_028-_composed.md)

- `strip`

### Slide 31 (slide_031_composed.md)

- `category`, `value`

### Slide 37 (slide_037_composed.md)

- `callout`, `multi`

