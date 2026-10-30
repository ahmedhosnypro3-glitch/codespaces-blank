# OMML prepass note — slide 036 (scope S13, run 299640)

Single-version law applied: the plain-named `slide_036_recreated.pptx` itself was wrapped in place
(`scripts/18_omml_wrapper.py` to temp, then atomic replace) — no _omml variant. Verdict below is
from a byte-identical LO 150dpi render check (render pipeline: soffice pdf + pdftoppm 150).

| step | value |
|---|---|
| pre-wrap pptx md5 | ad2a07ddd2e688b40d57d20e5c6ea701 |
| backup (superseded bytes) | pre_omml_backup_ad2a07dd.pptx |
| equations in manifest | 1 |
| baseline 150dpi render md5 (pre-wrap bytes) | 9477fc0fc9a5eb1a89e0cbc8e8288234 |
| post-wrap 150dpi render md5 | 9477fc0fc9a5eb1a89e0cbc8e8288234 |
| render verdict | byte-identical (0 differing pixels of 2251125) |
| post-wrap pptx md5 | ee60a2abd2eedcf665b241ff3f594f49 |

Manifest: `omml_manifest.json` (rel ids re-derived from the pre-wrap pptx).
Wrapper log: `omml_wrap_log.txt`.
