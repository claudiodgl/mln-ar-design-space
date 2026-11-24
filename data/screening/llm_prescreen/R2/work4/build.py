import re,csv,collections
L=open('batch4.txt',encoding='utf-8').read().splitlines()
cids=[re.match(r'\[([^\]]+)\]',l).group(1) for l in L if l.startswith('[')]
titles=[l.split(']',1)[1].split('|')[0].strip() for l in L if l.startswith('[')]
d={}
for f in ['d1','d2','d3','d4']:
    for l in open(f'work4/{f}.txt',encoding='utf-8'):
        if not l.strip(): continue
        i,c,n=l.rstrip('\n').split('|',2); i=int(i)
        assert i not in d,i; d[i]=(c,n.strip())
assert sorted(d)==list(range(len(cids))),(len(d),len(cids))
dec=lambda c:'include' if c.startswith('I') else 'background' if c=='B' else 'unsure' if c=='U' else 'exclude'
cnt=collections.Counter()
with open('batch4_decisions.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(['cid','decision','code','note'])
    for i,cid in enumerate(cids):
        c,n=d[i]; D=dec(c); cnt[D]+=1
        if D!='exclude': assert n and len(n.split())<=12,(i,n)
        w.writerow([cid,D,'' if c=='U' else c,n])
        if D in('include','background'): print(cid,c,titles[i][:70])
print(cnt, sum(cnt.values()), len(cids))
