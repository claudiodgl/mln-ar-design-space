import re,sys
sys.stdout.reconfigure(encoding='utf-8')
t=open(sys.argv[1],encoding='utf-8').read()
recs=re.split(r'\n(?=\[)',t.strip())
ids=sys.argv[2].split(',')
for r in recs:
    c=r[1:r.index(']')].replace('R2-C','')
    if c in ids: a=int(sys.argv[3]) if len(sys.argv)>3 else 0; print(c, r[a:a+1400]);print()
