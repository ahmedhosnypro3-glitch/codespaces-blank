[2026-10-31T00:03:52Z] WINDOW OPEN (pgrep=7, waited 2728s) — dispatching 5 legs on render_17
[info] context header injected: VIEW: Slide 019 zoomed crop noreg_rows — render vs original at matched scale (attempt 18, render_17) | CAPTURE: IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: NO Regularizer column: all three row groups (the disputed y-value cells)
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 356546
[info] context header injected: VIEW: Slide 019 zoomed crop table_right — render vs original at matched scale (attempt 18, render_17) | CAPTURE: IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: Ridge lambda=3 + Ridge lambda=10 columns: headers, all three row groups, bands A/B/C, bottom tint strip
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 356543
[info] context header injected: VIEW: Slide 19 — deck 03 certification full-slide | CAPTURE: 2001x1125 @150dpi render vs 960x540 original, app lane
[warn] --timeout > 600s: the gateway at localhost:17844 is shared (Stitch proxy + vision). Long-timeout retry loops SATURATE it for everyone — prefer one modest call and retry later.
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 356567
[warn] comparison :: images :: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[error] None: every model failed:
  images: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[info] context header injected: VIEW: Slide 019 zoomed crop header_strip — render vs original at matched scale (attempt 18, render_17) | CAPTURE: IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: title box + reference line + four column headers + outlier header
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 356558
[info] context header injected: VIEW: Slide 019 zoomed crop table_left — render vs original at matched scale (attempt 18, render_17) | CAPTURE: IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: outlier column + NO Regularizer column: headers, row groups 1-2, highlight band A
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 356551
[2026-10-31T00:03:53Z] crop noreg_rows: NO VERDICT (rc=1, 1s)
[warn] comparison :: images :: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[error] None: every model failed:
  images: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[2026-10-31T00:03:54Z] crop table_right: NO VERDICT (rc=1, 2s)
[warn] comparison :: images :: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[error] None: every model failed:
  images: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[warn] comparison :: images :: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[error] None: every model failed:
  images: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[warn] comparison :: images :: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[error] None: every model failed:
  images: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[2026-10-31T00:03:54Z] full A: NO VERDICT (rc=1, 2s)
[2026-10-31T00:03:54Z] crop header_strip: NO VERDICT (rc=1, 2s)
[2026-10-31T00:03:54Z] crop table_left: NO VERDICT (rc=1, 2s)
[2026-10-31T00:03:54Z] ALL 5 LEGS DONE
