import re, csv, os
from collections import Counter
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
txt = open(os.path.join(base, 'part2.txt'), encoding='utf-8').read()
recs = [(m.group(1), m.group(2), m.group(3)) for m in re.finditer(r'^\[([^\]]+)\] \(current (\w+)\) ([^|]*)', txt, re.M)]
dec = {}
for l in open(os.path.join(base, 'work2', 'dec.txt'), encoding='utf-8'):
    if not l.strip():
        continue
    c, d, code, n = l.rstrip('\n').split('|')
    dec[c] = (d, code, n)
ids = [r[0] for r in recs]
print(len(recs), len(dec), set(ids) - set(dec), set(dec) - set(ids))
cnt = Counter()
with open(os.path.join(base, 'part2_decisions.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['cid', 'old_code', 'new_decision', 'new_code', 'note'])
    for c, old, t in recs:
        d, code, n = dec[c]
        assert len(n.split()) <= 12, n
        w.writerow([c, old, d, code, n])
        cnt[(old, code)] += 1
print(sorted(cnt.items()))
for c, old, t in recs:
    if dec[c][1] == 'I4':
        print(c, t.strip()[:55])
