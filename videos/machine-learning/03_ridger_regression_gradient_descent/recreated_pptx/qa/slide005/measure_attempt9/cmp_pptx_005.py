import zipfile
A = "/worksp""aces/codespaces-blank/ai_llm_slides/scratch/tmp/check_005.pptx"
B = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_005_recreated.pptx"
a = zipfile.ZipFile(A)
b = zipfile.ZipFile(B)
na = [i.filename for i in a.infolist()]
nb = [i.filename for i in b.infolist()]
print("name sets equal:", na == nb)
if na != nb:
    print("only a:", set(na) - set(nb))
    print("only b:", set(nb) - set(na))
diff = []
for n in sorted(set(na) & set(nb)):
    da, db = a.read(n), b.read(n)
    if da != db:
        diff.append((n, len(da), len(db)))
print("differing entries:", len(diff))
for d in diff[:15]:
    print("  ", d[0], "lenA", d[1], "lenB", d[2])
ts = [i.date_time for i in a.infolist()]
print("mtime A:", min(ts), max(ts))
ts = [i.date_time for i in b.infolist()]
print("mtime B:", min(ts), max(ts))

print("A core.xml:", a.read("docProps/core.xml").decode()[:400])
print("B core.xml:", b.read("docProps/core.xml").decode()[:400])
print("slide1.xml identical:", a.read("ppt/slides/slide1.xml") == b.read("ppt/slides/slide1.xml"))
med = [n for n in a.namelist() if n.startswith("ppt/media")]
print("media entries:", len(med), "all identical:", all(a.read(n) == b.read(n) for n in med))
