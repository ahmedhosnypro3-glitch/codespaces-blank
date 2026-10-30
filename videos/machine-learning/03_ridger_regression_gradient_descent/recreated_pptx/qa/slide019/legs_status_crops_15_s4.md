[2026-10-25T04:47:09Z] WINDOW OPEN (pgrep=3, waited 0s) — DISPATCH crop table_left
[info] context header injected: VIEW: Slide 019 zoomed crop table_left — render vs original at matched scale (attempt 15) | CAPTURE: IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: outlier bracket + W bracketed 3-vectors + test grids
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 1038089
[warn] comparison :: images :: attempt 1: ABORT GarbageError: garbage: infinite/looping repetition in thinking stream — abort+retry 1/3
[warn] comparison :: images :: attempt 2: ABORT HangError: hard wall-clock 630s exceeded — call aborted (possible stuck thinking stream) — abort+retry 2/3
[warn] comparison :: images :: attempt 3: ABORT EmptyStreamError: empty content: no deltas — giving up
[error] None: every model failed:
  images: attempt 1: ABORT GarbageError: garbage: infinite/looping repetition in thinking stream — abort+retry 1/3
  images: attempt 2: ABORT HangError: hard wall-clock 630s exceeded — call aborted (possible stuck thinking stream) — abort+retry 2/3
  images: attempt 3: ABORT EmptyStreamError: empty content: no deltas — giving up
[info] degenerate events: 1 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
