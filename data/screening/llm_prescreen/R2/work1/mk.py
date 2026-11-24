import re, csv
from collections import Counter
d = 'C:/Users/TestAnvändare/Documents/MLN_method/screening_ai/R2/'
cids = [re.match(r'\[(R2-C\d+)\]', l).group(1) for l in open(d + 'batch1.txt', encoding='utf-8') if l.startswith('[')]
dec = {}
for l in open(d + 'work1/dec.txt', encoding='utf-8'):
    l = l.strip()
    if not l:
        continue
    p = l.split('|')
    c = 'R2-' + p[0]
    if c in dec:
        print('dup', c)
    dec[c] = p
miss = [c for c in cids if c not in dec]
extra = [c for c in dec if c not in cids]
print(len(cids), len(dec), 'miss', miss, 'extra', extra)
cnt = Counter()
with open(d + 'batch1_decisions.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['cid', 'decision', 'code', 'note'])
    for c in cids:
        p = dec[c]
        k = p[1]
        note = p[2] if len(p) > 2 else ''
        if k == 'U':
            de, code = 'unsure', ''
        elif k == 'B':
            de, code = 'background', 'B'
        elif k.startswith('I'):
            de, code = 'include', k
        else:
            de, code = 'exclude', k
        if de != 'exclude':
            assert note and len(note.split()) <= 12, (c, note)
        cnt[de] += 1
        w.writerow([c, de, code, note])
print(cnt)
