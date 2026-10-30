# Slide 014 — LEGS STATUS, attempt 3 (LEGS-ONLY lane, worker `w014-legs3`)

Date: 2026-10-24. Worker scope: **legs only** — dispatch + adjudicate + certify.
Per the lane contract this worker does NOT edit the build; a FAIL citing a real
build defect is handed back with measurements.

## 1. BANK VERIFIED (every claim re-checked with ls + md5)

| Item | Expected | Measured | Result |
|---|---|---|---|
| `recreated_pptx/qa/slide014/render_3.png` md5 | `da935d0ad0dfd1a8066a1180a492e319` | `da935d0ad0dfd1a8066a1180a492e319` | ✅ |
| `payload_A_3.txt` md5 | `9387f5fbb94ef05a31db19f1e018dde1` | same | ✅ |
| `payload_B_3.txt` md5 | `978be75de7b83501d09f8f0c5576cbee` | same | ✅ |
| `dispatch_attempt_3.sh` | executable, syntax-clean | `bash -n` clean; `PY` resolves to the real script | ✅ |
| 4 crop pairs | 1797×N, size-matched | title 1797×396, upper 1797×204, middle 1797×223, lower 1797×145 — `MATCH=True` all four | ✅ |
| payload A hygiene | 4115 chars, BLOCKER×4, no NNN/K | exactly that | ✅ |
| payload B hygiene | 1914 chars, BLOCKER×2, no NNN/K, `slide 014` substituted | exactly that | ✅ |

**IMPORTANT PATH CORRECTION** — the bank is NOT at the project root. It lives at
`videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014/`.
The project-root `recreated_pptx/qa/` contains only `slide046`. Every path in
`worker_report.md`'s resume block that omits the deck prefix will fail ENOENT.

## 2. GATE STATUS — CONGESTED (legs NOT fired)

Vision gateway probes (`pgrep -c -f analyze_image.py`), logged in
`gate_poll_attempt3.log`:

```
poll_start 11:47:58Z congestion=20
probe 1  11:47:58  congestion=20
probe 2  11:51:58  congestion=16
probe 3  11:55:58  congestion=17
probe 4  11:59:58  congestion=17
[poller restarted on 600s background cap]
probe 1  12:05:23  congestion=22
probe 2  12:09:23  congestion=22
probe 3  12:13:23  congestion=28
probe 4  12:17:23  congestion=28
probe 5  12:21:23  congestion=44
probe 6  12:25:23  congestion=49
probe 7  12:29:23  congestion=42
probe 8  12:33:23  congestion=39
manual probe 12:35:17 congestion=15
```

Manual probes in this worker's own window (13:00, 13:05): **48** and **48**.
Over the whole window the count never once read below 8, and the *minimum*
observed was 16. Congestion is fleet-wide and persistent: the queued
`analyze_image.py` processes form groups of 4 (one per raced model) belonging to
sibling lanes on slides 047/021/010 as well as this one.

**Reproduced the prior lane's diagnostic (13:06Z), same conclusion today:**

| Probe | Result |
|---|---|
| `GET /v1/models` | HTTP 401 in 0.7 ms — router alive |
| text-only chat turn | HTTP 401 (no key) in 0.7 ms — routing layer healthy |
| queued image judges (20 oldest shown) | elapsed 1284 s / 1112 s / 1099 s / 956 s / 916 s / 700 s, CPU **00:00:00–00:00:01** each — parked on network I/O |
| attempt-3 transcripts | `probe_3.txt`, `judge_attempt_3.txt`, `crop_3_*_judge.txt` — **none written** |

So the text path works and the image path is still wedged upstream. Dispatching
now would append 5 more processes to a queue that is not draining (~21 min
oldest, 0 verbosity) and burn ~25 min each for no verdict — precisely the waste
the gate law exists to prevent. Per the law, **no vision leg was fired** and no
verdict was fabricated.

**Poller stopped** at 13:06Z (TaskStop) after ~40 logged probes. Its log is banked
at `gate_poll_attempt3.log` and the marker file is absent.

## 3. PIL ADJUDICATION BASELINE — INDEPENDENTLY RE-MEASURED

I did not trust the inherited table. All numbers below are from my own scripts
(`chrome_reverify_3.py`, `pil_reverify_3.py`, `pil_samples_3.py`, `pil_focus_3.py`,
`pil_boxcheck_3.py`), measured on **both** images in 960×540 frame space
(1 px = 1 pt; render 2001×1125 ÷ 2.084375). Outputs banked next to the scripts.

### HOUSE CHROME — PASS (independently confirmed)

| Item | Deck law | Original | Render | Verdict |
|---|---|---|---|---|
| left stroke | x58.5 | x59 (JPEG-darkened to RGB ~(112,40,51)) | **x58.1** | ✅ Δ0.4 |
| right stroke | x901 | x900 | **x901.0** (RGB 192,0,0) | ✅ Δ0.0 |
| bottom stroke | y538.5 | y538..539 | **y537.8..538.3** | ✅ Δ0.5 |
| top stroke | NONE | 0 red px in y0..45 | **0 red px** | ✅ correct |
| panel | x54..903 y45..540 | x59..899 gray | x59..899.6 | ✅ |
| badge | (876,73) d≈35 | (876.0, 73.5) d33 | (875.3, 72.7) d32.6 | ✅ within tol 8 |

Chrome is NOT the problem. A judge finding about chrome is refutable with these.

### CONFIRMED REAL BUILD DEFECTS (all measured on BOTH images)

| # | Defect | Original (measured) | Render (measured) | Class |
|---|---|---|---|---|
| 1 | **Mid band 1 — peach block MISSING, text MISSING** | peach fill (249,222,193)/(244,223,192); runs y351..389, x170..559 / x94..561; red top border y349..351, bottom border y387..391; **ink 2242 px over 39 rows** | plain panel gray (233,233,231) x59..899.6 at y355/365/375/386; **ink = 0 px** | **BLOCKER** |
| 2 | **Mid band 2 — span wrong** | peach (249,222,192) x93..431 / x91..255 (block x~89..471) | pink FFEBEE (255,235,238) spanning **x54..903** at y420 — full panel *and* the gutter | **BLOCKER** |
| 3 | **Mid band 3 — yellow block MISSING, text MISSING** | yellow (250,255,219) x537..878, y405..414 (block x533..880 y404..444); **ink 1207 px over 24 rows** | no yellow at all in y335..460 (`mid_yellow-render = EMPTY`); **ink = 0 px** | **BLOCKER** |
| 4 | **Ridge band — inset missing** | yellow (245,252,218) x92..877, y247..281 (x54..903 is the render's) | FFF9C4 (255,249,196) **x54.2..902.9**, y250..278 | **MAJOR** |
| 5 | **Objective band — inset missing** | yellow (248,253,223) x91..877, y307..336 | FFF9C4 **x54.2..902.9**, y310..334 | **MAJOR** |
| 6 | **Lower blue region — geometry + artificial gutter** | continuous: at y470 ONE run x95..873 (779 px wide); y468..529, x85..883 | y467.8..523.9, x53.7..902.9, **gray gutter x449.5..499.4 on EVERY row**; left edge crosses the left stroke; right edge 20 px past the original's | **MAJOR** |
| 7 | **Band fills ≠ frame** | peach (248,222,193) / yellow (245,252,218) / lower blue (123,120,201) | pink FFEBEE (255,235,238) / FFF9C4 (255,249,196) / light blue (225,245,254) | **MAJOR** (see §5) |
| 8 | **Vector box spans + colour** | LEFT x80..433, RIGHT x457..810; borders dark maroon (143,18,32)/(144,22,35); interiors pink | LEFT x53.3..449.5, RIGHT x499.4..895.7; borders **black (0,0,0)**; interiors **white** | **MAJOR** (spans ~43 px too wide each, shifted onto the panel edge) |
| 9 | Vector box vertical band | y100..236 (h 136) | y103.6..231.7 (h 128) — ~3.5 px up, ~8 px short | MINOR |

### NON-ISSUES / REFUTATIONS

- **"Right vector box border sits ON the right stroke x901" (inherited claim) —
  REFUTED as stated.** The render's right-box border is a black vertical at
  **x895.2..895.7**; the right red stroke is a separate vertical at **x901.0**
  (5.3 px away). The inherited table's "x..901.1" measured the *stroke*, not the
  box border. The real defect is #8 (span + colour), not stroke coincidence.
  If the judge reports "box border merges with the right stroke", refute that
  mechanism and hand back #8 instead.
- **Top stroke** — the original has none and so does the render (0 red px both).
  A judge finding there is refutable.
- **Badge geometry** — matches within tol 8.
- **Textless boxes** — attempt 1's 9 BLOCKERs are gone. Ink census: title
  8806, left box 10186, right box 9659, ridge 7874, objective 7286, lower
  10459. Content is present everywhere **except mid bands 1 and 3**, where the
  render has literally zero ink.

## 4. WHAT THIS MEANS FOR CERTIFICATION

**Certification is NOT possible.** The render omits two content blocks outright
(bands 1 and 3, including their text) and mis-scales three other regions. Per the
lane contract I do not edit the build; this goes back to the build lane.

The inherited `worker_report.md` fix list was **correct and my measurements
confirm all three of its BLOCKERs**. One row of its table (the right-box/stroke
claim) needs correcting to defect #8 above.

## 5. SPEC-vs-FRAME TENSION (recorded, not resolved)

The analysis JSON's palette (`FFEBEE` pink, `FFF9C4` yellow) is faithfully
reproduced by the build, but the **frame** measures peach `(248,222,193)` and
yellow `(245,252,218)`, and a lower-blue `(123,120,201)` vs the build's
`(225,245,254)`. Per the deck's AGENTS.md ("the frame wins for recreation"), the
frame colours are authoritative for recreation. If the judge reads the JSON
palette as correct and reports a colour mismatch as a defect, **refute it with
the frame measurement** and route it to the build lane as a separate
(spec-vs-frame) decision, not as a judge error.

## 6. RESUME COMMANDS (exact)

```bash
cd /worksp/aces/codespaces-blank/ai_llm_slides
Q=videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide014

# 0. gate check — MUST read < 8
n=$(pgrep -c -f analyze_image.py); echo "congestion=$n"

# 1. legs 0-3, Template A probe + full-slide judge + 4 crop pairs
bash $Q/dispatch_attempt_3.sh

# 2. read every transcript for a real FINAL VERDICT line
for f in $Q/probe_3.txt $Q/judge_attempt_3.txt $Q/crop_3_*_judge.txt; do
  [ -f "$f" ] && echo "--- $f" && grep -c "FINAL VERDICT:" "$f"
done
```

If the gate never opens in this window, the row stays parked:
`gen_status=building`, `visual_check=null`, `visual_transcript=null`,
`worker_id=w014-buildfirst-20261024` (heartbeat maintained). Nothing is
fabricated.

## 7. FIX LIST FOR THE BUILD LANE

Priority order (all measured, both images, frame-space):

1. Add mid band 1: peach `(248,222,193)` block x90..665 y350..389 **with its text**.
2. Add mid band 3: yellow `(245,252,218)` block x533..880 y404..444 **with its text**.
3. Re-scope mid band 2 to x89..471 y403..444 (peach); do NOT span the gutter or the full panel.
4. Inset the ridge band to x92..877 y247..281.
5. Inset the objective band to x91..877 y307..336.
6. Lower blue region: x91..883, y468..529, continuous (remove the x449.5..499.4 gutter).
7. Reconsider the palette: frame peach/yellow/blue vs JSON FFEBEE/FFF9C4.
8. Vector boxes: LEFT x80..433, RIGHT x457..810, y100..236; maroon borders, pink interiors.

After the build fix: re-render `render_4.png`, re-cut `crop_4_*`, re-emit payloads
with K=4, re-run BOTH legs (Template A + all 4 crop pairs), then certify.

## 8. PARK STATE AT HANDOFF (2026-10-24 13:06Z, verified by `get 14`)

```json
{
 "slide_id": 14,
 "gen_status": "building",
 "visual_check": null,
 "visual_attempts": 0,
 "visual_transcript": null,
 "last_error": null,
 "worker_id": "w014-buildfirst-20261024",
 "worker_heartbeat_at": "2026-10-24T12:46:07"
}
```

- The claim stays with the parked build lane; this legs worker did **not** claim.
- This worker heartbeated at 12:46:07Z to keep the row from being swept as a
  ZOMBIE while the legs are parked. Heartbeating was protective only — it writes
  nothing else and fabricates nothing.
- **No certification sequence was run** (it requires a real PASS verdict).
- `visual_check` and `visual_transcript` are deliberately left `null`: no verdict
  exists and none was invented.
- Bank records untouched and re-verified at handoff: `render_3.png`
  `da935d0ad0dfd1a8066a1180a492e319`, `payload_A_3.txt`
  `9387f5fbb94ef05a31db19f1e018dde1`, `payload_B_3.txt`
  `978be75de7b83501d09f8f0c5576cbee`.
