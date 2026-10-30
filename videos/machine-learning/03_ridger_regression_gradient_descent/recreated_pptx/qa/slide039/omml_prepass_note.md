# OMML prepass note — slide 039 (scope S13, run 299640)

Single-version law applied: the plain-named `slide_039_recreated.pptx` itself was wrapped in place
(`scripts/18_omml_wrapper.py` to temp, then atomic replace) — no _omml variant. Verdict below is
from a byte-identical LO 150dpi render check (render pipeline: soffice pdf + pdftoppm 150).

| step | value |
|---|---|
| pre-wrap pptx md5 | 09311d1f96c4b5c8803e7fbc5e87197e |
| backup (superseded bytes) | pre_omml_backup_09311d1f.pptx |
| equations in manifest | 1 |
| baseline 150dpi render md5 (pre-wrap bytes) | 7fdd25e202da8ffb68765ee8b49d35bb |
| post-wrap 150dpi render md5 | 7fdd25e202da8ffb68765ee8b49d35bb |
| render verdict | byte-identical (0 differing pixels of 2251125) |
| post-wrap pptx md5 | f91f80995c1875596e696aef9b780479 |

Manifest: `omml_manifest.json` (rel ids re-derived from the pre-wrap pptx).
Wrapper log: `omml_wrap_log.txt`.
