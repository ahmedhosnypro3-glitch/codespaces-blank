[2026-10-26T02:18:38Z] A26: WINDOW OPEN (pgrep=3, waited 0s) — DISPATCH Template A render_26 (attempt 26)
[info] context header injected: VIEW: Slide 019 recreation attempt 26 - fidelity check vs original lecture frame | CAPTURE: IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame
[warn] --timeout > 600s: the gateway at localhost:17844 is shared (Stitch proxy + vision). Long-timeout retry loops SATURATE it for everyone — prefer one modest call and retry later.
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 2216399
[warn] comparison :: images :: attempt 1: ABORT EmptyStreamError: empty content: no deltas — abort+retry 1/3
[warn] comparison :: images :: attempt 2: HTTPConnectionPool(host='localhost', port=17844): Read timed out. (read timeout=1200)
[error] None: every model failed:
  images: attempt 1: ABORT EmptyStreamError: empty content: no deltas — abort+retry 1/3
  images: attempt 2: HTTPConnectionPool(host='localhost', port=17844): Read timed out. (read timeout=1200)
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[2026-10-26T02:46:46Z] A26: Template A attempt 26: NO VERDICT (rc=1) — honest no-verdict
