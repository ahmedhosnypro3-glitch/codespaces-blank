# VERIFY_W4.md — slide 001 "Introduction to Artificial Neural Networks (ANN)"

Wave: `src_w4_001_004` · worker `w4-src-001` · date **2026-10-30**
Frame of record: `unique_slides/slide_001.jpg` (md5 `e199229495fc31538da40386fd8dd302`, per the
doc-parse cascade header) · analysis record: `analysis/slide_001_final.json`
Status: **DONE** — no analysis corrections required; every DATA claim either CONFIRMED or flagged
as not publicly verifiable.

## Search transport

`agy -p` CLI is quota-blocked this wave (HTTP 429 `RESOURCE_EXHAUSTED / Individual quota reached`,
resets ~131h). All searches below ran through the **agy MCP web-search tool** (same Google grounding
via the antigravity proxy, redirect URLs resolved to real pages). No URL below was invented; every
one was returned by the search service. Direct `FetchURL` reads of the Zewail City pages returned
only the JS shell (`# Zewail City of Science, Technology and Innovation` + Arabic footer) — the site
is a client-rendered SPA — so those pages are cited from the grounding engine's read of them, and
that limitation is recorded honestly per claim.

## Claims checked

The frame is a title/credits slide: **no equations, algorithms, datasets, or numeric values**.
The factual claims are identity facts — course code, institution, instructor names and emails.

| # | Claim (frame text stays verbatim) | Status | Evidence URL | Change to analysis spec |
|---|---|---|---|---|
| 1 | "CSAI 253" is a real course at Zewail City, School of Computational Sciences and Artificial Intelligence | **CONFIRMED** | https://www.zewailcity.edu.eg/program/40 — "CSAI 253: Machine Learning", 3 credits [2+3], prerequisites CSAI 201 (Data Structures) and MATH 105 (Probability and Statistics) | none |
| 2 | The catalog title of CSAI 253 is **Machine Learning**; the slide's "Introduction to Artificial Neural Networks (ANN)" is a lecture topic inside that course, not the catalog course title | **CONFIRMED** (DATA note) | https://www.zewailcity.edu.eg/program/40 ; https://www.zewailcity.edu.eg/ar/academics/undergraduate-studies/schools/program/82 — topics listed: Regression, Classification, Clustering, Prediction, Reinforcement Learning, Dimensionality Reduction; CSAI 253 is the prerequisite of DSAI 308 (Deep Learning) | none — informs slide notes only |
| 3 | "Dr. Khaled Mostafa ElSayed" with email kmelsayed@zewailcity.edu.eg | **CONFIRMED** | https://www.zewailcity.edu.eg/ar/about/member/53 — Professor, School of Computational Sciences and Artificial Intelligence; Director of the Data Science Program; Academic Building S018; email kmelsayed@zewailcity.edu.eg | none |
| 4 | "Dr. Mohamed Maher Ata" with email momaher@zewailcity.edu.eg | **CONFIRMED** | https://www.zewailcity.edu.eg/about/member/29 — Associate Professor, CSAI school; Ph.D. Tanta University (Egypt) / University of Regina (Canada); research AI, computer vision, image/video processing ; corroborating: https://scholar.google.com/citations?user=ZvA8nX4AAAAJ&hl=en , https://www.researchgate.net/profile/Mohamed-Maher-8 | none |
| 5 | Institution branding: "ZEWAL CITY" wordmark + Arabic "جامعة العلوم والتكنولوجيا زويل" + "University of Science and Technology" | **CONFIRMED (DATA clarification)** | https://www.unirank.org/eg/uni/university-of-science-and-technology-at-zewail-city/ — official English name "University of Science and Technology at Zewail City (UST)"; https://www.zewailcity.edu.eg/about-ust ; https://en.wikipedia.org/wiki/Zewail_City_of_Science,_Technology_and_Innovation — parent institution "Zewail City of Science, Technology and Innovation" | none. The frame's "ZEWAL CITY" (one L) is an OCR misspelling of the official wordmark "Zewail City" and the official Arabic carries "بمدينة زويل" — both are **frame-text/literal-text items and stay verbatim** |
| 6 | "Spring 2024" semester label | **UNVERIFIED** (plausible, not independently checkable) | no public page confirms the exact term; the course is offered on the Zewail CSAI curriculum and the catalog is the 2024 catalog (https://www.scribd.com/document/772961333/CSAI-Catalog-2024) | none — keep as printed |

Tally: **6 claims checked · 5 CONFIRMED · 0 CORRECTED · 1 UNVERIFIED (honest, no public source).**

## Questions asked

1. "Zewail City University of Science and Technology CSAI 253 Machine Learning course catalog credits prerequisites"
2. "Zewail City faculty Dr. Khaled Mostafa ElSayed professor School of Computational Sciences and Artificial Intelligence"
3. "Zewail City Dr. Mohamed Maher Ata associate professor Computational Sciences and Artificial Intelligence"
4. "Zewail City CSAI 253 Machine Learning course description topics neural networks lecture"
5. "Zewail City جامعة العلوم والتكنولوجيا University of Science and Technology official name"
6. Direct fetches: `https://www.zewailcity.edu.eg/program/40`, `/about/member/29`, `/ar/about/member/53`, `/ar/academics/undergraduate-studies/schools/program/82` — all four returned the JS shell only (SPA); recorded as a fetch limitation, not a contradiction.

## Doc-parse cross-check

`sources/docparse_cascades/slide_001/composed/slide_001_composed.md` (independent second read of
the same frame, nemotron-3.5-parse, degraded: False, 10 elements, 0 failed calls) agrees with the
analysis JSON on every identity field: badge "1"; title "Introduction to Artificial Neural Networks
(ANN)"; "CSAI 253 - Spring 2024"; "Prepared By / Dr. Khaled Mostafa ElSayed / kmelsayed@
zewailcity.edu.eg"; "Instructors:" with ElSayed + "Dr. Mohamed Maher Ata / momaher@zewailcity.edu.eg";
footer "جامعة العلوم والتكنولوچيا University of Science and Technology". The crop parse of the
logo region is garbage ("ZEWAIL CITY STATE LAKE 2024 INDUSTRATE") — decorative branding only, no
frame text depends on it. Nothing in the analysis needed patching.

## Banked this wave (new URLs, all returned by the search service)

1. https://www.zewailcity.edu.eg/program/40
2. https://www.zewailcity.edu.eg/ar/academics/undergraduate-studies/schools/program/82
3. https://www.zewailcity.edu.eg/ar/about/member/53
4. https://www.zewailcity.edu.eg/about/member/29
5. https://www.zewailcity.edu.eg/about-ust
6. https://www.unirank.org/eg/uni/university-of-science-and-technology-at-zewail-city/
7. https://www.researchgate.net/profile/Khaled-El-Sayed-3
8. https://www.researchgate.net/scientific-contributions/Khaled-M-Elsayed-2112986768
9. https://scholar.google.com/citations?user=ZvA8nX4AAAAJ&hl=en
10. https://www.researchgate.net/profile/Mohamed-Maher-8
11. https://www.mecs-press.org/authors/111304.html
12. https://www.scribd.com/document/772961333/CSAI-Catalog-2024
13. https://en.wikipedia.org/wiki/Zewail_City_of_Science,_Technology_and_Innovation

## Left undone / follow-up

- The exact term "Spring 2024" cannot be web-confirmed; needs the course syllabus or the instructor.
  Not a blocker: frame text is verbatim either way.
