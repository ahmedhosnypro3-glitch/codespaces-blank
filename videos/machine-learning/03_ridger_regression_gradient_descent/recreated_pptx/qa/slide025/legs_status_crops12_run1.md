[2026-10-30T21:55:35Z] start attempt-12 legs on render_3; payloads B=d3769a804d34298a768f90ea15ad530f A=8fc119623b1f020c6d135c834969bf75
[2026-10-31T00:05:17Z] WINDOW OPEN for crop_tr (pgrep=7, waited 7782s)
[info] context header injected: VIEW: Slide 025 zoomed crop tr — render vs original at matched scale (attempt 12) | CAPTURE: IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: top-right convex bowl: inverted x-axis tick order, sharper spike, dotted gridlines, floor contours
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 362157
[warn] comparison :: images :: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[error] None: every model failed:
  images: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[2026-10-31T00:05:18Z] crop_12_tr_judge.txt: NO VERDICT (rc=1, transcript MISSING)
[2026-10-31T00:05:18Z] WINDOW OPEN for crop_tl (pgrep=7, waited 0s)
[info] context header injected: VIEW: Slide 025 zoomed crop tl — render vs original at matched scale (attempt 12) | CAPTURE: IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: top-left concave dome with floor contour projections
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 362244
[warn] comparison :: images :: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[error] None: every model failed:
  images: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[2026-10-31T00:05:19Z] crop_12_tl_judge.txt: NO VERDICT (rc=1, transcript MISSING)
[2026-10-31T00:05:19Z] WINDOW OPEN for crop_bl (pgrep=7, waited 0s)
[info] context header injected: VIEW: Slide 025 zoomed crop bl — render vs original at matched scale (attempt 12) | CAPTURE: IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: bottom-left non-convex surface with extrema labels and leaders
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 362306
[warn] comparison :: images :: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[error] None: every model failed:
  images: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[2026-10-31T00:05:19Z] crop_12_bl_judge.txt: NO VERDICT (rc=1, transcript MISSING)
[2026-10-31T00:05:19Z] WINDOW OPEN for crop_br (pgrep=7, waited 0s)
[info] context header injected: VIEW: Slide 025 zoomed crop br — render vs original at matched scale (attempt 12) | CAPTURE: IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: bottom-right gradient-descent path surface
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 362370
[warn] comparison :: images :: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[error] None: every model failed:
  images: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[2026-10-31T00:05:20Z] crop_12_br_judge.txt: NO VERDICT (rc=1, transcript MISSING)
[2026-10-31T00:05:20Z] WINDOW OPEN for crop_title (pgrep=7, waited 0s)
[info] context header injected: VIEW: Slide 025 zoomed crop title — render vs original at matched scale (attempt 12) | CAPTURE: IMG1=zoomed crop of a 150dpi PPTX render; IMG2=the SAME slide-space region cropped from the original lecture frame and upscaled to match IMG1's effective scale; region: title band text
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 362435
[warn] comparison :: images :: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[error] None: every model failed:
  images: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[2026-10-31T00:05:20Z] crop_12_title_judge.txt: NO VERDICT (rc=1, transcript MISSING)
[2026-10-31T00:05:20Z] WINDOW OPEN for full_A (pgrep=7, waited 0s)
[info] context header injected: VIEW: Slide 025 recreation attempt 12 — fidelity check vs original lecture frame | CAPTURE: IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame
[warn] --timeout > 600s: the gateway at localhost:17844 is shared (Stitch proxy + vision). Long-timeout retry loops SATURATE it for everyone — prefer one modest call and retry later.
[info] mode comparison | endpoint http://localhost:17844/v1 | models: images | auth: key file present | pid 362497
[warn] comparison :: images :: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[error] None: every model failed:
  images: attempt 1: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
[info] degenerate events: 0 (full-page tier: 0)
[info] 0/1 result(s) analyzed successfully
[2026-10-31T00:05:21Z] judge_att12_full.txt: NO VERDICT (rc=1, transcript MISSING)
[2026-10-31T00:05:21Z] attempt-12 leg run COMPLETE
