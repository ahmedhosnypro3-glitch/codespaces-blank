import subprocess, json, os

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
OUT = f"{NS}/recreated_pptx/build/eq_slide_020"
RENDER = "/home/codespace/ai_llm_slides/scripts/render_eq.py"
os.makedirs(OUT, exist_ok=True)

# Middle two chain-rule rows + right-panel 4 lines + delta + where.
# Frame text per parse/certified analysis (w_ji convention).
EQS = [
    ("eq_mid1.png", 13, r"\frac{\partial E}{\partial w_{ji}} = \frac{\partial E}{\partial Net_{k_1}}\frac{\partial Net_{k_1}}{\partial O_j} + \frac{\partial E}{\partial Net_{k_2}}\frac{\partial Net_{k_2}}{\partial O_j} + ... + \frac{\partial E}{\partial Net_{k_m}}\frac{\partial Net_{k_m}}{\partial O_j} \cdot \frac{\partial O_j}{\partial Net_j} \cdot \frac{\partial Net_j}{\partial w_{ji}}"),
    ("eq_mid2.png", 13, r"\frac{\partial E}{\partial w_{ji}} = \sum_{k=1}^{m} \frac{\partial E}{\partial Net_k}\frac{\partial Net_k}{\partial O_j} \cdot \frac{\partial O_j}{\partial Net_j} \cdot \frac{\partial Net_j}{\partial w_{ji}} = \sum_{k=1}^{m} -\delta_k w_{kj} \cdot O_j(1-O_j) \cdot O_i"),
    ("eq_r1.png", 11, r"\frac{\partial E}{\partial Net_k} \rightarrow -\delta_k"),
    ("eq_r2.png", 11, r"Net_k = \sum_{j} w_{kj} O_j \rightarrow \frac{\partial Net_k}{\partial O_j} = w_{kj}"),
    ("eq_r3.png", 11, r"O_j = \frac{1}{1+e^{-Net_j}} \rightarrow \frac{\partial O_j}{\partial Net_j} = O_j(1-O_j)"),
    ("eq_r4.png", 11, r"Net_j = \sum_{i} w_{ji} O_i \rightarrow \frac{\partial Net_j}{\partial w_{ji}} = O_i"),
    ("eq_delta.png", 13, r"\Delta_{ji} = -\eta \frac{\partial E}{\partial w_{ji}} = \sum_{k=1}^{m} \delta_k w_{kj} \cdot O_j(1-O_j) \cdot O_i = \eta \delta_j \cdot O_i"),
    ("eq_where.png", 11, r"\mathrm{Where}\ \delta_j = \sum_{k=1}^{m} \delta_k w_{kj} \cdot O_j(1-O_j) \quad (\mathrm{for\ each\ Node}\ j\ \mathrm{at\ hidden\ layer})"),
]

for name, fs, latex in EQS:
    r = subprocess.run(["python3", RENDER, latex, f"{OUT}/{name}", str(fs), "000000"],
                       capture_output=True, text=True)
    try:
        d = json.loads(r.stdout.strip().splitlines()[-1])
        print(f"{name}: {d['w_px']}x{d['h_px']}px  w={d['w_in']:.4f}in h={d['h_in']:.4f}in fs={fs}")
    except Exception:
        print(name, "FAIL", r.stdout[-200:], r.stderr[-200:])
