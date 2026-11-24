import re, csv, os
from collections import Counter
here = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(here, '..', 'batch7.txt'), encoding='utf-8').read()
cids = re.findall(r'^\[(R2-C\d+)\]', t, re.M)
d = {}
for line in open(os.path.join(here, 'dec.txt'), encoding='utf-8'):
    line = line.strip()
    if not line:
        continue
    k, rest = line.split(' ', 1)
    code, _, note = rest.partition('|')
    assert k not in d, k
    d[k] = (code, note)
missing = [c for c in cids if c.replace('R2-C', '') not in d]
extra = set(d) - {c.replace('R2-C', '') for c in cids}
print('records', len(cids), 'decided', len(d), 'missing', missing, 'extra', extra)
cnt = Counter()
with open(os.path.join(here, '..', 'batch7_decisions.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['cid', 'decision', 'code', 'note'])
    for c in cids:
        code, note = d[c.replace('R2-C', '')]
        dec = ('include' if code.startswith('I') else 'background' if code == 'B'
               else 'unsure' if code == 'unsure' else 'exclude')
        if dec in ('include', 'background', 'unsure'):
            assert note, c
        assert len(note.split()) <= 12, (c, note)
        w.writerow([c, dec, '' if code == 'unsure' else code, note])
        cnt[dec] += 1
print(cnt)
