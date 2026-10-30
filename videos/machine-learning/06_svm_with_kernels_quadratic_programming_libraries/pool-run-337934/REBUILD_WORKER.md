# REBUILD_WORKER.md — rebuild one slide from its NEW reanalysis spec

Video namespace (ALL writes stay inside it):
/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries

Read FIRST, in order:
1. `pool-run-337934/MISSION_PROTOCOL.md` — the "ADDENDUM — REBUILD WAVE 3" section is the binding contract.
2. The video `AGENTS.md` (house frame rule, math rule, graph rule).
3. This file. Your slide number N is in your spawn prompt.

## Steps
1. Read the NEW spec `qa/reanalysis2/slide_NNN_analysis.txt`. The spec starts at the
   line `1. SLIDE_TITLE` — ignore any preamble before it. NNN = zero-padded N (e.g. 007).
2. Write a FRESH `recreated_pptx/build/slide_NNN.js` (pptxgenjs) from THAT SPEC ONLY.
   Never build from `analysis/slide_NNN_raw.json`, never from a `## N.`-headed
   UI-audit transcript, never by copying the old dump build.
3. House chrome is MANDATORY and overrides the spec (never a discrepancy):
   - `LAYOUT_WIDE` 13.33x7.5 in; slide background `#E8E8E8`
   - outer frame: rect x=0.15 y=0.15 w=13.03 h=7.2, line #C00000 width 1.5, fill none
   - badge: OVAL x=12.48 y=0.30 w=0.5 h=0.5, fill #FFF9C4, line #FFF9C4, plus text
     String(N) centered (align center, valign middle) fontSize 18 bold #333333 Arial
   - title: text box x=0.6 y=0.28 w=12.13, align center, bold, color #C00000
4. All other content comes from the spec at its measured geometry. Normalized spec
   coords [x0,y0,x1,y1] → inches: x*13.33, y*7.5, w=(x1-x0)*13.33, h=(y1-y0)*7.5.
   Keep every verbatim string exactly (line breaks, case, punctuation, colors).
   Use pptxgenjs rich-text run arrays for multi-color lines. Add NO text the spec
   does not contain (a prior judge FAILed builds for invented lines like
   "Institution:" or "Slide Number: 1" body text).
5. Math (spec section 8): matplotlib mathtext → tight transparent PNG at 600 dpi →
   `addImage()` at exact size (w = px/600 in, never rescaled). Never inline `x^2`,
   `x_1`, `a/b`, or "sum from i=1 to n". Use `recreated_pptx/build/render_math.py`
   (see its docstring); assets go in `recreated_pptx/build/eq_NNN/`.
6. Plots/graphs (spec sections 4-5): generate a REAL plot with matplotlib /
   scikit-learn matched to the spec's region and colors. Reuse an existing
   `recreated_pptx/build/slide_NNN_graph.png` ONLY if the spec's plot region matches it.
7. Max 75 lines per single Write tool call — split the JS across Write + append calls.
8. Build: `cd recreated_pptx/build && NODE_PATH=$(npm root -g) node slide_NNN.js`
   → writes `recreated_pptx/slide_NNN_recreated.pptx` (single version, no suffix).
9. Render: from the video root `bash tools/render_all.sh N`
   → `recreated_pptx/renders/slide_NNN_recreated-1.png`.
10. Closed-loop PIL check of the render vs `qa/rejudge2/orig_png/slide_NNN.png`
    (text presence, rough ink positions). Fix obvious geometry errors, rebuild, re-render.
11. DB (absolute paths):
    `~/.agents/skills/pooled-missions/scripts/pool-db.sh scope-claim <NS>/mission.db scope_rb2_NNN rb2_worker_NNN`
    then `scope-done ... "built"` and `task-add ... <NNN> "<one-line note>"`.
12. Never delete anything, never commit, never write outside the namespace.

Report back (text only): content lines/colors placed, equation/graph assets + sizes,
render path, PIL-check numbers, deviations or blockers.
