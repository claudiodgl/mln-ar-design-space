import csv,sys,collections
base=sys.argv[1]
ids=[l.strip() for l in open(base+'/work6/ids.txt',encoding='utf-8')]
rows=[]
for f in 'd1 d2 d3 d4'.split():
    for l in open(f'{base}/work6/{f}.txt',encoding='utf-8'):
        l=l.rstrip('\n')
        if l: rows.append(l.split('|',3))
assert [r[0] for r in rows]==ids, 'order mismatch'
for r in rows:
    assert r[1] in ('include','background','exclude','unsure')
    if r[1]!='exclude': assert r[3] and len(r[3].split())<=12, r
with open(base+'/batch6_decisions.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(['cid','decision','code','note']); w.writerows(rows)
print(len(rows), collections.Counter(r[1] for r in rows))
print(collections.Counter(r[2] for r in rows if r[1]=='exclude'))
