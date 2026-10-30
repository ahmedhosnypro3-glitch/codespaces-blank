#!/usr/bin/env python3
"""Field-by-field diff: certified spec vs fresh reanalysis spec (REJUDGE_PROTOCOL step 2).

Usage: r1_diff.py <NNN>   -> writes qa/slideNNN/rejudge/analysis_diff.md
"""
import json
import os
import sys

VD = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"


def flat(obj, prefix=""):
    """Flatten nested dict/list into {dotted.key: scalar} for comparison."""
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flat(v, f"{prefix}{k}."))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(flat(v, f"{prefix}[{i}]."))
    else:
        out[prefix.rstrip(".")] = obj
    return out


def load(p):
    with open(p) as f:
        return json.load(f)


def main(n):
    cert_p = f"{VD}/analysis/slide_{n}_final.json"
    fresh_p = f"{VD}/analysis/reanalysis/slide_{n}_final.json"
    out_p = f"{VD}/qa/slide{n}/rejudge/analysis_diff.md"
    cert, fresh = load(cert_p), load(fresh_p)
    cf, ff = flat(cert), flat(fresh)

    groups = [
        ("slide_title", lambda k: k == "slide_title"),
        ("subtitle_or_header", lambda k: k == "subtitle_or_header"),
        ("verbatim_text", lambda k: k.startswith("verbatim_text")),
        ("layout.regions", lambda k: k.startswith("layout.regions")),
        ("visual_elements", lambda k: k.startswith("visual_elements")),
        ("colors", lambda k: k.startswith("colors")),
        ("recreation_brief", lambda k: k.startswith("recreation_brief")),
    ]
    lines = [f"# Analysis diff — slide {n}",
             "",
             "Certified: `analysis/slide_%s_final.json` (READ-ONLY)" % n,
             "Fresh: `analysis/reanalysis/slide_%s_final.json`" % n,
             ""]
    for name, pred in groups:
        ck = {k: v for k, v in cf.items() if pred(k)}
        fk = {k: v for k, v in ff.items() if pred(k)}
        allk = sorted(set(ck) | set(fk))
        match = [k for k in allk if k in ck and k in fk and ck[k] == fk[k]]
        div = [k for k in allk if not (k in ck and k in fk and ck[k] == fk[k])]
        lines.append(f"## {name} — {'MATCH' if not div else 'DIVERGENT'} "
                     f"({len(match)} match / {len(div)} divergent)")
        if not div:
            lines.append("- all fields identical")
        for k in div[:14]:
            lines.append(f"- DIVERGENT `{k}`")
            lines.append(f"  - certified: {json.dumps(ck.get(k), ensure_ascii=False)[:220]}")
            lines.append(f"  - fresh:     {json.dumps(fk.get(k), ensure_ascii=False)[:220]}")
        if len(div) > 14:
            lines.append(f"- ... {len(div)-14} further divergent fields "
                         f"(see JSON files)")
        lines.append("")
    # validation blocks
    lines.append("## validation (fresh) — " +
                 json.dumps(fresh.get("validation"), ensure_ascii=False)[:600])
    lines.append("")
    lines.append("## validation (certified) — " +
                 json.dumps(cert.get("validation"), ensure_ascii=False)[:600])
    lines.append("")
    os.makedirs(os.path.dirname(out_p), exist_ok=True)
    with open(out_p, "w") as f:
        f.write("\n".join(lines))
    print(f"wrote {out_p} ({len(lines)} lines)")


if __name__ == "__main__":
    main(sys.argv[1])
