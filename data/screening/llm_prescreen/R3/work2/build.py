import re,csv,collections,sys
base=sys.argv[1]
cids=re.findall(r'^\[(R3-C\d+)\]',open(base+'/batch2.txt',encoding='utf-8').read(),re.M)
d={}
for l in open(base+'/work2/dec.txt',encoding='utf-8'):
    l=l.rstrip('\n')
    if not l: continue
    c,dec,code,note=l.split('|')
    assert 'R3-'+c not in d, c
    d['R3-'+c]=(dec,code,note)
miss=[c for c in cids if c not in d]; extra=[c for c in d if c not in cids]
print('records',len(cids),'unique',len(set(cids)),'missing',miss,'extra',extra)
for c,(dec,code,note) in d.items():
    if dec in('include','background','unsure'): assert note, c
    assert len(note.split())<=12,(c,note)
with open(base+'/batch2_decisions.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['cid','decision','code','note'])
    for c in cids: w.writerow([c,*d[c]])
print(collections.Counter(v[0] for v in d.values()))
print(collections.Counter(v[1] for v in d.values()))
