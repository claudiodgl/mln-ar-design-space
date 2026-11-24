import csv, re, collections
base = r"C:\Users\TestAnvändare\Documents\MLN_method\screening_ai\R2"
cids = [re.match(r"\[([^\]]+)\]", l).group(1) for l in open(base + r"\batch5.txt", encoding="utf-8") if l.startswith("[")]
rows = {}
dups = []
for i in range(1, 5):
    for r in csv.reader(open(base + rf"\work5\part{i}.csv", encoding="utf-8")):
        if not r: continue
        if r[0] in rows: dups.append(r[0])
        rows[r[0]] = r[1:4]
missing = [c for c in cids if c not in rows]
extra = [c for c in rows if c not in set(cids)]
print("records", len(cids), "decided", len(rows), "missing", missing, "extra", extra, "dups", dups)
bad = [c for c, (d, code, n) in rows.items() if d != "exclude" and not n]
print("missing notes", bad)
with open(base + r"\batch5_decisions.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["cid", "decision", "code", "note"])
    for c in cids:
        w.writerow([c] + rows[c])
print(collections.Counter(v[0] for v in rows.values()))
print(collections.Counter(v[1] for v in rows.values() if v[0] == "exclude"))
