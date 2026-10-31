#!/usr/bin/env python3
"""Verify candidate mathtext for each slide_005 equation asset by re-rendering and
pixel-comparing against the baked PNG. Prints a table; only verified pairs go
into the OMML manifest."""
import importlib.util
import json
import sys
from pathlib import Path

SPEC = '/home/codespace/ai_llm_slides/scripts/render_eq.py'
_s = importlib.util.spec_from_file_location('render_eq', SPEC)
render_eq = importlib.util.module_from_spec(_spec) if (_spec := importlib.util.spec_from_file_location('render_eq', SPEC)) else None
_s.loader.exec_module(render_eq)

ASSETS = Path('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/assets')
OUT = Path('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/_pool/b03_eqverify')
OUT.mkdir(parents=True, exist_ok=True)

from PIL import Image


def png_size(p):
    with Image.open(p) as im:
        return im.size


def score(cand_path, asset):
    from PIL import ImageChops
    a = Image.open(cand_path).convert('RGBA')
    b = Image.open(ASSETS / f'{asset}.png').convert('RGBA')
    if a.size != b.size:
        return ('SIZE', a.size, b.size)
    d = ImageChops.difference(a, b)
    px = d.get_flattened_data() if hasattr(d, 'get_flattened_data') else list(d.getdata())
    n = sum(1 for p in px if p[3] > 8)
    return ('DIFF', n, a.size[0] * a.size[1])


# (asset, [candidate mathtext strings]) -- first match wins
CASES = {
    'eq_b_fa': [r'b=f(a)'],
    'eq_c_fb': [r'c=f(b)'],
    'eq_implies': [r'\Rightarrow'],
    'eq_c_fa': [r'c=f(a)'],
    'eq_01c': [r'\frac{\partial c}{\partial a} = \frac{\partial c}{\partial b} * \frac{\partial b}{\partial a}'],
    'eq_02a': [
        r'b=f(\underline{W}) = w_1.a_1+w_2.a_2+w_3.a_3+......+w_n.a_n',
        r'b=f(W) = w_1.a_1+w_2.a_2+w_3.a_3+......+w_n.a_n',
        r'b=\underline{f(W)} = w_1.a_1+w_2.a_2+w_3.a_3+......+w_n.a_n',
    ],
    'eq_02b': [
        r'\frac{\partial b}{\partial w_1} = a_1 \quad \frac{\partial b}{\partial w_2} = a_2 \quad \frac{\partial b}{\partial w_i} = a_i',
        r'\frac{\partial b}{\partial w_1} = a_1 \frac{\partial b}{\partial w_2} = a_2 \frac{\partial b}{\partial w_i} = a_i',
    ],
    'eq_bfw_u': [
        r'b=f(\underline{W})',
        r'b=f(W)',
    ],
    'eq_sum_ai_wi': [
        r'\sum_{i=1}^{n} w_i.a_i',
        r'\sum_{i=1}^{n} a_i.w_i',
    ],
    'eq_db_dwi': [
        r'\frac{\partial b}{\partial w_i} = a_i',
    ],
    'eq_3c_fa': [
        r'c=f(a_1) , c=f(a_2) , c=f(a_3)',
        r'c=f(a_1), c=f(a_2), c=f(a_3)',
    ],
    'eq_3a_fb': [
        r'a_1=f(b) , a_2=f(b) , a_3=f(b)',
        r'a_1=f(b), a_2=f(b), a_3=f(b)',
    ],
    'eq_cond2': [
        r'if b is changed , c will be changed accordingly',
    ],
    'eq_through': [
        r'[through a_1,a_2,a_3]',
    ],
    'eq_03c': [
        r'\frac{\partial c}{\partial b} = \left[ \frac{\partial c}{\partial a_1} * \frac{\partial a_1}{\partial b} \right] + \left[ \frac{\partial c}{\partial a_2} * \frac{\partial a_2}{\partial b} \right] + \left[ \frac{\partial c}{\partial a_3} * \frac{\partial a_3}{\partial b} \right] = \sum_{i=1}^{3} \frac{\partial c}{\partial a_i} * \frac{\partial a_i}{\partial b}',
    ],
}

results = {}
for asset, cands in CASES.items():
    side = OUT / f'{asset}.json'
    try:
        sidecar = json.loads((ASSETS / f'{asset}.json').read_text())
    except Exception:
        print(f'{asset}: NO SIDECAR'); continue
    fs = float(sidecar.get('fontsize_pt', 18.0))
    color = str(sidecar.get('color', '000000')).lstrip('#')
    best = None
    for i, cand in enumerate(cands):
        out = OUT / f'{asset}_c{i}.png'
        try:
            info = render_eq.render(cand, str(out), fs, color)
        except SystemExit as e:
            print(f'{asset} cand{i}: RENDER FAILED {e}')
            continue
        st = score(out, asset)
        if st[0] == 'DIFF':
            print(f'{asset} cand{i}: diff={st[1]}/{st[2]}')
            if st[1] == 0:
                best = cand
                break
            if best is None:
                best = cand
        else:
            print(f'{asset} cand{i}: {st}')
    results[asset] = best

(OUT / 'candidates.json').write_text(json.dumps(results, indent=1))
print('\n=== verified ===')
for k, v in results.items():
    print(f'{k:15s} {"OK" if v else "?"} {v}')
