# Source verification — slide 001

## Claims checked
- Institution name "Zewail City of Science and Technology" — CONFIRMED — Wikipedia (EN) https://en.wikipedia.org/wiki/Zewail_City_of_Science,_Technology_and_Innovation
- Arabic institution line "جامعة العلوم والتكنولوجيا" (parse shows a garbled Latin-1/UTF-8 misread of "ال…") — CONFIRMED — Arabic Wikipedia https://ar.wikipedia.org/wiki/مدينة_زويل_للعلوم_والتكنولوجيا
  The Arabic line names the University of Science and Technology at Zewail City; full form جامعة العلوم والتكنولوجيا بمدينة زويل (UniRank). Keep the mojibake artifact out of the rebuild; render the Arabic as typed by the source.
- Logo subtext containing the garbled year "2015" — CORRECTED — Wikipedia (EN) https://en.wikipedia.org/wiki/Zewail_City_of_Science,_Technology_and_Innovation and zewailcity.edu.eg https://www.zewailcity.edu.eg/about-zewail-city
  There is no authoritative 2015 founding/accreditation date for Zewail City. Zewail City was revived by Cabinet decree 2011-05-11, inaugurated 2011-11-01, and legally established under Law 161 on 2012-12-20; 2015 is a period of campus development and first pioneer-cohort graduation, not a founding. The OCR string "STATE LAKC 2015 INDIANACE" is misread seal/curved-inscription text; no numeric claim on this slide should be rebuilt from it.

## Overall
- VERDICT: CORRECTED
- Tolerance notes for the rebuild:
  - Frame text is verbatim-only: the slide's typed strings (title, emails, "ZEWAIL CITY", the Arabic line and its English "University of Science and Technology" gloss) are reproduced exactly, mojibake and OCR noise included.
  - The garbled logo subtext carries no reliable data; if a logo year is needed, cite the official site, not the OCR.
  - Emails are domain-only facts (zewailcity.edu.eg); no per-person verification is possible or needed.
  - Slide number "1" is a layout label, not a data claim.
