import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def render(label, s, out):
    fig = plt.figure(figsize=(10,4), dpi=600)
    fig.patch.set_alpha(0)
    fig.text(0.5,0.5,s,fontsize=16,color='#000000',ha='center',va='baseline')
    fig.canvas.draw()
    buf=np.asarray(fig.canvas.buffer_rgba()); ink=buf[:,:,3]>8
    rows=np.where(ink.any(axis=1))[0]; cols=np.where(ink.any(axis=0))[0]
    crop=buf[rows[0]:rows[-1]+1, cols[0]:cols[-1]+1]
    Image.fromarray(crop).save(out)
    a=crop[:,:,3]>8
    # longest horizontal run of ink in any single row
    best=0; bestrow=-1
    for r in range(a.shape[0]):
        row=a[r]; run=0
        for v in row:
            run = run+1 if v else 0
            if run>best: best=run; bestrow=r
    print(f'{label:28s} bbox={crop.shape[1]}x{crop.shape[0]} ink={a.sum()} longest_h_run={best}px @row{bestrow}')
    plt.close(fig)

render('math_mode_$_frac',      '$\\frac{TP}{TP + FN}$', 'probe_mathmode.png')
render('NO_$_literal_latex',    '\\frac{TP}{TP + FN}',    'probe_nomathmode.png')
render('plain_text',            'fracTPTP + FN',           'probe_plaintext.png')
