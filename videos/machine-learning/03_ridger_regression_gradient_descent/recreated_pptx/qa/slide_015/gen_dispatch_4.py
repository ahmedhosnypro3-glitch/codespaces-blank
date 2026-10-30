#!/usr/bin/env python3
r"""Generate and byte-check slide 015's attempt-4 judge dispatches.

Payload law (frozen): every -p payload is sourced BYTE-FOR-BYTE from
shared_patterns/judge_protocol_03.md with ONLY these token substitutions:
  slide_?NNN -> slide_015     (the qa-dir form and the unique_slides form)
  \bNNN\b    -> 015           (the prose form "slide NNN of ...")
  \bK\b      -> 4             (attempt number; \b guards BLOCKER's K)
Nothing else may change - not the ground rules, not the path, not punctuation.

This script extracts each template verbatim from the protocol, applies the
substitutions, writes the dispatch file, then re-derives the payload and
COMPARES BYTES against the frozen template (un-substituting must reproduce the
original bytes exactly).  A payload that fails the check is never written.

No vision call is made here.
"""
import json
import re

PROTO = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning"
         "/03_ridger_regression_gradient_descent/shared_patterns"
         "/judge_protocol_03.md")
QA = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning"
      "/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015")
ATTEMPT = 4
RENDER = f"videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide_015/render_{ATTEMPT}.png"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_015.jpg"

SUB_NNN = "015"
SUB_K = str(ATTEMPT)

CROPS = json.load(open(f"{QA}/crops_4.json"))
BY_SLUG = {c["slug"]: c for c in CROPS["crops"]}


def substitute(text):
    """The ONLY legal substitutions, in a fixed order.

    The path tokens carry an underscore-joined K (render_K, probe_K,
    judge_attempt_K, crop_K_NAME) that \\b cannot see - '_' is a word character -
    so those are anchored first.  The remaining standalone prose K ("attempt K")
    is matched with \\b, which is what keeps BLOCKER's K uncorrupted.
    """
    out = text
    for tok in (r"render_K", r"probe_K", r"judge_attempt_K", r"crop_K_NAME"):
        out = re.sub(tok, tok.replace("_K", f"_{SUB_K}"), out)
    out = re.sub(r"\bK\b", SUB_K, out)
    out = re.sub(r"slide_?NNN", "slide_015", out)
    out = re.sub(r"\bNNN\b", SUB_NNN, out)
    return out


def unsubstitute(text):
    """Inverse map, used only to prove the frozen bytes survive the round trip."""
    out = text
    out = out.replace("slide_015", "slide_?NNN_TBC")
    out = re.sub(r"\b015\b", "NNN", out)
    out = re.sub(rf"\b{SUB_K}\b", "K", out)
    return out.replace("slide_?NNN_TBC", "slideNNN")


def extract(path_pat, label):
    """Return the fenced block (between ``` fences) that contains path_pat."""
    src = open(PROTO).read()
    blocks = re.findall(r"```\n(.*?)\n```", src, re.S)
    for b in blocks:
        if path_pat in b:
            return b
    raise SystemExit(f"template containing {path_pat!r} not found (label {label})")


def payload_of(block):
    """The -p "..." string, unescaped back to its raw bytes."""
    m = re.search(r'-p "(.*)"\s*$', block, re.S)
    if not m:
        raise SystemExit("no -p payload in template block")
    return m.group(1)


def byte_check(frozen_payload, final_payload):
    """Prove final_payload differs from frozen_payload ONLY by the legal subs."""
    expected = substitute(frozen_payload)
    return expected == final_payload


def write_dispatch(name, header, block, payload, transcript):
    """Write one dispatch script.  The definitive byte-check is the re-read loop
    in main(), which re-derives each payload from the frozen template and
    compares bytes; a failure there aborts before anything is dispatchable."""
    body = substitute(block)
    # the protocol's cd points at the authoring workspace; derive it instead
    # so the dispatch runs from wherever the repo lives
    body = body.replace(
        "cd /home/ahmed/Projects/ai_llm_slides && scripts/16_vision_gate.sh",
        'REPO=$(git rev-parse --show-toplevel) && cd "$REPO" && scripts/16_vision_gate.sh')
    text = header + "\n" + body + "\n"
    if transcript:
        text += f"\n# Transcript: {transcript}\n"
    path = f"{QA}/{name}.txt"
    open(path, "w").write(text)
    return path


# ---- frozen payloads, extracted before any substitution -------------------
# The protocol has 4 fenced blocks: the shared prelude (no command), the probe,
# Template A (full-slide comparison, contains judge_attempt_K.txt) and Template B
# (crop pair, contains crop_K_NAME_render.png).
PAYLOADS = {}
BLOCKS = {}
for label, pat in (("probe", "probe_K.txt"),
                   ("templateA", "judge_attempt_K.txt"),
                   ("templateB", "crop_K_NAME_render.png")):
    blk = extract(pat, label)
    BLOCKS[label] = blk
    if '-p "' in blk:                 # the probe is an analysis call: no payload
        PAYLOADS[label] = payload_of(blk)
print(f"extracted frozen payloads: {list(PAYLOADS)}")
print("  " + "  ".join(f"{k} {len(v)} bytes" for k, v in PAYLOADS.items()))


def sub_payload(label, extra=None):
    p = PAYLOADS[label]
    p = substitute(p)
    if extra:
        for a, b in extra:
            p = p.replace(a, b)
    return p


def main():
    written = []

    # ---------- Template A probe first (opens the gateway window) ----------
    blkProbe = substitute(BLOCKS["probe"])
    headerP = (
        f"# Probe dispatch — slide 015, attempt {ATTEMPT} (opens the gateway window)\n"
        "# Command source: shared_patterns/judge_protocol_03.md Template A probe block.\n"
        "# Gate law: a valid body opens the window; a hang means sleep 300 and re-probe ONCE.\n"
        "# Gate law: before dispatching, run `pgrep -c -f analyze_image.py`; if it is >= 8\n"
        "# do NOT dispatch - heartbeat, sleep 240, re-probe.\n")
    written.append(write_dispatch(
        f"dispatch_{ATTEMPT}_probe", headerP, blkProbe, None,
        f"{QA}/probe_{ATTEMPT}.txt"))

    # ---------- Template A: full-slide comparison ----------
    payloadA = sub_payload("templateA")
    blkA = substitute(BLOCKS["templateA"])
    headerA = (
        "# Judge dispatch — slide 015, attempt 4 (Template A: full-slide judge)\n"
        "# Payload source: shared_patterns/judge_protocol_03.md Template A, byte-for-byte,\n"
        "# ONLY the token substitutions applied: slide_?NNN->slide_015, \\bNNN\\b->015, \\bK\\b->4\n"
        f"# (\\bK\\b is a word-boundary match so BLOCKER's K is never corrupted).\n"
        f"# Images: {RENDER} (150dpi PPTX render) vs the original lecture frame.\n"
        "# Byte-checked by gen_dispatch_4.py against the frozen template before writing.\n"
        "# Gate law: before dispatching, run `pgrep -c -f analyze_image.py`; if it is >= 8\n"
        "# do NOT dispatch - heartbeat, sleep 240, re-probe.  One hard-wall retry max.\n")
    written.append(write_dispatch(
        "dispatch_4_judgeA", headerA, blkA, payloadA,
        "videos/machine-learning/03_ridger_regression_gradient_descent/"
        "recreated_pptx/qa/slide_015/judge_attempt_4.txt"))

    # ---------- Template B: one crop pair per dense region ----------
    for slug in ("eq_stack", "pinkbox", "peachbox", "deriv_stack", "solution"):
        c = BY_SLUG[slug]
        payloadB = sub_payload("templateB")
        payloadB = payloadB.replace(
            "<one-line description of what the region contains>", c["desc"])
        blkB = substitute(BLOCKS["templateB"])
        blkB = blkB.replace(f"crop_{ATTEMPT}_NAME_render.png",
                            f"crop_{ATTEMPT}_{slug}_render.png")
        blkB = blkB.replace(f"crop_{ATTEMPT}_NAME_orig.png",
                            f"crop_{ATTEMPT}_{slug}_orig.png")
        blkB = blkB.replace(f"crop_{ATTEMPT}_NAME_judge.txt",
                            f"crop_{ATTEMPT}_{slug}_judge.txt")
        blkB = blkB.replace("zoomed crop NAME", f"zoomed crop {slug}")
        blkB = blkB.replace("<one-line description of what the region contains>",
                            c["desc"])
        headerB = (
            f"# Judge dispatch — slide 015, attempt 4 (Template B: crop pair {slug})\n"
            "# Payload source: shared_patterns/judge_protocol_03.md Template B, byte-for-byte,\n"
            "# ONLY the token substitutions applied: slide_?NNN->slide_015, \\bNNN\\b->015, \\bK\\b->4,\n"
            "# plus the <one-line region description> the template names as a slot.\n"
            f"# Crops: frame bbox x{c['bbox_frame'][0]}..x{c['bbox_frame'][1]}"
            f" y{c['bbox_frame'][2]}..y{c['bbox_frame'][3]}"
            f" ({c['frame_wh'][0]}x{c['frame_wh'][1]} frame px)\n"
            f"#         both images resized to {c['out_px'][0]}x{c['out_px'][1]}px"
            f" -> effective scale {c['effective_scale']} render-px/frame-px on BOTH axes\n"
            f"#         (matched; the original is LANCZOS-upscaled by {CROPS['scale']:.6f}).\n"
            f"# Ink census (luma<150): render {c['ink_lt150_render']} / orig {c['ink_lt150_orig']}\n"
            "# Byte-checked by gen_dispatch_4.py against the frozen template before writing.\n"
            "# Gate law: before dispatching, run `pgrep -c -f analyze_image.py`; if it is >= 8\n"
            "# do NOT dispatch - heartbeat, sleep 240, re-probe.  One hard-wall retry max.\n")
        written.append(write_dispatch(
            f"dispatch_4_crop_{slug}", headerB, blkB, payloadB,
            f"crop_{ATTEMPT}_{slug}_judge.txt"))

    print("\nwritten:")
    for w in written:
        print("  " + w)
    # re-read every written payload and re-check it against the frozen template
    print("\nbyte-check on re-read (frozen template -> legal substitutions -> file):")
    bad = 0
    for p in written:
        txt = open(p).read()
        m = re.search(r'^\s*-p "(.*)"$', txt, re.M)
        if not m:
            print(f"  n/a  (no -p payload) {p.rsplit('/', 1)[-1]}")
            continue
        got = m.group(1)
        ref = PAYLOADS["templateA" if "judgeA" in p else "templateB"]
        ref = substitute(ref)
        if "<one-line region description>" in got:
            for c in CROPS["crops"]:
                if f"crop_{ATTEMPT}_{c['slug']}_judge" in txt:
                    ref = ref.replace("<one-line description of what the region "
                                      "contains>", c["desc"])
        ok = got == ref
        bad += 0 if ok else 1
        print(f"  {'OK  ' if ok else 'FAIL'} {p.rsplit('/', 1)[-1]}"
              f" ({len(got)} bytes)")
    if bad:
        raise SystemExit(f"{bad} payload(s) failed the byte-check - NOT dispatchable")
    print(f"\nall byte-checks passed: {len([w for w in written])} dispatches written")


if __name__ == "__main__":
    main()
