import csv,re,sys,collections
d=sys.argv[1]
cids=[re.match(r'\[([^\]]+)\]',l).group(1) for l in open(d+'/batch2.txt',encoding='utf-8') if l.startswith('[')]
dec={}
for f in ['d1','d2','d3']:
    for l in open(d+'/work2/'+f+'.txt',encoding='utf-8'):
        l=l.rstrip('\n')
        if not l: continue
        c,a,code,note=l.split('|')
        k='R2-'+c; assert k not in dec,k; dec[k]=(a,code,note)
missing=[c for c in cids if c not in dec]; extra=[c for c in dec if c not in cids]
print('missing',missing,'extra',extra)
for c,(a,code,note) in dec.items():
    if a in('include','background','unsure'): assert note and len(note.split())<=12,(c,note)
with open(d+'/batch2_decisions.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['cid','decision','code','note'])
    for c in cids: w.writerow([c,*dec[c]])
print(len(cids), collections.Counter(v[0] for v in dec.values()))
