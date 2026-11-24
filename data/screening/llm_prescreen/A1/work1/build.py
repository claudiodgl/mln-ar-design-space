import re, csv, os
from collections import Counter
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
recs = re.findall(r'^\[([^\]]+)\] \(current (\w+)\) (.*?) \|', open(os.path.join(base, 'part1.txt'), encoding='utf-8').read(), re.M)
old = {c: o for c, o, _ in recs}
dec = {}
for l in open(os.path.join(base, 'work1', 'dec.txt'), encoding='utf-8').read().strip().split('\n'):
    p = l.split('|')
    assert len(p) == 4, l
    assert p[0] not in dec, p[0]
    assert len(p[3].split()) <= 12, l
    dec[p[0]] = p
print('records', len(recs), 'decisions', len(dec), 'missing', set(old) - set(dec), 'extra', set(dec) - set(old))
with open(os.path.join(base, 'part1_decisions.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['cid', 'old_code', 'new_decision', 'new_code', 'note'])
    for c, o, _ in recs:
        d = dec[c]
        w.writerow([c, o, d[1], d[2], d[3]])
cnt = Counter()
for c, o, _ in recs:
    d = dec[c]
    cnt[(o, 'kept' if d[2] == o else (d[2] or 'unsure'))] += 1
print(sorted(cnt.items()))
for c, o, t in recs:
    if o == 'I4' and dec[c][2] == 'I4':
        print(c, t[:55])
