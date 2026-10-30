# OMML prepass note — slide 009 (scope S13, run 299640)

Single-version law applied: the plain-named `slide_009_recreated.pptx` itself was wrapped in place
(`scripts/18_omml_wrapper.py` to temp, then atomic replace) — no _omml variant. Verdict below is
from a byte-identical LO 150dpi render check (render pipeline: soffice pdf + pdftoppm 150).

| step | value |
|---|---|
| pre-wrap pptx md5 | 9b0efe4f1255774d7c2aac4c3e2e04dc |
| backup (superseded bytes) | pre_omml_backup_9b0efe4f.pptx |
| equations in manifest | 2 |
| baseline 150dpi render md5 (pre-wrap bytes) | cfccd2962202937d10089c562622cff4 |
| post-wrap 150dpi render md5 | cfccd2962202937d10089c562622cff4 |
| render verdict | byte-identical (0 differing pixels of 2251125) |
| post-wrap pptx md5 | af0598c89f07fc08e59c46ec5e162531 |

Manifest: `omml_manifest.json` (rel ids re-derived from the pre-wrap pptx).
Wrapper log: `omml_wrap_log.txt`.
