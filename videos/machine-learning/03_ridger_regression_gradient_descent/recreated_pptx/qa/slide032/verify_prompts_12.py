#!/usr/bin/env python3
"""Assert the attempt-12 judge payloads are byte-for-byte the protocol payloads.

For each generated prompt file: locate the actual `-p "` argument, extract its
text (a trailing newline is allowed), undo the documented substitution, and
compare with the payload extracted from the protocol's fenced block.
"""
DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide032"
fs = open(DECK + "/shared_patterns/judge_protocol_03.md", encoding="utf-8").read().split("\n")


def payload_of(block):
    i = block.index('-p "') + 4
    return block[i:-1]


PAY_A = payload_of("\n".join(fs[61:71]))
PAY_B = payload_of("\n".join(fs[107:117]))


def actual_payload(path):
    t = open(path, encoding="utf-8").read()
    i = t.index('\n  -p "') + 7
    return t[i:t.rindex('"')].rstrip("\n")


fails = 0


def check(label, got, want):
    global fails
    ok = got == want
    print(f"{label:<24}: exact={ok} chars={len(got)} vs {len(want)} backtick={'```' in got}")
    if not ok:
        import difflib
        d = list(difflib.unified_diff(want.split("\n"), got.split("\n"), lineterm="", n=0))
        print("   " + "\n   ".join(d[:4]))
        fails += 1


check("A judge_attempt_12", actual_payload(QA + "/judge_prompt_12.txt"), PAY_A)

CMD_SLUGS = {
    "title": ["crop_12_title_render.png", "Slide 032 zoomed crop title"],
    "params": ["crop_12_params_render.png", "Slide 032 zoomed crop params"],
    "graph": ["crop_12_graph_render.png", "Slide 032 zoomed crop graph"],
    "callouts": ["crop_12_callouts_render.png", "Slide 032 zoomed crop callouts"],
    "table": ["crop_12_table_render.png", "Slide 032 zoomed crop table"],
}
for name, needles in CMD_SLUGS.items():
    check(f"B {name}", actual_payload(QA + f"/crop_12_{name}_prompt.txt").replace("slide 032", "slide NNN"), PAY_B)
    c = open(QA + f"/crop_12_{name}_prompt.txt", encoding="utf-8").read()
    for n in needles:
        if n not in c:
            print(f"   !! cmd B({name}) missing {n!r}")
            fails += 1
    for n in ("_orig.png", "_judge.txt", "matched scale (attempt 12)", "--timeout 1200"):
        if n not in c:
            print(f"   !! cmd B({name}) missing {n!r}")
            fails += 1
    if "(7, 7)" in c:
        print(f"   !! cmd B({name}) still asserts the refuted '(7, 7)' label")
        fails += 1

cmd = open(QA + "/judge_prompt_12.txt", encoding="utf-8").read()
for n in ("render_12.png", "unique_slides/slide_032.jpg", "judge_attempt_12.txt",
          '--view "Slide 032 recreation', "--thinking high --max-tokens 65536",
          "--timeout 1200 --rounds 1 --tries 1", "timeout 1700"):
    if n not in cmd:
        print(f"   !! cmd A missing {n!r}")
        fails += 1

print("\nTOTAL FAILURES:", fails)
